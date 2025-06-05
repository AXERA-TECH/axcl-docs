(sdk_compile)=
# SDK 编译

## 概述

本章节描述根据AX SDK编译设备侧固件(pac)的方法和deb、rpm的制作方法。

## 环境准备

设备侧固件编译需要用到如下资源：

- PC： 推荐 ubuntu-22.04.1
- gcc version 9.2.1 20191025
- SDK开发包,即：AX650_SDK_Vx.xx.xx.tgz, 比如:AX650_SDK_V3.6.2_20250603154858_NO4873.tgz

:::{tip}
关于工具链的下载、安装和配置请参考<<AX SDK 使用说明.docx>>
:::



## 安装SDK

1.   解压SDK

   ```bash
   tar -xvf AX650_SDK_Vx.xx.x.tgz
   ```

2.  cd AX650_SDK_Vx.xx.x 进入解压后的目录，执行`./sdk_unpack.sh`展开SDK包的内容

   ```bash
   cd AX650_SDK_Vx.xx.x
   ./sdk_unpack.sh
   ```

   :::{note}

   - 执行./sdk_unpack.sh命令时，可以带一个路径参数，用于指定Kernel 5.15.73源码tar包的位置。也可以不指定该路径，解压脚本后将自动拉取Kernel代码。

   - sdk_clean.sh脚本用于清理展开后的SDK包中的内容。sdk_clean.sh脚本是sdk_unpack.sh脚本的逆向操作，执行该脚本后所有通过sdk_unpack.sh脚本生成的文件及目录均会被清除，如果有私有数据请提前备份，谨慎使用！
   - 解压后axcl目录是主控的驱动和sample源码以及AXCL依赖动态库。制作deb、rpm安装包依赖axcl/out目录下的文件，请不要删除，否则会导致安装包制作失败。

   :::



## 编译

### 主控(HOST)编译

:::{note}

设备侧固件的编译时会自动生成deb、rpm安装包，而安装包制作依赖驱动和动态库，因此如果改动了axcl目录下的主控驱动等源码，并希望打包到deb、rpm安装包中，请首先编译axcl目录。

:::

1.  进入主控编译目录

   ```bash
   cd axcl/build
   ```

2.  编译

   ```bash
   # 一次全编译
   make clean && make host=x86 clean && make host=arm64 clean
   make all install -j128 && make host=x86 all install -j128 && make host=arm64 all install -j128

   # 或者依次编译各个主控
   make clean && make all install -j128
   make host=x86 clean && make host=x86 all install -j128
   make host=arm64 clean && make host=arm64 all install -j128
   ```

| 编译选项                    | 说明                                           | 编译输出路径                  |
| :-------------------------- | ---------------------------------------------- | ----------------------------- |
| `host=ax650`或者省略`host=` | 适用于主控芯片是AX650N                         | axcl/out/**axcl_linux_ax650** |
| `host=x86`                  | 适用于主控芯片是X86架构，比如INTEL、AMD64      | axcl/out/**axcl_linux_x86**   |
| `host=arm64`                | 适用于其他ARM64主控芯片，比如RK3588、树莓派5等 | axcl/out/**axcl_linux_arm64** |

### 设备(DEVICE)编译

1. 进入设备侧编译目录

   ```bash
   cd build
   ```

2. 编译

   ```bash
   make p=AX650_card clean all install axp -j128
   ```

3. 编译生成路径: `build/out`，其中AX650_card/**ax650_card.pac** 为设备侧固件。deb、rpm安装包路径位于`build/out`目录。



:::{tip}

- 设备侧使用ramdisk，rootfs路径位于`rootfs/card`目录。
- deb、rpm安装包描述参阅`axcl/build/package`目录，用户可以根据实际需求变更。

:::
