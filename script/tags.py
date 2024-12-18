import csv
import json


# 读取标题和数据并转换为 NDJSON 格式，同时匹配 JSON map 对象
def convert_to_ndjson_with_map(header_file_path, data_file_path, ndjson_file_path, json_file_path):
    # 读取标题
    with open(header_file_path, 'r', encoding='utf-8') as header_file:
        header = header_file.readline().strip().split('\t')

    # 读取 JSON 文件并找到匹配的 map 对象
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        map_data = None
        for item in json_data:
            if "name" in item and "(标签与特征)" in item["name"]:
                map_data = item.get("map", {})
                break

    if map_data is None:
        raise ValueError("未找到包含 '(标签与特征)' 的 map 数据。")

    # 读取数据并转换为 NDJSON 格式
    with open(data_file_path, 'r', encoding='utf-8') as data_file, \
            open(ndjson_file_path, 'w', encoding='utf-8') as ndjson_file:

        reader = csv.DictReader(data_file, fieldnames=header, delimiter='\t')

        for row in reader:
            # 将 "\N" 值转换为 None
            for key, value in row.items():
                if value == '\\N':
                    row[key] = None

            # 匹配 name 字段并添加 name_zh 字段
            if row["name"] in map_data:
                row["name_zh"] = map_data[row["name"]]
            else:
                row["name_zh"] = None  # 如果未匹配到，设置为 None

            # 将行数据写入 NDJSON 文件，每行为一个 JSON 对象
            ndjson_file.write(json.dumps(row, ensure_ascii=False) + '\n')

    print(f"数据已成功转换并保存到 {ndjson_file_path}")


# 使用函数进行转换
convert_to_ndjson_with_map(
    './vndb_data/db/tags.header',
    './vndb_data/db/tags',
    'tags.ndjson',
    'otherPageRules_output.json'
)
