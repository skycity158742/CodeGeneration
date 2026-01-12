# utils.py
import re

def extract_section(text: str, section_header: str) -> str:
    """
    从Markdown文本中提取指定标题下的内容。
    例如提取 '## Algorithm:' 后面的内容，直到下一个标题开始。
    对应论文中提到的“解析并处理为任务规划提示词”等步骤 [cite: 138]。
    """
    pattern = rf"{section_header}\s*(.*?)(?=\n##|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def extract_code(text: str) -> str:
    """
    提取Markdown中的Python代码块。
    对应论文中从输出结果解析程序代码的步骤 [cite: 140]。
    """
    # 匹配 ```python ... ``` 或 ``` ... ```
    pattern = r"```(?:python)?\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # 兜底逻辑：如果没找到代码块，且文本看起来像代码（包含def），则返回原文本
    if "def " in text:
        return text.strip()
        
    return ""

# ---- 简单测试代码 (运行此文件可验证解析功能) ----
if __name__ == "__main__":
    sample_text = """
    Here is the analysis.
    ## Problem Analyzing:
    This is a sorting problem.
    ## Algorithm:
    Quick Sort.
    ## Candidate Solutions:
    Plan A...
    """
    
    print(f"提取 Algorithm: {extract_section(sample_text, '## Algorithm:')}") 
    # 应该输出: Quick Sort.