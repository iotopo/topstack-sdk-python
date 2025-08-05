#!/usr/bin/env python3
"""
安装 NATS 依赖项脚本
"""

import subprocess
import sys


def install_package(package):
    """安装 Python 包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ 成功安装 {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ 安装 {package} 失败")
        return False


def main():
    """主函数"""
    print("正在安装 NATS 相关依赖项...")
    
    # 需要安装的包
    packages = [
        "nats-py",
        "asyncio"
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n安装完成: {success_count}/{total_count} 个包安装成功")
    
    if success_count == total_count:
        print("✓ 所有依赖项安装成功！")
        print("\n现在可以运行 NATS 示例了:")
        print("python examples/nats_example.py")
    else:
        print("✗ 部分依赖项安装失败，请手动安装")
        print("运行: pip install nats-py")


if __name__ == "__main__":
    main() 