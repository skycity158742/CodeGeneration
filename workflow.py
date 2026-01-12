# workflow.py
import config
from agents import ProblemAnalyst, TaskPlanner, CodeGenerator, CodeDebugger
import sandbox
import utils

class MultiAgentSystem:
    def __init__(self):
        # 初始化4个智能体 [cite: 57, 135]
        self.analyst = ProblemAnalyst()
        self.planner = TaskPlanner()
        self.coder = CodeGenerator()
        self.debugger = CodeDebugger()
        
        # 读取配置中的循环上限 [cite: 134]
        self.max_debug_loops = config.MAX_DEBUG_LOOPS
        self.max_reflect_loops = config.MAX_REFLECT_LOOPS

    def solve(self, problem: str, test_cases: str):
        """
        执行多智能体协同代码生成流程 (Algorithm 1)
        """
        print(f"\n{'='*20} Start Coding Task {'='*20}")
        
        # --- Stage 1: Problem Analysis [cite: 67, 137] ---
        print("\n>>> [Stage 1] Analyzing Problem...")
        analysis_result = self.analyst.analyze(problem)
        # 提取分析结果中的关键部分用于后续步骤 (可选，这里直接传递全文也可)
        
        # 初始化变量
        current_plan = ""
        current_code = ""
        test_report = ""
        
        # --- Outer Loop: Reflection (反思循环) [cite: 150-151] ---
        t_r = 0
        while t_r <= self.max_reflect_loops:
            print(f"\n{'*'*10} Reflection Loop: {t_r} {'*'*10}")
            
            # --- Stage 2: Task Planning [cite: 84, 138] ---
            if t_r == 0:
                # 首次尝试：生成初始规划
                print(">>> [Stage 2] Generating Initial Plan...")
                current_plan = self.planner.initial_plan(problem, analysis_result)
            else:
                # 失败后的重试：执行反思规划
                print(">>> [Stage 2] Reflecting and Re-planning...")
                # 将上一轮失败的信息传给Planner
                current_plan = self.planner.reflection_plan(
                    problem, 
                    prev_plan=current_plan, 
                    prev_code=current_code, 
                    test_report=test_report
                )
            
            # 解析出纯文本的 Plan (如果包含标题的话)
            # 这一步是为了让 Coder 看到的输入更干净
            parsed_plan = utils.extract_section(current_plan, "## Modified Planning:") or current_plan

            # --- Stage 3: Code Generation [cite: 115, 139] ---
            print(">>> [Stage 3] Generating Code...")
            current_code = self.coder.generate_code(problem, parsed_plan)
            
            # --- Inner Loop: Debugging (调试循环) [cite: 118, 141-145] ---
            t_d = 0
            while t_d <= self.max_debug_loops:
                print(f"\n  --- Debug Loop: {t_d} ---")
                
                # 3.1 执行测试 (Sandbox) [cite: 141]
                print(f"  [Sandbox] Running tests...")
                passed, report = sandbox.run_code(current_code, test_cases)
                test_report = report # 保存报告供反思使用
                
                if passed:
                    print("\n✅ SUCCESS: Code passed all tests!")
                    print(f"{'='*20} Task Completed {'='*20}")
                    return current_code
                
                print(f"  ❌ FAILED: Tests failed.")
                # print(f"  [Report Summary]: {report.strip().splitlines()[-1]}") # 打印最后一行报错
                
                # 3.2 如果没通过，且还有调试次数，进入调试智能体 [cite: 143]
                if t_d < self.max_debug_loops:
                    print(f"  [Debugger] Attempting to fix code...")
                    current_code = self.debugger.debug(
                        problem, 
                        plan=parsed_plan, 
                        code=current_code, 
                        test_report=test_report
                    )
                else:
                    print(f"  ⚠️ Debug limit reached for this plan.")
                
                t_d += 1
            
            # 如果调试循环结束了还没成功，进入下一轮反思循环 (t_r + 1)
            t_r += 1
            
        print("\n❌ FAIL: Unable to solve problem within all loop limits.")
        return current_code