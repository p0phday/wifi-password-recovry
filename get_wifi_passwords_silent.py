#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Windows WiFi密码导出专业工具（终极优化版）
功能特性：
1. 完美解决GBK编码问题
2. 直接输出到当前目录
3. 增强的错误处理和日志记录
4. 支持中英文系统环境
"""

import os
import sys
import ctypes
import subprocess
import xml.etree.ElementTree as ET
from threading import Lock
from datetime import datetime

# 全局配置
OUTPUT_FILE = "WiFi_Passwords_Report.txt"
LOG_FILE = "WiFi_Export.log"
XML_NAMESPACE = {'ns': 'http://www.microsoft.com/networking/WLAN/profile/v1'}
print_lock = Lock()

def is_admin():
    """检查管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def hide_window():
    """隐藏控制台窗口"""
    try:
        if sys.executable.endswith("pythonw.exe"):
            return
            
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
    except:
        pass

def log_message(message, level="INFO"):
    """记录日志到文件和屏幕"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    with print_lock:
        print(log_entry)
        with open(LOG_FILE, 'a', encoding='utf-8') as log:
            log.write(log_entry + "\n")

def run_command_safely(command):
    """安全执行命令并处理编码问题"""
    try:
        # 使用二进制模式捕获输出
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True
        )
        
        # 尝试多种编码解码
        encodings = ['gbk', 'utf-8', 'cp936']
        for enc in encodings:
            try:
                return result.stdout.decode(enc).strip(), None
            except UnicodeDecodeError:
                continue
        
        # 如果所有编码都失败，使用替代方案
        return result.stdout.decode('gbk', errors='replace').strip(), None
        
    except subprocess.CalledProcessError as e:
        error_msg = f"命令执行失败: {e.stderr.decode('gbk', errors='ignore')}"
        return None, error_msg
    except Exception as e:
        return None, str(e)

def export_wifi_profiles():
    """导出WiFi配置文件并返回XML文件名列表"""
    log_message("开始导出WiFi配置文件...")
    
    # 使用临时变量存储XML文件名
    xml_files = []
    
    # 方案1: 使用netsh export (首选)
    output, error = run_command_safely(['netsh', 'wlan', 'export', 'profile', 'key=clear'])
    if error:
        log_message(f"方案1失败: {error}", "WARNING")
        
        # 方案2: 回退到逐个导出 (兼容性更强)
        log_message("尝试替代导出方案...")
        profiles_output, _ = run_command_safely(['netsh', 'wlan', 'show', 'profiles'])
        if profiles_output:
            for line in profiles_output.split('\n'):
                if "所有用户配置文件" in line or "All User Profile" in line:
                    try:
                        ssid = line.split(":")[1].strip()
                        cmd = f'netsh wlan export profile name="{ssid}" key=clear'
                        _, export_error = run_command_safely(cmd)
                        if export_error:
                            log_message(f"导出'{ssid}'失败: {export_error}", "WARNING")
                    except Exception as e:
                        log_message(f"处理SSID时出错: {str(e)}", "ERROR")
    
    # 收集生成的XML文件
    try:
        xml_files = [f for f in os.listdir() if f.endswith('.xml')]
        log_message(f"找到 {len(xml_files)} 个WiFi配置文件")
    except Exception as e:
        log_message(f"查找XML文件失败: {str(e)}", "ERROR")
    
    return xml_files

def parse_wifi_password(xml_file):
    """解析单个XML文件获取WiFi密码"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # 使用命名空间精确查找
        ssid_elem = root.find('.//ns:SSIDConfig/ns:SSID/ns:name', XML_NAMESPACE)
        ssid = ssid_elem.text if ssid_elem is not None else None
        
        key_elem = root.find('.//ns:MSM/ns:security/ns:sharedKey/ns:keyMaterial', XML_NAMESPACE)
        password = key_elem.text if key_elem is not None else None
        
        if not ssid or not password:
            raise ValueError("未找到有效的SSID或密码")
            
        return ssid, password
        
    except ET.ParseError:
        log_message(f"XML解析错误: {xml_file} 可能是无效的XML文件", "ERROR")
        return None, None
    except Exception as e:
        log_message(f"解析 {xml_file} 失败: {str(e)}", "ERROR")
        return None, None

def generate_report(wifi_data):
    """生成格式化的密码报告"""
    report = ["WiFi密码安全审计报告"]
    report.append("生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    report.append("=" * 60)
    
    for ssid, password in wifi_data.items():
        report.append(f"SSID名称: {ssid}")
        report.append(f"连接密码: {password}")
        report.append("-" * 60)
    
    report.append(f"\n总计发现 {len(wifi_data)} 个可用的WiFi配置")
    return "\n".join(report)

def main():
    # 检查管理员权限
    if not is_admin():
        log_message("需要管理员权限，正在尝试提权...", "WARNING")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1
            )
        except Exception as e:
            log_message(f"提权失败: {str(e)}", "ERROR")
        sys.exit(1)
    
    # 清除旧日志文件
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    
    log_message("=== WiFi密码导出工具启动 ===")
    
    # 导出配置文件
    xml_files = export_wifi_profiles()
    if not xml_files:
        log_message("未找到可导出的WiFi配置", "ERROR")
        sys.exit(1)
    
    # 解析密码
    wifi_passwords = {}
    successful = 0
    
    for xml_file in xml_files:
        ssid, password = parse_wifi_password(xml_file)
        if ssid and password:
            wifi_passwords[ssid] = password
            successful += 1
        try:
            os.remove(xml_file)
        except:
            pass
    
    # 生成报告
    if wifi_passwords:
        report_content = generate_report(wifi_passwords)
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(report_content)
            log_message(f"成功提取 {successful} 个WiFi密码", "SUCCESS")
            log_message(f"报告已保存到: {os.path.abspath(OUTPUT_FILE)}")
        except Exception as e:
            log_message(f"保存报告失败: {str(e)}", "ERROR")
    else:
        log_message("未提取到任何有效的WiFi密码", "WARNING")
    
    log_message("=== 工具执行完成 ===")

if __name__ == '__main__':
    hide_window()
    main()
