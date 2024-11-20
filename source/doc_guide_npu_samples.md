# AXCL NPU 示例

## AXCL-Samples

AXCL-Samples 由 爱芯元智 主导开发。该项目实现了常见的深度学习开源算法在基于 爱芯元智 的 SoC 实现的 PCIE算力卡 产品上的运行的示例代码，方便社区开发者进行快速评估和适配。

- [axcl-samples](https://github.com/AXERA-TECH/axcl-samples)；
- 该仓库采用最简单的方式展示常用的开源模型，例如 Ultralytics 的 YOLO 系列，DepthAnything，YOLO-Worldv2 等等。

### 获取示例

- AXCL-Samples 的预编译 ModelZoo 请参考
  - [百度网盘](https://pan.baidu.com/s/1cnMeqsD-hErlRZlBDDvuoA?pwd=oey4)

### DepthAnything 运行

```
axera@raspberrypi:~/temp/axcl-samples/build $ ./install/bin/ax_depth_anything -m depth_anything.axmodel -i ssd_horse.jpg
--------------------------------------
model file : depth_anything.axmodel
image file : ssd_horse.jpg
img_h, img_w : 384 640
--------------------------------------
input size: 1
    name:    image [unknown] [unknown]
        1 x 384 x 640 x 3


output size: 1
    name:    depth
        1 x 1 x 384 x 640

==================================================

Engine push input is done.
post process cost time:4.43 ms
--------------------------------------
Repeat 1 times, avg time 44.02 ms, max_time 44.02 ms, min_time 44.02 ms
--------------------------------------
```
![](../res/depth_anything_out.png)

## LLM 示例

- 模型转请参考[大模型编译文档](https://pulsar2-docs.readthedocs.io/zh-cn/latest/appendix/build_llm.html)
- 预编译 ModelZoo-LLM 请参考[百度网盘](https://pan.baidu.com/s/1grJNjcpUln-fDBisJxuvCA?pwd=mys8)

### Tokenizer 解析器

**tokenizer 解析准备**

为了更方便、更准确的进行 LLM DEMO 展示，我们采用 transformers 内置的 tokenizer 解析服务，因此需要安装 python 环境和 transformers 库

安装 miniconda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
chmod a+x Miniconda3-latest-Linux-aarch64.sh
./Miniconda3-latest-Linux-aarch64.sh
```

启用 python 环境

```
conda create --name axcl python=3.9
conda activate axcl
```

安装 transformers

```
pip install transformers==4.41.1 -i https://mirrors.aliyun.com/pypi/simple
```

### Qwen2.5

拷贝相关文件到 Host

**文件说明**

```
(base) axera@raspberrypi:~/qwen2.5-0.5b-prefill-ax650 $ tree
.
├── main_pcie_prefill
├── qwen2.5-0.5B-prefill-ax650
│   ├── model.embed_tokens.weight.bfloat16.bin
│   ├── qwen2_p128_l0_together.axmodel
│   ├── qwen2_p128_l10_together.axmodel
......
│   ├── qwen2_p128_l8_together.axmodel
│   ├── qwen2_p128_l9_together.axmodel
│   └── qwen2_post.axmodel
├── qwen2.5_tokenizer
│   ├── merges.txt
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   └── vocab.json
├── qwen2.5_tokenizer.py
└── run_qwen2.5_0.5B_prefill_pcie.sh
```

**启动 tokenizer 解析器**

运行 tokenizer 服务，Host ip 默认为 localhost，端口号设置为 12345，正在运行后信息如下

```
(axcl) axera@raspberrypi:~/qwen2.5-0.5b-prefill-ax650 $ python qwen2.5_tokenizer.py --port 12345
None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
None None 151645 <|im_end|>
<|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>
<|im_start|>user
hello world<|im_end|>
<|im_start|>assistant

[151644, 8948, 198, 2610, 525, 1207, 16948, 11, 3465, 553, 54364, 14817, 13, 1446, 525, 264, 10950, 17847, 13, 151645, 198, 151644, 872, 198, 14990, 1879, 151645, 198, 151644, 77091, 198]
http://localhost:12345
```

**运行 Qwen 2.5**

```
(base) axera@raspberrypi:~/qtang/llama_axera_cpp $ ./run_qwen2_0.5B_prefill_pcie.sh
[I][                            Init][ 129]: LLM init start
  7% | ███                               |   2 /  27 [1.30s<17.54s, 1.54 count/s] embed_selector init okcat: /proc/ax_proc/mem_cmm_info: No such file or directory
 11% | ████                              |   3 /  27 [1.75s<15.74s, 1.72 count/s] init 0 axmodel ok,remain_cmm(-1 MB)cat: /proc/ax_proc/mem_cmm_info: No such file or directory
......
 96% | ███████████████████████████████   |  26 /  27 [7.34s<7.62s, 3.54 count/s] init 23 axmodel ok,remain_cmm(-1 MB)cat: /proc/ax_proc/mem_cmm_info: No such file or directory
100% | ████████████████████████████████ |  27 /  27 [12.84s<12.84s, 2.10 count/s] init post axmodel ok,remain_cmm(-1 MB)
[I][                            Init][ 253]: max_token_len : 1023
[I][                            Init][ 258]: kv_cache_size : 128, kv_cache_num: 1023
[I][                            Init][ 266]: prefill_token_num : 128
[I][                            Init][ 348]: LLM init ok
Type "q" to exit, Ctrl+c to stop current running
>> 你是谁？
[I][                             Run][ 511]: ttft: 128.70 ms
我是来自阿里云的大规模语言模型，我叫通义千问。
[N][                             Run][ 636]: hit eos,avg 26.44 token/s

>> 深圳在哪里？
[I][                             Run][ 511]: ttft: 128.96 ms
深圳位于中国广东省，是中国的经济中心之一。
[N][                             Run][ 636]: hit eos,avg 25.89 token/s

>> q

```

### InternVL2-1B

拷贝相关文件到 Host 

**文件说明**

```
(axcl) axera@raspberrypi:~/internvl2-1b-448-ax650 $ tree
.
├── internvl2_tokenizer
│   ├── added_tokens.json
│   ├── merges.txt
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── vocab.json
├── internvl2_tokenizer_448.py
├── internvl_448
│   ├── intervl_vision_part_448.axmodel
│   ├── model.embed_tokens.weight.bfloat16.bin
│   ├── qwen2_p320_l0_together.axmodel
......
│   ├── qwen2_p320_l9_together.axmodel
│   └── qwen2_post.axmodel
├── main_internvl
├── main_internvl_pcie
├── run_internvl2_448_ax650.sh
└── run_internvl2_448_pcie.sh
```

**启动 tokenizer 解析器**

运行 tokenizer 服务，Host ip 默认为 localhost，端口号设置为 12345，正在运行后信息如下

```
(axcl_test) axera@raspberrypi:~/internvl2-1b-448-ax650 $ python internvl2_tokenizer_448.py --port 12345
None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
None None 151645 <|im_end|>
[151644, 8948, 198, 56568, 104625, 100633, 104455, 104800, 101101, 32022, ...... 5501, 7512, 279, 2168, 19620, 13, 151645, 151644, 77091, 198]
310
[151644, 8948, 198, 56568, 104625, 100633, 104455, 104800, 101101, 32022, ......151645, 151644, 77091, 198]
http://localhost:12345
```

**运行 InternVL2-1B**

测试图片

![](../res/ssd_car.jpg)

输出信息

```
(base) axera@raspberrypi:~/internvl2-1b-448-ax650 $ ./run_internvl2_448_pcie.sh
[I][                            Init][ 135]: LLM init start
bos_id: -1, eos_id: 151645
  7% | ███                               |   2 /  27 [0.95s<12.82s, 2.11 count/s] embed_selector init okcat: /proc/ax_proc/mem_cmm_info: No such file or directory
 11% | ████                              |   3 /  27 [1.40s<12.61s, 2.14 count/s] init 0 axmodel ok,remain_cmm(-1 MB)cat: /proc/ax_proc/mem_cmm_info: No such file or directory
......
100% | ████████████████████████████████ |  27 /  27 [8.99s<8.99s, 3.00 count/s] init post axmodel ok,remain_cmm(-1 MB)
[I][                            Init][ 292]: max_token_len : 1023
[I][                            Init][ 297]: kv_cache_size : 128, kv_cache_num: 1023
[I][                            Init][ 305]: prefill_token_num : 320
[I][                            Init][ 307]: vpm_height : 448,vpm_width : 448
[I][                            Init][ 389]: LLM init ok
Type "q" to exit, Ctrl+c to stop current running
prompt >> who are you?
image >>
[I][                             Run][ 626]: ttft: 425.78 ms
I am an AI assistant whose name is InternVL, developed jointly by Shanghai AI Lab and SenseTime.
[N][                             Run][ 751]: hit eos,avg 29.24 token/s

prompt >> 图片中有什么?
image >> ./ssd_car.jpg
[I][                          Encode][ 468]: image encode time : 4202.367188 ms, size : 229376
[I][                             Run][ 626]: ttft: 425.97 ms
这张图片展示了一辆红色的双层巴士，巴士上有一个广告，广告上写着“THINGS GET MORE EXCITING WHEN YOU SAY YES”（当你说“是”时，事情会变得更加有趣）。巴士停在城市街道的一侧，街道两旁有建筑物和行人。图片中还有一位穿着黑色外套的女士站在巴士前微笑。
[N][                             Run][ 751]: hit eos,avg 29.26 token/s

prompt >> q
(base) axera@raspberrypi:~/internvl2-1b-448-ax650 $ 
```

## 音频大模型

本章节展示常用的 ASR（自动语音识别）、TTS（文本转语音）模型示例。

### Whisper

- 本小节只指导如何在 Raspberry Pi 5 上运行预编译好的基于 Whipser Small 的语音转文字示例；
- 模型转换、示例源码编译请参考 [whisper.axcl](https://github.com/ml-inory/whisper.axcl)。

**文件说明**

**运行 Whisper**

### MeloTTS

- 本小节只指导如何在 Raspberry Pi 5 上运行预编译好的 MeloTTS 文字转语音示例；
- 模型转换、示例源码编译请参考 [melotts.axcl](https://github.com/ml-inory/melotts.axcl)。

**文件说明**

**运行 MeloTTS**

