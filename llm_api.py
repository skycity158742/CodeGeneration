# llm_api.py
from openai import OpenAI
import config

# 初始化客户端
client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)

def call_llm(prompt: str, model: str = config.MODEL_NAME) -> str:
    """
    通用的大模型调用函数
    Args:
        prompt: 输入给模型的提示词
        model: 使用的模型名称
    Returns:
        模型的文本响应
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful expert developer."},
                {"role": "user", "content": prompt},
            ],
            # 论文  提到为了保证结果可重复性，建议使用贪心搜索(temperature=0)
            temperature=0.0, 
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return ""

# 简单的测试代码
if __name__ == "__main__":
    print("Testing connection to DeepSeek...")
    res = call_llm("Hello, reply 'Connection Successful' if you see this.")
    print(f"Response: {res}")