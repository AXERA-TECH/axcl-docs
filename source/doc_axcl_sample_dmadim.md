### sample for device DMA
1. memcpy between two device memories by AXCL_DMA_MemCopy
2. memset device memory to 0xAB by AXCL_DMA_MemCopy
3. checksum by AXCL_DMA_CheckSum
4. crop 1/4 image from (0, 0) by AXCL_DMA_MemCopyXD (AX_DMADIM_2D)

### usage
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

### example
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