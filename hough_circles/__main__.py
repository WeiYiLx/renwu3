"""允许通过 `python3 -m hough_circles` 启动本地界面。"""

from .server import main

if __name__ == "__main__":
    raise SystemExit(main())
