# 酷狗KGM混淆音频解密工具 Python版
[![Badge](https://img.shields.io/badge/link-996.icu-%23FF4D5B.svg?style=flat-square)](https://996.icu)
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg?style=flat-square)](/LICENSE)
[![Lang](https://img.shields.io/badge/lang-python-brightgreen?style=flat-square)](https://www.python.org)

## 项目介绍
本项目是 [ghtz08/kuguo-kgm-decoder](https://github.com/ghtz08/kuguo-kgm-decoder) 的纯 Python 移植实现。
特别感谢原作者开源完整解密算法，原项目程序可在 [Releases页面](https://github.com/ghtz08/kuguo-kgm-decoder/releases) 获取。

原项目基于 Rust 开发，Windows11 用户存在编译、运行兼容门槛；本版本无需编译，安装 Python 即可全平台（Windows/macOS/Linux）运行，支持批量、解密酷狗 KGM 加密歌曲，自动识别真实音频后缀。



## 前置准备
1.本仓库不提供 `kugou_key.xz` 密钥文件，请自行前往原项目仓库 `assets` 文件夹下载，放到脚本同目录。

2.请手动修改main函数中的 default_target 为自己电脑下的kmg文件存放路径

## 环境要求
Python 3.8 及以上，无任何第三方依赖，仅使用标准库。

## 快速开始
### 1. 拉取代码
```bash
git clone https://github.com/jieyideshijie/yijiedeshijie
cd yijiedeshijie
