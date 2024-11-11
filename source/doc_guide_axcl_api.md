# AXCL API

## 概览
`AXCL API` 分为两部分，第一部分是 `Runtime API`，第二部分是 `Native API`。其中 `Runtime API` 是独立的 `API` 组合，目前仅包含用于内存管理的 `Memory` 和用于驱动 `爱芯通元(TM)` `NPU` 工作的 `Engine API`。当 `AXCL API` 被用于计算卡形态，不使用编解码功能时，只使用 `Runtime API` 即可完成全部计算任务。当需要使用编解码功能时，需要了解 `Native API` 及 `FFMPEG` 模块的有关内容。

## Runtime API
使用 `Runtime API` 可以在宿主系统上调用 `NPU` 完成计算功能，其中 `Memory API` 可以分别在宿主和计算卡上申请释放内存空间，`Engine API` 可以完成模型初始化、`IO` 设置到推理的全部 `NPU` 功能。

### Runtime API

#### [axclInit](#axclInit)

```c
axclError axclInit(const char *config);
```

**使用说明**：

系统初始化，用户需要在调用AXCL API之前调用此函数。

**参数**：

- `config [IN]`：指定json配置文件路径。用户可以通过json配置文件配置系统参数，目前支持日志级别，格式[参阅FAQ](https://github.com/AXERA-TECH/axcl-docs/wiki/0.FAQ#how-to-configure-runtime-log--level)。

**限制**：

和[`axclFinalize`](#axclFinalize)成对调用对系统清理。

#### [axclFinailze](#axclFinalize)

```c
axclError axclFinalize();
```

**使用说明**：

系统去初始化。

**限制**：

和[`axclInit`](#axclInit)成对调用。

#### [axclrtGetVersion](#axclrtGetVersion)

```c
axclError axclrtGetVersion(int32_t *major, int32_t *minor, int32_t *patch);
```

**使用说明**：

获取runtime版本号。

**参数**：

- `major [OUT]`：主版本号。
- `minor[OUT]`：子版本号。
- `patch [OUT]`：patch版本号。

**限制**：

无特别限制。

#### [axclrtGetSocName](#axclrtGetSocName)

```c
const char *axclrtGetSocName();
```

**使用说明**：

返回SOC名。

**限制**：

无特别限制。

#### [axclrtSetDevice](#axclrtSetDevice)

```c
axclError axclrtSetDevice(int32_t deviceId);
```

**使用说明**：

切换并激活设备。

**参数**：

- `deviceId [IN]`：设备ID。

**限制**：

- [`axclrtSetDevice`](#axclrtSetDevice)内部将创建一个默认的运行上下文，该默认上下文由系统在[`axclrtResetDevice`](#axclrtResetDevice)自动回收，不能调用[`axclrtDestroyContext`](#axclrtDestroyContext)显示回收。
- 和[`axclrtResetDevice`](#axclrtResetDevice)成对使用。

#### [axclrtResetDevice](#axclrtResetDevice)

```c
axclError axclrtResetDevice(int32_t deviceId);
```

**使用说明**：

去激活设备。

**参数**：

- `deviceId [IN]`：设备ID。

**限制**：

和[`axclrtSetDevice`](#axclrtSetDevice)成对使用，系统将自动回收默认的上下文资源。

#### [axclrtGetDevice](#axclrtGetDevice)

```c
axclError axclrtGetDevice(int32_t *deviceId);
```

**使用说明**：

获取当前激活的设备ID。

**参数**：

- `deviceId [OUT]`：设备ID。

**限制**：

至少调用[`axclrtSetDevice`](#axclrtSetDevice)激活一个设备。

#### [axclrtGetDeviceCount](#axclrtGetDeviceCount)

```c
axclError axclrtGetDeviceCount(uint32_t *count);
```

**使用说明**：

获取连接的设备总个数。

**参数**：

- `count [OUT]`：设备个数。

**限制**：

无特别限制。

#### [axclrtGetDeviceList](#axclrtGetDeviceList)

```c
axclError axclrtGetDeviceList(axclrtDeviceList *deviceList);
```

**使用说明**：

获取全部连接的设备ID。

**参数**：

- `deviceList[OUT]`：全部连接的设备ID信息。

**限制**：

无特别限制。

#### [axclrtSynchronizeDevice](#axclrtSynchronizeDevice)

```c
axclError axclrtSynchronizeDevice();
```

**使用说明**：

同步执行当前设备的全部任务。

**限制**：

至少激活一个设备。

#### [axclrtGetDeviceUtilizationRate](#axclrtGetDeviceUtilizationRate)

```c
axclError axclrtGetDeviceUtilizationRate(int32_t deviceId, axclrtUtilizationInfo *utilizationInfo);
```

**使用说明**：

获取设备CPU、NPU和内存信息，**此接口暂未实现**。

**限制**：

需要先激活设备。

#### [axclrtCreateContext](#axclrtCreateContext)

```c
axclError axclrtCreateContext(axclrtContext *context, int32_t deviceId);
```

**使用说明**：

在指定设备创建运行上下文。

**参数**：

- `context [OUT]`：创建的上下文句柄。
- `deviceId [IN]`：设备Id。

**限制**：

- 用户创建的子线程若需要调用AXCL API，需要调用此接口显示创建运行上下文。
- 若deviceId设备未被激活，本接口内部将首先激活设备。
- 与[`axclrtDestroyContext`](#axclrtDestroyContext)成对调用清理上下文资源。

#### [axclrtDestroyContext](#axclrtDestroyContext)

```c
axclError axclrtDestroyContext(axclrtContext context);
```

**使用说明**：

清理创建的运行上下文。

**参数**：

- `context [IN]`：创建的上下文句柄。

**限制**：

- 与[`axclrtCreateContext`](#axclrtCreateContext)成对调用清理显示创建的上下文资源。
- 无法删除由[`axclrtSetDevice`](#axclrtSetDevice)内部创建的默认的运行上下文资源。

#### [axclrtSetCurrentContext](#axclrtSetCurrentContext)

```c
axclError axclrtSetCurrentContext(axclrtContext context);
```

**使用说明**：

显示设置当前显示的执行上下文。

**参数**：

- `context [IN]`：创建的上下文句柄。

**限制**：

- 多次调用本函数，则当前线程的上下文由最后一次调用的上下文为准。

#### [axclrtGetCurrentContext](#axclrtGetCurrentContext)

```c
axclError axclrtGetCurrentContext(axclrtContext *context);
```

**使用说明**：

获取当前的运行上下文句柄。

**参数**：

- `context [OUT]`：当前的上下文句柄。

**限制**：

- 当前线程需要执行[`axclrtSetCurrentContext`](#axclrtSetCurrentContext)或者[`axclrtCreateContext`](#axclrtCreateContext)设置或显示创建上下文后才能获取。

### Memory API


### Engine API

#### [axclrtEngineInit](#axclrtengineinit)
```c
axclError axclrtEngineInit(axclrtEngineVNpuKind npuKind);
```
**使用说明**：

此函数用于初始化 `Runtime Engine`。用户需要在使用 `Runtime Engine` 之前调用此函数。

**参数**：

- `npuKind [IN]`：指定要初始化的 `VNPU` 类型。

**限制**：

用户在使用完 `Runtime Engine` 后，需要调用 [`axclrtEngineFinalize`](#axclrtEngineFinalize) 来完成 `Runtime Engine` 的清理工作。

---

#### [axclrtEngineGetVNpuKind](#axclrtenginegetvnpukind)
```c
axclError axclrtEngineGetVNpuKind(axclrtEngineVNpuKind *npuKind);
```
**使用说明**：

此函数用于获取 `Runtime Engine` 初始化的 `VNPU` 类型。  

**参数**：
- `npuKind [OUT]`：返回 `VNPU` 类型。

**限制**：

用户必须在调用此函数之前调用 [`axclrtEngineInit`](#axclrtengineinit) 来初始化 `Runtime Engine`。

---

#### [axclrtEngineFinalize](#axclrtenginefinalize)
```c
axclError axclrtEngineFinalize();
```
**使用说明**：

此函数用于完成 `Runtime Engine` 的清理工作。用户在完成所有操作后需要调用此函数。  

**限制**：

用户必须在调用此函数之前调用 [`axclrtEngineInit`](#axclrtengineinit) 来初始化 `Runtime Engine`。

---

#### [axclrtEngineLoadFromFile](#axclrtengineloadfromfile)
```c
axclError axclrtEngineLoadFromFile(const char *modelPath, uint64_t *modelId);
```
**使用说明**：

此函数从文件加载模型数据，创建模型 `ID`。  

**参数**：
- `modelPath [IN]`：离线模型文件的存储路径。
- `modelId [OUT]`：加载模型后生成的模型 `ID` ，用于后续操作的标识。

**限制**：

用户必须在调用此函数之前调用 [`axclrtEngineInit`](#axclrtengineinit) 来初始化 `Runtime Engine`。

---

#### [axclrtEngineLoadFromMem](#axclrtengineloadfrommem)
```c
axclError axclrtEngineLoadFromMem(const void *model, uint64_t modelSize, uint64_t *modelId);
```
**使用说明**：

此函数从内存加载离线模型数据，并由系统内部管理模型运行的内存。  

**参数**：
- `model [IN]`：存储在内存中的模型数据。
- `modelSize [IN]`：模型数据的大小。
- `modelId [OUT]`：加载模型后生成的模型 `ID` ，用于后续操作的标识。

**限制**：

模型内存必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineUnload](#axclrtengineunload)
```c
axclError axclrtEngineUnload(uint64_t modelId);
```
**使用说明**：

此函数用于卸载指定模型 `ID`  的模型。  

**参数**：
- `modelId [IN]`：要卸载的模型 `ID` 。

**限制**：

无特别限制。

---

#### [axclrtEngineGetModelCompilerVersion](#axclrtenginegetmodelcompilerversion)
```c
const char* axclrtEngineGetModelCompilerVersion(uint64_t modelId);
```
**使用说明**：

此函数用于获取模型构建工具链的版本。  

**参数**：
- `modelId [IN]`：模型 `ID` 。

**限制**：

无特别限制。

---

#### [axclrtEngineSetAffinity](#axclrtenginesetaffinity)
```c
axclError axclrtEngineSetAffinity(uint64_t modelId, axclrtEngineSet set);
```
**使用说明**：

此函数用于设置模型的 NPU 亲和性。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `set [OUT]`：设置的亲和性集。

**限制**：

不允许为零，设置的掩码位不能超出亲和性范围。

---

#### [axclrtEngineGetAffinity](#axclrtenginegetaffinity)
```c
axclError axclrtEngineGetAffinity(uint64_t modelId, axclrtEngineSet *set);
```
**使用说明**：

此函数用于获取模型的 NPU 亲和性。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `set [OUT]`：返回的亲和性集。

**限制**：

无特别限制。

---

#### [axclrtEngineGetUsage](#axclrtenginegetusage)
```c
axclError axclrtEngineGetUsage(const char *modelPath, int64_t *sysSize, int64_t *cmmSize);
```
**使用说明**：

此函数根据模型文件获取模型执行所需的系统内存大小和 CMM 内存大小。  

**参数**：
- `modelPath [IN]`：用于获取内存信息的模型路径。
- `sysSize [OUT]`：执行模型所需的工作系统内存大小。
- `cmmSize [OUT]`：执行模型所需的 CMM 内存大小。

**限制**：

无特别限制。

---

#### [axclrtEngineGetUsageFromMem](#axclrtenginegetusagefrommem)
```c
axclError axclrtEngineGetUsageFromMem(const void *model, uint64_t modelSize, int64_t *sysSize, int64_t *cmmSize);
```
**使用说明**：

此函数根据模型数据在内存中获取模型执行所需的系统内存大小和 CMM 内存大小。  

**参数**：
- `model [IN]`：用户管理的模型内存。
- `modelSize [IN]`：模型数据大小。
- `sysSize [OUT]`：执行模型所需的工作系统内存大小。
- `cmmSize [OUT]`：执行模型所需的 CMM 内存大小。

**限制**：

模型内存必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineGetUsageFromModelId](#axclrtenginegetusagefrommodelid)
```c
axclError axclrtEngineGetUsageFromModelId(uint64_t modelId, int64_t *sysSize, int64_t *cmmSize);
```
**使用说明**：

此函数根据模型 `ID`  获取模型执行所需的系统内存大小和 CMM 内存大小。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `sysSize [OUT]`：执行模型所需的工作系统内存大小。
- `cmmSize [OUT]`：执行模型所需的 CMM 内存大小。

**限制**：

无特别限制。

---

#### [axclrtEngineGetModelType](#axclrtenginegetmodeltype)
```c
axclError axclrtEngineGetModelType(const char *modelPath, axclrtEngineModelKind *modelType);
```
**使用说明**：

此函数根据模型文件获取模型类型。  

**参数**：
- `modelPath [IN]`：用于获取模型类型的模型路径。
- `modelType [OUT]`：返回的模型类型。

**限制**：

无特别限制。

---

#### [axclrtEngineGetModelTypeFromMem](#axclrtenginegetmodeltypefrommem)
```c
axclError axclrtEngineGetModelTypeFromMem(const void *model, uint64_t modelSize, axclrtEngineModelKind *modelType);
```
**使用说明**：

此函数根据内存中的模型数据获取模型类型。  

**参数**：
- `model [IN]`：用户管理的模型内存。
- `modelSize [IN]`：模型数据大小。
- `modelType [OUT]`：返回的模型类型。

**限制**：

模型内存必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineGetModelTypeFromModelId](#axclrtenginegetmodeltypefrommodelid)
```c
axclError axclrtEngineGetModelTypeFromModelId(uint64_t modelId, axclrtEngineModelKind *modelType);
```
**使用说明**：

此函数根据模型 `ID`  获取模型类型。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `modelType [OUT]`：返回的模型类型。

**限制**：

无特别限制。

---

#### [axclrtEngineGetIOInfo](#axclrtenginegetioinfo)
```c
axclError axclrtEngineGetIOInfo(uint64_t modelId, axclrtEngineIOInfo *ioInfo);
```
**使用说明**：

此函数根据模型 `ID`  获取模型的 IO 信息。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `ioInfo [OUT]`：返回的 axclrtEngineIOInfo 指针。

**限制**：

用户在模型 `ID` 销毁前应调用 `axclrtEngineDestroyIOInfo` 来释放 `axclrtEngineIOInfo`。

---

#### [axclrtEngineDestroyIOInfo](#axclrtenginedestroyioinfo)
```c
axclError axclrtEngineDestroyIOInfo(axclrtEngineIOInfo ioInfo);
```
**使用说明**：

此函数用于销毁类型为 `axclrtEngineIOInfo` 的数据。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。

**限制**：

无特别限制。

---

#### [axclrtEngineGetShapeGroupsCount](#axclrtenginegetshapegroupscount)
```c
axclError axclrtEngineGetShapeGroupsCount(axclrtEngineIOInfo ioInfo, int32_t *count);
```
**使用说明**：

此函数用于获取 IO 形状组的数量。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `count [OUT]`：形状组的数量。

**限制**：

Pulsar2 工具链可以在模型转换时指定多个形状。普通模型只有一个形状，因此对于正常转换的模型，调用此函数没有必要。

---

#### [axclrtEngineGetNumInputs](#axclrtenginegetnuminputs)
```c
uint32_t axclrtEngineGetNumInputs(axclrtEngineIOInfo ioInfo);
```
**使用说明**：

此函数根据 `axclrtEngineIOInfo` 数据获取模型的输入数量。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。

**限制**：

无特别限制。

---

#### [axclrtEngineGetNumOutputs](#axclrtenginegetnumoutputs)
```c
uint32_t axclrtEngineGetNumOutputs(axclrtEngineIOInfo ioInfo);
```
**使用说明**：

此函数根据 `axclrtEngineIOInfo` 数据获取模型的输出数量。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。

**限制**：

无特别限制。

---

#### [axclrtEngineGetInputSizeByIndex](#axclrtenginegetinputsizebyindex)
```c
uint64_t axclrtEngineGetInputSizeByIndex(axclrtEngineIOInfo ioInfo, uint32_t group, uint32_t index);
```
**使用说明**：

此函数根据 `axclrtEngineIOInfo` 数据获取指定输入的大小。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `group [IN]`：输入形状组索引。
- `index [IN]`：要获取的输入大小的索引值，从 0 开始。

**限制**：

无特别限制。

---

#### [axclrtEngineGetOutputSizeByIndex](#axclrtenginegetoutputsizebyindex)
```c
uint64_t axclrtEngineGetOutputSizeByIndex(axclrtEngineIOInfo ioInfo, uint32_t group, uint32_t index);
```
**使用说明**：

此函数根据 `axclrtEngineIOInfo` 数据获取指定输出的大小。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `group [IN]`：输出形状组索引。
- `index [IN]`：要获取的输出大小的索引值，从 0 开始。

**限制**：

无特别限制。

---

#### [axclrtEngineGetInputNameByIndex](#axclrtenginegetinputnamebyindex)
```c
const char *axclrtEngineGetInputNameByIndex(axclrtEngineIOInfo ioInfo, uint32_t index);
```
**使用说明**：

此函数获取指定输入的名称。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `index [IN]`：输入 IO 索引。

**限制**：

返回的输入张量名称与 `ioInfo` 的生命周期相同。

---

#### [axclrtEngineGetOutputNameByIndex](#axclrtenginegetoutputnamebyindex)
```c
const char *axclrtEngineGetOutputNameByIndex(axclrtEngineIOInfo ioInfo, uint32_t index);
```
**使用说明**：

此函数获取指定输出的名称。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `index [IN]`：输出 IO 索引。

**限制**：

返回的输出张量名称与 `ioInfo` 的生命周期相同。

---

#### [axclrtEngineGetInputIndexByName](#axclrtenginegetinputindexbyname)
```c
int32_t axclrtEngineGetInputIndexByName(axclrtEngineIOInfo ioInfo, const char *name);
```
**使用说明**：

此函数根据输入张量的名称获取输入索引。  

**参数**：
- `ioInfo [IN]`：模型描述。
- `name [IN]`：输入张量名称。

**限制**：

无特别限制。

---

#### [axclrtEngineGetOutputIndexByName](#axclrtenginegetoutputindexbyname)
```c
int32_t axclrtEngineGetOutputIndexByName(axclrtEngineIOInfo ioInfo, const char *name);
```
**使用说明**：

此函数根据输出张量的名称获取输出索引。  

**参数**：
- `ioInfo [IN]`：模型描述。
- `name [IN]`：输出张量名称。

**限制**：

无特别限制。

---

#### [axclrtEngineGetInputDims](#axclrtenginegetinputdims)
```c
axclError axclrtEngineGetInputDims(axclrtEngineIOInfo ioInfo, uint32_t group, uint32_t index, axclrtEngineIODims *dims);
```
**使用说明**：

此函数获取指定输入的维度信息。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `group [IN]`：输入形状组索引。
- `index [IN]`：输入张量索引。
- `dims [OUT]`：返回的维度信息。

**限制**：

`axclrtEngineIODims` 的存储空间是用户申请的，用户在模型 `axclrtEngineIOInfo` 销毁前应释放 `axclrtEngineIODims`。

---

#### [axclrtEngineGetOutputDims](#axclrtenginegetoutputdims)
```c
axclError axclrtEngineGetOutputDims(axclrtEngineIOInfo ioInfo, uint32_t group, uint32_t index, axclrtEngineIODims *dims);
```
**使用说明**：

此函数获取指定输出的维度信息。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `group [IN]`：输出形状组索引。
- `index [IN]`：输出张量索引。
- `dims [OUT]`：返回的维度信息。

**限制**：

`axclrtEngineIODims` 的存储空间是用户申请的，用户在模型 `axclrtEngineIOInfo` 销毁前应释放 `axclrtEngineIODims`。

---

#### [axclrtEngineCreateIO](#axclrtenginecreateio)
```c
axclError axclrtEngineCreateIO(axclrtEngineIOInfo ioInfo, axclrtEngineIO *io);
```
**使用说明**：

此函数创建类型为 `axclrtEngineIO` 的数据。  

**参数**：
- `ioInfo [IN]`：axclrtEngineIOInfo 指针。
- `io [OUT]`：创建的 axclrtEngineIO 指针。

**限制**：

用户在模型 `ID` 销毁前应调用 `axclrtEngineDestroyIO` 来释放 `axclrtEngineIO`。

---

#### [axclrtEngineDestroyIO](#axclrtenginedestroyio)
```c
axclError axclrtEngineDestroyIO(axclrtEngineIO io);
```
**使用说明**：

此函数用于销毁类型为 `axclrtEngineIO` 的数据。  

**参数**：
- `io [IN]`：要销毁的 axclrtEngineIO 指针。

**限制**：

无特别限制。

---

#### [axclrtEngineSetInputBufferByIndex](#axclrtenginesetinputbufferbyindex)
```c
axclError axclrtEngineSetInputBufferByIndex(axclrtEngineIO io, uint32_t index, const void *dataBuffer, uint64_t size);
```
**使用说明**：

此函数通过 IO 索引设置输入数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `index [IN]`：输入张量索引。
- `dataBuffer [IN]`：要添加的数据缓冲区地址。
- `size [IN]`：数据缓冲区大小。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineSetOutputBufferByIndex](#axclrtenginesetoutputbufferbyindex)
```c
axclError axclrtEngineSetOutputBufferByIndex(axclrtEngineIO io, uint32_t index, const void *dataBuffer, uint64_t size);
```
**使用说明**：

此函数通过 IO 索引设置输出数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `index [IN]`：输出张量索引。
- `dataBuffer [IN]`：要添加的数据缓冲区地址。
- `size [IN]`：数据缓冲区大小。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineSetInputBufferByName](#axclrtenginesetinputbufferbyname)
```c
axclError axclrtEngineSetInputBufferByName(axclrtEngineIO io, const char *name, const void *dataBuffer, uint64_t size);
```
**使用说明**：

此函数通过 IO 名称设置输入数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `name [IN]`：输入张量名称。
- `dataBuffer [IN]`：要添加的数据缓冲区地址。
- `size [IN]`：数据缓冲区大小。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineSetOutputBufferByName](#axclrtenginesetoutputbufferbyname)
```c
axclError axclrtEngineSetOutputBufferByName(axclrtEngineIO io, const char *name, const void *dataBuffer, uint64_t size);
```
**使用说明**：

此函数通过 IO 名称设置输出数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `name [IN]`：输出张量名称。
- `dataBuffer [IN]`：要添加的数据缓冲区地址。
- `size [IN]`：数据缓冲区大小。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineGetInputBufferByIndex](#axclrtenginegetinputbufferbyindex)
```c
axclError axclrtEngineGetInputBufferByIndex(axclrtEngineIO io, uint32_t index, void **dataBuffer, uint64_t *size);
```
**使用说明**：

此函数通过 IO 索引获取输入数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `index [IN]`：输入张量索引。
- `dataBuffer [OUT]`：数据缓冲区地址。
- `size [IN]`：数据缓冲区大小。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineGetOutputBufferByIndex](#axclrtenginegetoutputbufferbyindex)
```c
axclError axclrtEngineGetOutputBufferByIndex(axclrtEngineIO io, uint32_t index, void **dataBuffer, uint64_t *size);
```
**使用说明**：

此函数通过 IO 索引获取输出数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `index [IN]`：输出张量索引。
- `dataBuffer [OUT]`：数据缓冲区地址。
- `size [IN]`：数据缓冲区大小。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineGetInputBufferByName](#axclrtenginegetinputbufferbyname)
```c
axclError axclrtEngineGetInputBufferByName(axclrtEngineIO io, const char *name, void **dataBuffer, uint64_t *size);
```
**使用说明**：

此函数通过 IO 名称获取输入数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `name [IN]`：输入张量名称。
- `dataBuffer [OUT]`：数据缓冲区地址。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineGetOutputBufferByName](#axclrtenginegetoutputbufferbyname)
```c
axclError axclrtEngineGetOutputBufferByName(axclrtEngineIO io, const char *name, void **dataBuffer, uint64_t *size);
```
**使用说明**：

此函数通过 IO 名称获取输出数据缓冲区。  

**参数**：
- `io [IN]`：axclrtEngineIO 数据缓冲区的地址。
- `name [IN]`：输出张量名称。
- `dataBuffer [OUT]`：数据缓冲区地址。

**限制**：

数据缓冲区必须是设备内存，用户需要自行管理和释放。

---

#### [axclrtEngineSetDynamicBatchSize](#axclrtenginesetdynamicbatchsize)
```c
axclError axclrtEngineSetDynamicBatchSize(axclrtEngineIO io, uint32_t batchSize);
```
**使用说明**：

此函数在动态批处理场景中设置一次处理的图像数量。  

**参数**：
- `io [IN]`：模型推理的 IO。
- `batchSize [IN]`：一次处理的图像数量。

**限制**：

无特别限制。

---

#### [axclrtEngineCreateContext](#axclrtenginecreatecontext)
```c
axclError axclrtEngineCreateContext(uint64_t modelId, uint64_t *contextId);
```
**使用说明**：

此函数为模型 `ID`  创建一个模型运行环境上下文。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `contextId [OUT]`：创建的上下文 `ID` 。

**限制**：

一个模型 `ID`  可以创建多个运行上下文，每个上下文仅在其自己的设置和内存空间中运行。

---

#### [axclrtEngineExecute](#axclrtengineexecute)
```c
axclError axclrtEngineExecute(uint64_t modelId, uint64_t contextId, uint32_t group, axclrtEngineIO io);
```
**使用说明**：

此函数执行模型的同步推理，直到返回推理结果。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `contextId [IN]`：模型推理上下文。
- `group [IN]`：模型形状组索引。
- `io [IN]`：模型推理的 IO。

**限制**：

无特别限制。

---

#### [axclrtEngineExecuteAsync](#axclrtengineexecuteasync)
```c
axclError axclrtEngineExecuteAsync(uint64_t modelId, uint64_t contextId, uint32_t group, axclrtEngineIO io, axclrtStream stream);
```
**使用说明**：

此函数执行模型的异步推理，直到返回推理结果。  

**参数**：
- `modelId [IN]`：模型 `ID` 。
- `contextId [IN]`：模型推理上下文。
- `group [IN]`：模型形状组索引。
- `io [IN]`：模型推理的 IO。
- `stream [IN]`：流。

**限制**：

无特别限制。
