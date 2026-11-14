"""本地 HTTP 服务：提供图形界面、检测与导出接口。"""

from __future__ import annotations

import argparse
import base64
import json
import threading
import uuid
from collections import OrderedDict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

import numpy as np

from .core import HoughParams, annotate, decode_image, detect, encode_png

STATIC_DIR = Path(__file__).resolve().parent / "static"
INDEX_FILE = STATIC_DIR / "index.html"
MAX_REQUEST_BYTES = 32 * 1024 * 1024
MAX_IMAGES = 8
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png"}


class ImageStore:
    """保存上传的图片，最多保留若干张，按最近使用淘汰。"""

    def __init__(self, capacity: int = MAX_IMAGES) -> None:
        self._capacity = capacity
        self._items: OrderedDict[str, tuple[np.ndarray, str]] = OrderedDict()
        self._lock = threading.Lock()

    def add(self, image: np.ndarray, filename: str) -> str:
        key = uuid.uuid4().hex
        with self._lock:
            self._items[key] = (image, filename)
            while len(self._items) > self._capacity:
                self._items.popitem(last=False)
        return key

    def get(self, key: str) -> tuple[np.ndarray, str]:
        with self._lock:
            item = self._items.get(key)
            if item is None:
                raise KeyError(key)
            self._items.move_to_end(key)
            return item


def parse_params(raw: object) -> HoughParams:
    """把请求中的参数对象转换为 HoughParams 并校验。"""
    if not isinstance(raw, dict):
        raise ValueError("params 必须是对象")
    defaults = HoughParams()

    def number(key: str, default: float) -> float:
        value = raw.get(key, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{key} 必须是数字")
        return float(value)

    def integer(key: str, default: int) -> int:
        value = number(key, default)
        if value != int(value):
            raise ValueError(f"{key} 必须是整数")
        return int(value)

    params = HoughParams(
        dp=number("dp", defaults.dp),
        min_dist=number("minDist", defaults.min_dist),
        param1=number("param1", defaults.param1),
        param2=number("param2", defaults.param2),
        min_radius=integer("minRadius", defaults.min_radius),
        max_radius=integer("maxRadius", defaults.max_radius),
        blur=integer("blur", defaults.blur),
    )
    params.validate()
    return params


class Handler(BaseHTTPRequestHandler):
    server_version = "HoughCircleGUI/1.0"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler 接口
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            try:
                body = INDEX_FILE.read_bytes()
            except OSError:
                self._send_json({"error": "界面文件缺失"}, HTTPStatus.INTERNAL_SERVER_ERROR)
                return
            self._send_bytes(body, "text/html; charset=utf-8")
        else:
            self._send_json({"error": "未找到该地址"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler 接口
        path = urlparse(self.path).path
        try:
            if path == "/api/upload":
                self._handle_upload()
            elif path == "/api/detect":
                self._handle_detect()
            elif path == "/api/export":
                self._handle_export()
            else:
                self._send_json({"error": "未找到该地址"}, HTTPStatus.NOT_FOUND)
        except ValueError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except KeyError:
            self._send_json({"error": "图片已过期，请重新导入"}, HTTPStatus.NOT_FOUND)

    def _handle_upload(self) -> None:
        data = self._read_body()
        filename = unquote(self.headers.get("X-Filename", "")) or "image"
        if Path(filename).suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError("仅支持 JPEG 或 PNG 图片")
        image = decode_image(data)
        image_id = self.server.store.add(image, filename)
        height, width = image.shape[:2]
        self._send_json(
            {
                "id": image_id,
                "filename": filename,
                "width": width,
                "height": height,
            }
        )

    def _handle_detect(self) -> None:
        payload = self._read_json()
        image, _ = self._resolve_image(payload)
        params = parse_params(payload.get("params"))
        circles = detect(image, params)
        preview = base64.b64encode(encode_png(annotate(image, circles))).decode("ascii")
        self._send_json(
            {
                "count": len(circles),
                "circles": [circle.as_dict() for circle in circles],
                "preview": "data:image/png;base64," + preview,
            }
        )

    def _handle_export(self) -> None:
        payload = self._read_json()
        image, filename = self._resolve_image(payload)
        params = parse_params(payload.get("params"))
        circles = detect(image, params)
        if not circles:
            raise ValueError("当前没有可导出的圆，请先调整参数")
        png = encode_png(annotate(image, circles))
        name = Path(filename).stem + "-annotated.png"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(png)))
        self.send_header(
            "Content-Disposition",
            f"attachment; filename=\"annotated.png\"; filename*=UTF-8''{quote(name)}",
        )
        self.end_headers()
        self.wfile.write(png)

    def _resolve_image(self, payload: dict) -> tuple[np.ndarray, str]:
        image_id = payload.get("id")
        if not isinstance(image_id, str) or not image_id:
            raise ValueError("缺少图片 ID")
        return self.server.store.get(image_id)

    def _read_json(self) -> dict:
        data = self._read_body()
        try:
            payload = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("请求体不是合法的 JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("请求体必须是 JSON 对象")
        return payload

    def _read_body(self) -> bytes:
        raw_length = self.headers.get("Content-Length")
        if not raw_length:
            raise ValueError("缺少请求内容")
        try:
            length = int(raw_length)
        except ValueError as exc:
            raise ValueError("Content-Length 无效") from exc
        if length <= 0 or length > MAX_REQUEST_BYTES:
            raise ValueError("请求内容大小超出限制")
        return self.rfile.read(length)

    def _send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send_bytes(body, "application/json; charset=utf-8", status)

    def _send_bytes(
        self,
        body: bytes,
        content_type: str,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")


class HoughServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        store: ImageStore | None = None,
    ) -> None:
        super().__init__(address, Handler)
        self.store = store or ImageStore()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="本地霍夫圆检测图形界面")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址，默认 127.0.0.1")
    parser.add_argument("--port", type=int, default=8000, help="监听端口，默认 8000")
    args = parser.parse_args(argv)

    server = HoughServer((args.host, args.port))
    print(f"霍夫圆检测工具已启动：http://{args.host}:{args.port}/")
    print("按 Ctrl+C 停止。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        server.server_close()
    return 0
