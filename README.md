# ai-quickstart



本项目旨在可以快速搭建 DeepSeek 等 AI 大模型的 API 调用基础环境及代码。

> [!note]
>
> 本项目需均在具有相应大模型 API 的情况下使用。

## 安装依赖

### pip 安装

```sh
pip install -r requirements.txt
```

### conda 安装

```sh
# 在此使用的为 mamba

# 通过文件直接创建环境
mamba env create -f environment.yml

# 可通过 -n 指定环境名
mamba env create -f environment.yml -n 新环境名

# 更新现有环境
mamba env update -f environment.yml -n 环境名
```

## DeepSeek



