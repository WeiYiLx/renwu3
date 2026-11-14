#!/usr/bin/env python3
"""按 README 记录的参数验收两张实拍样图，输出指标并生成标注图。"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hough_circles.core import (  # noqa: E402
    HoughParams,
    annotate,
    decode_image,
    detect,
    encode_png,
)


@dataclass(frozen=True)
class Case:
    name: str
    image: str
    params: HoughParams
    expected_count: int
    radius_range: tuple[int, int]
    note: str


CASES = (
    Case(
        name="coins",
        image="examples/coins.jpg",
        params=HoughParams(
            dp=1.2,
            min_dist=200,
            param1=100,
            param2=50,
            min_radius=150,
            max_radius=210,
            blur=5,
        ),
        expected_count=2,
        radius_range=(170, 190),
        note="两枚硬币的外缘",
    ),
    Case(
        name="cookie-plate",
        image="examples/cookie-plate.jpg",
        params=HoughParams(
            dp=1.2,
            min_dist=200,
            param1=100,
            param2=40,
            min_radius=200,
            max_radius=280,
            blur=5,
        ),
        expected_count=1,
        radius_range=(235, 255),
        note="饼干盘沿",
    ),
)


def edge_support(gray: np.ndarray, x: float, y: float, r: float) -> float:
    """圆周上落在强梯度位置的比例，用于复核圆是否贴合真实边缘。"""
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(gx, gy)
    angles = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    px = np.rint(x + r * np.cos(angles)).astype(int)
    py = np.rint(y + r * np.sin(angles)).astype(int)
    inside = (px >= 0) & (px < gray.shape[1]) & (py >= 0) & (py < gray.shape[0])
    if not inside.any():
        return 0.0
    sampled = magnitude[py[inside], px[inside]]
    return float((sampled > np.percentile(magnitude, 90)).mean())


def main() -> int:
    output_dir = ROOT / "docs" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []

    for case in CASES:
        image_path = ROOT / case.image
        image = decode_image(image_path.read_bytes())
        circles = detect(image, case.params)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        print(f"[{case.name}] {case.image}")
        print(
            f"  期望：{case.expected_count} 个圆（{case.note}），"
            f"半径 {case.radius_range[0]}–{case.radius_range[1]} px"
        )
        print(f"  实测：{len(circles)} 个圆")
        for index, circle in enumerate(circles, start=1):
            support = edge_support(gray, circle.x, circle.y, circle.r)
            print(
                f"    #{index} 圆心=({circle.x:.1f}, {circle.y:.1f}) "
                f"半径={circle.r:.1f} px 边缘支持度={support:.2f}"
            )

        problem = None
        if len(circles) != case.expected_count:
            problem = f"检出数量 {len(circles)}，期望 {case.expected_count}"
        else:
            low, high = case.radius_range
            outside = [circle for circle in circles if not low <= circle.r <= high]
            if outside:
                problem = "半径超出验收区间：" + ", ".join(f"{circle.r:.1f}" for circle in outside)

        if problem:
            failures.append(f"{case.name}: {problem}")
            print(f"  结果：失败（{problem}）")
        else:
            print("  结果：通过")

        annotated = annotate(image, circles)
        target = output_dir / f"{image_path.stem}-annotated.png"
        target.write_bytes(encode_png(annotated))
        print(f"  标注图：{target.relative_to(ROOT)}")
        print()

    if failures:
        print("验收失败：")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"验收通过：{len(CASES)} 张样图符合判据。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
