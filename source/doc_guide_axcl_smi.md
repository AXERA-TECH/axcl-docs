(doc-axcl-smi)=
# AXCL-SMI

## 概述

AXCL-SMI (System Management Interface) 工具用于设备信息收集，对设备进行配置等功能，支持如下设备信息收集：

- 硬件设备型号
- 固件版本号
- 驱动版本号
- 设备利用率
- 内存使用情况
- 设备芯片结温
- 其他信息



## 使用说明

### 快速使用

在正确安装AXCL驱动包后，AXCL-SMI即安装成功，直接执行`axcl-smi`显示内容如下：

```bash
$ axcl-smi
+------------------------------------------------------------------------------------------------+
| AXCL-SMI  V2.18.0                                                              Driver  V2.18.0 |
+-----------------------------------------+--------------+---------------------------------------+
| Card  Name                     Firmware | Bus-Id       |                          Memory-Usage |
| Fan   Temp                Pwr:Usage/Cap | CPU      NPU |                             CMM-Usage |
|=========================================+==============+=======================================|
|    0  AX650N                    V2.18.0 | 0001:81:00.0 |                181 MiB /      954 MiB |
|   --   52C                      -- / -- | 3%        0% |                 22 MiB /     3072 MiB |
+-----------------------------------------+--------------+---------------------------------------+

+------------------------------------------------------------------------------------------------+
| Processes:                                                                                     |
| Card      PID  Process Name                                                   NPU Memory Usage |
|================================================================================================|
|    0      763  /opt/bin/axcl/axcl_run_model                                            160 KiB |
+------------------------------------------------------------------------------------------------+
```

**字段说明**

| 字段             | 说明                               | 字段         | 说明                 |
| ---------------- | ---------------------------------- | ------------ | -------------------- |
| Card             | 设备索引编号，注意不是PCIe的设备号 | Bus-Id       | 设备Bus ID           |
| Name             | 设备名称                           | CPU          | CPU平均利用率        |
| Fan              | 风扇转速比（未支持）               | NPU          | NPU平均利用率        |
| Temp             | 设备芯片结温Tj                     | Memory-Usage | 系统内存： 使用/总量 |
| Firmware         | 设备固件版本号                     | CMM-Usage    | 媒体内存： 使用/总量 |
| Pwr: Usage/Cap   | 功耗（未支持）                     |              |                      |
|                  |                                    |              |                      |
| PID              | 主控进程PID                        |              |                      |
| Process Name     | 主控进程名称                       |              |                      |
| NPU Memory Usage | 设备NPU已使用的CMM内存             |              |                      |

:::{note}

参阅FAQ [DDR带宽](#faq_device_ddr_bw) 和 [NPU利用率](#faq_device_npu_tilization) 章节了解获取详细的DDR和NPU利用率。

:::



### 帮助 (-h) 和版本 (-v)

`axcl-smi -h`  查询帮助信息

```bash
$ axcl-smi -h
usage: axcl-smi [<command> [<args>]] [--device] [--version] [--help]

axcl-smi System Management Interface V2.18.1

Commands
    info                                    Show device information
        --temp                                  Show SoC temperature
        --mem                                   Show memory usage
        --cmm                                   Show CMM usage
        --cpu                                   Show CPU usage
        --npu                                   Show NPU usage
    proc                                    cat device proc
        --vdec                                  cat /proc/ax_proc/vdec
        --venc                                  cat /proc/ax_proc/venc
        --jenc                                  cat /proc/ax_proc/jenc
        --ivps                                  cat /proc/ax_proc/ivps
        --rgn                                   cat /proc/ax_proc/rgn
        --ive                                   cat /proc/ax_proc/ive
        --pool                                  cat /proc/ax_proc/pool
        --link                                  cat /proc/ax_proc/link_table
        --cmm                                   cat /proc/ax_proc/mem_cmm_info
    set                                     Set
        -f[MHz], --freq=[MHz]                   Set CPU frequency in MHz. One of: 1200000, 1400000, 1700000
    log                                     Dump logs from device
        -t[mask], --type=[mask]                 Specifies which logs to dump by a combination (bitwise OR) value of blow:
                                                  -1: all (default) 0x01: daemon 0x02: worker 0x10: syslog 0x20: kernel
        -o[path], --output=[path]               Specifies the path to save dump logs (default: ./)
    sh                                      Execute a shell command
        cmd                                     Shell command
        args...                                 Shell command arguments
-d, --device                            Card index [0, connected cards number - 1]
-v, --version                           Show axcl-smi version
-h, --help                              Show this help menu
```

`axcl-smi -v` 查询AXCL-SMI工具的版本

```bash
$ axcl-smi -v
AXCL-SMI V2.26.1 BUILD: Feb 13 2025 11:08:47
```



### 选项

#### 设备号 (-d, --device)

```bash
-d, --device                             Card index [0, connected cards number - 1]
```

`[-d, --device]` 指定设备号索引，范围：[0, 连接设备数量 - 1]， **默认为0号设备**。

:::{Important}

- SDK V2.25.0（含）以前的版本设备ID指的是PCIe bus number。
- SDK V2.26.0（含）以后的版本设备ID指的是设备索引号。

:::



### 信息查询（info）

`axcl-smi info`用于显示设备的详细信息，支持子命令如下：

| 子命令 | 说明                                                         |
| ------ | ------------------------------------------------------------ |
| --temp | 显示设备芯片结温，单位是摄氏度x1000。                        |
| --mem  | 显示设备系统详细内存使用情况。                               |
| --cmm  | 显示设备媒体内存使用情况。如果需要更详细的媒体内存，执行`axcl-smi sh cat /proc/ax_proc/mem_cmm_info -d xx`  (xx是PCIe设备号)。 |
| --cpu  | 显示设备CPU利用率。                                          |
| --npu  | 显示设备NPU利用率。                                          |

**示例**：查询索引号为0号的设备的媒体内存使用情况：

```bash
$ axcl-smi info --cmm -d 0
Device ID           : 129 (0x81)
CMM Total           :  3145728 KiB
CMM Used            :    18876 KiB
CMM Remain          :  3126852 kiB
```



### PROC查询（proc）

`axcl-smi proc`用于查询设备模块的proc信息，支持子命令如下：

| 子命令 | 说明                                               |
| ------ | -------------------------------------------------- |
| --vdec | 查询VDEC模块proc (`cat /proc/ax_proc/vdec`)        |
| --venc | 查询VENC模块proc (`cat /proc/ax_proc/venc`)        |
| --jenc | 查询JENC模块proc (`cat /proc/ax_proc/jenc`)        |
| --ivps | 查询IVPS模块proc (`cat /proc/ax_proc/ivps`)        |
| --rgn  | 查询RGN模块proc (`cat /proc/ax_proc/rgn`)          |
| --ive  | 查询IVE模块proc (`cat /proc/ax_proc/ive`)          |
| --pool | 查询POOL模块proc (`cat /proc/ax_proc/pool`)        |
| --link | 查询LINK模块proc (`cat /proc/ax_proc/link_table`)  |
| --cmm  | 查询CMM模块proc (`cat /proc/ax_proc/mem_cmm_info`) |

**示例**：查询0号设备的VDEC proc信息

```bash
$ axcl-smi proc --vdec -d 0
```



### 参数设置（set）

`axcl-smi set` 用户配置设备信息，支持的子命令如下：

| 子命令                | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| -f[MHz], --freq=[MHz] | 设置设备的CPU频率，只支持 1200000, 1400000, 1700000 三种频率 |

**示例**：设置索引号为0号的设备CPU主频为1200MHz

```bash
$ axcl-smi set -f 1200000 -d 0
set cpu frequency 1200000 to device 129 succeed.
```



### 下载日志（log）

`axcl-smi log` 用于下载设备的日志文件到主控侧，支持的参数如下：

| 参数                      | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| -t[mask], --type=[mask]   | 指定下载的日志类别。设备侧日志类别如下：<br />-1： 全部日志<br />0x01：守护进程<br />0x02:  业务进程<br />0x10：syslog<br />0x20：内核日志<br />推荐-1下载全部日志 |
| -o[path], --output=[path] | 指定日志保存路径，支持绝对和相对路径，默认是当前目录。注意目录需要有写权限。 |

**示例**：下载索引为0号的设备的全部日志，并保存到当前目录

```bash
$ axcl-smi log -d 0
[2025-02-13 21:07:40.302][1265][C][log][dump][73]: log dump finished: ./dev129_log_20250213210740.tar.gz
```



### shell命令（sh）

`axcl-smi sh` 支持shell命令查询设备信息，通常用于查询设备侧模块的运行proc信息，**示例**：查询索引号为0号的设备CMM信息

```bash
$ axcl-smi sh cat /proc/ax_proc/mem_cmm_info -d 0
--------------------SDK VERSION-------------------
[Axera version]: ax_cmm V2.26.0_20250211193319 Feb 11 2025 19:52:13 JK
+---PARTITION: Phys(0x180000000, 0x23FFFFFFF), Size=3145728KB(3072MB),    NAME="anonymous"
 nBlock(Max=0, Cur=23, New=0, Free=0)  nbytes(Max=0B(0KB,0MB), Cur=19329024B(18876KB,18MB), New=0B(0KB,0MB), Free=0B(0KB,0MB))  Block(Max=0B(0KB,0MB), Min=0B(0KB,0MB), Avg=0B(0KB,0MB))
   |-Block: phys(0x180000000, 0x180013FFF), cache =non-cacheable, length=80KB(0MB),    name="TDP_DEV"
   |-Block: phys(0x180014000, 0x180014FFF), cache =non-cacheable, length=4KB(0MB),    name="TDP_CMODE3"
   |-Block: phys(0x180015000, 0x180015FFF), cache =non-cacheable, length=4KB(0MB),    name="TDP_CMODE3_CPU"
   |-Block: phys(0x180016000, 0x180029FFF), cache =non-cacheable, length=80KB(0MB),    name="TDP_DEV"
   |-Block: phys(0x18002A000, 0x18002AFFF), cache =non-cacheable, length=4KB(0MB),    name="TDP_CMODE3"
   |-Block: phys(0x18002B000, 0x18002BFFF), cache =non-cacheable, length=4KB(0MB),    name="TDP_CMODE3_CPU"
   |-Block: phys(0x18002C000, 0x180047FFF), cache =non-cacheable, length=112KB(0MB),    name="VGP_DEV"
   |-Block: phys(0x180048000, 0x180048FFF), cache =non-cacheable, length=4KB(0MB),    name="VGP_CMODE3"
   |-Block: phys(0x180049000, 0x180049FFF), cache =non-cacheable, length=4KB(0MB),    name="VGP_CMODE3_CPU"
   |-Block: phys(0x18004A000, 0x1801C9FFF), cache =non-cacheable, length=1536KB(1MB),    name="h26x_ko"
   |-Block: phys(0x1801CA000, 0x180349FFF), cache =non-cacheable, length=1536KB(1MB),    name="h26x_ko"
   |-Block: phys(0x18034A000, 0x18034AFFF), cache =non-cacheable, length=4KB(0MB),    name="h26x_ko"
   |-Block: phys(0x18034B000, 0x18094AFFF), cache =non-cacheable, length=6144KB(6MB),    name="vdec_ko"
   |-Block: phys(0x18094B000, 0x180ACAFFF), cache =non-cacheable, length=1536KB(1MB),    name="jenc_ko"
   |-Block: phys(0x180ACB000, 0x180C4AFFF), cache =non-cacheable, length=1536KB(1MB),    name="jenc_ko"
   |-Block: phys(0x180C4B000, 0x180C4BFFF), cache =non-cacheable, length=4KB(0MB),    name="jenc_ko"
   |-Block: phys(0x180C4C000, 0x180C67FFF), cache =non-cacheable, length=112KB(0MB),    name="VPP_DEV"
   |-Block: phys(0x180C68000, 0x180C68FFF), cache =non-cacheable, length=4KB(0MB),    name="VPP_CMODE3"
   |-Block: phys(0x180C69000, 0x180C69FFF), cache =non-cacheable, length=4KB(0MB),    name="VPP_CMODE3_CPU"
   |-Block: phys(0x180C6A000, 0x181269FFF), cache =non-cacheable, length=6144KB(6MB),    name="vdec_ko"
   |-Block: phys(0x18126A000, 0x18126AFFF), cache =non-cacheable, length=4KB(0MB),    name="GDC_CMDA3"
   |-Block: phys(0x18126B000, 0x18126BFFF), cache =non-cacheable, length=4KB(0MB),    name="GDC_CMDA3_CPU"
   |-Block: phys(0x18126C000, 0x18126EFFF), cache =non-cacheable, length=12KB(0MB),    name="GDC_CMD"

---CMM_USE_INFO:
 total size=3145728KB(3072MB),used=18876KB(18MB + 444KB),remain=3126852KB(3053MB + 580KB),partition_number=1,block_number=23
```

:::{Important}

- shell命令参数如果包含`-`,`--`,`>`等字段，可以用双引号`"-l"`将命令和参数包含在一个字符串中，比如`axcl-smi sh "ls -l" -d 0`
- 谨慎使用shell命令对设备进行配置

:::



### 重启（reboot）

`axcl-smi reboot` 命令首先复位指定设备，随后将自动加载固件，示例如下：

```bash
$ axcl-smi reboot -d 0
Do you want to reboot device 0 ? (y/n): y
```
