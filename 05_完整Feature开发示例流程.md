# 完整Feature开发示例流程

## 场景

新增订单查询接口。

## Step1 需求

输入：

order-query.yaml

包含：

- API
- 数据结构
- 业务规则
- 验收标准

## Step2 Architecture Agent

输出：

architecture.md

定义：

- Controller
- Service
- Mapper

## Step3 Coding Agent

生成：

```
OrderController
OrderService
OrderMapper
OrderDTO
```

## Step4 Test Agent

生成：

```
OrderServiceTest
```

覆盖：

- 正常查询
- 数据不存在
- 参数为空

## Step5 Workflow执行

执行：

```
mvn clean test
```

## Step6 Fix Agent

如果失败：

读取：

```
error.log
```

自动修改。

最多3轮。

## Step7 人工审核

确认：

- 业务正确
- 架构合理
- 代码规范

最终提交。
