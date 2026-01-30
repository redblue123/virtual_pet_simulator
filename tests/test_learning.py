#!/usr/bin/env python3
"""
测试 learning.py 模块中的 LearningSystem 类
"""

import unittest
import os
import sys

# 添加项目根目录到 Python 搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pet.intelligent import IntelligentPet

class TestLearningSystem(unittest.TestCase):
    """测试 LearningSystem 类的功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.pet = IntelligentPet('测试宠物')
        self.learning_system = self.pet.learning_system
    
    def test_initialization(self):
        """测试学习系统初始化"""
        self.assertIsNotNone(self.learning_system)
        self.assertIsInstance(self.learning_system.behavior_history, list)
    
    def test_record_behavior(self):
        """测试记录行为"""
        initial_history_length = len(self.learning_system.behavior_history)
        
        # 记录行为
        self.learning_system.record_behavior('feed', '喂食成功', {})
        
        # 历史记录应该增加
        self.assertGreater(len(self.learning_system.behavior_history), initial_history_length)
    
    def test_record_user_interaction(self):
        """测试记录用户交互"""
        # 记录用户交互
        self.learning_system.record_user_interaction('feed', {'food_type': '普通食物'})
        # 交互记录应该被添加
        self.assertIn('feed', self.learning_system.user_interactions)
    
    def test_learn_from_interaction(self):
        """测试从交互中学习"""
        initial_history_length = len(self.learning_system.behavior_history)
        
        # 从交互中学习
        self.learning_system.learn_from_interaction('feed', '喂食成功')
        
        # 历史记录应该增加
        self.assertGreater(len(self.learning_system.behavior_history), initial_history_length)
    
    def test_get_preferences(self):
        """测试获取偏好"""
        # 记录一些行为
        self.learning_system.record_behavior('feed', '喂食成功', {})
        self.learning_system.record_behavior('play', '玩耍成功', {})
        
        # 获取偏好
        preferences = self.learning_system.get_preferences()
        self.assertIsInstance(preferences, dict)
        self.assertIn('feed', preferences)
        self.assertIn('play', preferences)
    
    def test_get_behavior_patterns(self):
        """测试获取行为模式"""
        # 记录一些行为
        for i in range(5):
            self.learning_system.record_behavior('feed', '喂食成功', {})
        for i in range(3):
            self.learning_system.record_behavior('play', '玩耍成功', {})
        
        # 获取行为模式
        patterns = self.learning_system.get_behavior_patterns()
        self.assertIsInstance(patterns, dict)
        self.assertIn('action_frequency', patterns)
        self.assertIn('feed', patterns['action_frequency'])
        self.assertIn('play', patterns['action_frequency'])
    
    def test_predict_behavior(self):
        """测试预测行为"""
        # 记录一些行为
        for i in range(5):
            self.learning_system.record_behavior('feed', '喂食成功', {})
        
        # 预测行为
        predicted_behavior = self.learning_system.predict_behavior({})
        self.assertIsInstance(predicted_behavior, str)

if __name__ == '__main__':
    unittest.main()
