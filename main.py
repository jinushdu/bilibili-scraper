"""
B站热门视频爬虫

用法：
    python main.py                          # 默认：综合热门 + 全站排行榜各3页
    python main.py --mode popular           # 只看综合热门
    python main.py --mode ranking --rid 4   # 只看游戏区排行榜
    python main.py --mode both --pages 5    # 各爬5页

B站公开API，无需登录、无需cookie，即开即用。
"""

import argparse
from bilibili_scraper.scraper import get_popular_all_pages, get_ranking_all_pages
from bilibili_scraper.exporter import export_csv, export_json

RID_MAP = {
    "全站": 0,   "动画": 1,   "音乐": 3,   "游戏": 4,
    "娱乐": 5,   "知识": 36,  "鬼畜": 119, "舞蹈": 129,
    "生活": 160, "科技": 188, "美食": 211, "动物圈": 217,
}


def main():
    parser = argparse.ArgumentParser(
        description="B站热门视频爬虫 — 基于B站公开API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python main.py
  python main.py --mode popular --pages 5
  python main.py --mode ranking --rid 4
  python main.py --mode both --pages 3 --rid 188
区域编码：""" + ", ".join(f"{k}={v}" for k, v in RID_MAP.items()),
    )
    parser.add_argument("--mode", choices=["popular", "ranking", "both"], default="both",
                        help="爬取模式（默认 both）")
    parser.add_argument("--rid", type=int, default=0,
                        help="排行榜分区编码（默认 0=全站）")
    parser.add_argument("--pages", "-p", type=int, default=3,
                        help="每种模式爬取页数（默认 3）")
    parser.add_argument("--ps", type=int, default=50,
                        help="每页数量（默认 50）")
    parser.add_argument("--format", "-f", choices=["csv", "json", "both"], default="both",
                        help="导出格式（默认 both）")
    args = parser.parse_args()

    print("=" * 50)
    print("  B站热门视频爬虫")
    print("=" * 50)
    print(f"  模式：{args.mode}")
    print(f"  页数：{args.pages} 页 × {args.ps} 条/页")
    if args.mode != "popular":
        label = [k for k, v in RID_MAP.items() if v == args.rid]
        print(f"  分区：{'全站' if args.rid == 0 else label[0] if label else args.rid}")
    print("=" * 50)

    all_videos: list[dict] = []

    if args.mode in ("popular", "both"):
        print("\n[热门] 正在爬取综合热门...")
        popular = get_popular_all_pages(max_pages=args.pages, ps=args.ps)
        print(f"  获取 {len(popular)} 条")
        all_videos.extend(popular)

    if args.mode in ("ranking", "both"):
        print("\n[排行] 正在爬取排行榜...")
        ranking = get_ranking_all_pages(rid=args.rid, max_pages=args.pages, ps=args.ps)
        print(f"  获取 {len(ranking)} 条")
        all_videos.extend(ranking)

    if not all_videos:
        print("\n未获取到数据，请检查网络连接。")
        return

    # 按播放量去重排序
    seen = set()
    unique = []
    for v in all_videos:
        if v["BV号"] not in seen:
            seen.add(v["BV号"])
            unique.append(v)
    unique.sort(key=lambda x: x["播放量"], reverse=True)

    print(f"\n去重后共 {len(unique)} 条视频")

    # 导出
    print()
    if args.format in ("csv", "both"):
        export_csv(unique)
    if args.format in ("json", "both"):
        export_json(unique)

    # 预览 Top 5
    print("\n" + "=" * 50)
    print("  Top 5")
    print("=" * 50)
    for i, v in enumerate(unique[:5], 1):
        wan = v["播放量"] / 10000
        print(f"\n  {i}. {v['标题'][:40]}")
        print(f"     UP主: {v['UP主']} | 播放: {wan:.1f}万 | 弹幕: {v['弹幕数']}")
        print(f"     {v['视频链接']}")


if __name__ == "__main__":
    main()
