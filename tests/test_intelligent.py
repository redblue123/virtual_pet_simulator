#!/usr/bin/env python3
"""
测试 intelligent.py 模块中的 IntelligentPet 类
"""

import unittest
import os
import sys

# 添加项目根目录到 Python 搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pet.intelligent import IntelligentPet

class TestIntelligentPet(unittest.TestCase):
    """测试 IntelligentPet 类的功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.pet = IntelligentPet('智能测试宠物')
    
    def test_initialization(self):
        """测试智能宠物初始化"""
        self.assertEqual(self.pet.name, '智能测试宠物')
        self.assertIsNotNone(self.pet.reinforcement_learning)
        self.assertIsNotNone(self.pet.behavior_tree)
        self.assertIsNotNone(self.pet.learning_system)
    
    def test_execute_spontaneous_action(self):
        """测试执行自发行为"""
        result = self.pet.execute_spontaneous_action()
        self.assertIsInstance(result, str)
    
    def test_execute_behavior_tree_action(self):
        """测试执行行为树动作"""
        result = self.pet.execute_behavior_tree_action()
        self.assertIsInstance(result, str)
        self.assertIn('行为树执行状态', result)
    
    def test_reinforcement_learning(self):
        """测试强化学习系统"""
        rl = self.pet.reinforcement_learning
        # 测试获取离散状态
        state = rl.get_discrete_state()
        self.assertIsInstance(state, tuple)
        
        # 测试选择动作
        action = rl.choose_action(state)
        self.assertIsInstance(action, (str, type(None)))
    
    def test_learning_system(self):
        """测试学习系统"""
        ls = self.pet.learning_system
        # 测试记录行为
        ls.record_behavior('feed', '喂食成功', {})
        # 记录行为应该没有返回值
        
        # 测试获取偏好
        preferences = ls.get_preferences()
        self.assertIsInstance(preferences, dict)
        self.assertIn('feed', preferences)

if __name__ == '__main__':
    unittest.main()
