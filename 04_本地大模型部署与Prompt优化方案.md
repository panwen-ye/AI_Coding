# 本地大模型部署与Prompt优化方案

## 1. 目标

让本地模型稳定完成：

- Java编码
- 测试生成
- Bug修复

## 2. Prompt设计原则

不要：

```
帮我写代码
```

应该：

```
角色
背景
输入
约束
输出
验证方式
```

## 3. Coding Agent Prompt示例

```
你是一名高级Java工程师。

技术栈:
SpringBoot3
MyBatisPlus

必须遵守:
codestyle.md
log-standard.md

要求:
1.先分析已有代码
2.禁止修改无关文件
3.生成JUnit测试
4.执行mvn test
```

## 4. 模型效果优化

增加：

- 项目知识库
- 示例代码
- 架构文档
- 常见问题库

## 5. 推荐能力分工

大模型负责：

推理和生成。

工具负责：

编译、测试、执行。
