# sandbox.py
import subprocess
import tempfile
import os
import sys

def run_code(code: str, test_cases: str, timeout: int = 5) -> tuple[bool, str]:
    """
    执行代码并返回测试报告。
    
    Args:
        code: 待测试的功能代码
        test_cases: 测试用例代码 (包含 assert 语句)
        timeout: 执行超时时间(秒)
        
    Returns:
        (passed: bool, report: str)
        passed: 是否全部通过
        report: 执行日志或错误信息，将作为 Feedback 输入给调试智能体
    """
    
    # 1. 构造完整的可执行脚本
    # 这里的做法是将代码和测试用例拼接。
    # 为了捕获 assert 错误，我们不需要额外的 try-catch，Python 默认会打印 AssertionError
    full_script = f"{code}\n\n# --- Test Cases ---\n{test_cases}"
    
    # 2. 创建临时文件
    # 使用 tempfile 避免文件名冲突
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp_file:
        tmp_file_path = tmp_file.name
        tmp_file.write(full_script)
        
    try:
        # 3. 使用 subprocess 启动独立进程运行
        # capture_output=True 会捕获 stdout 和 stderr
        result = subprocess.run(
            [sys.executable, tmp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # 4. 分析运行结果
        stdout = result.stdout
        stderr = result.stderr
        
        # 如果 returncode 为 0，说明没有抛出异常 (assert 通过)
        if result.returncode == 0:
            return True, "All test cases passed successfully.\n" + stdout
        else:
            # returncode 不为 0，说明有报错
            feedback = f"Execution Failed (Return Code {result.returncode}):\n"
            feedback += f"Error Output:\n{stderr}\n"
            if stdout:
                feedback += f"Standard Output:\n{stdout}\n"
            return False, feedback

    except subprocess.TimeoutExpired:
        return False, f"Execution Timed Out (Limit: {timeout}s). Likely infinite loop."
    
    except Exception as e:
        return False, f"System Error during execution: {str(e)}"
    
    finally:
        # 5. 清理临时文件
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

# ---- 简单测试代码 (运行此文件可验证沙箱功能) ----
if __name__ == "__main__":
    # 模拟一个正确的代码
    good_code = "def add(a, b): return a + b"
    tests = "assert add(1, 1) == 2\nassert add(10, 20) == 30\nprint('Tests done')"
    
    print("Testing Good Code...")
    passed, report = run_code(good_code, tests)
    print(f"Passed: {passed}") # 应该为 True
    
    print("-" * 20)
    
    # 模拟一个错误的代码
    bad_code = "def add(a, b): return a - b" # 逻辑错误
    print("Testing Bad Code...")
    passed, report = run_code(bad_code, tests)
    print(f"Passed: {passed}") # 应该为 False
    print(f"Report Preview: {report.strip().splitlines()[0:2]}") # 应该包含 AssertionError