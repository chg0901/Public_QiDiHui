import json
import os
import time
import warnings

import appbuilder
import gradio as gr
import modelscope_studio as mgr

from rag_full.rag_langchain import FaissSearch, tokenize_chinese  # tokenize_chinese需要在这里import，否则pickle会报错

warnings.filterwarnings('ignore')

# 配置密钥与应用ID
# 设置环境变量APPBUILDER_TOKEN，目前填的这个是官方的受限试用TOKEN
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-DyYuSA9DVtgt3uLCJvj09/66566c4c39901e34c20829d07bbe993654c03452"
app_id = "b2c236c9-e544-4d16-8e74-016c602ef342"

# 创建一个FaissSearch实例，用于检索向量数据库，每次检索返回top_k个相关文档
search_engine = FaissSearch(path='./faiss_index_llama_full_ernie', top_k=5, threshold=10)

# 使用appbuilder创建LLM对话接口
llm = appbuilder.AppBuilderClient(app_id)

prompt = """
检索结果:
第1个段落:
{doc}
检索语句: 你的名字是启迪绘，擅长把科学事实编成有趣易懂的故事，以激发儿童对相关领域的好奇心，同时这个故事应当作为成为亲子共读的桥梁，助力孩子们在轻松愉快的氛围中学习成长。
你需要根据我的问题和你所知道的知识为我创作符合以上要求的故事。
我的问题是：
{query}
请根据以上检索结果回答检索语句的问题
"""
docs = []


def resolve_assets(relative_path):
    return os.path.join(os.path.dirname(__file__), "resources",
                        relative_path)


conversation = [
    [None, {
        "text": "你好，欢迎来到😶‍🌫️智慧启迪绘！",
        "flushing": False
    }],
]


def get_last_bot_message(chatbot):
    return chatbot[-1][1]


def create_video_bot_message(text: str):
    return {
        "text": text,
    }


def create_image_bot_message(text: str):
    return {
        "text": text,
    }


async def chat_bot_with_llm(_input: mgr.MultimodalInput, _chatbot):
    global prompt, docs, search_engine, llm
    _chatbot.append([_input, [""]])
    yield gr.update(interactive=False, value=None), _chatbot

    docs = search_engine.search(_input.text)

    if len(docs) > 0:
        # 取出检索到的相关性最高的文档
        doc = docs[0]['content']
    else:
        # 如果没有检索到相关文档，则将doc置为空字符串
        doc = ""

    final_prompt = prompt.replace('{query}', _input.text).replace('{doc}', doc)

    conversation_id = llm.create_conversation()
    messages = llm.run(conversation_id, final_prompt, stream=True)

    for content in messages.content:
        if content.answer is not None:
            _chatbot[-1][1][0] += content.answer
            yield {
                chat_bot_1: _chatbot,
            }


async def chat_bot_with_llm_image(_input: mgr.MultimodalInput, _chatbot):
    global prompt, docs, search_engine, llm
    _chatbot.append([_input, [""]])
    yield gr.update(interactive=False, value=None), _chatbot

    docs = search_engine.search(_input.text)

    if len(docs) > 0:
        # 取出检索到的相关性最高的文档
        doc = docs[0]['content']
        # 取出图片信息
        image_paths = docs[0]['image']
    else:
        # 如果没有检索到相关文档，则将doc置为空字符串
        doc = ""
        # 如果没有检索到相关文档，则将image_paths置为空列表
        image_paths = []

    final_prompt = prompt.replace('{query}', _input.text).replace('{doc}', doc)

    conversation_id = llm.create_conversation()
    messages = llm.run(conversation_id, final_prompt, stream=True)

    for content in messages.content:
        if content.answer is not None:
            _chatbot[-1][1][0] += content.answer
            yield {
                chat_bot_2: _chatbot,
            }


    for path_dict in image_paths:
        image_path = './data/data269367/OEBPS/' + path_dict['path']
        _chatbot[-1][1][0] += f"""
<div style="text-align:center">
    <img style="width: 100%; border-radius: 0.32em;
    box-shadow: 0 2px 5px 0 rgba(35,36,38,.12),0 2px 10px 0 rgba(35,36,38,.08);" 
    src="{image_path}">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d7;
    display: inline-block;
    color: #999;
    padding: 2px;">{path_dict['tushuo']}</div>
</div>
"""
        yield {
            chat_bot_2: _chatbot,
        }


def chat_image(_input, _chatbot):
    _chatbot.append([_input, None])
    yield gr.update(interactive=False, value=None), _chatbot
    _chatbot[-1][1] = [
        create_image_bot_message("")
    ]

    time.sleep(1)
    get_last_bot_message(_chatbot)[0][
        "text"] = """你好，欢迎来到😶‍🌫️智慧启迪绘 \n
        <accordion title="生成图片">

        ![IMAGEGEN]("https://oss.lingkongstudy.com.cn/blog/202405261707489.jpg")

        </accordion>"""
    yield {
        chat_bot_2: _chatbot,
    }


def chat_video(_input, _chatbot):
    _chatbot.append([_input, None])
    yield gr.update(interactive=False, value=None), _chatbot
    _chatbot[-1][1] = [
        create_video_bot_message("")
    ]

    time.sleep(1)
    get_last_bot_message(_chatbot)[0][
        "text"] = f"""你好，欢迎来到😶‍🌫️智慧启迪绘 \n
        <video src="{resolve_assets("dog.mp4")}"></video> \n
        <accordion title="生成图片">

        <img src="https://oss.lingkongstudy.com.cn/blog/202405261707489.jpg" style="float: left;">
        <img src="https://oss.lingkongstudy.com.cn/blog/202405261707489.jpg" style="float: left;">

        </accordion>"""
    yield {
        chat_bot_3: _chatbot,
    }


def flushed():
    return gr.update(interactive=True)


def read_grouped_queries(file_path):
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取并返回 "grouped_queries" 列表
    grouped_queries = data.get('grouped_queries', [])

    # 返回第一个子列表，如果没有则返回空列表
    if grouped_queries:
        return grouped_queries
    else:
        return []


css = """
h1 {
  text-align: center;
  display: block;
}
"""
json_path = "list.json"

avatar_images = [
    # resolve_assets('user.jpeg'),
    # default bot avatar and name
    [{
        "name": "Curious baby",
        "avatar": "https://oss.lingkongstudy.com.cn/blog/202405271251981.png"
    }],

    [{
        "name": "QiDiHui",
        "avatar": "https://oss.lingkongstudy.com.cn/blog/202405261707489.jpg"
    }],

]

# 创建Gradio界面
with gr.Blocks(gr.themes.Soft(), css=css) as demo:
    html_code = """
            <h1 style="text-align: center;">😶‍🌫️ 智慧启迪绘</h1>

            <p align="center">
                <img src="https://oss.lingkongstudy.com.cn/blog/202405261707489.jpg" alt="Logo" width="20%" style="border-radius: 5px;">
            </p>
            <div class="hint" style="text-align: center; background-color: rgba(255, 255, 0, 0.15); padding: 20px; margin: 20px; border-radius: 5px; border: 1px solid #ffcc00;">
                <h3 align="center">智慧启迪绘展示了语言与智能技术的深度融合，旨在为用户带来全新的互动体验。</h3>
            </div>

        """
    gr.Markdown(html_code)
    with gr.Tabs():
        with gr.TabItem("对话"):
            chat_bot_1 = mgr.Chatbot(
                value=conversation,
                avatar_image_width=60,
                avatar_images=avatar_images,
                height=500,
                flushing_speed=6,
            )
            state = gr.State([])

            input = mgr.MultimodalInput()
            input.submit(fn=chat_bot_with_llm, inputs=[input, chat_bot_1], outputs=[input, chat_bot_1])
            chat_bot_1.flushed(fn=flushed, outputs=[input])

            with gr.Column():
                with gr.Accordion(open=True, label="😀输入示例："):  # 使用 Accordion 组件创建可以折叠的区域
                    gr.Examples(examples=read_grouped_queries(json_path), inputs=input, outputs=chat_bot_1)

        with gr.TabItem("文生图"):
            chat_bot_2 = mgr.Chatbot(
                value=conversation,
                avatar_image_width=40,
                avatar_images=avatar_images,
                height=500,
                flushing_speed=6,
            )

            input = mgr.MultimodalInput()
            input.submit(fn=chat_bot_with_llm_image, inputs=[input, chat_bot_2], outputs=[input, chat_bot_2])
            chat_bot_2.flushed(fn=flushed, outputs=[input])

            with gr.Column():
                with gr.Accordion(open=True, label="😀输入示例："):  # 使用 Accordion 组件创建可以折叠的区域
                    gr.Examples(examples=read_grouped_queries(json_path), inputs=input, outputs=chat_bot_2)

        with gr.TabItem("文生视频"):
            chat_bot_3 = mgr.Chatbot(
                value=conversation,
                avatar_image_width=40,
                avatar_images=avatar_images,
                height=500,
                flushing_speed=6,
            )

            input = mgr.MultimodalInput()
            input.submit(fn=chat_video, inputs=[input, chat_bot_3], outputs=[input, chat_bot_3])
            chat_bot_3.flushed(fn=flushed, outputs=[input])

            with gr.Column():
                with gr.Accordion(open=True, label="😀输入示例："):  # 使用 Accordion 组件创建可以折叠的区域
                    gr.Examples(examples=read_grouped_queries(json_path), inputs=input, outputs=chat_bot_3)

# 启动Gradio应用
if __name__ == "__main__":
    demo.queue().launch()
