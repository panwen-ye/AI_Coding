#!/usr/bin/env python3
"""
generate_feature_spec.py (Oracle-only)

- 读取 config.yaml 获取 Oracle DB 连接与目标表
- 读取 input feature-spec yaml
- 查询 Oracle 表结构与少量示例数据
- 合并并输出 feature-spec-final.yaml

依赖: pyyaml, oracledb (安装: pip install pyyaml oracledb)

使用示例:
  python3 generate_feature_spec.py --config ../config.yaml --input ../prompts/feature-spec-template.yaml --out ../outputs

config.yaml 示例 (放在 ai-workflow/config.yaml):

database:
  type: oracle
  host: db.example.com
  port: 1521
  service_name: ORCLPDB1
  user: APP_USER
  password: secret
  schema: APP_USER  # 可选，若未指定则使用 user

table: MY_SCHEMA.MY_TABLE

"""

import argparse
import os
import sys
import yaml
from collections import OrderedDict


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(obj, f, allow_unicode=True, sort_keys=False)


def fetch_table_info_oracle(conn_info, table_full):
    try:
        import oracledb
    except Exception as e:
        print("Required module 'oracledb' not found. Install with: pip install oracledb", file=sys.stderr)
        raise

    host = conn_info.get('host', 'localhost')
    port = conn_info.get('port', 1521)
    service_name = conn_info.get('service_name')
    user = conn_info.get('user')
    password = conn_info.get('password')
    schema_cfg = conn_info.get('schema')

    if not service_name:
        raise ValueError("config.database.service_name is required for Oracle")

    dsn = oracledb.makedsn(host, port, service_name=service_name)
    conn = oracledb.connect(user=user, password=password, dsn=dsn)

    # Determine owner and table name
    if '.' in table_full:
        owner, table = table_full.split('.', 1)
    else:
        owner = schema_cfg or user
        table = table_full
    owner = owner.upper()
    table = table.upper()

    cur = conn.cursor()

    # Query column metadata
    q_cols = '''
    SELECT column_name, data_type, nullable, data_default
    FROM all_tab_columns
    WHERE owner = :owner AND table_name = :table
    ORDER BY column_id
    '''
    cur.execute(q_cols, {'owner': owner, 'table': table})
    cols = cur.fetchall()
    columns = []
    colnames = []
    for col in cols:
        name, dtype, nullable, default = col
        columns.append({'name': name, 'type': dtype, 'nullable': (nullable == 'Y'), 'default': default})
        colnames.append(name)

    # Sample rows (limit 5)
    sample_rows = []
    try:
        # Avoid SQL injection risks: owner and table are uppercased and expected safe; still wrap in double quotes if needed
        full_name = '"{}"."{}"'.format(owner, table)
        cur.execute(f"SELECT * FROM {full_name} WHERE ROWNUM <= 5")
        rows = cur.fetchall()
        descr = [d[0] for d in cur.description]
        for row in rows:
            sample_rows.append(dict(zip(descr, row)))
    except Exception:
        # fallback: try without owner
        try:
            cur.execute(f"SELECT * FROM {table} WHERE ROWNUM <= 5")
            rows = cur.fetchall()
            descr = [d[0] for d in cur.description]
            for row in rows:
                sample_rows.append(dict(zip(descr, row)))
        except Exception:
            sample_rows = []

    cur.close()
    conn.close()
    return columns, colnames, sample_rows


def generate_final_spec(cfg, feature, columns, colnames, sample_rows):
    final = OrderedDict()
    final['feature'] = feature.get('feature', {})
    final['db_table'] = cfg.get('table')
    final['db_columns'] = columns
    final['sample_rows'] = sample_rows

    # mapping suggestions
    req_fields = feature.get('request', {}).get('fields', []) or []
    mapping = []
    lower_cols = {c['name'].lower(): c['name'] for c in columns}
    for f in req_fields:
        candidates = []
        # direct match
        if f.lower() in lower_cols:
            candidates.append(lower_cols[f.lower()])
        # suffix/prefix match
        for cname in lower_cols.values():
            if cname.lower().endswith(f.lower()) or cname.lower().startswith(f.lower()):
                if cname not in candidates:
                    candidates.append(cname)
        mapping.append({'request_field': f, 'db_candidates': candidates})
    final['field_mapping_suggestions'] = mapping

    # basic tests
    first_field = req_fields[0] if req_fields else 'id'
    final['tests_generated'] = [
        {'name': 'normal_query', 'description': '正常参数，返回200', 'request_example': {first_field: 'SAMPLE'}},
        {'name': 'missing_param', 'description': '缺少必填参数，返回400', 'request_example': {}},
        {'name': 'not_found', 'description': 'db 无记录，返回404', 'request_example': {first_field: 'NOT_EXIST'}}
    ]

    return final


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--config', required=True)
    p.add_argument('--input', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()

    cfg = load_yaml(args.config)
    db = cfg.get('database', {})
    table = cfg.get('table')
    if not table:
        print("config missing 'table' field", file=sys.stderr)
        sys.exit(2)

    # Only support Oracle
    db_type = db.get('type', 'oracle').lower()
    if db_type != 'oracle':
        print("Only Oracle database is supported by this script. Set database.type: oracle", file=sys.stderr)
        sys.exit(3)

    # load input feature spec
    feature = load_yaml(args.input)

    try:
        columns, colnames, sample_rows = fetch_table_info_oracle(db, table)
    except Exception as e:
        print("Failed to fetch table info:", str(e), file=sys.stderr)
        sys.exit(4)

    final = generate_final_spec({'table': table}, feature, columns, colnames, sample_rows)

    os.makedirs(args.out, exist_ok=True)
    outpath = os.path.join(args.out, 'feature-spec-final.yaml')
    save_yaml(final, outpath)
    print("Wrote", outpath)


if __name__ == '__main__':
    main()
