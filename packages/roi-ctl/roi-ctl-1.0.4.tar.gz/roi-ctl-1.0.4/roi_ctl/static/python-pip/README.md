# {NAME}

模块描述，自行补充


## 工程说明

```
{NAME}
├── LICENSE                    # 版权
├── package.json               # 项目配置
├── {PACKAGE_NAME}             # 包名
│   ├── app_logger.py          # LOG 工具
│   ├── app.py                 # 程序入口
│   ├── __init__.py            
│   └── static                 # 静态资源文件夹
│       └── README.md
├── README.md                  # 项目说明
├── RELEASE.md                 # 版本说明
|-- main.py                    # 单元测试，主入口
└── requirements.txt           # 依赖
|-- static                     # 静态资源
|   `-- README.md
`-- tests                      # 单元测试
    |-- test_app.py            # 单元测试示例
    `-- utils.py
```

## 构建说明

```
# 测试打包
roictl build --env dev
# 生产打包
roictl build --env product
# 发布
roictl upload
# 安装
roictl install {NAME}
```


## 单元测试

在  tests  文件夹下自定义 test_{module}.py 文件，函数名也是 `test_{method}` 定义用例

```
# 执行用例
python main.py
```


## 使用说明

功能清单，自行补充