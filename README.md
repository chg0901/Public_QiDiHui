# Public QiDiHui 

<!---->
<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Stargazers][stars-shield]][stars-url]
<br /> 

## 项目概述

智慧启迪绘不仅仅是一个应用程序，它是一位能引领孩子们踏上奇妙求知之旅的伙伴，带领孩子们进入神奇知识世界的导航员，帮助父母陪伴自己孩子一起阅读《十万个为什么》系列丛书和解答阅读过程中更多疑问的知识助手。

本项目为我们公开的项目开发初期的迭代版本，包含了基本的问答功能，文生图和文生视频做了简化处理， 还请理解。

## 技术亮点

- 借由RAG技术与多模态生成技术的力量，我们倾心打造了一款既具娱乐性又富含教育意义，充满趣味性和互动性的视频生成平台，在孩子们阅读《十万个为什么》系列丛书时，进一步激发他们的好奇心，培养更好的观察能力、思考能力和表达能力，成为开启孩子智慧大门的一把钥匙。
- 两种LLM{appbuilder+ERNIEBot}接口: 充分运用百度文心一言的AIGC能力
- 两种RAG框架: Langchain & LlamaIndex
- RAG创新点: 新型向量数据库存储策略
- 多模态生成: 文本、语音和视频，也支持语音输入
- 流式输出交互UI: 在线生成，快速响应
- 预生成图片， tts和视频， 提高体验

> 以上亮点为我们项目的**完整功能**，并没有完全开源，**请为我们的项目Star以便关注最新更新**

## 主要文件功能介绍
                   
- 开源版本demo：[https://openxlab.org.cn/apps/detail/chg0901/Public_QiDiHui ](https://openxlab.org.cn/apps/detail/chg0901/Public_QiDiHui )              
- AI Studio一键跑通教程： [https://aistudio.baidu.com/projectdetail/8185249](https://aistudio.baidu.com/projectdetail/8185249)

- `requirements.txt`: 相关实验环境所需依赖包
> GPU环境只需把faiss-cpu改为faiss-gpu即可, 可以加快建库
- `web_demo.py`: Gradio Demo 
- `data_full/dataset/Astronomical_dataset.json`: 展示了示例数据， 我们只放置了10个QA数据，由于十万数据有数据隐私协议，书中包含的图片并没有开源，该数据只是展示我们的数据结构
- `faiss_index_langchain_full_ernie/bm25retriever.pkl`: 采用 BM 25 Retriever方案的数据库，这里我们只开源了使用Langchain建的库
- `rag_full/rag_langchain.py`: Langchain建库代码

## 有关宣传资料

### 更新

#### 08/07/2024 项目在Paddle AI Studio上被加精置顶

![image](https://github.com/user-attachments/assets/5e33898a-baaf-49f1-a188-fd7f1219ebee)

**《智慧启迪绘》项目介绍与【LIC2024 RAG赛道第一名方案】大揭秘！**：[https://aistudio.baidu.com/projectdetail/8185249](https://aistudio.baidu.com/projectdetail/8185249?channel=0&channelType=0&sUid=785756&shared=1&ts=1723035546414)

### B站视频: 【 LIC2024 RAG赛道智慧启迪绘】"十万个所以"团队 有关介绍视频

- 【最新版本进展】[https://www.bilibili.com/video/BV1yT8SejEQ8/](https://www.bilibili.com/video/BV1yT8SejEQ8/)
- 【产品说明】[https://www.bilibili.com/video/BV1kn4y1o7VY/](https://www.bilibili.com/video/BV1kn4y1o7VY/)
- 【中期设计demo和进展】[https://www.bilibili.com/video/BV1rb421q7xe/](https://www.bilibili.com/video/BV1rb421q7xe/)
- 【智慧启迪绘】流式输出 超快响应 [https://www.bilibili.com/video/BV1ss8qejEQ5/](https://www.bilibili.com/video/BV1ss8qejEQ5/ ) 


## 启动部署方法

### 环境搭建

这里建议使用conda重新建立一个测试环境

```Bash
# 搭建环境
conda create -n QiDiHui python=3.10
conda activate QiDiHui

# 克隆本项目
git clone https://github.com/chg0901/Public_QiDiHui.git

# 安装软件库
cd Public_QiDiHui
pip install -r requirements.txt

# 启动WebDemo
python web_demo.py
```

### 部署成功后截图

![](https://ai-studio-static-online.cdn.bcebos.com/279f504a36df433c863bd8d2db921fe87bbc2e05761c4e0b8d9b2e534c4c1fcf)

## QiDiHui整体功能逻辑

### 1. 总体图示

QiDiHui的整体功能逻辑可以用下图表示：

![](https://ai-studio-static-online.cdn.bcebos.com/44ca4894cb6f4400a3ab2b3482cc68a1341b638b226441d3bbedcfa454b483d5)

### 2. 通过问题生成有声绘本

QiDiHui支持直接通过一个问题生成有声绘本。

- 若您体验的是OpenXLab上部署的版本：

您可以直接在输入框中输入问题（下图1.a）或者在示例问题中选择问题（下图1.b）之后直接点击“输入问题，生成有声绘本”即可，在线文生图可能需要等待较长时间。

![](https://ai-studio-static-online.cdn.bcebos.com/8a4f6aec13a747d2ae2feccadfb5010fc750870668a84577872e17ea21b0703f)

- 若您体验的是星河社区上部署的版本：

我们为了适配星河社区的部署环境，解耦了有声绘本生成的各个步骤。问题的输入方式不变，但您需要按照下图中的数字顺序依次点击按钮，才可以看到生成的有声绘本。

<img src="https://ai-studio-static-online.cdn.bcebos.com/6f96d79aa11348108d6071f888210a3f95e7fae6964c41d69e1efc5de378817d" width="350"/>

### 3. 通过故事生成有声绘本

**注意：您的故事长度需要在50字以上才能触发剧本生成操作。**

QiDiHui还支持通过现有的故事生成绘本。

- 若您体验的是OpenXLab上部署的版本：

您需要在输入框中输入您的故事，之后按照下图中数字顺序依次点击按钮，就可以看到生成的有声绘本了。

![](https://ai-studio-static-online.cdn.bcebos.com/4d73a363b6fd4456b31f110f696255e8ad93e4bf444f40d09916118350e57b9b)

- 若您体验的是星河社区上部署的版本：

同样地，您需要按照下图中的数字顺序依次点击按钮，就可以看到生成结果了。
![](https://ai-studio-static-online.cdn.bcebos.com/4fa5611c172a4c31b1c60ab2e8dcdc5f08652158f3bf4bc99fe076d3e9c4d8c5)

### 4. 视频演示

请点击[此处](https://www.bilibili.com/video/BV1yT8SejEQ8/?share_source=copy_web&vd_source=fb12a11d11545b5c1139ee0654f2f1c5)跳转到B站观看高清视频和其他合集视频, 欢迎给我们点赞收藏投币一键三连!


### 体验链接

- 智慧启迪绘 基于文心erniebot 和千帆appbuilder 最新体验链接】
  
1.AIStudio主体验链接[https://aistudio.baidu.com/application/detail/40487](https://aistudio.baidu.com/application/detail/40487)
2. OpenXLab 全功能版本[https://openxlab.org.cn/apps/detail/chg0901/QiDiHui_appbuilder_V2](https://openxlab.org.cn/apps/detail/chg0901/QiDiHui_appbuilder_V2)
  
- 【开发版本1：智慧启迪绘 基于文心erniebot 体验链接】[https://openxlab.org.cn/apps/detail/chg0901/QiDiHui](https://openxlab.org.cn/apps/detail/chg0901/QiDiHui)
- 【开发版本2：智慧启迪绘 基于千帆appbuilder 体验链接】[https://openxlab.org.cn/apps/detail/chg0901/QiDiHui_appbuilder](https://openxlab.org.cn/apps/detail/chg0901/QiDiHui_appbuilder)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=chg0901/Public_QiDiHui&type=Date)](https://star-history.com/#chg0901/Public_QiDiHui&Date)

## Contributors: 十万个所以团队

<a href="https://github.com/chg0901/Public_QiDiHui/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=chg0901/Public_QiDiHui" />
</a>

<!--
<a href="https://github.com/chg0901/test_app/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=chg0901/test_app" />
</a>
-->
### 团队成员来自RAG兴趣小组，分别是

- 1. 来自韩国光云大学的 计算机工程博士生 程宏
- 2. 来自 复旦大学的 NLP准研究生 高杨帆
- 3. 来自上海海洋大学的 NLP本科毕业生 彭文博
- 4. 毕业于南京大学的 算法工程师 房宇亮
- 5. 来自昌吉学院 计算机科学与技术专业大三的 郭志航

### 团队过往开源项目 

- 1. EmoLLM [https://github.com/SmartFlowAI/EmoLLM](https://github.com/SmartFlowAI/EmoLLM) 
- 2. 食神 [https://github.com/SmartFlowAI/TheGodOfCookery](https://github.com/SmartFlowAI/TheGodOfCookery)
- 3. 峡谷小狐仙 [https://github.com/chg0901/Honor_of_Kings_Multi-modal_Dataset](https://github.com/chg0901/Honor_of_Kings_Multi-modal_Dataset)
- 4. 程宏和郭志航是Datawhale鲸英助教团成员


[your-project-path]: chg0901/Public_QiDiHui
[contributors-shield]: https://img.shields.io/github/contributors/chg0901/Public_QiDiHui.svg?style=flat-square
[contributors-url]: https://github.com/chg0901/Public_QiDiHui/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/chg0901/Public_QiDiHui.svg?style=flat-square
[forks-url]: https://github.com/chg0901/Public_QiDiHui/network/members
[stars-shield]: https://img.shields.io/github/stars/chg0901/Public_QiDiHui.svg?style=flat-square
[stars-url]: https://github.com/chg0901/Public_QiDiHui/stargazers
[issues-shield]: https://img.shields.io/github/issues/chg0901/Public_QiDiHui.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/chg0901/Public_QiDiHui.svg
[license-shield]: https://img.shields.io/github/license/chg0901/Public_QiDiHui.svg?style=flat-square
[license-url]: https://github.com/chg0901/Public_QiDiHui/blob/main/LICENSE
