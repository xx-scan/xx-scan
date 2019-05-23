# 开发流程


## 安装 Redis
```bash
docker run --name redis -d --restart=always \
  -p 6379:6379 \
  -e 'REDIS_PASSWORD=xxscan' \
  -v /srv/docker/redis:/var/lib/redis \
  sameersbn/redis:4.0.9-2
```

## 安装

