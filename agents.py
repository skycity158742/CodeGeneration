# agents.py
import llm_api
from prompts import Prompts
import utils

class ProblemAnalyst:
    """问题分析智能体 (论文 3.2)"""
    def analyze(self, problem: str) -> str:
        print(f"  [Analyst] Analyzing problem...")
        prompt = Prompts.ANALYSIS_PROMPT.format(problem=problem)
        response = llm_api.call_llm(prompt)
        # 这里我们直接返回整个分析结果，因为它将完整地作为Planner的输入
        return response

class TaskPlanner:
    """任务规划智能体 (论文 3.3)"""
    def initial_plan(self, problem: str, analysis_result: str) -> str:
        print(f"  [Planner] Creating initial plan...")
        prompt = Prompts.PLANNING_PROMPT.format(
            problem=problem,
            analysis_result=analysis_result
        )
        response = llm_api.call_llm(prompt)
        return response

    def reflection_plan(self, problem: str, prev_plan: str, prev_code: str, test_report: str) -> str:
        """对应论文中的反思机制 (Reflection Loop)"""
        print(f"  [Planner] Reflecting on failure...")
        prompt = Prompts.REFLECTION_PROMPT.format(
            problem=problem,
            previous_plan=prev_plan,
            previous_code=prev_code,
            test_report=test_report
        )
        response = llm_api.call_llm(prompt)
        # 只需要提取修正后的计划部分
        modified_plan = utils.extract_section(response, "## Modified Planning:")
        # 如果提取失败（模型没遵循格式），则兜底返回整个回复
        return modified_plan if modified_plan else response

class CodeGenerator:
    """代码生成智能体 (论文 3.4)"""
    def generate_code(self, problem: str, plan: str) -> str:
        print(f"  [Coder] Generating code...")
        prompt = Prompts.CODING_PROMPT.format(
            problem=problem,
            plan=plan
        )
        response = llm_api.call_llm(prompt)
        code = utils.extract_code(response)


        # 【新增】故意搞破坏：如果是在测试斐波那契，强制在代码末尾加个 Bug
        if "fibonacci" in problem.lower():
            print("  [😈 Sabotage] Injecting a bug to test Debugger...")
            code = code.replace("return", "retrun") # 故意算错结果

        return code

class CodeDebugger:
    """代码调试智能体 (论文 3.5)"""
    def debug(self, problem: str, plan: str, code: str, test_report: str) -> str:
        print(f"  [Debugger] Fixing code...")
        prompt = Prompts.DEBUGGING_PROMPT.format(
            problem=problem,
            plan=plan,
            code=code,
            test_report=test_report
        )
        response = llm_api.call_llm(prompt)
        fixed_code = utils.extract_code(response)
        return fixed_code