# AXCL Samples 说明

## AXCL Runtime API Samples

### axcl_sample_runtime

1. Initialize axcl runtime by axclrtInit.
2. Active EP by axclrtSetDevice.
3. Create context by axclrtCreateDevice for main thread. (optional)
4. Create and destory thread context. (must)
5. Destory context of main thread.
6. Deactive EP by axclrtResetDevice
7. Deinitialize runtime by axclFinalize

**usage**：

```bash
usage: ./axcl_sample_runtime [options] ... 
options:
  -d, --device    device id (int [=0])
      --json      axcl.json path (string [=./axcl.json])
  -?, --help      print this message

-d: EP slot id, if 0, means conntect to 1st detected EP id
--json: axcl.json file path
```

**example**：

```bash
/opt/bin/axcl # ./axcl_sample_runtime 
[INFO ][                            main][  22]: ============== V2.15.1_20241022175101 sample started Oct 22 2024 18:04:34 ==============
[INFO ][                            main][  34]: json: ./axcl.json
[INFO ][                            main][  48]: device id: 129
[INFO ][                            main][  78]: ============== V2.15.1_20241022175101 sample exited Oct 22 2024 18:04:34 ==============
```

### axcl_sample_memory

sample for memcpy between host and device

        HOST                      DEVICE
    host_mem[0] ---------------> dev_mem[0] ----
                                               |
                                               |
    host_mem[1] <--------------- dev_mem[1] <---

1. alloc 2 host memories: *host_mem[2]*
2. alloc 2 device memories: *dev_mem[2]*
3. memcpy from host_mem[0] to dev_mem[0] by AXCL_MEMCPY_HOST_TO_DEVICE
4. memcpy from dev_mem[0] to dev_mem[1] by AXCL_MEMCPY_DEVICE_TO_DEVICE
5. memcpy from dev_mem[1] to host_mem[0] by AXCL_MEMCPY_DEVICE_TO_HOST
6. memcmp between host_mem[0] and host_mem[1]


**usage**：

```bash
usage: ./axcl_sample_memory [options] ... 
options:
  -d, --device    device id (int [=0])
      --json      axcl.json path (string [=./axcl.json])
  -?, --help      print this message

-d: EP slot id, if 0, means conntect to 1st detected EP id
--json: axcl.json file path
```

**example**：

```bash
/opt/bin/axcl # ./axcl_sample_memory
[INFO ][                            main][  32]: ============== V2.15.1_20241022175101 sample started Oct 22 2024 18:04:36 ==============
[INFO ][                           setup][ 112]: json: ./axcl.json
[INFO ][                           setup][ 127]: device id: 129
[INFO ][                            main][  51]: alloc host and device memory, size: 0x800000
[INFO ][                            main][  63]: memory [0]: host 0xffff963fd010, device 0x1c126f000
[INFO ][                            main][  63]: memory [1]: host 0xffff95bfc010, device 0x1c1a6f000
[INFO ][                            main][  69]: memcpy from host memory[0] 0xffff963fd010 to device memory[0] 0x1c126f000
[INFO ][                            main][  75]: memcpy device memory[0] 0x1c126f000 to device memory[1] 0x1c1a6f000
[INFO ][                            main][  81]: memcpy device memory[1] 0x1c1a6f000 to host memory[0] 0xffff95bfc010
[INFO ][                            main][  88]: compare host memory[0] 0xffff963fd010 and host memory[1] 0xffff95bfc010 success
[INFO ][                         cleanup][ 142]: deactive device 129 and cleanup axcl
[INFO ][                            main][ 106]: ============== V2.15.1_20241022175101 sample exited Oct 22 2024 18:04:36 ==============
```

## AXCL Native API Samples

### axcl_sample_dmadim

1. memcpy between two device memories by AXCL_DMA_MemCopy
2. memset device memory to 0xAB by AXCL_DMA_MemCopy
3. checksum by AXCL_DMA_CheckSum
4. crop 1/4 image from (0, 0) by AXCL_DMA_MemCopyXD (AX_DMADIM_2D)

**usage**：

```bash
usage: ./axcl_sample_dmadim --image=string --width=unsigned int --height=unsigned int [options] ... 
options:
  -d, --device    device id (int [=0])
  -i, --image     nv12 image file path (string)
  -w, --width     width of nv12 image (unsigned int)
  -h, --height    height of nv12 image (unsigned int)
      --json      axcl.json path (string [=./axcl.json])
  -?, --help      print this message

-d: EP slot id, if 0, means conntect to 1st detected EP id
--json: axcl.json file path
-i: nv12 image to crop
-w: width of input nv12 image
-h: height of input nv12 image
```

**example**：
```bash
/opt/bin/axcl # ./axcl_sample_dmadim -i 1920x1080.nv12.yuv -w 1920 -h 1080
[INFO ][                            main][  30]: ============== V2.15.1_20241022175101 sample started Oct 22 2024 18:04:43 ==============
[INFO ][                            main][  46]: json: ./axcl.json
[INFO ][                            main][  61]: device id: 129
[INFO ][                        dma_copy][ 115]: dma copy device memory succeed, from 0x1c126f000 to 0x1c166f000
[INFO ][                      dma_memset][ 135]: dma memset device memory succeed, 0x1c126f000 to 0xab
[INFO ][                    dma_checksum][ 162]: dma checksum succeed, checksum = 0xaaa00000
[INFO ][                      dma_copy2d][ 277]: [0] dma memcpy 2D succeed
[INFO ][                      dma_copy2d][ 277]: [1] dma memcpy 2D succeed
[INFO ][                      dma_copy2d][ 304]: /opt/data/dma2d_output_image_960x540.nv12 is saved
[INFO ][                      dma_copy2d][ 324]: dma copy2d nv12 image pass
[INFO ][                            main][  78]: ============== V2.15.1_20241022175101 sample exited Oct 22 2024 18:04:43 ==============
```

### axcl_sample_vdec

1. Load .mp4 or .h264/h265 stream file
2. Demux nalu by ffmpeg
3. Send nalu to VDEC by frame
4. Get decodec YUV


**usage**：

```bash
usage: ./axcl_sample_vdec --url=string [options] ... 
options:
  -i, --url       mp4|.264|.265 file path (string)
  -d, --device    device id (int [=0])
      --count     grp count (int [=1])
      --json      axcl.json path (string [=./axcl.json])
  -w, --width     frame width (int [=1920])
  -h, --height    frame height (int [=1080])
      --VdChn     channel id (int [=0])
      --yuv       transfer nv12 from device (int [=0])
  -?, --help      print this message

-d: EP slot id, if 0, means conntect to 1st detected EP id
--json: axcl.json file path
-i: mp4|.264|.265 file path
--count: how many streams are decoded at same time
-w: width of decoded output nv12 image
-h: height of decoded output nv12 image
--VdChn: VDEC output channel index
      0: PP0, same width and height for input stream, cannot support scaler down.
    1: PP1, support scale down. range: [48x48, 4096x4096]
    2: PP2, support scale down. range: [48x48, 1920x1080]
```

**example**：

decode 4 streams:

```bash
/opt/bin/axcl # ./axcl_sample_vdec -i bangkok_30952_1920x1080_30fps_gop60_4Mbps.
mp4  --count 4
[INFO ][                            main][  43]: ============== V2.16.0_20241108173111 sample started Nov  8 2024 17:45:03 ==============

[INFO ][                            main][  67]: json: ./axcl.json
[INFO ][                            main][  82]: device id: 129
[INFO ][                            main][  86]: active device 129
[INFO ][             ffmpeg_init_demuxer][ 415]: [0] url: bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4
[INFO ][             ffmpeg_init_demuxer][ 478]: [0] url bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4: codec 96, 1920x1080, fps 30
[INFO ][             ffmpeg_init_demuxer][ 415]: [1] url: bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4
[INFO ][             ffmpeg_init_demuxer][ 478]: [1] url bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4: codec 96, 1920x1080, fps 30
[INFO ][             ffmpeg_init_demuxer][ 415]: [2] url: bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4
[INFO ][             ffmpeg_init_demuxer][ 478]: [2] url bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4: codec 96, 1920x1080, fps 30
[INFO ][             ffmpeg_init_demuxer][ 415]: [3] url: bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4
[INFO ][             ffmpeg_init_demuxer][ 478]: [3] url bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4: codec 96, 1920x1080, fps 30
[INFO ][                            main][ 112]: init sys
[INFO ][                            main][ 121]: init vdec
[INFO ][                            main][ 135]: start decoder 0
[INFO ][sample_get_vdec_attr_from_stream_info][ 244]: stream info: 1920x1080 payload 96 fps 30
[INFO ][ sample_get_decoded_image_thread][ 303]: [decoder  0] decode thread +++
[INFO ][                            main][ 172]: start demuxer 0
[INFO ][          ffmpeg_dispatch_thread][ 180]: [0] +++
[INFO ][             ffmpeg_demux_thread][ 280]: [0] +++
[INFO ][                            main][ 135]: start decoder 1
[INFO ][sample_get_vdec_attr_from_stream_info][ 244]: stream info: 1920x1080 payload 96 fps 30
[INFO ][ sample_get_decoded_image_thread][ 303]: [decoder  1] decode thread +++
[INFO ][                            main][ 172]: start demuxer 1
[INFO ][          ffmpeg_dispatch_thread][ 180]: [1] +++
[INFO ][             ffmpeg_demux_thread][ 280]: [1] +++
[INFO ][                            main][ 135]: start decoder 2
[INFO ][sample_get_vdec_attr_from_stream_info][ 244]: stream info: 1920x1080 payload 96 fps 30
[INFO ][                            main][ 172]: start demuxer 2
[INFO ][ sample_get_decoded_image_thread][ 303]: [decoder  2] decode thread +++
[INFO ][          ffmpeg_dispatch_thread][ 180]: [2] +++
[INFO ][             ffmpeg_demux_thread][ 280]: [2] +++
[INFO ][                            main][ 135]: start decoder 3
[INFO ][sample_get_vdec_attr_from_stream_info][ 244]: stream info: 1920x1080 payload 96 fps 30
[INFO ][ sample_get_decoded_image_thread][ 303]: [decoder  3] decode thread +++
[INFO ][                            main][ 172]: start demuxer 3
[INFO ][          ffmpeg_dispatch_thread][ 180]: [3] +++
[INFO ][             ffmpeg_demux_thread][ 280]: [3] +++
[INFO ][             ffmpeg_demux_thread][ 316]: [0] reach eof
[INFO ][             ffmpeg_demux_thread][ 411]: [0] demuxed    total 470 frames ---
[INFO ][             ffmpeg_demux_thread][ 316]: [1] reach eof
[INFO ][             ffmpeg_demux_thread][ 411]: [1] demuxed    total 470 frames ---
[INFO ][             ffmpeg_demux_thread][ 316]: [2] reach eof
[INFO ][             ffmpeg_demux_thread][ 411]: [2] demuxed    total 470 frames ---
[INFO ][             ffmpeg_demux_thread][ 316]: [3] reach eof
[INFO ][             ffmpeg_demux_thread][ 411]: [3] demuxed    total 470 frames ---
[INFO ][          ffmpeg_dispatch_thread][ 257]: [0] dispatched total 470 frames ---
[INFO ][          ffmpeg_dispatch_thread][ 257]: [1] dispatched total 470 frames ---
[INFO ][          ffmpeg_dispatch_thread][ 257]: [2] dispatched total 470 frames ---
[INFO ][          ffmpeg_dispatch_thread][ 257]: [3] dispatched total 470 frames ---
[WARN ][ sample_get_decoded_image_thread][ 349]: [decoder  0] flow end
[WARN ][ sample_get_decoded_image_thread][ 349]: [decoder  2] flow end
[INFO ][ sample_get_decoded_image_thread][ 384]: [decoder  2] total decode 470 frames
[INFO ][ sample_get_decoded_image_thread][ 384]: [decoder  0] total decode 470 frames
[INFO ][                            main][ 193]: stop decoder 0
[WARN ][ sample_get_decoded_image_thread][ 349]: [decoder  1] flow end
[INFO ][ sample_get_decoded_image_thread][ 384]: [decoder  1] total decode 470 frames
[INFO ][ sample_get_decoded_image_thread][ 390]: [decoder  2] dfecode thread ---
[INFO ][ sample_get_decoded_image_thread][ 390]: [decoder  0] dfecode thread ---
[INFO ][ sample_get_decoded_image_thread][ 390]: [decoder  1] dfecode thread ---
[INFO ][                            main][ 198]: decoder 0 is eof
[INFO ][                            main][ 193]: stop decoder 1
[WARN ][ sample_get_decoded_image_thread][ 349]: [decoder  3] flow end
[INFO ][ sample_get_decoded_image_thread][ 384]: [decoder  3] total decode 470 frames
[INFO ][ sample_get_decoded_image_thread][ 390]: [decoder  3] dfecode thread ---
[INFO ][                            main][ 198]: decoder 1 is eof
[INFO ][                            main][ 193]: stop decoder 2
[INFO ][                            main][ 198]: decoder 2 is eof
[INFO ][                            main][ 193]: stop decoder 3
[INFO ][                            main][ 198]: decoder 3 is eof
[INFO ][                            main][ 213]: stop demuxer 0
[INFO ][                            main][ 213]: stop demuxer 1
[INFO ][                            main][ 213]: stop demuxer 2
[INFO ][                            main][ 213]: stop demuxer 3
[INFO ][                            main][ 227]: deinit vdec
[INFO ][                            main][ 231]: deinit sys
[INFO ][                            main][ 235]: axcl deinit
[INFO ][                            main][ 239]: ============== V2.16.0_20241108173111 sample exited Nov  8 2024 17:45:03 ==============
```

### transcode sample (PPL: VDEC - IVPS - VENC)

1. Load .mp4 or .h264/h265 stream file
2. Demux nalu by ffmpeg
3. Send nalu frame to VDEC
4. VDEC send decoded nv12 to IVPS (if resize)
5. IVPS send nv12 to VENC
6. Send encoded nalu frame by VENC to host.


**modules deployment**：

```bash
|-----------------------------|
|          sample             |
|-----------------------------|
|      libaxcl_ppl.so         |
|-----------------------------|
|      libaxcl_lite.so        |
|-----------------------------|
|         axcl sdk            |
|-----------------------------|
|         pcie driver         |
|-----------------------------|
```

**transcode ppl attributes**：

```bash
        attribute name                       R/W    attribute value type
 *  axcl.ppl.transcode.vdec.grp             [R  ]       int32_t                            allocated by ax_vdec.ko
 *  axcl.ppl.transcode.ivps.grp             [R  ]       int32_t                            allocated by ax_ivps.ko
 *  axcl.ppl.transcode.venc.chn             [R  ]       int32_t                            allocated by ax_venc.ko
 *
 *  the following attributes take effect BEFORE the axcl_ppl_create function is called:
 *  axcl.ppl.transcode.vdec.blk.cnt         [R/W]       uint32_t          8                depend on stream DPB size and decode mode
 *  axcl.ppl.transcode.vdec.out.depth       [R/W]       uint32_t          4                out fifo depth
 *  axcl.ppl.transcode.ivps.in.depth        [R/W]       uint32_t          4                in fifo depth
 *  axcl.ppl.transcode.ivps.out.depth       [R  ]       uint32_t          0                out fifo depth
 *  axcl.ppl.transcode.ivps.blk.cnt         [R/W]       uint32_t          4
 *  axcl.ppl.transcode.ivps.engine          [R/W]       uint32_t   AX_IVPS_ENGINE_VPP      AX_IVPS_ENGINE_VPP|AX_IVPS_ENGINE_VGP|AX_IVPS_ENGINE_TDP
 *  axcl.ppl.transcode.venc.in.depth        [R/W]       uint32_t          4                in fifo depth
 *  axcl.ppl.transcode.venc.out.depth       [R/W]       uint32_t          4                out fifo depth

NOTE:
 The value of "axcl.ppl.transcode.vdec.blk.cnt" depends on input stream.
 Usually set to dpb + 1
```

**usage**：

```bash
usage: ./axcl_sample_transcode --url=string --device=int [options] ... 
options:
  -i, --url       mp4|.264|.265 file path (string)
  -d, --device    device id (int)
      --json      axcl.json path (string [=./axcl.json])
      --loop      1: loop demux for local file  0: no loop(default) (int [=0])
      --dump      dump file path (string [=])
  -?, --help      print this message

-d: EP slot id
--json: axcl.json file path
-i: mp4|.264|.265 file path
--loop: loop to transcode local file until CTRL+C to quit
--dump: dump encoded nalu to local file
```

>
> ./axcl_sample_transcode: error while loading shared libraries: libavcodec.so.58: cannot open shared object file: No such file or directory
> if above error happens, please configure ffmpeg libraries into LD_LIBRARY_PATH.
> As for x86_x64 OS:  *export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/axcl/ffmpeg*
>

**example**：

```bash
# transcode input 1080P@30fps 264 to 1080P@30fps 265, save into /tmp/axcl/transcode.dump.pidxxx file.
./axcl_sample_transcode -i bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4  -d 129 --dump /tmp/axcl/transcode.265
[INFO ][                            main][  65]: ============== V2.16.0 sample started Nov  7 2024 16:40:05 pid 1623 ==============

[WARN ][                            main][  85]: if enable dump, disable loop automatically
[INFO ][             ffmpeg_init_demuxer][ 415]: [1623] url: bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4
[INFO ][             ffmpeg_init_demuxer][ 478]: [1623] url bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4: codec 96, 1920x1080, fps 30
[INFO ][         ffmpeg_set_demuxer_attr][ 547]: [1623] set ffmpeg.demux.file.frc to 1
[INFO ][         ffmpeg_set_demuxer_attr][ 550]: [1623] set ffmpeg.demux.file.loop to 0
[INFO ][                            main][ 173]: pid 1623: [vdec 00] - [ivps -1] - [venc 00]
[INFO ][                            main][ 191]: pid 1623: VDEC attr ==> blk cnt: 8, fifo depth: out 4
[INFO ][                            main][ 192]: pid 1623: IVPS attr ==> blk cnt: 4, fifo depth: in 4, out 0, engine 3
[INFO ][                            main][ 194]: pid 1623: VENC attr ==> fifo depth: in 4, out 4
[INFO ][          ffmpeg_dispatch_thread][ 180]: [1623] +++
[INFO ][             ffmpeg_demux_thread][ 280]: [1623] +++
[INFO ][             ffmpeg_demux_thread][ 316]: [1623] reach eof
[INFO ][             ffmpeg_demux_thread][ 411]: [1623] demuxed    total 470 frames ---
[INFO ][          ffmpeg_dispatch_thread][ 257]: [1623] dispatched total 470 frames ---
[INFO ][                            main][ 223]: ffmpeg (pid 1623) demux eof
[2024-11-07 16:51:16.541][1633][W][axclite-venc-dispatch][dispatch_thread][44]: no stream in veChn 0 fifo
[INFO ][                            main][ 240]: total transcoded frames: 470
[INFO ][                            main][ 241]: ============== V2.16.0 sample exited Nov  7 2024 16:40:05 pid 1623 ==============
```

**launch_transcode.sh**：

**launch_transcode.sh** supports to launch multi.(max. 16) axcl_sample_transcode and configure LD_LIBRARY_PATH automatically.

```bash
Usage:
./launch_transcode.sh 16 -i bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4  -d 3 --dump /tmp/axcl/transcode.265
```

>
> The 1st argument must be the number of *axcl_sample_transcode* processes. range: [1, 16]
>
