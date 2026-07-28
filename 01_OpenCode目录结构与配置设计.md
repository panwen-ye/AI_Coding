# OpenCode 目录结构与配置设计

## 1. 目标

设计 OpenCode 在企业 AI Coding Workflow 中的工程化目录结构。

## 2. 推荐结构

```
project-ai/

├── opencode/
│
├── agents/
│   ├── workflow-agent.md
│   ├── coding-agent.md
│   ├── test-agent.md
│   ├── fix-agent.md
│
├── skills/
│   ├── java-coding/
│   ├── junit-testing/
│   ├── code-review/
│
├── prompts/
│
├── context/
│   ├── architecture.md
│   ├── codestyle.md
│   ├── database.md
│
└── workflows/
    └── feature-dev.yaml
```

## 3. Agent设计原则

- 一个Agent只负责一种专业能力
- Prompt、Skill、Context分离
- Workflow负责调度

## 4. Skill设计

Skill不是Prompt，而是可复用能力。

例如：

java-coding:

- Spring Boot开发规范
- 分层规范
- 异常处理规范

## 5. 配置管理

建议：

- 项目级配置
- 公司级规范
- Agent个人能力

分层加载。
