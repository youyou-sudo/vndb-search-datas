# vndb-search-datas

此存储库用于处理 Vndb 条目 & 发布的 `title`、`alias`、`steam_id` 等字段数据为一个大型 NDJSON 文件；
此文件可以倒入 Mongondb 等 NoSQL 数据库进行定位索引或分析。也可以导入 Meilisearch 搭配 rome 匹配搜索（搜索结果可信度非常高）。

## Todo

- [x] Meilisearch 搜索的 `JSON` 数据
- [ ] Bgm & ymgal 项目 ID 关联表
- [ ] 基于此数据库的面向 CN 用户的模糊搜索 page & api
- [ ] 基于此项目数据的视觉小说游戏文件命名工具（根据 vnid 关联，文档尽请期待）

## 鸣谢

- [vndb.org](https://vndb.org/) 提供的 API 及数据。
