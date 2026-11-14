# Proposal

## Why

需要把霍夫圆检测从零散脚本变成可调参、可视化的本地工具，并用两张实拍图形成可复现的验收证据：硬币图标出两枚硬币外缘，饼干盘图标出盘沿。仓库中已有一版实现与归档记录，本次按重新评审的流程固化范围；apply 阶段以复核现有实现、补齐缺口为主，不重复返工已验收的检测逻辑。

## What Changes

- 检测核心：解码 JPEG/PNG，灰度化与中值滤波后调用霍夫圆检测，返回按圆心坐标排序的圆列表，并对参数组合做显式校验。
- 标注与导出：在原图分辨率上绘制绿色圆周与红色圆心，编码为 PNG，供预览和下载复用同一套渲染逻辑。
- 本地图形界面：图片导入、dp/minDist/param1/param2/半径范围/滤波核滑杆、防抖自动重检、标注预览、圆列表、导出按钮与错误提示。
- 验收脚本：用固定参数处理 `examples/coins.jpg` 与 `examples/cookie-plate.jpg`，断言检出数量与半径区间，输出圆心、半径、边缘支持度，并生成 `docs/results/` 下的标注图。
- README：写明环境与启动方式、两张图各自的验收参数、验收结果，并放置两张标注结果图。
- 不修改样图或验收判据来迁就实现；参数或判据若调整，README、设计文档与验收脚本同步更新。

## Capabilities

### New Capabilities

无。`circle-detection` 与 `detection-gui` 已在主规格中存在，本次按需求重新确认并细化。

### Modified Capabilities

- `circle-detection`: 明确参数化检测接口、标注图导出，以及两张实拍图的固定参数与验收判据。
- `detection-gui`: 明确图片导入、参数调节与实时预览、标注图导出的界面行为与错误处理。

## Impact

- 代码：`hough_circles/`（检测核心、HTTP 服务、前端页面）、`scripts/acceptance.py`。
- 依赖：Python 3.10+、`opencv-python`、`numpy`；HTTP 服务使用标准库，界面无额外前端框架。
- 素材与产物：`examples/` 两张样图；`docs/results/` 两张标注图。
- 仓库已有上一轮实现与归档变更 `2026-11-14-add-hough-circle-gui`；本变更不删除既有成果，apply 阶段先核对差异再决定补齐范围。
