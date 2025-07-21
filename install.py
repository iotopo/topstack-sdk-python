#!/usr/bin/env python3
"""
TopStack Python SDK 快速安装脚本

这个脚本会自动安装依赖并验证安装是否成功
"""

import sys
import subprocess
import os

def check_python_version():
    """检查 Python 版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要 Python 3.8 或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✓ Python 版本检查通过: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    
    try:
        # 升级 pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # 安装依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✓ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖安装失败: {e}")
        return False

def verify_installation():
    """验证安装"""
    print("验证安装...")
    
    try:
        # 检查关键依赖
        import requests
        import pydantic
        print("✓ 核心依赖检查通过")
        
        # 检查 SDK 导入
        from topstack import TopStackClient, IotApi, DeviceApi
        print("✓ SDK 导入检查通过")
        
        # 检查配置文件
        from config import TOPSTACK_CONFIG
        print("✓ 配置文件检查通过")
        
        return True
    except ImportError as e:
        print(f"✗ 安装验证失败: {e}")
        return False

def create_virtual_environment():
    """创建虚拟环境"""
    print("创建虚拟环境...")
    
    try:
        # 检查是否已存在虚拟环境
        if os.path.exists("venv"):
            print("虚拟环境已存在，跳过创建")
            return True
        
        # 创建虚拟环境
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✓ 虚拟环境创建成功")
        
        # 激活虚拟环境并安装依赖
        if os.name == 'nt':  # Windows
            activate_script = os.path.join("venv", "Scripts", "activate.bat")
            subprocess.check_call([activate_script, "&&", sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], shell=True)
        else:  # Linux/macOS
            activate_script = os.path.join("venv", "bin", "activate")
            subprocess.check_call(f"source {activate_script} && pip install -r requirements.txt", shell=True)
        
        print("✓ 虚拟环境依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 虚拟环境创建失败: {e}")
        return False

def main():
    """主函数"""
    print("TopStack Python SDK 快速安装")
    print("=" * 40)
    
    # 检查 Python 版本
    if not check_python_version():
        return 1
    
    # 询问是否创建虚拟环境
    create_venv = input("是否创建虚拟环境？(y/n): ").lower().strip() == 'y'
    
    if create_venv:
        if not create_virtual_environment():
            return 1
    else:
        # 直接安装依赖
        if not install_dependencies():
            return 1
    
    # 验证安装
    if not verify_installation():
        return 1
    
    print("\n" + "=" * 40)
    print("✓ 安装完成！")
    print("\n使用方法:")
    if create_venv:
        if os.name == 'nt':  # Windows
            print("1. 激活虚拟环境: venv\\Scripts\\activate")
        else:  # Linux/macOS
            print("1. 激活虚拟环境: source venv/bin/activate")
    print("2. 修改 config.py 中的配置参数")
    print("3. 运行示例: python run_example.py")
    print("4. 或者使用批处理脚本: run_example.bat (Windows) 或 ./run_example.sh (Linux/macOS)")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 