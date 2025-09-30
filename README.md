
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




