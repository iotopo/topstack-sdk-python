@echo off
chcp 65001 >nul
echo TopStack Python SDK 运行示例
echo ================================================

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8 或更高版本
    pause
    exit /b 1
)

echo Python 环境检查通过

REM 检查依赖是否安装
echo 检查依赖...
python -c "import requests, pydantic" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

echo 依赖检查通过

REM 运行示例
echo.
echo 开始运行示例...
python run_example.py

echo.
echo 示例运行完成
pause 