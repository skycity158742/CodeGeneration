# prompts.py

class Prompts:
    # ----------------------------------------------------------------
    # 1. 问题分析智能体 (对应论文 Figure 2) [cite: 69-79]
    # ----------------------------------------------------------------
    ANALYSIS_PROMPT = """
Given a coding problem. Please analyze the problem, extract the requirement and constraint, and identify the difficulties. Then identify the algorithm needs to be used for the problem. Finally, propose a group of plans and codes as candidate solutions to solve this problem.

# Problem: {problem}

Your response must follow the following format:
## Problem Analyzing:
## Algorithm:
## Candidate Solutions:
"""

    # ----------------------------------------------------------------
    # 2. 任务规划智能体 - 初始规划 (对应论文 Figure 3 上半部分) [cite: 91-98]
    # ----------------------------------------------------------------
    PLANNING_PROMPT = """
Given a coding problem. Please generate a concrete planning to solve the problem.

# Problem: {problem}
## Problem analyzing: {analysis_result}

Your response should give only the planning to solve the problem.
"""

    # ----------------------------------------------------------------
    # 2.1 任务规划智能体 - 反思模式 (对应论文 Figure 3 下半部分) [cite: 99-111]
    # ----------------------------------------------------------------
    # 当任务失败进入反思循环时使用
    REFLECTION_PROMPT = """
Given a coding problem.
# Problem: {problem}

Given your previous trial to solve the problem, including Planning, Codes, Test Report and Debugging Record. Please explain why the previous trial is wrong as indicated by the tests. Then generate the modified planning to solve the problem.

## Planning: {previous_plan}
## Codes: {previous_code}
## Test Report: {test_report}

Your response must follow the following format:
## Explanation:
## Modified Planning:
"""

    # ----------------------------------------------------------------
    # 3. 代码生成智能体 (对应论文 3.4 节) [cite: 114-116]
    # ----------------------------------------------------------------
    # 论文中提到代码生成需要基于详细的任务规划
    CODING_PROMPT = """
Please generate the Python code based on the following planning.
Ensure the code is enclosed in a markdown code block (```python ... ```).

# Problem: {problem}
# Planning: {plan}

Your response must contain the code inside a code block.
"""

    # ----------------------------------------------------------------
    # 4. 代码调试智能体 (对应论文 Figure 4) [cite: 122-132]
    # ----------------------------------------------------------------
    DEBUGGING_PROMPT = """
Given a coding problem. The generated planning and code can not pass the test cases. Please improve the planning and codes to solve the problem correctly.

# Problem: {problem}
## Planning: {plan}
## Code needs to be modified: {code}
## Test Report: {test_report}

Your response must contain the modified planning and the code inside a ```python``` block to solve this problem.
"""