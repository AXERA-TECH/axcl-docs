## 系统信息

CentOS 9 镜像下载 [here](https://pan.baidu.com/s/19Sv60nAvJb97lSiYfv_39g?pwd=aa4g)

```bash
[axera@localhost ~]$ uname -a
Linux localhost.localdomain 5.14.0-522.el9.x86_64 #1 SMP PREEMPT_DYNAMIC Sun Oct 20 13:04:34 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
[axera@localhost ~]$ 
[axera@localhost ~]$ uname -r
5.14.0-522.el9.x86_64
[axera@localhost ~]$ 
[axera@localhost ~]$ cat /etc/os-release 
NAME="CentOS Stream"
VERSION="9"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="9"
PLATFORM_ID="platform:el9"
PRETTY_NAME="CentOS Stream 9"
ANSI_COLOR="0;31"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:centos:centos:9"
HOME_URL="https://centos.org/"
BUG_REPORT_URL="https://issues.redhat.com/"
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux 9"
REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
```



## 坏境搭建

1. sudo yum update  更新软件包

2. sudo yum install -y kernel-devel kernel-headers

3. 修改grub文件添加reserved cma size

   ![](https://github.com/AXERA-TECH/axcl-docs/blob/main/res/centos_grub_info.png)

   