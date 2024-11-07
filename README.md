# AXCL 使用手册

[Web Preview]((https://axcl-docs.readthedocs.io/zh-cn/latest/)

## 1. 项目背景

**AXCL** 是基于 AX650N 的 PCIE EP 产品 Host API。

- 提供 AXCL 使用 NPU 计算的相关 API 和示例;
- 促进社区开发人员共同维护文档。

## 2. 本地编译指南

### 2.1 git clone

```bash
git clone https://github.com/AXERA-TECH/axcl-docs.git
```

目录如下:

```bash
.
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
└── source
    ├── conf.py
    ├── doc_guide_axcl_api.md
    ├── doc_guide_hardware.md
    ├── doc_guide_quick_start.md
    ├── doc_introduction.md
    ├── doc_update_info.md
    ├── index.rst
    └── media
        ├── demo
        └── hardware
```

### 2.2 编译

安装依赖

```bash
pip install -r requirements.txt
```

在项目根目录下执行以下命令

```bash
$ make clean
$ make html
```

### 2.3 本地预览

编译后，使用浏览器查看它 `build/html/index.html`

## 3. 参考设计

这个项目是基于Sphinx，更多关于Sphinx的信息可以在这里找到 https://www.sphinx-doc.org/en/master/

## 4. 在线发布

基于 [ReadtheDocs](https://readthedocs.org/) 平台代理在线 Web 服务。
