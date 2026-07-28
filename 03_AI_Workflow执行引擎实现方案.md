# AI Workflow执行引擎实现方案

## 1. 目标

实现：

需求 -> Agent -> 代码 -> 测试 -> 修复

自动流程。

## 2. 推荐POC方案

不要开发复杂平台。

采用：

- YAML Workflow
- OpenCode CLI
- Shell脚本
- Maven

## 3. Workflow示例

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

## 4. 执行流程

1.读取OpenSpec

2.Workflow Agent拆解任务

3.Coding Agent生成代码

4.Test Agent生成JUnit

5.maven test验证

6.Fix Agent修复

## 5. 后续演进

POC:

脚本调度

企业版:

Workflow Service + Web UI
