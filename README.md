# 霍夫圆检测工具

带本地图形界面的霍夫圆检测工具：导入实拍图片、调节参数、实时预览标注结果并导出 PNG 标注图。两张实拍样图（两枚硬币、饼干盘）已按固定参数验收通过。

## 环境与启动

需要 Python 3.10+ 与 OpenCV。Ubuntu / WSL2 下：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m hough_circles
```

浏览器访问 <http://127.0.0.1:8000/>。端口被占用时：

```bash
python3 -m hough_circles --port 8080
```

`--host` 可修改监听地址，默认只监听本机。

## 界面用法

| 操作 | 行为 |
| --- | --- |
| 导入图片 | 选择 JPEG/PNG，导入后立即用当前参数检测 |
| 调参 | 拖动滑杆，250 ms 防抖后自动重新检测 |
| 预览 | 显示原分辨率标注图、检出数量、每个圆的圆心与半径 |
| 导出 | 下载 `<原图名>-annotated.png`；无检出结果时按钮禁用 |

| 参数 | 含义 | 范围 | 默认值 |
| --- | --- | --- | --- |
| dp | 累加器分辨率与图像分辨率之比 | 1.0–2.0 | 1.2 |
| minDist | 两个圆心的最小距离（像素） | 10–500 | 100 |
| param1 | Canny 边缘检测高阈值 | 30–300 | 100 |
| param2 | 累加器阈值，越小越容易检出 | 10–150 | 45 |
| minRadius | 最小半径（像素） | 0–600 | 20 |
| maxRadius | 最大半径（像素），0 表示按图像短边一半自动取值 | 0–1200 | 0 |
| blur | 中值滤波核大小 | 1–15 的奇数 | 5 |

## 验收

样图在 `examples/`，验收生成的结果图在 `docs/results/`。复现命令：

```bash
python3 scripts/acceptance.py
```

### 硬币图

参数：`dp=1.2, minDist=200, param1=100, param2=50, minRadius=150, maxRadius=210, blur=5`

结果：检出 2 个圆，分别对应两枚硬币的外缘。

| 圆 | 圆心 | 半径 (px) | 边缘支持度 |
| --- | --- | --- | --- |
| 1 | (192.6, 192.6) | 180.0 | 0.56 |
| 2 | (567.0, 191.4) | 179.3 | 0.63 |

![硬币检测结果](docs/results/coins-annotated.png)

### 饼干盘图

参数：`dp=1.2, minDist=200, param1=100, param2=40, minRadius=200, maxRadius=280, blur=5`

结果：检出 1 个圆，对应盘沿。

| 圆 | 圆心 | 半径 (px) | 边缘支持度 |
| --- | --- | --- | --- |
| 1 | (263.4, 258.6) | 245.2 | 0.84 |

![饼干盘检测结果](docs/results/cookie-plate-annotated.png)

边缘支持度是圆周采样点中落在强梯度位置的比例，用于复核检出的圆是否贴合真实边缘。

## 目录结构

```text
hough_circles/   检测核心、HTTP 服务与前端页面
scripts/         验收脚本
examples/        两张实拍样图及来源说明
docs/results/    验收生成的标注图
openspec/        规格与变更记录
```

## OpenSpec 记录

开发由变更 `add-hough-circle-gui` 驱动，完成后已归档；规格、规划与任务进度见：

- `openspec/changes/archive/2026-11-14-add-hough-circle-gui/proposal.md`
- `openspec/changes/archive/2026-11-14-add-hough-circle-gui/specs/`（能力 `circle-detection`、`detection-gui`）
- `openspec/changes/archive/2026-11-14-add-hough-circle-gui/design.md`
- `openspec/changes/archive/2026-11-14-add-hough-circle-gui/tasks.md`（全部勾选）

归档时已同步主规格：

- `openspec/specs/circle-detection/spec.md`
- `openspec/specs/detection-gui/spec.md`

用 `openspec validate --specs --strict` 校验主规格，用 `openspec list --specs` 查看能力列表。

## 样图许可

见 [examples/SOURCES.md](examples/SOURCES.md)。
