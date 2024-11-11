## 系统信息

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



## 环境搭建

1. sudo yum update  更新软件包

2. sudo yum install -y kernel-devel kernel-headers

3. 修改grub文件添加reserved cma size （转码卡建议256MB）

   ```bash
   [axera@localhost ~]$ cat /etc/default/grub
   GRUB_TIMEOUT=5
   GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
   GRUB_DEFAULT=saved
   GRUB_DISABLE_SUBMENU=true
   GRUB_TERMINAL_OUTPUT="console"
   GRUB_CMDLINE_LINUX="crashkernel=1G-4G:192M,4G-64G:256M,64G-:512M resume=/dev/mapper/cs-swap rd.lvm.lv=cs/root rd.lvm.lv=cs/swap rhgb cma=256M"
   GRUB_DISABLE_RECOVERY="true"
   GRUB_ENABLE_BLSCFG=true
   ```

   ![](https://github.com/AXERA-TECH/axcl-docs/blob/main/res/centos_grub_info.png)

4. 更新grub

   ```bash
   sudo su
   grub2-mkconfig -o /boot/grub2/grub.cfg
   grub2-editenv - set "$(grub2-editenv - list | grep kernelopts) cma=256M"
   grubby --update-kernel=ALL --args="cma=256M"
   ```

5. 关闭SELinux

   ```
   [axera@localhost ~]$ cat /etc/selinux/config
   
   # This file controls the state of SELinux on the system.
   # SELINUX= can take one of these three values:
   #     enforcing - SELinux security policy is enforced.
   #     permissive - SELinux prints warnings instead of enforcing.
   #     disabled - No SELinux policy is loaded.
   # See also:
   # https://docs.fedoraproject.org/en-US/quick-docs/getting-started-with-selinux/#getting-started-with-selinux-selinux-states-and-modes
   #
   # NOTE: In earlier Fedora kernel builds, SELINUX=disabled would also
   # fully disable SELinux during boot. If you need a system with SELinux
   # fully disabled instead of SELinux running with no policy loaded, you
   # need to pass selinux=0 to the kernel command line. You can use grubby
   # to persistently set the bootloader to boot with selinux=0:
   #
   #    grubby --update-kernel ALL --args selinux=0
   #
   # To revert back to SELinux enabled:
   #
   #    grubby --update-kernel ALL --remove-args selinux
   #
   SELINUX=disabled
   # SELINUXTYPE= can take one of these three values:
   #     targeted - Targeted processes are protected,
   #     minimum - Modification of targeted policy. Only selected processes are protected.
   #     mls - Multi Level Security protection.
   SELINUXTYPE=targeted
   ```

   ![](https://github.com/AXERA-TECH/axcl-docs/blob/main/res/centos_selinux.png)

6. 安装make, gcc, patch, rpm-build

   ```bash
   sudo yum install -y patch
   sudo yum install -y rpm-build
   ```

7. 重启 reboot

8. dmesg |  grep cma 查看CMA reserved是否成功

   ```bash
   [axera@localhost ~]$ dmesg | grep cma
   [    0.000000] Command line: BOOT_IMAGE=(hd0,msdos2)/vmlinuz-5.14.0-522.el9.x86_64 root=/dev/mapper/cs-root ro crashkernel=1G-4G:192M,4G-64G:256M,64G-:512M resume=/dev/mapper/cs-swap rd.lvm.lv=cs/root rd.lvm.lv=cs/swap rhgb quiet cma=256M
   [    0.009093] cma: Reserved 256 MiB at 0x0000000100000000 on node -1
   [    0.020735] Kernel command line: BOOT_IMAGE=(hd0,msdos2)/vmlinuz-5.14.0-522.el9.x86_64 root=/dev/mapper/cs-root ro crashkernel=1G-4G:192M,4G-64G:256M,64G-:512M resume=/dev/mapper/cs-swap rd.lvm.lv=cs/root rd.lvm.lv=cs/swap rhgb quiet cma=256M
   [    0.040339] Memory: 2252120K/16608544K available (16384K kernel code, 5666K rwdata, 13072K rodata, 3996K init, 7680K bss, 733484K reserved, 262144K cma-reserved)
   [    0.098563] cma: Initial CMA usage detected
   ```

   ![](https://github.com/AXERA-TECH/axcl-docs/blob/main/res/centos_dmsg_grep_cma.png)



## rpm安装

rpm的安装分为2个步骤：将**src**.rpm源码编译成二进制的rpm，然后安装rpm。

> [!IMPORTANT]
>
> 因安装后将自动加载设备固件，因此安装前请确认子卡已和主机正确连接。

1. **rpm -Uvh axcl_host-V2.16.0_20241111020148-NO4430.src.rpm**

   ```bash
   [axera@localhost]$ rpm -Uvh axcl_host-V2.16.0_20241111020148-NO4430.src.rpm
   Updating / installing...
      1:axcl_host-V2.16.0_20241111020148-warning: user jenkins does not exist - using root
   warning: group jenkins does not exist - using root
   warning: user jenkins does not exist - using root
   warning: group jenkins does not exist - using root
   ################################# [100%]
   ```

2.  源码安装完之后，在/home/user目录可以找到rmpbuild目录（如果是sudo，目录在/root）

   [axera@localhost ~]$ ls
   Desktop  Documents  Downloads  jingxiaoping  mp4  Music  Pictures  Public  **rpmbuild**  Templates  Videos

3. 构建二进制rpm安装包：**rpmbuild -bb --nodebuginfo rpmbuild/SPECS/axcl_host.spec**

   ```
   [axera@localhost rpmbuild]$ rpmbuild -bb --nodebuginfo SPECS/axcl_host.spec
   warning: bogus date in %changelog: Thu Oct 30 2024 root <root@localhost> - 1.0-1
   setting SOURCE_DATE_EPOCH=1730246400
   Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.qShrCO
   + umask 022
   + cd /home/axera/rpmbuild/BUILD
   + cd /home/axera/rpmbuild/BUILD
   + rm -rf axcl
   + /usr/bin/gzip -dc /home/axera/rpmbuild/SOURCES/axcl.tar.gz
   + /usr/bin/tar -xof -
   + STATUS=0
   + '[' 0 -ne 0 ']'
   + cd axcl
   + /usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .
   ++ cat /etc/os-release
   ++ grep '^VERSION_ID='
   ++ cut -d = -f2
   ++ tr -d '"'
   + os_version=9
   ++ cat /etc/os-release
   ++ grep '^NAME='
   ++ cut -d = -f2
   ++ tr -d '"'
   + os_name='CentOS Stream'
   + [[ CentOS Stream == \C\e\n\t\O\S\ \S\t\r\e\a\m ]]
   + [[ 9 == \9 ]]
   + echo 'Apply patch for centos stream 9'
   Apply patch for centos stream 9
   + cd /home/axera/rpmbuild/BUILD/axcl/drv/pcie/driver
   + patch -p3
   patching file include/ax_pcie_dev.h
   patching file net/rc-net/ax_pcie_net.c
   + RPM_EC=0
   ++ jobs -p
   + exit 0
   Executing(%build): /bin/sh -e /var/tmp/rpm-tmp.l1AJjV
   + umask 022
   + cd /home/axera/rpmbuild/BUILD
   + cd axcl
   + cd /home/axera/rpmbuild/BUILD/axcl/drv/pcie/driver
   + make host=x86 clean all install -j8
   + RPM_EC=0
   ++ jobs -p
   + exit 0
   Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.xiLHDC
   ... ...
   Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/axera/rpmbuild/BUILDROOT/axcl_host-1.0-1.el9.x86_64
   Wrote: /home/axera/rpmbuild/RPMS/x86_64/axcl_host-1.0-1.el9.x86_64.rpm
   Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.a78fQ2
   + umask 022
   + cd /home/axera/rpmbuild/BUILD
   + cd axcl
   + /usr/bin/rm -rf /home/axera/rpmbuild/BUILDROOT/axcl_host-1.0-1.el9.x86_64
   + RPM_EC=0
   ++ jobs -p
   + exit 0
   ```

4. 安装rpm：**sudo rpm -Uvh --nodeps rpmbuild/RPMS/x86_64/axcl_host-1.0-1.el9.x86_64.rpm**

   ```
   [axera@localhost rpmbuild]$ sudo rpm -Uvh --nodeps RPMS/x86_64/axcl_host-1.0-1.el9.x86_64.rpm
   [sudo] password for axera:
   Verifying...                          ################################# [100%]
   Preparing...                          ################################# [100%]
   Updating / installing...
      1:axcl_host-1.0-1.el9              ################################# [100%]
   [axera@localhost rpmbuild]$
   ```

5.  source /etc/profile

   ```bash
   [axera@localhost axcl]$ ls  /usr/lib/axcl/
   ffmpeg                libaxcl_ive.so      libaxcl_npu.so          libaxcl_pkg.so     libaxcl_skel.debug   libaxcl_vdec.debug  libspdlog.so.1.14.1
   libaxcl_comm.debug    libaxcl_ivps.debug  libaxcl_pcie_dma.debug  libaxcl_ppl.debug  libaxcl_skel.so      libaxcl_vdec.so
   libaxcl_comm.so       libaxcl_ivps.so     libaxcl_pcie_dma.so     libaxcl_ppl.so     libaxcl_sys.debug    libaxcl_venc.debug
   libaxcl_dmadim.debug  libaxcl_lite.debug  libaxcl_pcie_msg.debug  libaxcl_proto.a    libaxcl_sys.so       libaxcl_venc.so
   libaxcl_dmadim.so     libaxcl_lite.so     libaxcl_pcie_msg.so     libaxcl_rt.debug   libaxcl_token.debug  libspdlog.so
   libaxcl_ive.debug     libaxcl_npu.debug   libaxcl_pkg.debug       libaxcl_rt.so      libaxcl_token.so     libspdlog.so.1.14
   [axera@localhost axcl]$ ls  /usr/bin/axcl/
   axcl_demo       axcl_sample_dmadim  axcl_sample_ivps    axcl_sample_runtime  axcl_sample_sys        axcl_sample_vdec  axcl_smi  launch_transcode.sh
   axcl_run_model  axcl_sample_ive     axcl_sample_memory  axcl_sample_skel     axcl_sample_transcode  axcl_sample_venc  data      ut
   [axera@localhost axcl]$
   ```

## rpm卸载

```bash
sudo rpm -e axcl_host
rpm包卸载后会自动reset子卡，子卡会进入pcie download mode
```