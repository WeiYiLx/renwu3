# Spec Delta

## MODIFIED Requirements

### Requirement: 图片导入

系统 SHALL 支持在界面中选择本地 JPEG/PNG 图片并显示原图。

#### Scenario: 导入有效图片

- **WHEN** 用户选择一张 JPEG 或 PNG 图片
- **THEN** 界面显示原图与图片尺寸，并立即用当前参数执行一次检测

#### Scenario: 导入不支持的格式

- **WHEN** 用户选择非 JPEG/PNG 文件或损坏文件
- **THEN** 界面提示无法读取该图片，原图与上一次结果保持不变

### Requirement: 参数调节与实时预览

系统 SHALL 为 dp、minDist、param1、param2、最小半径、最大半径与滤波核提供可调节控件，参数变化后自动重新检测并显示标注预览与检出数量。

#### Scenario: 调节参数后预览更新

- **WHEN** 用户修改任一参数
- **THEN** 界面在短暂防抖后显示新的标注预览、检出数量，以及每个圆的圆心与半径

#### Scenario: 未导入图片时调参

- **WHEN** 尚未导入图片时用户调节参数
- **THEN** 界面不发起检测请求，并提示先导入图片

#### Scenario: 恢复默认参数

- **WHEN** 用户点击恢复默认参数
- **THEN** 所有滑杆回到默认值，并按默认参数重新检测当前图片

### Requirement: 导出标注图

系统 SHALL 允许用户下载当前参数下的 PNG 标注图。

#### Scenario: 导出当前结果

- **WHEN** 用户点击导出且当前已有检测结果
- **THEN** 浏览器下载 PNG 文件，内容为当前预览中的标注结果，文件名包含原图名

#### Scenario: 无结果时导出

- **WHEN** 尚未导入图片或当前参数未检出任何圆时用户点击导出
- **THEN** 界面提示没有可导出的标注结果，不下载文件
