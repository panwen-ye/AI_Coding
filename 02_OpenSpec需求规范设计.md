# OpenSpec需求规范设计

## 1. 定位

OpenSpec是AI开发任务协议。

作用：

让人工需求变成AI可执行任务。

## 2. 设计原则

需求必须包含：

- 背景
- 输入
- 输出
- 业务规则
- 技术约束
- 验收标准

## 3. 模板

```yaml
feature:
  name: order-query

description:
  查询订单详情

business:
  actor:
    客服

scenario:
  - 查询存在订单
  - 查询不存在订单

api:
  method: GET
  path: /orders/{id}

technical:
  framework:
    - SpringBoot3
    - MyBatisPlus

rules:
  - 不存在订单返回404

test:
  - 正常查询
  - 参数异常

acceptance:
  command:
    mvn clean test
```

## 4. 编写流程

人工填写Feature。

Architecture Agent审核。

Coding Agent执行。

Test Agent验证。
