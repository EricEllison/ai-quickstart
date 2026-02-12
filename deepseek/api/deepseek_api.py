import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()   # 加载 .env 文件中的变量到 os.environ

# DeepSeek API Key 的环境变量名
ENV_API_KEY = "DEEPSEEK_API_KEY"
# DeepSeek API 基础 URL
BASE_URL = "https://api.deepseek.com"
# 使用的模型名称
MODEL_NAME = "deepseek-chat"
# 输出 HTML 文件的路径
OUTPUT_HTML_PATH = Path("game.html")
# 系统消息，用于设定 AI 助手的角色
SYSTEM_MESSAGE = "你是一个专业的 Web 开发助手,擅长用 HTML/CSS/JavaScript 编写游戏。"

# 用户提示词，描述要生成的五子棋游戏需求
PROMPT = """
请创建一个现代风格的五子棋游戏，保存在单个 HTML 文件中。
设计要求：
1. UI 风格：深色极简主题（Dark Mode），背景使用深蓝色或深灰色渐变。
2. 棋盘：使用 Canvas 绘制，具有逼真的木质质感或高对比度网格。
3. 交互：棋子要有 CSS 阴影和渐变使其看起来有立体感。
4. 功能：双人对战模式，必须包含"悔棋"和"重新开始"按钮，获胜时弹出美观的模态框（Modal）提示。
5. 代码格式：请尽量紧凑，确保在单次回答中能生成完整的代码。
注意：请只提供代码，不要添加 Markdown 标记。
"""


def require_env(name: str) -> str:
    """
    获取必需的环境变量，如果不存在则抛出异常
    
    Args:
        name: 环境变量名称
        
    Returns:
        环境变量的值
        
    Raises:
        ValueError: 当环境变量未设置时
    """
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"请设置环境变量 {name}")

    return value


def create_client() -> OpenAI:
    """
    创建并返回 OpenAI 客户端实例（用于 DeepSeek API）
    
    Returns:
        配置好的 OpenAI 客户端实例
    """
    api_key = require_env(ENV_API_KEY)
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def generate_html_via_chat(client: OpenAI, prompt: str) -> str:
    """
    通过 DeepSeek Chat API 生成 HTML 游戏代码
    
    Args:
        client: OpenAI 客户端实例
        prompt: 用户提示词，描述要生成的游戏需求
        
    Returns:
        生成的 HTML 代码字符串
        
    Raises:
        RuntimeError: 当 API 返回空响应或无效内容时
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        stream=False,
    )

    # 检查响应是否包含有效的选项
    if not getattr(response, "choices", None):
        raise RuntimeError("API 返回了空响应，无法生成游戏代码")

    # 提取消息内容
    message = response.choices[0].message
    html = getattr(message, "content", None)
    if not html:
        raise RuntimeError("API 响应中未包含有效内容，无法生成游戏代码")

    return html


def write_text(path: Path, content: str) -> None:
    """
    将文本内容写入指定路径的文件
    
    Args:
        path: 文件路径
        content: 要写入的文本内容
    """
    path.write_text(content, encoding="utf-8")


def main() -> None:
    """
    主函数：创建客户端，调用 API 生成五子棋游戏，并保存为 HTML 文件
    """
    # 创建 DeepSeek API 客户端
    client = create_client()

    try:
        # 调用 API 生成 HTML 游戏代码
        html = generate_html_via_chat(client, PROMPT)
        # 将生成的代码保存到文件
        write_text(OUTPUT_HTML_PATH, html)
        print(f"游戏代码已生成并保存为 {OUTPUT_HTML_PATH}")
    except Exception as exc:
        print(f"调用 API 出错: {exc}")


if __name__ == "__main__":
    main()
