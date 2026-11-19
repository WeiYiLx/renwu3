# 视频导入检测交接记录

记录日期：2026-11-20

## 分支与合并

| 项目 | 值 |
| --- | --- |
| 仓库 | `git@github.com:WeiYiLx/renwu3.git` |
| 工作分支 | `feat/issue-1-video-import-detection` |
| 起始版本 | `origin/main` @ `108bd3f`（2026-11-14 归档完成） |
| 远端分支 | `origin/feat/issue-1-video-import-detection` |
| 合并目标 | `WeiYiLx/renwu3` 的 `main` |
| PR 方式 | 同仓库 PR：工作分支 → `main`；保持打开待评审，验收后合并或关闭，不删除工作分支。PR 尚未创建，见下方创建链接 |
| 规划 Issue | `#1`（编号用于分支命名；本机没有已登录的 GitHub API/浏览器会话，交接时未自动创建，见下方创建链接） |

分支直达链接：

<https://github.com/WeiYiLx/renwu3/tree/feat/issue-1-video-import-detection>

PR 创建链接：

<https://github.com/WeiYiLx/renwu3/compare/main...feat/issue-1-video-import-detection?expand=1>

Issue 创建链接（标题已预填，正文可用下方“后续入口”一节）：

<https://github.com/WeiYiLx/renwu3/issues/new?title=%E6%94%AF%E6%8C%81%E5%AF%BC%E5%85%A5%E8%A7%86%E9%A2%91%E5%B9%B6%E5%AE%8C%E6%88%90%E9%80%90%E5%B8%A7%E5%9C%86%E6%A3%80%E6%B5%8B>

> 仓库当前只有 `origin`，没有上游仓库；不要把 PR 指向不存在的 `Ecrypted-Data/renwu3`。如果后续提供团队上游仓库，再把 `main` 换成上游 `main`，分支内容不变。

## 当前状态

**已完成并验证（图片功能）**

- 图片导入、7 个参数滑杆、250 ms 防抖、标注预览、圆心/半径列表、PNG 导出。
- 两张实拍样图的固定参数验收：`python3 scripts/acceptance.py` 退出码 0。
- 实测输出：
  - `coins.jpg`：2 个圆，`(192.6, 192.6) r=180.0`、`(567.0, 191.4) r=179.3`，边缘支持度 0.56/0.63。
  - `cookie-plate.jpg`：1 个圆，`(263.4, 258.6) r=245.2`，边缘支持度 0.84。
- `openspec validate --specs --strict`：`circle-detection`、`detection-gui` 共 2 项通过。
- 两轮图片变更均已归档，见 `openspec/changes/archive/`。

**未实现（视频功能）**

- 视频上传与元数据读取、逐帧霍夫圆检测、任务进度/取消、逐帧 CSV、视频模式界面。
- OpenSpec 变更 `openspec/changes/add-video-import-detection/` 已写好提案、规格、设计与任务清单；当前 4/29 完成，4 项均为交接准备，不是功能实现。
- 仓库没有视频样例，也没有视频验收判据。

**未验证事项**

- 视频样例的来源、许可与固定参数；视频验收的采样帧数、CSV 行数和半径区间尚未确定。
- OpenCV 5.0 自带的 FFmpeg 后端对目标 MP4/AVI/MOV 编码的实际支持；需要用样例实测。
- 512 MiB 上传上限、流式写入临时文件和 LRU 淘汰在真实大文件下的行为。
- 浏览器中的视频模式手工流程（进度轮询、取消、帧预览、CSV 下载）。
- 本次交接没有重新做图片界面的浏览器手工验收；图片验收证据来自脚本与已有归档记录。
- `#1` Issue 尚未在 GitHub 上创建；创建后把链接补到 PR 描述即可，分支名不用改。

## 复现当前验收

在仓库根目录：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/acceptance.py
```

期望：退出码 0，终端输出两张样图的期望/实测数量、圆心、半径和边缘支持度，并生成 `docs/results/coins-annotated.png` 与 `docs/results/cookie-plate-annotated.png`。

校验 OpenSpec：

```bash
openspec validate --specs --strict
openspec status --change add-video-import-detection
```

期望：主规格 2 项通过；视频变更状态为进行中，任务进度 4/29。

## 后续入口

1. 先读 `openspec/changes/add-video-import-detection/proposal.md` 和 `design.md`，确认视频范围与非目标。
2. 从 `tasks.md` 第 1 节开始：先补视频样例与验收判据，再实现核心、接口、前端。
3. 用 OpenSpec 的 apply 流程获取任务上下文：

   ```bash
   openspec instructions apply --change add-video-import-detection --json
   ```

4. 每完成一项就把 `tasks.md` 中对应复选框改为 `[x]`，并记录实际命令与输出。
5. 合并前必须确认 `python3 scripts/acceptance.py` 仍以退出码 0 通过，图片功能没有回退。

## PR 描述模板

标题：`feat: prepare video import detection handoff`

正文：

```markdown
## 变更

- 从 `main` @ `108bd3f` 建立视频导入检测交接分支。
- 新增未实施的 OpenSpec 变更 `add-video-import-detection`：提案、规格、设计与 29 项任务。
- README 补齐依赖、启动、样例获取、验收结果和交接状态。
- 新增 `docs/handoff.md`，记录分支、基线、合并目标、PR 方式、未验证事项和后续入口。

## 验证

- `python3 scripts/acceptance.py`：退出码 0，两张样图通过。
- `openspec validate --specs --strict`：2/2 通过。
- 视频功能未实现，视频验收未执行。

## 合并

目标分支 `main`；保持 PR 打开待评审，验收后合并或关闭，不删除工作分支。
```
