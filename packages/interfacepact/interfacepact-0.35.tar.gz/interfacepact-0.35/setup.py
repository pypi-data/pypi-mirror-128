#coding=utf-8
import setuptools


long_description="interface pact"
setuptools.setup(
    name="interfacepact",
    version="0.35",
    author="jaygeli",
    author_email="348447053@qq.com",
    description="interface pact verify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crazymonkey/PactVerify_demo",
    packages=setuptools.find_packages(),
    install_requires=['six'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)