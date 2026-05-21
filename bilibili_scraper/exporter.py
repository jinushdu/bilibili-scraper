"""数据导出：CSV / JSON"""

import csv
import json
import os
from datetime import datetime


def export_csv(data: list[dict], prefix: str = "bilibili") -> str:
    """导出为 CSV"""
    if not data:
        print("无数据可导出")
        return ""
    os.makedirs("output", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join("output", f"{prefix}_{ts}.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)
    print(f"  CSV → {path}")
    return path


def export_json(data: list[dict], prefix: str = "bilibili") -> str:
    """导出为 JSON"""
    if not data:
        print("无数据可导出")
        return ""
    os.makedirs("output", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join("output", f"{prefix}_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  JSON → {path}")
    return path
