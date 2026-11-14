# Spec Delta

## Purpose

在本地对图像执行霍夫圆检测，输出可直接用于标注与验收的圆心、半径，并保证两张实拍样图的检测结果可复核。

## ADDED Requirements

### Requirement: 参数化圆检测

系统 SHALL 接受 JPEG 或 PNG 图像与检测参数（dp、minDist、param1、param2、最小半径、最大半径、中值滤波核大小），返回检出的圆心坐标与半径列表。

#### Scenario: 使用给定参数检测

- **WHEN** 用户提交一张有效图像和一组合法参数
- **THEN** 系统返回每条结果的圆心 x、y 与半径 r，并按圆心 x 升序、y 升序排列

#### Scenario: 参数非法

- **WHEN** 用户提交 dp 不为正数，或最大半径小于最小半径且最大半径不为 0，或滤波核不是正奇数
- **THEN** 系统拒绝请求并说明哪一项参数非法，不产生检测结果

#### Scenario: 无法解码的文件

- **WHEN** 用户提交的文件不是可解码的图像
- **THEN** 系统返回错误提示，界面保持可用

### Requirement: 标注图导出

系统 SHALL 在原图分辨率上为每个检出圆绘制圆周与圆心，并导出 PNG 标注图，导出内容与界面预览一致。

#### Scenario: 导出标注结果

- **WHEN** 用户对一张已检出圆的结果执行导出
- **THEN** 系统返回与原图同宽同高的 PNG，文件名为原图名加 `-annotated` 后缀，图中圆的位置与当前预览一致

### Requirement: 实拍图验收判据

系统 SHALL 在 README 记录的固定参数下，对 `examples/coins.jpg` 恰好检出 2 个圆且半径均落在 170–190 像素，对 `examples/cookie-plate.jpg` 恰好检出 1 个圆且半径落在 235–255 像素。

#### Scenario: 硬币样图验收

- **WHEN** 使用验收参数检测 `coins.jpg`
- **THEN** 检出恰好 2 个圆，半径约为 179 与 180 像素，分别对应两枚硬币的外缘

#### Scenario: 饼干盘样图验收

- **WHEN** 使用验收参数检测 `cookie-plate.jpg`
- **THEN** 检出恰好 1 个圆，半径约为 245 像素，对应盘沿
