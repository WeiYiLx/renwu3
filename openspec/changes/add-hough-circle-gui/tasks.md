# Tasks

## 1. 工程骨架与检测核心

- [x] 1.1 建立 `hough_circles` 包、`requirements.txt` 与 `.gitignore`，验证 `python3 -c "import hough_circles"` 成功
- [x] 1.2 实现检测参数对象与校验（dp、minDist、param1、param2、minRadius、maxRadius、blur），验证非法参数抛出的 `ValueError` 消息包含具体参数名
- [x] 1.3 实现 `detect()`：灰度化、中值滤波、霍夫圆检测、按圆心排序，验证用验收参数检测两张样图得到的数量与半径与 design.md 参数表一致

## 2. 标注与验收脚本

- [x] 2.1 实现 `annotate()` 与 PNG 编解码，验证标注图与原图尺寸相同且圆周像素存在
- [x] 2.2 编写 `scripts/acceptance.py`：固定参数、断言数量与半径区间、输出指标并写入 `docs/results/*-annotated.png`，验证命令退出码为 0 且两张图存在

## 3. 图形界面

- [x] 3.1 实现 HTTP 服务与接口（页面、上传、检测、导出），验证用 `curl` 上传样图后检测返回 2 个圆、导出的 PNG 与原图尺寸一致
- [x] 3.2 实现前端页面（文件选择、参数滑杆、防抖预览、数量与圆列表、导出、错误提示），验证在浏览器中导入 `coins.jpg`、拖动参数后预览更新并能下载标注图

## 4. 文档与交付

- [x] 4.1 编写 README（启动方式、界面用法、两张图的验收参数与结果图）与 AGENTS.md，验证按 README 命令可启动并访问页面
- [x] 4.2 将验收脚本输出写入 README，验证 README 中的数量与半径与脚本输出一致
- [ ] 4.3 提交并推送 `main`，验证 `git ls-remote origin` 返回 `main` 的提交且仓库链接可访问

## Workflow follow-up

- 保留 `openspec/changes/add-hough-circle-gui/` 变更记录，供组长查看规格、任务进度与验收结果。
