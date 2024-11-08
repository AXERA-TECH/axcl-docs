````bash
### sample for memcpy between host and device

         HOST          |               DEVICE
      host_mem[0] -----------> dev_mem[0]
                                    |---------> dev_mem[1]
      host_mem[1] <----------------------------------|

1. alloc 2 host memories: *host_mem[2]*
2. alloc 2 device memories: *dev_mem[2]*
3. memcpy from host_mem[0] to dev_mem[0] by AXCL_MEMCPY_HOST_TO_DEVICE
4. memcpy from dev_mem[0] to dev_mem[1] by AXCL_MEMCPY_DEVICE_TO_DEVICE
5. memcpy from dev_mem[1] to host_mem[0] by AXCL_MEMCPY_DEVICE_TO_HOST
6. memcmp between host_mem[0] and host_mem[1]

### usage
```bash
usage: ./axcl_sample_memory [options] ... 
options:
  -d, --device    device id (int [=0])
      --json      axcl.json path (string [=./axcl.json])
  -?, --help      print this message

-d: EP slot id, if 0, means conntect to 1st detected EP id
--json: axcl.json file path
```

### example

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

````