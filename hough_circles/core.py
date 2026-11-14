"""霍夫圆检测核心：参数校验、检测、标注与图片编解码。

界面与服务端都调用这里的函数，保证预览和导出结果一致。
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

__all__ = [
    "Circle",
    "HoughParams",
    "annotate",
    "decode_image",
    "detect",
    "encode_png",
    "to_gray",
]

GREEN = (0, 255, 0)
RED = (0, 0, 255)


@dataclass(frozen=True, slots=True)
class Circle:
    """一个检测结果，坐标与半径单位为像素。"""

    x: float
    y: float
    r: float

    def as_dict(self) -> dict[str, float]:
        return {
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "r": round(self.r, 1),
        }


@dataclass(frozen=True, slots=True)
class HoughParams:
    """霍夫圆检测参数，字段含义与 OpenCV HoughCircles 对应。"""

    dp: float = 1.2
    min_dist: float = 100.0
    param1: float = 100.0
    param2: float = 45.0
    min_radius: int = 20
    max_radius: int = 0
    blur: int = 5

    def validate(self) -> None:
        """校验参数，非法时抛出带参数名的 ValueError。"""
        if self.dp <= 0:
            raise ValueError("dp 必须大于 0")
        if self.min_dist <= 0:
            raise ValueError("minDist 必须大于 0")
        if self.param1 <= 0:
            raise ValueError("param1 必须大于 0")
        if self.param2 <= 0:
            raise ValueError("param2 必须大于 0")
        if self.min_radius < 0:
            raise ValueError("minRadius 不能为负数")
        if self.max_radius < 0:
            raise ValueError("maxRadius 不能为负数")
        if self.max_radius and self.max_radius < self.min_radius:
            raise ValueError("maxRadius 不能小于 minRadius")
        if self.blur < 1 or self.blur % 2 == 0:
            raise ValueError("blur 必须是正奇数")

    def resolved_max_radius(self, shape: tuple[int, ...]) -> int:
        """maxRadius 为 0 时按图像短边的一半取值。"""
        if self.max_radius:
            return self.max_radius
        return max(1, min(shape[0], shape[1]) // 2)


def to_gray(image: np.ndarray) -> np.ndarray:
    """把 BGR/BGRA/灰度图转换为灰度图。"""
    if image is None or image.size == 0:
        raise ValueError("图像为空")
    if image.ndim == 2:
        return image
    if image.ndim == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    raise ValueError("不支持的图像通道数")


def detect(image: np.ndarray, params: HoughParams) -> list[Circle]:
    """检测圆并按圆心坐标排序，未检出时返回空列表。"""
    params.validate()
    gray = to_gray(image)
    if params.blur > 1:
        gray = cv2.medianBlur(gray, params.blur)
    found = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=params.dp,
        minDist=params.min_dist,
        param1=params.param1,
        param2=params.param2,
        minRadius=params.min_radius,
        maxRadius=params.resolved_max_radius(gray.shape),
    )
    if found is None:
        return []
    circles = [Circle(float(x), float(y), float(r)) for x, y, r in found[0]]
    circles.sort(key=lambda circle: (round(circle.x), round(circle.y), round(circle.r)))
    return circles


def annotate(image: np.ndarray, circles: list[Circle]) -> np.ndarray:
    """在原图副本上绘制圆周与圆心。"""
    result = image.copy()
    if not circles:
        return result
    height, width = result.shape[:2]
    thickness = max(2, round(min(height, width) / 300))
    for circle in circles:
        center = (int(round(circle.x)), int(round(circle.y)))
        cv2.circle(result, center, int(round(circle.r)), GREEN, thickness, cv2.LINE_AA)
        cv2.circle(result, center, max(2, thickness * 2), RED, -1, cv2.LINE_AA)
    return result


def decode_image(data: bytes) -> np.ndarray:
    """把上传的字节解码为 BGR 图像。"""
    if not data:
        raise ValueError("图片内容为空")
    buffer = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("无法解码图片，请选择 JPEG 或 PNG 文件")
    return image


def encode_png(image: np.ndarray) -> bytes:
    """把图像编码为 PNG 字节。"""
    ok, buffer = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("PNG 编码失败")
    return buffer.tobytes()
