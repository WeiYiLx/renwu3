# Proposal

## Why

需要对两张实拍照片（两枚硬币、饼干盘）做霍夫圆检测，并快速调参确认外缘是否被正确标出。当前只能反复改脚本、看不到即时标注结果，既拖慢调参，也无法给组长留下可复核的验收证据。

## What Changes

- 新增参数化霍夫圆检测核心：读取 JPEG/PNG，按 dp、minDist、param1、param2、半径范围、中值滤波核参数检出圆，并按固定顺序返回圆心与半径。
- 新增本地图形界面：导入图片、滑杆调参、实时预览标注结果、导出 PNG 标注图。
- 新增可重复执行的验收脚本：用固定参数处理两张样图，断言检出数量与半径范围，并生成标注结果图。
- README 写明启动方式、两张图各自的验收参数、验收结果与标注图。

## Capabilities

### New Capabilities

- `circle-detection`: 参数化霍夫圆检测、结果标注与导出，以及两张实拍图的验收判据。
- `detection-gui`: 本地图形界面，支持图片导入、参数调节、标注预览与结果导出。

### Modified Capabilities

无。

## Impact

- 新增代码：`hough_circles/`（检测核心、HTTP 服务、前端页面）、`scripts/acceptance.py`。
- 依赖：Python 3、`opencv-python`、`numpy`；界面使用标准库 HTTP 服务，无额外框架依赖。
- 新增素材：`examples/coins.jpg`、`examples/cookie-plate.jpg`；产物位于 `docs/results/`。
- 不涉及既有系统改造。
