@echo off
echo 正在上传到 PyPI...
echo 忽略已存在的版本文件...

REM 检查 dist 目录是否存在
if not exist "dist" (
    echo 错误: dist 目录不存在，请先运行 build.bat 构建项目
    pause
    exit /b 1
)

REM 检查 dist 目录是否为空
dir /b "dist" >nul 2>&1
if errorlevel 1 (
    echo 错误: dist 目录为空，请先运行 build.bat 构建项目
    pause
    exit /b 1
)

REM 上传到 PyPI，跳过已存在的版本
twine upload --skip-existing dist/*

if %errorlevel% equ 0 (
    echo 上传成功！已跳过所有已存在的版本文件。
) else (
    echo 上传过程中出现错误，请检查网络连接和认证信息。
)

pause