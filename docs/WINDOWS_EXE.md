# Windows EXE 使用与构建

下载 Releases 的 Windows x64 EXE，双击运行；也可下载 ZIP，解压后双击其中的
COMSOLOrigin.exe。无需安装 Python、pip、Git 或初始化 submodule。
首次单文件解包启动可能需要数十秒。

COMSOL 引擎和 Origin 桌面程序仍需单独安装并获得有效许可证。
兼容目标：Windows 10/11 x64、Origin 2025/2025b、模型所需的 COMSOL 版本。
高版本保存的 MPH 不能用低版本 COMSOL 打开。

配置和日志持久保存于 `%LOCALAPPDATA%\COMSOLOrigin`，不写入单文件 EXE 临时解包目录。
默认图片位于该目录的 output/figures；可通过“Origin 绘图参数…”浏览选择其他输出目录。
GUI 模式的 OPJU 仍保存到模型对应的原项目输出目录。
不附带任何个人模型、个人配置、科研结果或授权信息。

程序未做商业代码签名；请使用本仓库 Release 中的 SHA256SUMS.txt 校验下载文件。

## 从源码构建（开发者）

```powershell
git clone --recurse-submodules <repo>
python -m pip install -r requirements-build.txt
python scripts/build_windows.py
```

产物：dist/COMSOLOrigin.exe。打包资源与配置样例列在 COMSOLOrigin.spec；
Python、Qt、MPh/JPype、OriginExt、pandas/numpy/scipy/matplotlib 均打入应用。
上游源码保持原样，以打包资源随 EXE 携带。

内置验证选项供开发者使用：

* `COMSOLOrigin.exe --bundle-check`：模块、配置、原界面、设置按钮和安装发现。
* `COMSOLOrigin.exe --verify-origin`：使用合成数据验证处理、导入、三种图片导出和工程重开。
* `COMSOLOrigin.exe --verify-comsol`：读取本机 COMSOL 6.3 安装示例 busbar 的已有 Table。

检查结果在上述应用数据目录的 bundle-test 子目录；不会随 Release 上传本机路径记录。
`--verify-comsol --verify-origin` 可用同一份提取结果串联验证绘图、三种导出和工程重开。验证工程保存于当前工作目录的 bundle-test；保存采用临时工程加原子替换，避免 Origin 自动化进程对目标目录的写入限制。
