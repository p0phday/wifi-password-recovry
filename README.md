#📶 Windows WiFi密码导出小工具

Python 适用系统 授权协议
一个简单的Windows WiFi密码导出小工具，主要用于帮助用户找回自己遗忘的WiFi密码。工具还比较初级，如有不足之处，还请多多指教。

🌟 主要功能
会自动检查是否需要管理员权限
尝试兼容不同编码，减少乱码问题
会生成操作日志，方便排查问题
提供两种密码导出方式，提高成功率
支持无窗口静默运行
生成的报告会整理成易读格式
⚙️ 使用准备
Windows 7/10/11系统
需要安装Python 3.7+
建议使用PyInstaller打包
📥 获取方式
方法一：直接下载
在发布页面下载编译好的程序
将app_logo.ico图标文件放在同一个文件夹里(可选)
右键选择"以管理员身份运行"
方法二：自己编译
<BASH>
git clone https://github.com/您的用户名/wifi-password-extractor.git
cd wifi-password-extractor
# 安装必要的包
pip install pyinstaller
# 编译程序
build.bat
💻 基本使用
双击运行程序后，会在当前文件夹生成：

WiFi_Passwords_Report.txt - 保存找到的WiFi密码
WiFi_Export.log - 记录运行过程
🔨 编译说明
首先确保安装了Python 3.7+
安装依赖项：
<BASH>
pip install pyinstaller pypiwin32
放好图标文件app_logo.ico
运行编译脚本：
<BASH>
build.bat
编译好的程序在dist文件夹里
🗂️ 项目文件说明
<TEXT>
wifi-password-extractor/
├── dist/                           
├── build/                          
├── get_wifi_passwords_silent.py    # 主程序
├── build.bat                       # 编译脚本
├── app_logo.ico                    # 程序图标(可选)
├── WiFi_Passwords_Report.txt       # 密码报告
├── WiFi_Export.log                 # 运行日志
└── README.md                       # 说明文件
⚠️ 注意事项
这个小工具只能用于找回自己设备的WiFi密码，请不要用于其他用途。使用时请注意遵守相关法律法规。

📃 开源说明
采用MIT开源协议，具体内容可以参考LICENSE文件。

