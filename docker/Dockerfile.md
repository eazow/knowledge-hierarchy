

### 1. Dockerfile

Docker 通过读取 Dockerfile 中的指令自动构建镜像

Docker 镜像由只读层组成，每个层代表一个 Dockerfile 指令。这些层是堆叠的，每一层都是前一层变化的增量

以下是 Dockerfile 的示例

```
FROM python:3.10.10-slim-buster
COPY . /app
RUN make /app
CMD python /app/app.py
```

每条指令创建一层layer

- `FROM`从 Docker 镜像创建一个图层
- `COPY`从 Docker 客户端的当前目录添加文件
- `RUN`使用make构建您的应用程序
- `CMD`指定在容器中运行的命令



### 2. 构建镜像

```
docker build -t demo:v1 .
```

其中的`.`表示**上下文路径**

当构建的时候，用户会指定构建镜像上下文的路径，`docker build` 命令得知这个路径后，会将路径下的所有内容打包，然后上传给 Docker Engine

因此`COPY ../package.json /app` 或者`COPY /opt/xxx /app`会有问题





### 3. 指令

#### FROM

```
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
```

FROM 指令初始化新的生成阶段，并为后续指令设置 BaseImage。因此，有效的 Dockerfile 必须以 FROM 指令开始

尽可能使用当前的官方图像作为图像的基础。推荐使用[Alpine 镜像](https://hub.docker.com/_/alpine/)，因为它受到严格控制且体积小（目前不到 6 MB），同时仍然是一个完整的 Linux 发行版



#### RUN

RUN 指令将执行当前图像顶部新层中的任何命令并提交结果。生成的提交Image将用于 Dockerfile 中的下一步

将长或复杂的 RUN 语句拆分为多行，并用反斜杠分隔，以使 Dockerfile 更易读、更易理解和更易维护

##### 

RUN 最常见的用例可能是 apt-get 

在相同的 RUN 语句中将 `RUN apt-get update`和 `apt-get install`l结合起来。例如:

```
RUN apt-get update && \
    apt-get install -y package-bar package-baz package-foo && \
    rm -rf /var/lib/apt/lists/*
```



#### CMD

使用 CMD 指令来运行图像中包含的软件以及参数

例如运行`supervisor`

```
CMD ["supervisord", "-c", "supervisord.conf"]
```

CMD会在**docker run没有指定其他命令时运行**



#### ADD or COPY

虽然 ADD 和 COPY 在功能上是相似的，但一般来说，COPY 是首选



#### WORKDIR

为了清晰和可靠，应该始终为 WORKDIR 使用绝对路径。此外，应该使用 WORKDIR，而不是增加指令，如运行 `cd... && do-something`，这样难以阅读和维护



#### ENV

```
ENV <key>=<value> ...
```

使用 ENV 添加环境变量

例如

```
ENV PATH=/usr/local/lib
```



#### EXPOSE

EXPOSE 指令指示容器侦听连接的端口

```
EXPOSE 80
```







### Vue的Dockerfile

```
# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

