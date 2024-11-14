# AXCL FAQ

## 抓取设备侧日志

**axcl_smi** 工具支持将设备侧的日志（内核和SDK的syslog，运行时库日志）抓取到Host本地，使用方法如下：

```bash
  ./axcl_smi COMMAND {OPTIONS}

  OPTIONS:

      commands
        log                               dump log from slave
      arguments for <log> command
        -d[device], --device=[device]     device, default 0
        -t[type], --type=[type]           type: -1: all, bit mask: 0x01: daemon;
                                          0x02: worker; 0x10: syslog; 0x20:
                                          kernel
        -o[output], --output=[output]     output
```

示例如下：

```bash
/opt/bin/axcl # ./axcl_smi log -t -1
command is log
log type is -1
[11-08 20:36:34:240][E][axcl_smi][main][ 117]: device id: 129
[2024-11-08 20:36:34.474][942][C][control][dump][60]: log dump finished: ./log_20241108203634.tar.gz
```

## 调整运行时库日志级别

- Host的AXCL日志默认路径: `/tmp/axcl/axcl_logs.txt`，Device侧的日志默认路径：`/opt/data/axclLog`

- Host和Device侧的AXCL 运行时库日志级别默认为`info`等级，支持通过json文件和API配置。

  - json格式

    ```
    {
    	"log": {
    		"host": {
    			"path": "/tmp/axcl/axcl_logs.txt",
    			"//   ": "0: trace, 1: debug, 2: info, 3: warn, 4: error, 5: critical, 6: off",
    			"level": 2
    		},
    		"device": {
    			"//   ": "0: trace, 1: debug, 2: info, 3: warn, 4: error, 5: critical, 6: off",
    			"level": 2
    		}
    	}
    }
    ```

    调用`axclInit`接口时，传入json的文件路径生效。

    ```c
    axclError ret = axclInit("./axcl.json");
    ```

  - `axclSetLogLevel`接口更改Host的运行时库日志

    ```c
    axclSetLogLevel(3);
    ```

  :::{Note}
  json文件支持更改Host侧的日志存放路径，日志级别以及Device侧的日志级别，而`axclSetLogLevel`接口只能动态更改Host侧的日志级别。
  :::



## 调整PCIe传输DMA内存大小

AXCL运行时库(`libaxcl_rt.so`) PCIe传输DMA内存从CMA分配，对每个进程需要3块`dma buf size`的内存，即总大小 = 3 x `dma buf size` Bytes。

默认`dma buf size`大小为4MBytes，支持通过axcl.json配置，调用`axclInit`接口生效, json格式如下：

```json
{
	"log": {
		"host": {
			"path": "/tmp/axcl/axcl_logs.txt",
			"//   ": "0: trace, 1: debug, 2: info, 3: warn, 4: error, 5: critical, 6: off",
			"level": 2
		},
		"device": {
			"//   ": "0: trace, 1: debug, 2: info, 3: warn, 4: error, 5: critical, 6: off",
			"level": 2
		}
	},
    "dma buf size": "0x200000"
}
```

如上所示，将`dma buf size`调整为2MBytes。

:::{Note}

- 应用根据实际业务需求和内存容量更改该参数，**最小大小为2MBytes**(0x200000)。
- `dma buf size` **同时**修改Host和Device的PCIe CMA缓存分配。

:::
