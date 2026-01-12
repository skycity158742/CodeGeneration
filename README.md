# LLM-Driven Multi-Agent Collaborative Code Generation Framework
# 大语言模型驱动的多智能体协同代码生成框架

> 本项目是对论文《大语言模型驱动的多智能体协同代码生成技术》[1] 的复现与工程实现。

## 📖 项目介绍 | Introduction

[cite_start]本项目实现了一个基于多智能体协同（Multi-Agent Collaboration）的代码生成系统。系统通过模拟人类开发者的工作流程，将编程任务分解为**问题分析**、**任务规划**、**代码生成**和**代码调试**四个阶段 [cite: 16, 57]。

[cite_start]不同于直接询问大模型，本框架引入了 **反思循环 (Reflection Loop)** 和 **调试循环 (Debugging Loop)** [cite: 18, 56]，允许智能体根据代码执行反馈（Sandbox Execution Feedback）自动修复错误，显著提升了代码生成的准确率和鲁棒性。

### 核心特性 | Key Features

- [cite_start]**多智能体架构**: 包含 `ProblemAnalyst` (分析), `TaskPlanner` (规划), `CodeGenerator` (编码), `CodeDebugger` (调试) 四个角色的智能体 [cite: 57]。
- **DeepSeek API 集成**: 采用 DeepSeek V3/Coder 模型作为底层推理核心。
- **自我修正机制**: 
  - [cite_start]**Debugging Loop**: 基于沙箱执行结果（Pass/Fail/Error Log）自动修复代码 [cite: 141-143]。
  - [cite_start]**Reflection Loop**: 当多次调试失败后，触发反思机制，重新调整任务规划 [cite: 150]。
- **安全沙箱**: 使用独立子进程执行生成的 Python 代码，支持超时控制。

## 📂 项目结构 | Project Structure

```text
DeepSeek-MultiAgent-Coder/
├── agents.py           # 智能体类定义 (Analyst, Planner, Coder, Debugger)
[cite_start]├── workflow.py         # 核心调度器 (实现论文 Algorithm 1) [cite: 135]
├── sandbox.py          # 代码执行沙箱与测试运行器
├── prompts.py          # 结构化提示词模板 (对应论文 Figure 2, 3, 4)
├── utils.py            # Markdown 解析与代码提取工具
├── config.example.py   # 配置文件模版 (需重命名使用)
├── main.py             # 系统入口与演示 Demo
└── evaluate.py         # 批量评估脚本 (Mini-HumanEval)
```

## 🚀 快速开始 | Quick Start
1. 环境准备
确保已安装 Python 3.8+，并安装依赖库：
    ```Bash
    pip install openai
    ```

2. 配置 API Key
- 为了安全起见，本项目不包含直接的配置文件。
- 将 config.example.py 重命名为 config.py。
- 编辑 config.py，填入你的 DeepSeek API Key：
    ```Python
    API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
    BASE_URL = "[https://api.deepseek.com](https://api.deepseek.com)"
    ```

3. 运行演示
运行主程序，观察多智能体如何协同解决一个编程问题（如斐波那契数列或24点游戏）：
    ```Bash
    python main.py
    ```

4. 运行评估
使用内置的迷你数据集进行批量测试：
    ```Bash
    python evaluate.py
    ```

## 📊 实验设计 | Methodology
本系统的核心逻辑遵循论文中的协同调度算法：
- 分析阶段: 提取需求与约束。
- 规划阶段: 制定初始计划或基于失败记录进行反思规划。
- 编码阶段: 基于规划生成代码。
- 调试阶段: 执行测试用例。如果失败，Debugger 智能体将读取错误报告并尝试修复 。

## 📚 参考文献 | References
[1] 夏鹏, 张钧, 齐骥. 大语言模型驱动的多智能体协同代码生成技术 [J]. 计算机科学, 2025. [2] Xia Peng, Zhang Yijun, Qi Ji. Multi-agent Collaborative Code Generation Technology Driven by Large Language Models. Computer Science, 2025.

## 📝 License
MIT License