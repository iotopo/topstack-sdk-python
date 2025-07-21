#!/bin/bash

echo "TopStack Python SDK 运行示例"
echo "================================================"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "Python 环境检查通过"

# 检查依赖是否安装
echo "检查依赖..."
if ! python3 -c "import requests, pydantic" &> /dev/null; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

echo "依赖检查通过"

# 运行示例
echo ""
echo "开始运行示例..."
python3 run_example.py

echo ""
echo "示例运行完成" 