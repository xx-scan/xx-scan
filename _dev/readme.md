# 开发流程

## 宿主机centos7.4同步时间
- `cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime`

## 安装docker-compose 
```
yum -y install gcc gcc-c++ make openssl openssl-devel
pip3 install docker-compose -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 安装python3
```
yum install yum-fastestmirror
# /etc/yum/pluginconf.d/fastestmirror.conf
yum -y install epel-release 
yum -y install python36 python36-pip python36-devel gcc 

mkidr /home/django && cd /home/django && python3 -m venv cso_venv && \ 
git clone https://github.com/xx-scan/xx-scan 
```

## 安装 Redis
```bash
docker run --name redis -d --restart=always \
  -p 6379:6379 \
  -e 'REDIS_PASSWORD=xxscan' \
  -v /srv/docker/redis:/var/lib/redis \
  sameersbn/redis:4.0.9-2
```

## 安装Mysql
```
docker run -itd --name=mysql -p 3306:3306 --restart=always \
-v /srv/docker/data/mysqldata:/var/lib/mysql \
-e MYSQL_USER=admin007 \
-e MYSQL_PASSWORD=myadmin@816 \
-e MYSQL_DATABASE=xxscan \
-e MYSQL_ROOT_PASSWORD=test@1q2w2e4R \
-e character-set-server=utf8 \
-e collation-server=utf8_general_ci \
mysql:5.7

drop database xxscan;
CREATE DATABASE blog DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```
## 安装 Postgresql
```
docker run --name postgresql -itd --net=host --restart always \
  -e DB_USER=admin007 -e DB_PASS=myadmin@816 -e DB_NAME=xxscan,bbs -e DB_EXTENSION=unaccent,pg_trgm \
  sameersbn/postgresql:10-1
```

## 初始化数据库并创建超级角色[免登陆中间件必须]
```bash
cd apps && python manage.py createsuperuser 
```


## 2019-5-30
- 昨天尝试了下 `backbox5.3` 今天尝试了 `ubuntu:16.04` 发现环境可以在这个中。
- 已经更新对应的安装文档和说明的环境 [Ubuntu-Secuciry](https://github.com/xx-scan/ubsec)

