#!/bin/bash
# TopStack Python SDK 示例运行脚本

set -e

echo "TopStack Python SDK 运行示例"
echo "================================================"

# 检查 Python 环境
python3 --version

# 安装依赖（推荐用 pyproject.toml）
pip3 install -e .

# 运行示例
python3 examples/basic_usage.py 