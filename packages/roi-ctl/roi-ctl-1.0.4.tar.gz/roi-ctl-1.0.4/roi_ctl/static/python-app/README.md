# {NAME}

请补充项目工程描述信息

## 项目结构

```
{NAME}
├── app                              # 源代码路径
│   ├── app_logger.py                # LOG
│   ├── app_product.py               # 多环境，配置在 Package.json
│   ├── app.py                       # 程序入口
│   └── __init__.py
├── Dockerfile                       # Dockerfile 示例
├── case.py                          # 单元测试入口
├── main.py                          # 项目入口
├── package.json                     # 配置信息
├── README.md                        # 说明
├── requirements.txt                 # 依赖  
└── static                           # 静态文件
    └── README.md
`-- tests                      # 单元测试
    |-- test_app.py            # 单元测试示例
    `-- utils.py
```

## 项目构建

- tag 自定义

```
docker build -f Dockerfile -t {DOCKER_IMAGE}:tag .
```

## 单元测试

在  tests  文件夹下自定义 test_{module}.py 文件，函数名也是 `test_{method}` 定义用例

```
# 执行用例
python case.py
```

## 项目说明