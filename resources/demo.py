# import json

# # 读取JSON文件
# file_path = 'all_output.json'

# with open(file_path, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # 假设queries在文件中的键是'queries'
# queries = [item['query'] for item in data]

# # 将 query 值每十个为一组存为 list
# grouped_queries = [queries[i:i + 10] for i in range(0, len(queries), 10)]

# # 打印结果
# output_data = {'grouped_queries': grouped_queries}

# with open('grouped_queries.json', 'w', encoding='utf-8') as f:
#     json.dump(output_data, f, ensure_ascii=False, indent=4)

# print("Grouped queries have been written to 'grouped_queries.json'")

import json


def read_grouped_queries(file_path):
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取并返回 "grouped_queries" 列表
    return data.get(f'grouped_queries[{0}]', [])


print(read_grouped_queries('grouped_queries.json'))
