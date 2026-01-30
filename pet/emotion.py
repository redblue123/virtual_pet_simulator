from datetime import datetime
from collections import defaultdict
from .enums import EmotionType

class EmotionEvent:
    """情感事件"""
    def __init__(self, emotion_type, intensity, trigger, timestamp=None):
        self.emotion_type = emotion_type
        self.intensity = intensity  # 0.0-1.0
        self.trigger = trigger      # 触发原因
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self):
        return {
            "emotion_type": self.emotion_type.value,
            "intensity": self.intensity,
            "trigger": self.trigger,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @classmethod
    def from_dict(cls, data):
        emotion_type = EmotionType(data["emotion_type"])
        intensity = data["intensity"]
        trigger = data["trigger"]
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        return cls(emotion_type, intensity, trigger, timestamp)

class EmotionalSystem:
    """情感系统"""
    def __init__(self, pet):
        self.pet = pet
        
        # 情感维度（0.0-1.0）
        self.emotions = {
            EmotionType.JOY: 0.5,
            EmotionType.EXCITEMENT: 0.3,
            EmotionType.CALM: 0.6,
            EmotionType.ANXIETY: 0.1,
            EmotionType.FEAR: 0.1,
            EmotionType.ANGER: 0.1,
            EmotionType.SADNESS: 0.1,
            EmotionType.LOVE: 0.5,
            EmotionType.CURIOSITY: 0.4
        }
        
        # 情感历史
        self.emotion_history = []
        self.max_history_length = 100
        
        # 情感触发记忆
        self.emotion_triggers = defaultdict(list)
        
    def trigger_emotion(self, emotion_type, intensity, trigger):
        """触发情感"""
        # 确保强度在有效范围内
        intensity = max(0.0, min(1.0, intensity))
        
        # 应用情感强度
        self.emotions[emotion_type] = min(1.0, self.emotions[emotion_type] + intensity)
        
        # 创建情感事件
        event = EmotionEvent(emotion_type, intensity, trigger)
        self.emotion_history.append(event)
        
        # 限制历史长度
        if len(self.emotion_history) > self.max_history_length:
            self.emotion_history.pop(0)
        
        # 记录触发因素
        self.emotion_triggers[emotion_type].append((trigger, intensity))
        
        # 情感衰减（情感会随时间减弱）
        self._decay_emotions()
        
        return event
    
    def _decay_emotions(self):
        """情感衰减"""
        decay_rate = 0.05  # 衰减速率
        for emotion_type in self.emotions:
            if emotion_type != EmotionType.CALM:  # 平静状态不衰减
                self.emotions[emotion_type] = max(0.1, self.emotions[emotion_type] - decay_rate)
        
        # 平静状态会自然恢复
        self.emotions[EmotionType.CALM] = min(0.8, self.emotions[EmotionType.CALM] + 0.02)
    
    def get_dominant_emotion(self):
        """获取当前主导情感"""
        return max(self.emotions.items(), key=lambda x: x[1])[0]
    
    def get_emotional_state(self):
        """获取情感状态"""
        return {
            "dominant_emotion": self.get_dominant_emotion().value,
            "emotions": {k.value: v for k, v in self.emotions.items()},
            "recent_emotions": [e.to_dict() for e in self.emotion_history[-5:]]
        }
    
    def get_emotion_intensity(self, emotion_type):
        """获取特定情感的强度"""
        return self.emotions.get(emotion_type, 0.0)
    
    def to_dict(self):
        """序列化情感系统状态"""
        return {
            "emotions": {k.value: v for k, v in self.emotions.items()},
            "emotion_history": [e.to_dict() for e in self.emotion_history]
        }
    
    def from_dict(self, data):
        """从序列化数据恢复情感系统状态"""
        if "emotions" in data:
            for emotion_name, intensity in data["emotions"].items():
                try:
                    emotion_type = EmotionType(emotion_name)
                    self.emotions[emotion_type] = intensity
                except ValueError:
                    pass
        
        if "emotion_history" in data:
            self.emotion_history = [EmotionEvent.from_dict(e) for e in data["emotion_history"]]
