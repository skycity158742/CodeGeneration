# test_agents.py
from agents import ProblemAnalyst, TaskPlanner, CodeGenerator

def test_flow():
    problem = "Write a Python function to check if a number is prime."
    
    # 1. 测试分析
    analyst = ProblemAnalyst()
    analysis = analyst.analyze(problem)
    print("--- Analysis Result (Preview) ---")
    print(analysis[:100] + "...") 
    
    # 2. 测试规划
    planner = TaskPlanner()
    plan = planner.initial_plan(problem, analysis)
    print("\n--- Plan Result (Preview) ---")
    print(plan[:100] + "...")
    
    # 3. 测试写代码
    coder = CodeGenerator()
    code = coder.generate_code(problem, plan)
    print("\n--- Generated Code ---")
    print(code)

if __name__ == "__main__":
    test_flow()