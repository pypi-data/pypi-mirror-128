# -*- coding: utf-8 -*-
# @Author  : LG


from setuptools import setup, find_packages

setup(
    name = "changeable",                                # 包名
    version = "0.0.2",                                  # 版本号
    author = "yatengLG",
    author_email = "yatenglg@qq.com",
    description="Data transforms for object detection.",
    long_description="Data transforms for object detection base on pytorch.",
    url="https://github.com/yatengLG/Changeable",  # 项目相关文件地址

    keywords = ("pip", "changeable"),
    license = "MIT Licence",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",

    python_requires=">=3.6",                            # python 版本要求
    install_requires = ["torch",                        # 依赖包
                        "numpy",
                        "pillow",
                        "opencv-python"
                        ]
)
