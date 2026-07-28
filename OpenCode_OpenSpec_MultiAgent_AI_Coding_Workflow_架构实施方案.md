# OpenCode + OpenSpec + Multi-Agent AI Coding Workflow 架构实施方案

> 定位：基于已有 SpringBoot + Vue 基础框架、代码规范、日志规范、JUnit规范，构建 AI 辅助研发闭环。

## 一、目标架构

```
人工需求
  |
  v
OpenSpec需求规范
  |
  v
Workflow Agent
  |
  +----------------+
  |                |
  v                v
Architecture   Coding Agent
Agent              |
                   v
              Test Agent
                   |
                   v
          CodeStyle + Maven Test
                   |
                   v
              Fix Agent
                   |
                   v
             Human Review
```

---

# 二、核心组件职责

## OpenCode

定位：AI执行引擎。

负责：

- 读取代码
- 修改代码
- 执行命令
- 多轮推理


## OpenSpec

定位：AI开发任务协议。

用于描述：

- 功能目标
- 输入输出
- 技术要求
- 验收标准


## Workflow Agent

负责：

- 任务拆分
- Agent调度
- 流程控制
- 状态管理


## Architecture Agent

职责：

- 设计Controller/Service/DAO结构
- 检查模块边界
- 输出architecture.md


## Coding Agent

职责：

- 编写SpringBoot代码
- 遵守codestyle
- 遵守日志规范
- 执行mvn test


## Test Agent

职责：

- 生成JUnit5
- Mockito测试
- 覆盖正常、异常、边界场景


## Fix Agent

职责：

根据：

```
mvn test错误日志
```

自动修复代码。


---

# 三、Workflow实现

POC阶段不建议开发复杂平台。

采用：

```
OpenCode
+
OpenSpec
+
Workflow脚本
+
Maven
+
Git
```

目录：

```
ai-workflow/

├── workflow.yaml
├── agents/
├── prompts/
├── scripts/
└── logs/
```

workflow:

```yaml
workflow:
 name: feature-development

steps:

 - architecture-agent

 - coding-agent

 - test-agent

 - mvn-test

 - fix-agent
```

---

# 四、完整开发流程

## Step1 需求输入

创建：

```
feature/order-query.yaml
```

状态：

```
CREATED
```

---

## Step2 架构分析

Architecture Agent输出：

```
architecture.md
```

包含：

- 类设计
- 分层结构
- 技术方案


---

## Step3 Coding Agent开发

输入：

```
OpenSpec
architecture.md
codestyle.md
```

输出：

```
Controller
Service
DTO
Mapper
```

---

## Step4 Test Agent

生成：

```
OrderServiceTest.java
```

覆盖：

- 正常流程
- 异常流程
- 边界条件


---

## Step5 自动验证

执行：

```bash
mvn clean test
```

检查：

- 编译
- CheckStyle
- JUnit


---

## Step6 自动修复

失败：

```
error.log
```

进入Fix Agent。

限制：

最多3轮。


---

# 五、Agent Prompt设计

## Workflow Agent

```
你是一名高级软件项目经理。

职责：

1.读取OpenSpec
2.拆解任务
3.调度Agent
4.检查状态

禁止：
编写业务代码。

输出：
执行计划。
```

---

## Architecture Agent

```
你是一名Java架构师。

技术：
SpringBoot3
MyBatisPlus
Vue3

根据需求设计：

1.Controller
2.Service
3.DTO
4.异常处理
5.日志方案

输出architecture.md。
```

---

## Coding Agent

```
你是一名高级Java开发工程师。

必须遵守：

- codestyle.md
- log-standard.md
- junit-standard.md

要求：

1.复用已有代码
2.禁止修改无关代码
3.完成后执行mvn test
```

---

## Test Agent

```
你是一名测试开发工程师。

生成JUnit5测试。

必须覆盖：

1.正常流程
2.异常流程
3.边界条件

使用Mockito模拟依赖。
```

---

## Fix Agent

```
你是一名Java问题修复专家。

输入：
Maven错误日志。

要求：

1.定位根因
2.修改代码
3.保持规范
4.重新执行mvn test

禁止删除测试绕过问题。
```

---

# 六、需求文档模板

AI最适合结构化需求。

不要：

```
开发订单查询
```

应该：

```
Feature Spec
```

模板：

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


request:

 fields:
  - orderId


response:

 fields:
  - status
  - createTime


technical:

 framework:
  - SpringBoot3
  - MyBatisPlus


rules:

 - 不存在订单返回404


logging:

 - 必须记录requestId
 - 必须记录耗时


test:

 - 正常查询
 - 空参数
 - 数据不存在


acceptance:

 command:
  mvn clean test
```

---

# 七、项目知识库优化

建议建立：

```
project-context/

├── architecture.md
├── codestyle.md
├── database.md
├── api-standard.md
└── example-code/
```

作用：

让AI从通用开发者变成了解项目规范的开发者。


---

# 八、实施计划

## 第一阶段（1周）

目标：

跑通：

需求 → AI代码 → Maven Test

组件：

- OpenCode
- OpenSpec
- Coding Agent


## 第二阶段（2周）

增加：

- Test Agent
- Fix Agent
- Workflow


## 第三阶段（2-4周）

增加：

- Architecture Agent
- RAG知识库
- Git自动提交


---

# 九、优化建议

## 1. 不追求完全自动开发

目标：

AI完成70%-80%。

人工负责：

- 需求确认
- 架构决策
- 最终审核


## 2. 需求质量比Prompt更重要

AI效果：

输入质量 > Prompt技巧。


## 3. 优先建设项目知识库

知识库包含：

- 架构
- 规范
- 示例代码


## 4. Workflow必须固定

不要：

Agent自由发挥。

应该：

固定流程 + Agent能力。


---

# 十、最终架构总结

```
Feature Spec

    |
    v

Workflow Agent

    |
+---+---+---+

Architecture
Coding
Testing

    |
    v

CodeStyle

    |
    v

Maven Test

    |
    v

Fix Agent

    |
    v

Human Review
```

核心理念：

OpenCode负责智能执行。

OpenSpec负责需求约束。

Workflow负责工程流程。

Multi-Agent负责专业分工。

Maven/JUnit负责质量验证。
