## ScanBox 参考的内容
    - [ScanBox](https://raw.githubusercontent.com/We5ter/Scanners-Box/master/README_CN.md)
    
- [Install-all-kali-tools](https://github.com/LionSec/katoolin)
- [ScanBox](https://github.com/We5ter/Scanners-Box/blob/master/README_CN.md)
- [awesome-pentest](https://github.com/enaqx/awesome-pentest)
- [awesome-hacking](https://github.com/carpedm20/awesome-hacking)
- [awesome-hacking权威](https://github.com/Hack-with-Github/Awesome-Hacking)
- [awesome-hacking中文](https://github.com/sunnyelf/awesome-hacking)
- [awesome-hacking-tools](https://github.com/m4ll0k/Awesome-Hacking-Tools)
- [awesome-ctf](https://github.com/apsdehal/awesome-ctf)


## 搭建教程
- 使用环境为 `ubuntu/trusty` Box/Docker
  - 原因是使用者多, 开源工具多，集成多。


### 预备内容

```bash
cat > /etc/apt/source.list <<- EOF
deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
EOF


```****
