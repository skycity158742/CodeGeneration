# main.py
from workflow import MultiAgentSystem

def main():
    # 1. 定义一个稍微有点难度的题目 (斐波那契数列，但要求处理异常输入)
    # 这样的题目容易第一次写错（比如忘了负数），从而触发Debug流程，展示系统能力。
    problem = """
    Write a Python function `fibonacci(n)` that returns the n-th Fibonacci number. 
    The sequence starts with 0, 1. So fibonacci(0)=0, fibonacci(1)=1, fibonacci(2)=1, etc.
    If n is negative, raise a ValueError with message "Input cannot be negative".
    """

    # 2. 定义测试用例 (Assert Statements)
    # 注意：这些将直接拼接在生成代码后面运行
    test_cases = """
print("Running Test Cases...")
assert fibonacci(0) == 0, "Test 0 Failed"
assert fibonacci(1) == 1, "Test 1 Failed"
assert fibonacci(2) == 1, "Test 2 Failed"
assert fibonacci(10) == 55, "Test 10 Failed"

# 测试异常处理
try:
    fibonacci(-5)
except ValueError as e:
    assert str(e) == "Input cannot be negative", "Error message mismatch"
else:
    assert False, "Did not raise ValueError for negative input"

print("All Test Cases Passed!")
    """

    # 3. 启动系统
    system = MultiAgentSystem()
    final_code = system.solve(problem, test_cases)
    
    # 4. 展示最终结果
    print("\n\n" + "="*30)
    print("FINAL GENERATED CODE:")
    print("="*30)
    print(final_code)

if __name__ == "__main__":
    main()