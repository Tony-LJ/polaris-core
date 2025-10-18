
# polaris-core

---


## 介绍
```.text
python项目开发通用工具包
```

## 项目设计
```.text

```


## 功能模块
### Ai模块
```.text

```
### Api处理模块
```.text

```
### 通用工具common模块
```.text
一.工具类
  1.字符串 处理  
```
### 存储系统connector模块
```.text

```
### 加密crypto模块
```.text

```
### 枚举enums模块
```.text

```
### 异常处理exception模块
```.text

```
### 日志logger模块
```.text

```
### 消息推送message模块
```.text

```
### 消息中间件mq模块
```.text

```



## 项目部署
```.text
 Python 源码
   │
 加密/编译（Pyarmor、Cython、Nuitka）
   │
 打包（PyInstaller/poetry）
   │
 ️加固（混淆、壳保护、完整性校验）
   │
 发布（本地安装包、网盘等分享）
```

## 本地化调试
### 安装构建产物与本地测试
```.text
在构建出 .whl 包后，你可以在本地测试安装以确保其正确性
pip install dist/polaris_core-0.1.0-py3-none-any.whl
或在另一个使用 Poetry 的项目中
poetry add ../path/to/dist/polaris_core-0.1.0-py3-none-any.whl
```
### 测试环境安装
```.text
pip install -i https://test.pypi.org/simple/ polaris-core==1.1.3
```
### 正式环境安装
```.text
pip install -i https://pypi.org/simple/ polaris-core==1.1.3
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

## 发布到PyPI或私有仓库
### PyPI 凭据配置
```.text
方式1：
在发布前，需要配置仓库地址与登录凭据。默认的公开仓库为 pypi。如果你要上传到测试仓库（TestPyPI）进行预发布测试：
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config http-basic.test-pypi <username> <password_or_token>
如果是正式 PyPI：
poetry config pypi-token.pypi <your_api_token>

方式2：
twine upload dist/* -r testpypi
twine upload dist/* -r pypi
```
- [发布到 TestPyPI]()
  ```.text
  方式1：
  先构建后发布，以免忘记构建：
  poetry publish -r test-pypi --build
  方式2：
  twine upload --repository testpypi --verbose dist/*
  twine upload dist/* -r testpypi
  Tony pypi-AgENdGVzdC5weXBpLm9yZwIkNGRhYWM1ODMtNDEwMi00ODQ1LWI3YzktODVjZjllYzEwMzRhAAIqWzMsIjhkMmI0YTBlLTRmZmUtNGMyNi04NGJhLTE0MmViZjgwYWQxMyJdAAAGIOHlQrxUOURhfUSJeVMNNeI_9doWDHodjuP8mk-eE7ys
  ```
  ![img](/docs/imgs/642375874689070.png) </br>

- [发布到正式 PyPI]()
  ```.text
  方式1：
  确认测试无误后，即可发布到 PyPI：
  poetry publish --build
  方式2：
  twine upload dist/* -r pypi
  ```


python -m build
twine upload --repository testpypi --verbose dist/*
Tony pypi-AgENdGVzdC5weXBpLm9yZwIkNGRhYWM1ODMtNDEwMi00ODQ1LWI3YzktODVjZjllYzEwMzRhAAIqWzMsIjhkMmI0YTBlLTRmZmUtNGMyNi04NGJhLTE0MmViZjgwYWQxMyJdAAAGIOHlQrxUOURhfUSJeVMNNeI_9doWDHodjuP8mk-eE7ys

## 参考资料
- [python之poetry模块，项目管理](https://blog.csdn.net/randy521520/article/details/135305694)
- [利用pyinstaller_poetry简化Python应用打包](https://blog.csdn.net/weixin_32661831/article/details/146264445)
- [Python PyInstaller 打包、Pyarmor加密等](https://www.cnblogs.com/LungGiyo/p/18868979)
- [python使用企业微信机器人发送测试报告](https://www.cnblogs.com/lifeng0402/articles/14122401.html)
- [python使用企业微信机器人发送测试报告](https://blog.csdn.net/weixin_44738514/article/details/120186857)
