# 项目约定

这是本地霍夫圆检测工具：Python + OpenCV 负责检测，标准库 HTTP 服务提供图形界面。一次变更只解决一个目标，保持 `python3 -m hough_circles` 与 `python3 scripts/acceptance.py` 可用。

开工前阅读 `openspec/changes/` 中的对应变更，确认规格与验收场景；会改变外部行为的歧义先向需求方确认。完成后运行验收脚本并记录实际结果。

验收判据：

- `examples/coins.jpg`：检出 2 个圆，半径落在 170–190 px，对应两枚硬币外缘。
- `examples/cookie-plate.jpg`：检出 1 个圆，半径落在 235–255 px，对应盘沿。

不要修改样图或验收参数来让检查通过。调整验收参数时同步更新 README、`design.md` 与 `scripts/acceptance.py`。
