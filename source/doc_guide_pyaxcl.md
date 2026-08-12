# pyAXCL

pyAXCL 是 AXCL 的 Python 接口封装，用于在 Python 环境中调用 AXCL runtime、sys、pool、npu、vdec、venc、ivps、dmadim、ive、utils 等模块能力。

## 运行要求

- Python >= 3.9
- 64 位 Python
- Linux 环境

## 安装

从 SDK 的 `axcl/out/python/` 目录取出 wheel 包并安装：

```bash
pip3 install pyAXCL-X.YY.Z-py3-none-any.whl
pip3 show pyAXCL
```

验证安装：

```python
>>> import axcl
```

卸载：

```bash
pip3 uninstall pyAXCL -y
```

## 模块说明

| 模块 | 说明 |
| --- | --- |
| `axcl` | AXCL 初始化、去初始化、日志设置等基础接口 |
| `axcl.rt` | runtime、device、context、memory、engine 相关接口 |
| `axcl.sys` | 系统和设备内存相关接口 |
| `axcl.pool` | 内存池相关接口 |
| `axcl.npu` | NPU SMI、VNPU 配置相关接口 |
| `axcl.vdec` | 视频解码相关接口 |
| `axcl.venc` | 视频编码相关接口 |
| `axcl.ivps` | IVPS 图像处理相关接口 |
| `axcl.dmadim` | DMA DIM 相关接口 |
| `axcl.ive` | IVE 相关接口 |
| `axcl.utils` | 工具函数和日志辅助接口 |

## 构建 wheel

如需重新构建 pyAXCL wheel，请参考 [SDK 编译](#sdk_compile) 中的 Python wheel 编译说明。
