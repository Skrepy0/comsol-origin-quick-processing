# Origin 可视化参数设置验收

入口：原主窗口顶部“Origin 绘图参数…”；或双击
`D:\COMSOL-to-CSV-and-Origin-parser\Origin-Settings.cmd`。

五个设置页签覆盖数据列/曲线、坐标轴、字体图例布局、尺寸导出和数据处理。
每条 Y 可独立指定颜色、线型、图例；颜色使用原生颜色选择器。
保存会先校验 TOML 参数，再原子替换配置文件，保留上一份 .ui-backup。

实际检查：

* 五个 Qt 页签渲染，已检查中文字体及布局。
* 当前所有可编辑字段保存/回读一致，未编辑配置段保留。
* 非法偶数平滑窗口被拒绝，配置文件字节保持不变。
* 修改标题、坐标下限、添加曲线、颜色、线型、导出格式均正确持久化。
* 未修改的 A 原窗口被真实创建，设置按钮成功插入；未加载模型。
* 原导入回调读取设置窗口保存后的最新配置（mock 验证，无需重启）。

验证脚本：scripts/verify_settings_ui.py。
图像：output/settings_preview/tab_1.png～tab_5.png、original_window.png。

测试不启动 COMSOL/Origin 引擎。底层 Origin 绘图和导出沿用已经真机验证的适配器；
这次没有重新运行完整大模型提取。A submodule 未修改。
