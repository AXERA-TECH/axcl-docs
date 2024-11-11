### transcode sample (PPL: VDEC - IVPS - VENC)
1. Load .mp4 or .h264/h265 stream file
2. Demux nalu by ffmpeg
3. Send nalu frame to VDEC
4. VDEC send decoded nv12 to IVPS (if resize)
5. IVPS send nv12 to VENC
6. Send encoded nalu frame by VENC to host.


### modules deployment
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

### transcode ppl attributes
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
### usage
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
--dump: dump encoded nalu
```

> [!NOTE]
>
> ./axcl_sample_transcode: error while loading shared libraries: libavcodec.so.58: cannot open shared object file: No such file or directory
> if above error happens, please configure ffmpeg libraries into LD_LIBRARY_PATH.
> As for x86_x64 OS:  *export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/axcl/ffmpeg*

### example

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

### launch_transcode.sh

**launch_transcode.sh** supports to launch multi.(max. 16) axcl_sample_transcode and configure LD_LIBRARY_PATH automatically.

```bash
Usage:
launch_transcode.sh 16 -i bangkok_30952_1920x1080_30fps_gop60_4Mbps.mp4  -d 3 --dump /tmp/axcl/transcode.265
```

> [!NOTE]
>
> The 1st argument must be the number of *axcl_sample_transcode* processes. range: [1, 16]