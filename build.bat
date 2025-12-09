@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Configuration Section
set "SCRIPT_FILE=get_wifi_passwords_silent.py"
set "ICON_FILE=app_logo.ico"
set "APP_NAME=WiFiPasswordExtractor"

:: Strictly validate icon file existence
if not exist "%ICON_FILE%" (
    echo [ERROR] Icon file not found: %ICON_FILE%
    echo Please place a valid .ico file in current directory
    echo 错误：未找到图标文件 %ICON_FILE%
    echo 请在当前目录放置有效的.ico格式图标文件
    pause
    exit /b 1
)

:: Build executable with production-grade parameters
echo Building executable with custom icon...
echo.

pyinstaller ^
  --onefile ^
  --noconsole ^
  --clean ^
  --icon="%ICON_FILE%" ^
  --name "%APP_NAME%" ^
  --add-data "%SCRIPT_FILE%;." ^
  --runtime-tmpdir=. ^
  --uac-admin ^
  --hidden-import win32api ^
  "%SCRIPT_FILE%"

:: Completion notification
echo.
if exist "dist\%APP_NAME%.exe" (
    echo Build successful! Output: dist\%APP_NAME%.exe
    echo 打包成功！输出文件: dist\%APP_NAME%.exe
) else (
    echo [ERROR] Build failed
    echo 错误：构建失败
)

pause
EXIT /B 0
