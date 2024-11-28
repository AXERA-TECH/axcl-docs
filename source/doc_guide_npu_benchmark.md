# AXCL NPU Benchmark

Benchmark 是了解硬件平台网络模型运行速度的最佳途径。以下数据基于 Raspberry Pi 5 Host 进行测试获取，仅供社区参考，不代表商业交付最终性能。

## 工况说明

- 更新时间：2024.11.22
- 工具链版本：Pulsar2 3.2-patch2
- 测试工具：axcl_run_model
- Batch Size：1 或 8
- 单位：IPS（Image/Second）

*由于不同 Host 其 memcopy、pcie 性能差异，因此 axcl_run_model 只统计网络模型在 Device 上的推理耗时*

## Vision Model

| Models       | Input Size | Batch 1(IPS) | Batch 8(IPS) |
| ------------ | ---------- | ------------ | ------------ |
| Inceptionv1  | 224        | 1073         | 2494         |
| Inceptionv3  | 224        | 478          | 702          |
| MobileNetv1  | 224        | 1508         | 4854         |
| MobileNetv2  | 224        | 1366         | 5073         |
| ResNet18     | 224        | 1066         | 2254         |
| ResNet50     | 224        | 576          | 1045         |
| SqueezeNet11 | 224        | 1560         | 5961         |
| Swin-T       | 224        | 342          | 507          |
| ViT-B/16     | 224        | 162          | 207          |
| YOLOv5s      | 640        | 326          | 394          |
| YOLOv6s      | 640        | 282          | 322          |
| YOLOv8s      | 640        | 248          | 279          |
| YOLOv9s      | 640        | 237          |              |
| YOLOv10s     | 640        | 298          |              |
| YOLOv11n     | 640        | 860          |              |
| YOLOv11s     | 640        | 305          |              |
| YOLOv11m     | 640        | 114          |              |
| YOLOv11l     | 640        | 87           |              |
| YOLOv11x     | 640        | 41           |              |

## Audio Model
| Models        | RTF  |
| ------------- | ---- |
| Whisper-Tiny  | 0.03 |
| Whisper-Small | 0.18 |
| MeloTTS       | 0.04 |

## LLM

| Models       | Prompt length（tokens） | TTFT（ms） | Generate（tokens/s) |
| ------------ | ----------------------- | ---------- | ------------------- |
| Qwen2.5-0.5B | 128                     | 188        | 28                  |

## VLM

| Models       | Input Image | Image Encoder（ms） | Prompt length（tokens） | TTFT（ms） | Generate（tokens/s) |
| ------------ | ----------- | ------------------- | ----------------------- | ---------- | ------------------- |
| InternVL2-1B | 448*448     | 4200                | 320                     | 425        | 29                  |
