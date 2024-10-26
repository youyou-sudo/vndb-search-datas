import csv
import json
from collections import defaultdict

# 读取标题和数据并转换为NDJSON格式
def convert_to_ndjson(header_file_path, data_file_path, ndjson_file_path):
    # 读取标题
    with open(header_file_path, 'r', encoding='utf-8') as header_file:
        header = header_file.readline().strip().split('\t')

    # 存储每个(tag, vid)的评分和计数
    ratings = defaultdict(lambda: {
        'total_vote': 0,
        'vote_count': 0,
        'total_spoiler': 0,
        'spoiler_count': 0,
        'lie': None  # 用于存储 lie 的最终值
    })

    # 读取数据
    with open(data_file_path, 'r', encoding='utf-8') as data_file:
        reader = csv.DictReader(data_file, fieldnames=header, delimiter='\t')

        # 遍历每一行
        for row in reader:
            # 将"\N"值转换为None
            for key, value in row.items():
                if value == '\\N':
                    row[key] = None

            # 提取评分信息
            vote = row['vote']
            spoiler = row['spoiler']
            lie = row['lie']
            if vote is None:
                continue

            # 转换评分为整数
            vote = int(vote)
            tag = row['tag']
            vid = row['vid']

            # 更新总评分和计数
            ratings[(tag, vid)]['total_vote'] += vote
            ratings[(tag, vid)]['vote_count'] += 1

            # 更新剧透信息
            if spoiler is not None and spoiler.isdigit():  # 确保 spoiler 是一个数字
                spoiler_value = int(spoiler)
                ratings[(tag, vid)]['total_spoiler'] += spoiler_value
                ratings[(tag, vid)]['spoiler_count'] += 1

            # 处理 lie 字段
            if lie == 't':
                ratings[(tag, vid)]['lie'] = 't'  # 最后出现的 lie 为 't'
            elif lie == 'f':
                ratings[(tag, vid)]['lie'] = 'f'  # 最后出现的 lie 为 'f'

    # 计算平均评分和剧透，并逐行写入 NDJSON 文件
    with open(ndjson_file_path, 'w', encoding='utf-8') as ndjson_file:
        for (tag, vid), values in ratings.items():
            average_rating = values['total_vote'] / values['vote_count'] if values['vote_count'] > 0 else 0
            average_rating = round(average_rating)  # 四舍五入为整数

            average_spoiler = values['total_spoiler'] / values['spoiler_count'] if values['spoiler_count'] > 0 else 0
            average_spoiler = round(average_spoiler)  # 四舍五入为整数

            entry = {
                'tag': tag,
                'vid': vid,
                'average_rating': average_rating,
                'average_spoiler': average_spoiler,
                'lie': values['lie']  # 最终的 lie 值
            }

            # 将每个条目写入 NDJSON 文件
            ndjson_file.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"数据已成功转换并保存到 {ndjson_file_path}")

# 使用函数进行转换
convert_to_ndjson('./vndb_data/db/tags_vn.header', './vndb_data/db/tags_vn', 'tags_vn.ndjson')
