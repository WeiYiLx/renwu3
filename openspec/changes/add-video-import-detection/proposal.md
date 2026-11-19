# Proposal

## Why

现有工具只能逐张导入 JPEG/PNG 图片做霍夫圆检测，无法直接处理实拍视频。下一阶段需要把视频导入、逐帧检测、进度反馈和结果导出串成一条可复现的流程，让接手人不依赖口头说明就能继续实现。

本次交接只固化需求、设计取舍和验收入口，不实现视频功能；图片检测的现有能力与验收结果保持不变。

## What Changes

- 新增视频导入：支持 MP4、AVI、MOV 文件，校验可解码性，读取帧数、FPS、分辨率等元数据。
- 逐帧检测：复用现有 `HoughParams` 与 `detect()`，按帧间隔对采样帧执行霍夫圆检测，记录帧号、时间戳、检出数量与圆心/半径。
- 任务与进度：服务端以任务 ID 管理一次视频处理，提供进度查询、完成状态与取消操作；处理结果在任务生命周期内可查询和导出。
- 结果导出：导出逐帧结果 CSV，至少包含 `frame`、`time_ms`、`circle_index`、`x`、`y`、`r`；无检出的帧保留一行 `count=0` 的记录。
- 界面：在现有图片界面增加视频模式，可选择视频、设置帧间隔、查看进度、预览指定采样帧的标注图并下载 CSV。
- 验收：增加一段可公开获取的短视频样例和固定参数，验证采样帧数量、CSV 行数、至少一帧检出圆，以及取消和损坏文件的行为。
- 不在本次范围：实时摄像头、跨帧目标跟踪、多人并发任务持久化、自动调参。

## Capabilities

### New Capabilities

- `video-detection`: 规定视频导入、逐帧霍夫圆检测、任务进度、取消和逐帧结果导出的外部行为。

### Modified Capabilities

- `detection-gui`: 在现有图片界面中增加视频模式，规定视频选择、参数、进度、预览与导出的界面行为。

## Impact

- 代码：`hough_circles/core.py`（视频解码与逐帧检测）、`hough_circles/server.py`（上传、任务、进度、导出接口）、`hough_circles/static/index.html`（视频模式界面）、`scripts/acceptance.py`（视频验收用例）。
- 依赖：继续使用 Python 3.10+、`opencv-python`、`numpy` 和标准库，不新增 Python 依赖；视频编解码依赖 OpenCV 自带的 FFmpeg 后端。
- 素材与产物：`examples/` 新增短视频样例及来源说明；验收产物写入 `docs/results/`。
- 兼容性：现有 `/api/upload`、`/api/detect`、`/api/export` 与图片验收判据保持不变；视频接口为新增路径。
- 交接状态：本变更当前只有规划与交接记录，任务清单中的实现项均未开始；详见 `docs/handoff.md`。
