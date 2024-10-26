import csv
import json
from collections import defaultdict
from datetime import datetime

# 定义列名
vn_columns = ['id', 'olang', 'image', 'l_wikidata', 'c_votecount', 'c_rating', 'c_average', 'length', 'devstatus',
              'alias', 'l_renai', 'description']
vn_titles_columns = ['id', 'lang', 'official', 'title', 'latin']
releases_titles_columns = ['id', 'lang', 'mtl', 'title', 'latin']
releases_vn_columns = ['id', 'vid', 'rtype']

releases_fields = [
    'id', 'olang', 'gtin', 'l_toranoana', 'l_appstore', 'l_nintendo_jp', 'l_nintendo_hk', 'released',
    'l_steam', 'l_digiket', 'l_melon', 'l_mg', 'l_getchu', 'l_getchudl', 'l_egs', 'l_erotrail',
    'l_melonjp', 'l_gamejolt', 'l_animateg', 'l_freem', 'l_novelgam', 'voiced', 'reso_x', 'reso_y',
    'minage', 'ani_story', 'ani_ero', 'ani_story_sp', 'ani_story_cg', 'ani_cutscene', 'ani_ero_sp',
    'ani_ero_cg', 'ani_bg', 'ani_face', 'has_ero', 'patch', 'freeware', 'uncensored', 'official',
    'website', 'catalog', 'engine', 'notes', 'l_dlsite', 'l_gog', 'l_denpa', 'l_jlist', 'l_jastusa',
    'l_itch', 'l_nutaku', 'l_googplay', 'l_fakku', 'l_freegame', 'l_playstation_jp', 'l_playstation_na',
    'l_playstation_eu', 'l_playstation_hk', 'l_nintendo', 'l_gyutto', 'l_dmm', 'l_booth', 'l_patreonp',
    'l_patreon', 'l_substar'
]


def clean_data(data):
    """清理数据中的字段，如果字段值仅为\\N，则删除该字段"""

    def clean_entry(entry):
        keys_to_remove = [key for key, value in entry.items() if value == '\\N']
        for key in keys_to_remove:
            del entry[key]

    for entry in data:
        clean_entry(entry)
        if 'titles' in entry:
            for title in entry['titles']:
                clean_entry(title)
        if 'releases' in entry:
            for release in entry['releases']:
                clean_entry(release)


def tsv_to_json(vn_tsv_file_path, vn_titles_tsv_file_path, releases_titles_tsv_file_path, releases_vn_tsv_file_path,
                releases_file_path, json_file_path, timestamp_file_path):
    # 使用defaultdict来组织数据
    vn_data = defaultdict(
        lambda: {"id": None, "titles": [], "image": None, "olang": None, "alias": [], "releases": []})

    # 读取vn表的TSV文件
    with open(vn_tsv_file_path, newline='', encoding='utf-8') as vn_tsv_file:
        reader = csv.DictReader(vn_tsv_file, delimiter='\t', fieldnames=vn_columns)

        for row in reader:
            entry_id = row['id']
            vn_data[entry_id]["id"] = entry_id
            vn_data[entry_id]["image"] = row["image"]
            vn_data[entry_id]["olang"] = row.get("olang", None)
            aliases = row["alias"].replace('\\n', '\n').splitlines()
            vn_data[entry_id]["alias"] = [alias.strip() for alias in aliases if alias.strip()]

    # 读取vn_titles表的TSV文件
    with open(vn_titles_tsv_file_path, newline='', encoding='utf-8') as vn_titles_tsv_file:
        reader = csv.DictReader(vn_titles_tsv_file, delimiter='\t', fieldnames=vn_titles_columns)

        for row in reader:
            entry_id = row['id']
            if entry_id in vn_data:  # 确保vn_data中存在这个id
                vn_data[entry_id]["titles"].append({
                    "lang": row["lang"],
                    "official": row["official"],
                    "title": row["title"],
                    "latin": row["latin"]
                })

    # 读取releases_vn表的TSV文件
    releases_mapping = defaultdict(list)
    with open(releases_vn_tsv_file_path, newline='', encoding='utf-8') as releases_vn_tsv_file:
        reader = csv.DictReader(releases_vn_tsv_file, delimiter='\t', fieldnames=releases_vn_columns)

        for row in reader:
            releases_mapping[row['id']].append({
                "vid": row["vid"],
                "rtype": row["rtype"]
            })

    # 读取releases_titles表并合并数据
    releases_data = {}
    with open(releases_titles_tsv_file_path, newline='', encoding='utf-8') as releases_titles_tsv_file:
        reader = csv.DictReader(releases_titles_tsv_file, delimiter='\t', fieldnames=releases_titles_columns)

        for row in reader:
            entry_id = row['id']
            if entry_id not in releases_data:
                releases_data[entry_id] = {
                    "id": row["id"],
                    "lang": row["lang"],
                    "mtl": row["mtl"],
                    "title": row["title"],
                    "latin": row["latin"],
                    "releases": []
                }
            releases_data[entry_id]["releases"].append(releases_mapping[entry_id])

    # 读取 releases 表并填充数据
    added_releases = set()  # 用于跟踪已添加的记录
    with open(releases_file_path, newline='', encoding='utf-8') as releases_file:
        reader = csv.DictReader(releases_file, delimiter='\t', fieldnames=releases_fields)

        for row in reader:
            entry_id = row['id']
            if entry_id in releases_data:
                for release in releases_data[entry_id]["releases"]:
                    for r in release:
                        if r["vid"] in vn_data:  # 确保 vn_data 中存在这个 vid
                            # 处理 released 字段
                            released_str = row["released"]
                            try:
                                # 将字符串转换为 datetime 对象
                                released_date = datetime.strptime(released_str, "%Y%m%d")
                                # 转换为 ISO 8601 字符串（标准日期格式）
                                released_iso = released_date.isoformat()
                            except ValueError:
                                # 如果解析失败，则使用默认值或跳过
                                released_iso = None

                            release_data = {
                                "rid": row["id"],
                                "released": released_iso,
                                "lang": releases_data[entry_id]["lang"],
                                "mtl": releases_data[entry_id]["mtl"],
                                "title": releases_data[entry_id]["title"],
                                "latin": releases_data[entry_id]["latin"],
                                "rtype": r["rtype"]
                            }
                            # 添加字段值时排除值为0的字段
                            if row.get("l_steam") != "0":
                                release_data["l_steam"] = row.get("l_steam")
                            if row.get("l_digiket") != "0":
                                release_data["l_digiket"] = row.get("l_digiket")
                            if row.get("l_egs") != "0":
                                release_data["l_egs"] = row.get("l_egs")
                            if row.get("l_dlsite") != "0":
                                release_data["l_dlsite"] = row.get("l_dlsite")

                            release_key = (release_data["rid"], release_data["lang"])  # 以 rid 和 lang 作为唯一标识
                            if release_key not in added_releases:
                                vn_data[r["vid"]]["releases"].append(release_data)
                                added_releases.add(release_key)

    # 清理数据中的字段
    transformed_data_list = list(vn_data.values())
    clean_data(transformed_data_list)

    # 删除没有 image 字段的条目
    transformed_data_list = [entry for entry in transformed_data_list if entry.get("image")]

    # 获取当前时间戳
    timestamp = datetime.now().isoformat()

    # 构建包含时间戳和数据的字典
    output_data = {
        "timestamp": timestamp,
        "data": transformed_data_list
    }

    # 将时间戳和数据分别写入 NDJSON 文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:

        # 写入数据列表中的每个项
        for item in output_data["data"]:
            json_file.write(json.dumps(item, ensure_ascii=False) + '\n')


# 使用示例
tsv_to_json('./vndb_data/db/vn', './vndb_data/db/vn_titles', './vndb_data/db/releases_titles',
            './vndb_data/db/releases_vn', './vndb_data/db/releases', 'vn_data.ndjson', 'timeVersion.ndjson')
