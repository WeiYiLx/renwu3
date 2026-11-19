# Tasks

> 当前进度：4/29 完成。仅完成交接基线、文档和规划；视频功能尚未实现，样例与视频验收均未验证。接手人从第 1 节开始。

## 0. 交接基线与记录

- [x] 0.1 从 `origin/main` @ `108bd3f` 切出 `feat/issue-1-video-import-detection`，确认工作区干净
- [x] 0.2 在副本中运行 `python3 scripts/acceptance.py`，确认退出码 0：硬币 2 个圆（r=180.0/179.3），饼干盘 1 个圆（r=245.2）
- [x] 0.3 运行 `openspec validate --specs --strict`，确认 `circle-detection` 与 `detection-gui` 均通过
- [x] 0.4 在 `docs/handoff.md` 记录分支、基线、合并目标、PR 方式、已完成与未验证事项

## 1. 视频样例与验收判据

- [ ] 1.1 选取一段不超过 10 秒、不超过 5 MiB、许可允许再分发的 MP4 样例；或在 `examples/SOURCES.md` 记录来源与许可
- [ ] 1.2 若没有合适公开素材，新增 `scripts/make_sample_video.py`，用 `coins.jpg` 与 `cookie-plate.jpg` 生成确定性 MP4，并在 README 写明生成命令
- [ ] 1.3 固定样例的 `HoughParams` 与 `frameStep`，在 README 与 `design.md` 中记录参数、期望采样帧数、CSV 行数和半径区间
- [ ] 1.4 在 `scripts/acceptance.py` 增加视频用例：样例缺失时非零退出并提示获取方式；样例存在时校验采样帧数、CSV 行数、至少一帧检出
- [ ] 1.5 增加取消用例与损坏视频用例，确认两者都不会产生 `completed` 任务

## 2. 核心与任务

- [ ] 2.1 在 `hough_circles/core.py` 增加视频元数据读取与逐帧检测函数，复用 `HoughParams.validate()`、`detect()`、`annotate()` 与 `encode_png()`
- [ ] 2.2 实现 `VideoJob` 与任务表：状态字段、进度计数、逐帧结果、取消事件、LRU 淘汰和临时文件清理
- [ ] 2.3 实现后台处理循环：按 `frameStep` 采样、写入帧号/时间戳/圆列表、每帧检查取消事件、异常转为 `failed`
- [ ] 2.4 实现 CSV 生成：固定列、`count=0` 帧保留一行、只在 `completed` 状态可导出

## 3. HTTP 接口

- [ ] 3.1 新增 `POST /api/video/upload`：按块写入临时文件、限制 512 MiB、校验容器与首帧、返回元数据
- [ ] 3.2 新增 `POST /api/video/start`：校验 `frameStep` 与参数，创建任务并返回任务 ID
- [ ] 3.3 新增 `GET /api/video/status`、`POST /api/video/cancel`、`GET /api/video/results`，返回状态、进度、错误和逐帧摘要
- [ ] 3.4 新增 `GET /api/video/frame` 与 `GET /api/video/export`：单帧 PNG 预览、完成态 CSV 下载；错误映射为 4xx/409
- [ ] 3.5 确认现有 `/api/upload`、`/api/detect`、`/api/export` 的请求与响应未改变

## 4. 前端视频模式

- [ ] 4.1 增加图片/视频模式切换、视频文件选择、帧间隔输入和开始处理按钮，复用现有 7 个参数滑杆
- [ ] 4.2 处理中每 500 ms 轮询状态，显示已处理/总采样帧数、进度比例和取消按钮
- [ ] 4.3 完成后显示采样帧数、检出帧数、总圆数，启用 CSV 下载和采样帧下拉预览
- [ ] 4.4 处理失败、取消、未选择视频、模式切换时保持状态一致，不丢失运行中任务

## 5. 验收与文档

- [ ] 5.1 用样例视频跑完整流程，记录实际采样帧数、CSV 行数、检出帧数和每帧数量到 README
- [ ] 5.2 用损坏视频和非法 `frameStep` 验证错误信息，确认不创建成功任务
- [ ] 5.3 在浏览器中手工验证视频模式的上传、进度、取消、预览和 CSV 下载
- [ ] 5.4 更新 README 的依赖、启动、样例获取、视频验收结果和 OpenSpec 记录；更新 `examples/SOURCES.md` 的视频来源
- [ ] 5.5 运行 `python3 scripts/acceptance.py` 与 `openspec validate --specs --strict`，确认图片验收未回退

## 6. 归档与交付

- [ ] 6.1 把任务清单全部勾选，记录真实结果与未验证项，提交并推送到工作分支
- [ ] 6.2 归档 `add-video-import-detection` 并同步 `video-detection` 主规格；保留 `docs/handoff.md` 作为接手入口
