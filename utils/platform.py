#!/usr/bin/env python3
import os
import sys
import platform

class PlatformUtils:
    """跨平台工具类"""
    
    @staticmethod
    def get_platform():
        """获取当前平台"""
        return platform.system()
    
    @staticmethod
    def is_windows():
        """检查是否为Windows平台"""
        return os.name == 'nt'
    
    @staticmethod
    def is_linux():
        """检查是否为Linux平台"""
        return sys.platform.startswith('linux')
    
    @staticmethod
    def is_macos():
        """检查是否为macOS平台"""
        return sys.platform == 'darwin'
    
    @staticmethod
    def clear_screen():
        """清屏（跨平台兼容）"""
        if PlatformUtils.is_windows():
            os.system('cls')
        else:
            os.system('clear')
    
    @staticmethod
    def get_path_separator():
        """获取路径分隔符"""
        return os.path.sep
    
    @staticmethod
    def join_path(*args):
        """拼接路径（跨平台兼容）"""
        return os.path.join(*args)
    
    @staticmethod
    def get_absolute_path(relative_path):
        """获取绝对路径"""
        return os.path.abspath(relative_path)
    
    @staticmethod
    def get_current_directory():
        """获取当前目录"""
        return os.getcwd()
    
    @staticmethod
    def ensure_directory_exists(directory):
        """确保目录存在"""
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def get_user_home_directory():
        """获取用户主目录"""
        return os.path.expanduser('~')
    
    @staticmethod
    def get_temp_directory():
        """获取临时目录"""
        return os.path.join(os.environ.get('TEMP', '/tmp'), 'virtual_pet_simulator')
