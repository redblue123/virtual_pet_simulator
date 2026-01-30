#!/usr/bin/env python3
"""
测试 emotion.py 模块中的 EmotionalSystem 类
"""

import unittest
import os
import sys

# 添加项目根目录到 Python 搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pet.base import Pet

class TestEmotionalSystem(unittest.TestCase):
    """测试 EmotionalSystem 类的功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.pet = Pet('测试宠物')
        self.emotion_system = self.pet.emotional_system
    
    def test_initialization(self):
        """测试情感系统初始化"""
        self.assertIsNotNone(self.emotion_system)
        self.assertIsInstance(self.emotion_system.emotions, dict)
    
    def test_trigger_emotion(self):
        """测试触发情感"""
        from pet.enums import EmotionType
        initial_emotion_value = self.emotion_system.emotions[self.emotion_system.get_dominant_emotion()]
        event = self.emotion_system.trigger_emotion(EmotionType.JOY, 0.5, '测试触发')
        self.assertIsInstance(event, object)
        # 情感值应该增加
        new_emotion_value = self.emotion_system.emotions[self.emotion_system.get_dominant_emotion()]
        self.assertGreater(new_emotion_value, initial_emotion_value)
    
    def test_get_dominant_emotion(self):
        """测试获取主导情感"""
        dominant_emotion = self.emotion_system.get_dominant_emotion()
        self.assertIsInstance(dominant_emotion, object)
    
    def test_get_emotional_state(self):
        """测试获取情感状态"""
        emotional_state = self.emotion_system.get_emotional_state()
        self.assertIsInstance(emotional_state, dict)
        self.assertIn('dominant_emotion', emotional_state)
        self.assertIn('emotions', emotional_state)
        self.assertIn('recent_emotions', emotional_state)
    
    def test_get_emotion_intensity(self):
        """测试获取特定情感的强度"""
        from pet.enums import EmotionType
        intensity = self.emotion_system.get_emotion_intensity(EmotionType.JOY)
        self.assertIsInstance(intensity, (int, float))
        self.assertGreaterEqual(intensity, 0.0)
        self.assertLessEqual(intensity, 1.0)

if __name__ == '__main__':
    unittest.main()
