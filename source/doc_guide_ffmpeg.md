# FFmpeg

## 环境准备

AXCL_FFMPEG动态库存放在 `/usr/lib/axcl/ffmpeg`，AXCL_FFMPEG可执行程序存放在 `/usr/bin/axcl/ffmpeg`.

执行ffmpeg需要首先设置动态库查找路径，环境变量设置：
```sh
export LD_LIBRARY_PATH="/usr/lib/axcl/ffmpeg:$LD_LIBRARY_PATH";
```



## 如何重新编译FFmpeg？

SDK FFmpeg基于7.1版本开发，并提供了编译后的so和ffmpeg bin文件可直接链接和运行。

如果需要重新编译FFmpeg，按照如下步骤：

1.  从github下载FFmpeg-n7.1.tar.gz，[点我下载](https://github.com/FFmpeg/FFmpeg/releases/tag/n7.1)。将FFmpeg-n7.1.tar.gz拷贝到`axcl/3rdparty/ffmpeg` 目录。

2.  解压

   ```bash
   tar -zxvf FFmpeg-n7.1.tar.gz
   ```

3.  patch

   ```bash
   patch -p3 < FFmpeg-n7.1.patch
   ```

4. 编译

   - arm64

     ```bash
     cd axcl/3rdparty/ffmpeg
     make host=arm64 clean all install
     ```

     目标文件路径：

     ```
     lib: axcl/out/axcl_linux_arm64/lib/ffmpeg
     bin: axcl/out/axcl_linux_arm64/bin/ffmpeg
     ```

   - x86

     ```bash
     cd axcl/3rdparty/ffmpeg
     make host=x86 clean all install
     ```

     目标文件路径：

     ```
     lib: axcl/out/axcl_linux_x86/lib/ffmpeg
     bin: axcl/out/axcl_linux_x86/bin/ffmpeg
     ```
