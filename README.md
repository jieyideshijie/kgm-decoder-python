# yijiedeshijie
# 酷狗混淆的歌曲文件的解码器

[![Badge](https://img.shields.io/badge/link-996.icu-%23FF4D5B.svg?style=flat-square)](https://996.icu)
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg?style=flat-square)](/LICENSE)
[![Lang](https://img.shields.io/badge/lang-rust-brightgreen?style=flat-square)](https://www.rust-lang.org)
![Repo Size](https://img.shields.io/github/repo-size/ghtz08/kuguo-kgm-decoder?style=flat-square)
![Code Size](https://img.shields.io/github/languages/code-size/ghtz08/kuguo-kgm-decoder?style=flat-square)

介绍
本项目是 ghtz08/kuguo-kgm-decoder 的 Python 移植版本，基于原项目的解密算法逻辑，使用纯 Python 重写实现。
原项目为 Rust 语言开发，对 Windows 普通用户存在编译门槛，因此本项目提供无需编译、开箱即用的 Python 版本，支持 Windows /macOS/ Linux 全平台运行。
可用于解码酷狗缓存歌曲文件和下载的单曲加密文件，解码原理来自博客孤心浪子 - 闲来无事研究一下酷狗缓存文件 kgtemp 的加密方式和 ix64 的 unlock-music 项目中的酷狗解码实现。
感谢 ix64 提供用于解码的 Key，ix64 的 unlock-music 项目提供了包括酷狗、网易云等多个平台的歌曲文件解码功能，并有网页和命令行两种使用方式。
ix64 主页: https://github.com/ix64
unlock-music 项目: https://github.com/ix64/unlock-music

前置准备
请先从原项目仓库 (https://github.com/ghtz08/kuguo-kgm-decoder) 的 assets 目录获取 kugou_key.xz 密钥文件，将其与脚本放在同一目录下。
本仓库不包含解密密钥文件，仅提供算法实现。

环境要求
Python 3.8 及以上版本，无需安装任何第三方依赖。

使用方式（在Kmg_trans.py这个文件中的main函数进行修改default_target kmg文件所在对应的路径）
针对单个文件
python Kmg_trans.py <文件名>

针对某个目录下的文件（不包括子目录）
python Kmg_trans.py <目录名>

针对某个目录下的文件（包括子目录）
python Kmg_trans.py -r <目录名>

其它参数
参数	解释
-k, --keep-file	保留原加密文件
--key <文件路径>	指定密钥文件路径，默认读取同目录下的 kugou_key.xz
脚本会根据解码后的文件头自动识别真实音频格式（mp3/flac/wav/ogg/aac）并修改对应后缀。
免责声明
本工具仅用于技术研究与个人合法拥有版权的音频文件格式转换，请遵守所在地区的知识产权相关法律，禁止用于商业传播、盗版侵权等非法用途。
使用者自行承担使用本工具产生的一切责任与风险。

反 996 许可证版本 1.0，详见 /LICENSE 文件
