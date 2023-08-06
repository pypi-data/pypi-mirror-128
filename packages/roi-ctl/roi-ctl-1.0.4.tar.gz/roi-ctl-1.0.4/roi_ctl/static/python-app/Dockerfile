FROM python:3.8-slim

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装依赖: build-essential 是 pycryptodome 所需要的依赖
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update \
    && apt-get install -y sudo curl wget inetutils-ping net-tools build-essential libgl1-mesa-glx libglib2.0-dev
# 安装依赖
COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt -i https://pypi.douban.com/simple
# 自定义依赖
# 1.安装
RUN pip install roi-ctl 
# 工作目录
WORKDIR /app
# 2.项目
COPY . /app/code/
# 3.打包
RUN cd /app/code/ && roictl build --env product
# 4.复制与删除
RUN cp -rf /app/code/build /app/ && rm -rf /app/code &&  mv /app/build /app/code
# 5.卸载
# RUN pip uninstall roi-ctl -y
# 6.运行
CMD ["/app/code/app.bin"]

