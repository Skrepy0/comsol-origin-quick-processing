# COMSOL → Origin 快速处理

Windows 科研绘图工具：在[COMSOL-to-CSV-and-Origin-parser](https://github.com/GhVost/COMSOL-to-CSV-and-Origin-parser)的基础上，接入 Origin 自动绘图和图片导出。

工作流程：
COMSOL 已求解模型 → 原项目提取并导入 Origin → 配置曲线与样式 → PNG / TIFF / PDF / OPJU。

## 安装与双击启动

需要 Git、64 位 Python 3.11 或 3.12、有效授权的 COMSOL 与 Origin 2025/2025b。

```powershell
git clone --recurse-submodules https://github.com/ikunabc/comsol-origin-quick-processing.git
cd comsol-origin-quick-processing
```

1. 双击 `Setup-GUI.cmd`，初始化 submodule 并安装 Python 依赖。
2. 双击 `Start-GUI.cmd`，打开原项目的模型读取和结果选择界面。
3. 点击顶部 **Origin 绘图参数…**，设置结果 Tag、X/Y 列和绘图样式。
4. 打开已求解 MPH，勾选对应结果及“Import extracted results into OriginLab”，点击 Extract。

也可双击 `Origin-Settings.cmd`，单独打开参数设置窗口。
首次启动自动从 `config.default.toml` 生成本机 `config.toml`。本机配置、模型、工程、输出和日志不会提交到 Git。

安装失败时，检查 Python、Git、网络和许可证；已有 clone 可执行：

```powershell
git submodule update --init --recursive
python -m pip install -r requirements-gui.txt
```

## 可视化参数

- 曲线：line、line_symbol、scatter、column；X/Y 列、标题、Origin 模板。
- 每条曲线：颜色选择器、实线/虚线/点线/点划线、图例文字；统一线宽与符号大小。
- 坐标：标题、显示单位、min/max/major_step 自动或手动、linear/log10。
- 字体与图例：字体、各类字号、位置、边框、图层边距。
- 导出：像素宽高、PNG/TIFF/PDF、DPI、透明背景、目录和文件名。
- 数据处理：NaN/Inf 清理、排序、Savitzky–Golay/移动平均/中值滤波，以及 linear/cubic/pchip 插值。

“保存设置”先校验再原子写入，并备份到 `config.toml.ui-backup`；原界面导入后读取最新设置，无需重启。
单位标签不会自动换算数值。m/s → μm/s 必须对数据实际乘以 10⁶。
多 Y 当前指同一个数据集中的多列；跨多表、多模型条件合并和多面板绘图尚未实现。

## 两种工作方式

**GUI 模式（推荐）**：复用原项目读取、勾选、提取、导入流程；新增适配器只在导入后复用 Workbook 绘图。
OPJU 保存到原项目本次输出目录；图片按设置中的导出路径保存。

**可选命令行模式**：

```powershell
python main.py
python main.py --config config.example-csv.toml
python main.py --check
python main.py --dry-run
python main.py --list-results
```

CSV 模式不启动 COMSOL。附带 example.csv 是合成数据；不附带科研模型。
--check 不启动应用，检查包版本、submodule、COMSOL 安装及 Origin COM 注册。
--dry-run 只打印计划；--list-results 加载模型列出 Tables/1D/2D/3D，不求解。

## 后端与真实 API

以 Git submodule 保存在 `lib/comsol_csv_tool/`，固定 commit：
`4c63ac17fbb6272603a893e0233c6d27aa485180`。
不复制、不修改上游源码，兼容和扩展在 `src/adapters/`。

实际调用 `discover_items`、`extract_table`、`extract_via_export`；Origin 使用官方 originpro/OriginExt，
不模拟鼠标键盘。源码核查见 [API_AUDIT.md](docs/API_AUDIT.md)。

## 数据与图像约束

- 模型需要事先求解；不调用 solve 或保存源 MPH。高版本保存的模型需要兼容版本的 COMSOL。
- Savitzky–Golay 要求近似等距 X；插值要求唯一递增 X；cubic 至少 4 点。
- 拼接参数扫描被拒绝跨扫描平滑；应先拆分条件或准备独立 Y 宽表。
- 插值会移除未选中列，避免给新网格伪造其他物理量。
- 图页物理尺寸 = 像素尺寸 / DPI。PDF 是矢量页面，没有整页像素 DPI；透明背景仅支持 PNG/TIFF。
- GUI 内部临时会话隐藏地追加图并保存，完成后由原项目打开工程；失败保留已导入工程并提示错误。
- COMSOL/Origin 必须自行安装与授权；若软件输出 demo 水印，需要处理软件授权。

## 项目结构

```text
Start-GUI.cmd / Origin-Settings.cmd / Setup-GUI.cmd
gui_main.py / origin_settings.py / main.py
config.default.toml / config.example-*.toml
src/
  settings_ui.py           # 可视化参数编辑器
  config.py / pipeline.py / diagnostics.py
  adapters/
    comsol_adapter.py      # 原项目真实提取 API 包装
    gui_adapter.py         # 原界面导入后追加绘图
    origin_adapter.py      # Origin 图形与导出
    process_adapter.py     # 科学数据处理
  models/dataset.py
lib/comsol_csv_tool/       # 上游 submodule
scripts/                  # 合成数据、安装示例和 UI 验证
 tests/                   # 配置、处理、CSV、适配器测试
```

## 测试

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
# 需 GUI 依赖，不启动 COMSOL/Origin 引擎：
python scripts/verify_settings_ui.py
# 实际 Origin 合成数据绘图与文件检查：
python scripts/verify_origin.py
python scripts/verify_images.py
```

本机验证覆盖 COMSOL 6.3/6.4 的已求解数据提取、Origin 2025b Workbook、四类图型、
PNG/TIFF/PDF、透明 PNG/TIFF、OPJU 重开，以及 Qt 参数保存与原窗口接入。
这是运行环境相关结果，不保证其他版本/许可证配置自动通过。完整原始科研测试记录保留在本机，不公开上传。

## 常见问题

- COMSOL 未发现或 license 错误：检查安装和授权，使用 --check 检查版本；高版本 MPH 不能由低版本打开。
- 结果/列名不存在：--list-results 查询 tag；表头去单位后的名称用于 X/Y 配置，重复名称需 column_map。
- GUI 选中结果与绘图设置不一致：导入仍可完成，自动绘图会明确提示缺少配置结果。
- Origin 连接失败：先手动完成首次运行和许可提示，确认 64 位 Python 与 originpro/OriginExt。
- CSV 解析失败：显式指定 standard/backend/native 格式及 encoding；不自动推断十进制逗号。
- 导出/保存失败：检查路径、权限、文件锁与 Origin 对话框；长路径 OPJU 建议改用短本地路径。
- 日志：`logs/gui.log` 和 `logs/pipeline.log`；终端/弹窗显示简洁错误，完整 traceback 在日志。

更新上游后应重新审查 API 并验证：`git submodule update --remote --recursive`。
