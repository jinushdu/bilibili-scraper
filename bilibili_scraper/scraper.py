"""B站热门视频爬虫 — 调用B站公开API，无需登录"""

import requests
from typing import Optional

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.bilibili.com/",
}

# 综合热门
POPULAR_URL = "https://api.bilibili.com/x/web-interface/popular"
# 全站排行榜
RANKING_URL = "https://api.bilibili.com/x/web-interface/ranking/v2"
# 视频详情
VIDEO_INFO_URL = "https://api.bilibili.com/x/web-interface/view"
# 分区列表
REGIONS_URL = "https://api.bilibili.com/x/web-interface/ranking/region"


def fetch_json(url: str, params: dict) -> dict:
    """通用请求封装"""
    resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data["code"] != 0:
        return {"error": data.get("message", "未知错误")}
    return data["data"]


def get_popular(pn: int = 1, ps: int = 50) -> list[dict]:
    """获取综合热门视频"""
    data = fetch_json(POPULAR_URL, {"pn": pn, "ps": ps})
    if isinstance(data, dict) and "error" in data:
        return [data]
    return [_parse_video(item) for item in data.get("list", [])]


def get_ranking(rid: int = 0, pn: int = 1, ps: int = 50) -> list[dict]:
    """
    获取排行榜视频

    rid 分区编码（常用）：
         0 - 全站     1 - 动画     3 - 音乐
         4 - 游戏     5 - 娱乐    36 - 知识
       119 - 鬼畜   129 - 舞蹈   160 - 生活
       188 - 科技   211 - 美食   217 - 动物圈
    """
    params = {"rid": rid, "type": "all", "pn": pn, "ps": ps}
    data = fetch_json(RANKING_URL, params)
    if isinstance(data, dict) and "error" in data:
        return [data]
    return [_parse_video(item) for item in data.get("list", [])]


def get_popular_all_pages(max_pages: int = 3, ps: int = 50) -> list[dict]:
    """爬取多页综合热门"""
    results = []
    for pn in range(1, max_pages + 1):
        print(f"  热门第 {pn}/{max_pages} 页...")
        videos = get_popular(pn=pn, ps=ps)
        if not videos or "error" in videos[0]:
            break
        results.extend(videos)
    return results


def get_ranking_all_pages(rid: int = 0, max_pages: int = 3, ps: int = 50) -> list[dict]:
    """爬取多页排行榜"""
    results = []
    for pn in range(1, max_pages + 1):
        print(f"  排行榜第 {pn}/{max_pages} 页...")
        videos = get_ranking(rid=rid, pn=pn, ps=ps)
        if not videos or "error" in videos[0]:
            break
        results.extend(videos)
    return results


def _parse_video(v: dict) -> dict:
    """解析视频字段，统一输出格式"""
    stat = v.get("stat", {})
    return {
        "标题": v.get("title", ""),
        "BV号": v.get("bvid", ""),
        "播放量": stat.get("view", 0),
        "弹幕数": stat.get("danmaku", 0),
        "评论数": stat.get("reply", 0),
        "收藏数": stat.get("favorite", 0),
        "点赞数": stat.get("like", 0),
        "硬币数": stat.get("coin", 0),
        "分享数": stat.get("share", 0),
        "UP主": v.get("owner", {}).get("name", ""),
        "视频链接": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
        "封面": v.get("pic", ""),
        "时长": _fmt_duration(v.get("duration", 0)),
        "简介": (v.get("desc", "") or "")[:100],
    }


def _fmt_duration(seconds: int) -> str:
    """秒数转 mm:ss 或 hh:mm:ss"""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"
