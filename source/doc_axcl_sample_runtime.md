### runtime sample
1. Initialize axcl runtime by axclrtInit.
2. Active EP by axclrtSetDevice.
3. Create context by axclrtCreateDevice for main thread. (optional)
4. Create and destory thread context. (must)
5. Destory context of main thread.
6. Deactive EP by axclrtResetDevice
7. Deinitialize runtime by axclFinalize


### usage
```bash
usage: ./axcl_sample_runtime [options] ... 
options:
  -d, --device    device id (int [=0])
      --json      axcl.json path (string [=./axcl.json])
  -?, --help      print this message

-d: EP slot id, if 0, means conntect to 1st detected EP id
--json: axcl.json file path
```

### example

```bash
/opt/bin/axcl # ./axcl_sample_runtime 
[INFO ][                            main][  22]: ============== V2.15.1_20241022175101 sample started Oct 22 2024 18:04:34 ==============
[INFO ][                            main][  34]: json: ./axcl.json
[INFO ][                            main][  48]: device id: 129
[INFO ][                            main][  78]: ============== V2.15.1_20241022175101 sample exited Oct 22 2024 18:04:34 ==============
```