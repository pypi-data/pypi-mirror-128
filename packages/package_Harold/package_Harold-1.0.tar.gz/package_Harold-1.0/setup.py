from distutils.core import setup
setup(
    name='package_Harold',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，测试哦',  # 描述
    author='Harold',  # 作者
    author_email='hezhuangres@163.com',
    py_modules=['package_Harold.demo1', 'package_Harold.demo2']  # 要发布的模块
)
