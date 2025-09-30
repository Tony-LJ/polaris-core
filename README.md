
# polaris-common-core

---


## 介绍
```.text
python项目开发通用工具包
```


## 项目设计
```.text

```




## 项目部署
```.text

```

## 本地化调试
### 安装构建产物与本地测试
```.text
在构建出 .whl 包后，你可以在本地测试安装以确保其正确性
pip install dist/polaris_common_core-0.1.0-py3-none-any.whl
或在另一个使用 Poetry 的项目中
poetry add ../path/to/dist/polaris_common_core-0.1.0-py3-none-any.whl
```

## 常用命令
```.text
创建项目
poetry new polaris_common_core
poetry初始化，会在项目根目录生成pyproject.toml文件
poetry init
添加与更新依赖项
poetry add requests
poetry update
只想更新特定的依赖项
poetry update requests
想安装 requests 的最新版本，而不受当前版本约束的限制
poetry add requests@latest
删除依赖
poetry remove requests
查看已安装的依赖
poetry show
查看环境信息
poetry env info
构建项目,这将创建一个 dist 目录，其中包含 .tar.gz 和 .whl 格式的打包文件
poetry build
发布项目,pyproject.toml 中配置 PyPI 的凭据，或者在命令行中输入
poetry publish
使用 Poetry 的虚拟环境来运行项目
poetry run python <your_script.py>
```


## 参考资料




