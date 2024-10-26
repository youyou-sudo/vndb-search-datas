import csv
import json


# 读取标题和数据并转换为NDJSON格式
def convert_to_ndjson(header_file_path, data_file_path, ndjson_file_path):
    # 读取标题
    with open(header_file_path, 'r', encoding='utf-8') as header_file:
        header = header_file.readline().strip().split('\t')

    # 读取数据并转换为 NDJSON 格式
    with open(data_file_path, 'r', encoding='utf-8') as data_file, \
            open(ndjson_file_path, 'w', encoding='utf-8') as ndjson_file:

        reader = csv.DictReader(data_file, fieldnames=header, delimiter='\t')

        for row in reader:
            # 将 "\N" 值转换为 None
            for key, value in row.items():
                if value == '\\N':
                    row[key] = None

            # 将行数据写入 NDJSON 文件，每行为一个 JSON 对象
            ndjson_file.write(json.dumps(row, ensure_ascii=False) + '\n')

    print(f"数据已成功转换并保存到 {ndjson_file_path}")


# 使用函数进行转换
convert_to_ndjson('./vndb_data/db/tags.header', './vndb_data/db/tags', 'tags.ndjson')
