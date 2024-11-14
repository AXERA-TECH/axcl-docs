# AXCL 简介

## 概述

AXCL是用于在AX芯片平台上开发深度神经网络推理、转码等应用的C、Python语言API库，提供运行资源管理，内存管理，模型加载和执行，媒体数据处理等API，其逻辑架构图如下图所示：

![](../res/axcl_architecture.svg)

:::{Warning}
ffmpeg 和 python 尚在开发中，计划 2025 年 2 月发布。
:::


## 概念

AXCL运行时库有Device、Context、Stream、Task等基本概念，其关系如下图所示：

![](../res/axcl_concept.svg)

- Device： 提供计算和媒体处理的硬件设备，通过PCIe接口和Host连接。
  - Device的生命周期源于首次调用`axclrtSetDevice`接口。
  - Device使用引用计数管理生命周期，`axclrtSetDevice` 引用计数加1，`axclrtResetDevice` 引用计数减1。
  - 当引用计数减少为零时，本进程中的Device资源不可用。
  - **若存在多个Device，多个Device之间的内存资源不能共享**。
- Context：执行上下文容器，管理包括Stream，内存等生命周期，Context和应用线程绑定。Context一定隶属于一个唯一的Device。Context分为隐式和显示两种：
  - 隐式Context（即默认Context）：
    - 调用`axclrtSetDevice`接口指定设备时，系统会创建一个隐式Context，当`axclrtResetDevice`接口引用计数为零时隐式Context被自动销毁。
    - 一个Device只会有有一个隐式Context，隐式Context不能通过`axclrtDestroyContext`接口销毁。
  - 显示Context：
    - 调用`axclrtCreateContext`接口显示创建，调用`axclrtDestroyContext`接口销毁。
    - 进程内的Context是共享的，可以通过`axclrtSetCurrentContext`进行切换。**推荐应用为每个线程中创建和销毁显示Context**。
- Stream：执行任务流，隶属于Context，同一个Stream的任务执行保序。Stream分为隐式和显示两种：
  - 隐式Stream（即默认Stream）：
    - 每个Context都会创建一个隐式Stream，生命周期归属于Context。
    - native sdk模块（比如`AXCL_VDEC_XXX`’’、`AXCL_SYS_XXX`等）使用隐式Stream。
  - 显示Stream：
    - 由`axclrtCreateStream`接口创建，由`axclrtDestroyStream`接口销毁。
    - 当显示Stream归属的Context被销毁或生命周期结束后，即使该Stream没有被销毁，亦不可使用。
- Task：Device任务执行实体，应用不可见。

## 应用线程和Context

- 一个应用线程一定会绑定一个Context，所有Device的任务都必须基于Context。
- 一个线程中当前会有一个唯一的Context，Context中绑定了本线程任务执行的Device。
- 应用线程中支持通过`axclrCreateContext`创建多个Context，但一个线程同一时刻只能使用一个Context。连续创建多个Context，线程绑定的是最后一个创建的Context。
- 进程内支持通过`axclrtSetCurrentContext` 绑定当前线程的Context，连续多次调用`axclrtSetCurrentContext`，最终绑定的是最后一次的Context。
- 多线程推荐为每个线程显示创建一个Context。
- 推荐通过`axclrtSetCurrentContext`切换Device。



## 已支持设备

- M.2算力卡

  芯茧® 人工智能算力卡是 **深圳市云集互联生态科技有限公司** 推出的基于 **AX650N** 芯片的 M.2 2280 计算卡。

  ![芯茧®](../res/M2_YUNJI_DSC05130.jpg)

- PCIE x8 半高 4 芯计算卡
