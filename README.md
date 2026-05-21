# B站热门视频爬虫

基于 B站公开 API 的热门视频爬取工具，**无需登录、无需 Cookie**，开箱即用。

## 功能

- 爬取 B站**综合热门**视频
- 爬取 B站**排行榜**（支持按分区筛选）
- 自动翻页，支持自定义页数和每页数量
- 数据去重，按播放量排序
- 导出为 **CSV** 和 **JSON** 格式

## 项目结构

```
├── main.py                  # 主入口
├── bilibili_scraper/        # 核心模块
│   ├── __init__.py
│   ├── scraper.py           # 爬虫逻辑（调用B站公开API）
│   └── exporter.py          # CSV / JSON 导出
├── requirements.txt
├── .gitignore
└── README.md
```

## 快速开始

```bash
pip install -r requirements.txt
python main.py
```

## 用法示例

```bash
# 默认：综合热门 + 全站排行榜，各爬3页
python main.py

# 只看综合热门，爬5页
python main.py --mode popular --pages 5

# 只看游戏区排行榜
python main.py --mode ranking --rid 4

# 科技区排行榜，导出为 CSV
python main.py --mode ranking --rid 188 --format csv

# 全功能：both 模式，5页，知识区
python main.py --mode both --pages 5 --rid 36
```

## 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--mode` | — | 爬取模式：popular / ranking / both | both |
| `--rid` | — | 排行榜分区编码 | 0（全站） |
| `--pages` | `-p` | 爬取页数 | 3 |
| `--ps` | — | 每页视频数 | 50 |
| `--format` | `-f` | 导出格式：csv / json / both | both |

## 分区编码速查

| 分区 | 编码 | 分区 | 编码 |
|------|------|------|------|
| 全站 | 0 | 鬼畜 | 119 |
| 动画 | 1 | 舞蹈 | 129 |
| 音乐 | 3 | 生活 | 160 |
| 游戏 | 4 | 科技 | 188 |
| 娱乐 | 5 | 美食 | 211 |
| 知识 | 36 | 动物圈 | 217 |

## 输出字段

每条视频包含：标题、BV号、播放量、弹幕数、评论数、收藏数、点赞数、硬币数、分享数、UP主、视频链接、封面图、时长、简介

数据导出到 `output/` 目录。
