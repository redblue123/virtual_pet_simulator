#!/usr/bin/env python3
"""
测试 base.py 模块中的 Pet 类
"""

import unittest
import tempfile
import os
import sys

# 添加项目根目录到 Python 搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pet.base import Pet
from pet.enums import PetState

class TestPet(unittest.TestCase):
    """测试 Pet 类的功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.pet = Pet('测试宠物')
    
    def test_initialization(self):
        """测试宠物初始化"""
        self.assertEqual(self.pet.name, '测试宠物')
        self.assertEqual(self.pet.species, '未知')
        self.assertEqual(self.pet.state, PetState.BABY)
        self.assertIsNotNone(self.pet.last_update_time)
    
    def test_feed(self):
        """测试喂食功能"""
        # 先让宠物饥饿度增加
        self.pet.hunger = 50.0
        initial_hunger = float(self.pet.get_status()['hunger'].split('/')[0])
        result = self.pet.feed('普通食物')
        self.assertIn('喂食成功', result)
        new_hunger = float(self.pet.get_status()['hunger'].split('/')[0])
        self.assertLess(new_hunger, initial_hunger)  # 喂食后饥饿度应该降低
    
    def test_play(self):
        """测试玩耍功能"""
        result = self.pet.play('普通游戏')
        self.assertIn('玩耍成功', result)
    
    def test_clean(self):
        """测试清洁功能"""
        # 先让宠物清洁度降低
        self.pet.hygiene = 50.0
        initial_hygiene = float(self.pet.get_status()['hygiene'].split('/')[0])
        result = self.pet.clean()
        self.assertIn('成功', result)
        new_hygiene = float(self.pet.get_status()['hygiene'].split('/')[0])
        self.assertGreater(new_hygiene, initial_hygiene)
    
    def test_sleep(self):
        """测试睡觉功能"""
        result = self.pet.sleep()
        self.assertIn('开始睡觉', result)
        self.assertTrue(self.pet.is_sleeping)
    
    def test_wake_up(self):
        """测试醒来功能"""
        self.pet.sleep()  # 先让宠物睡觉
        result = self.pet.wake_up()
        self.assertIn('醒来', result)
        self.assertFalse(self.pet.is_sleeping)
    
    def test_train(self):
        """测试训练功能"""
        result = self.pet.train('speed')
        self.assertIn('训练成功', result)
        self.assertIn('speed', self.pet.skills)
    
    def test_change_color(self):
        """测试改变颜色功能"""
        initial_color = self.pet.color
        result = self.pet.change_color('白色')
        self.assertIn('颜色已更改', result)
        self.assertEqual(self.pet.color, '白色')
    
    def test_get_status(self):
        """测试获取状态功能"""
        status = self.pet.get_status()
        self.assertIsInstance(status, dict)
        self.assertIn('name', status)
        self.assertIn('species', status)
        self.assertIn('age', status)
        self.assertIn('mood', status)
        self.assertIn('hunger', status)
        self.assertIn('energy', status)
        self.assertIn('hygiene', status)
    
    def test_save_and_load(self):
        """测试保存和加载功能"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # 保存宠物数据
            save_result = self.pet.save_to_file(temp_file)
            self.assertIn('已保存到', save_result)
            
            # 加载宠物数据
            loaded_pet = Pet.load_from_file(temp_file)
            self.assertIsInstance(loaded_pet, Pet)
            self.assertEqual(loaded_pet.name, self.pet.name)
            self.assertEqual(loaded_pet.species, self.pet.species)
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_update(self):
        """测试状态更新功能"""
        initial_age = self.pet.age_in_days
        # 强制更新状态
        self.pet.update()
        # 年龄应该增加
        self.assertGreaterEqual(self.pet.age_in_days, initial_age)

if __name__ == '__main__':
    unittest.main()
