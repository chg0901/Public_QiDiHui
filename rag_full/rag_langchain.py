import json
import os
import time
import jieba
from langchain_core.documents import Document


def resolve_assets(relative_path):
    """
    根据相对路径解析出绝对路径
    """
    return os.path.join(os.path.dirname(__file__), relative_path)


# 数据集路径
data_path = resolve_assets("../data_full/dataset")

# 向量数据库持久化路径
faiss_name = resolve_assets("../faiss_index_langchain_full_ernie")


def load_dataset():
    """
    加载数据集文件
    """
    book_list = ["Astronomical"]
    json_data = []
    for book_name in book_list:
        with open(f"{data_path}/{book_name}_dataset.json", 'r', encoding='utf-8') as f:
            json_data.extend(json.load(f))
    return json_data


def generate_docs(json_data=None):
    """
    将原始数据转换为适用于问答对编码的langchain Document对象
    """
    if json_data is None:
        json_data = load_dataset()

    # 创建待编码文档集
    docs = []
    for i in range(len(json_data)):
        # 取出每个问答对的问题和答案
        question = json_data[i]['question']
        answer = json_data[i]['answer']
        image = json_data[i]['image']
        source_book = json_data[i]['source_book']
        source_file = json_data[i]['source_file']
        # 问题部分作为文本节点的text用于编码和检索，答案部分存储在metadata中
        docs.append(Document(page_content=question,
                             metadata={"answer": answer, "image": image, "source_book": source_book,
                                       "source_file": source_file}))
    return docs


class FaissSearch:
    def __init__(self, path=faiss_name, top_k=5, threshold=10):
        """
        初始化函数，用于创建一个检索器对象。

        Args:
            path (str, optional): FAISS索引文件持久化的路径，默认为'faiss_name'。
            top_k (int, optional): 返回的相似度最高的k个结果，默认为5。
            threshold (float, optional): 相似度阈值，只有当相似度大于该阈值时，才会被作为候选结果，默认为10。
        """
        self.top_k = top_k
        self.threshold = threshold
        self.retriever = get_BM25_retriever(top_k)

    def bm25_search(self, real_query):
        """
        调用BM25检索器
        """
        print("开始检索")
        start_time = time.time()
        docs = self.retriever.get_relevant_documents(real_query)
        print("检索结束，耗时：", time.time() - start_time)
        retrieval_results = []
        score = len(docs)
        for doc in docs:
            # 遍历检索到的文档
            # 把答案从metadata中取出，作为检索结果返回
            # langchain的BM25检索器不返回score，只返回文档
            # 这里不进行过滤，而是直接用文档的顺序作为评分，靠前的文档评分高
            print(doc)
            retrieval_results.append(
                {"content": doc.metadata["answer"], "score": score, "title": doc.page_content,
                 "image": doc.metadata["image"], "source_book": doc.metadata["source_book"],
                 "source_file": doc.metadata["source_file"]}
            )
            score -= 1
            # 将文档的内容、评分和标题添加到结果列表中
        return retrieval_results

    def search(self, query, **kwargs):
        """
        执行检索
        """
        real_query = query
        return self.bm25_search(real_query)


def tokenize_chinese(text):
    """
    使用jieba进行中文分词
    """
    # 我也不知道为什么，直接把jieba.lcut作为BM25Retriever.from_defaults的参数，会导致无法pickle序列化
    # 这里重新封装一下，就可以了
    return jieba.lcut(text)


def create_BM25_retriever(top_k=5):
    """
    基于待编码文档集，创建BM25检索器，分词器使用jieba
    """
    from langchain_community.retrievers import BM25Retriever
    docs = generate_docs()
    bm25_retriever = BM25Retriever.from_documents(documents=docs, preprocess_func=tokenize_chinese)
    bm25_retriever.k = top_k
    return bm25_retriever


def get_BM25_retriever(top_k=5):
    """
    获取BM25检索器，如果已经存在则加载，否则创建并持久化
    """
    import pickle
    if os.path.exists(faiss_name + "/bm25retriever.pkl"):
        bm25_retriever = pickle.load(open(faiss_name + "/bm25retriever.pkl", 'rb'))
        bm25_retriever.k = top_k
    else:
        bm25_retriever = create_BM25_retriever(top_k)
        pickle.dump(bm25_retriever, open(faiss_name + "/bm25retriever.pkl", 'wb'))
    return bm25_retriever


def faiss_search_test(top_k=5, threshold=10):
    """
    FaissSearch类的测试函数
    """
    faiss_search = FaissSearch(top_k=top_k, threshold=threshold)
    results = faiss_search.search("天上有多少颗星星")
    for result in results:
        print(result)


def bm25_retriever_test(top_k=5):
    """
    BM25检索器的测试函数
    """
    bm25_retriever = get_BM25_retriever(top_k)
    results = bm25_retriever.get_relevant_documents("天上有多少颗星星")
    for result in results:
        print(result)


if __name__ == "__main__":
    # 启动FaissSearch类的测试
    faiss_search_test(top_k=3, threshold=10)
    # 启动BM25检索器的测试
    bm25_retriever_test(3)
