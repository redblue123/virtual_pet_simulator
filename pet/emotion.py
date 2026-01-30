from datetime import datetime, timedelta
from collections import defaultdict, deque
from .enums import EmotionType
import random

class EmotionEvent:
    """情感事件"""
    def __init__(self, emotion_type, intensity, trigger, timestamp=None):
        self.emotion_type = emotion_type
        self.intensity = intensity  # 0.0-1.0
        self.trigger = trigger      # 触发原因
        self.timestamp = timestamp or datetime.now()
        self.duration = random.uniform(1.0, 5.0)  # 情感持续时间（秒）
    
    def to_dict(self):
        return {
            "emotion_type": self.emotion_type.value,
            "intensity": self.intensity,
            "trigger": self.trigger,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": self.duration
        }
    
    @classmethod
    def from_dict(cls, data):
        emotion_type = EmotionType(data["emotion_type"])
        intensity = data["intensity"]
        trigger = data["trigger"]
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        event = cls(emotion_type, intensity, trigger, timestamp)
        event.duration = data.get("duration", random.uniform(1.0, 5.0))
        return event

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
            EmotionType.CURIOSITY: 0.4,
            EmotionType.GRATITUDE: 0.3,  # 新增情感：感激
            EmotionType.PRIDE: 0.2,       # 新增情感：自豪
            EmotionType.ENVY: 0.1         # 新增情感：嫉妒
        }
        
        # 情感历史
        self.emotion_history = deque(maxlen=200)  # 使用双端队列，自动限制长度
        
        # 情感触发记忆
        self.emotion_triggers = defaultdict(list)
        
        # 情感关联矩阵（情感之间的相互影响）
        self.emotion_connections = {
            EmotionType.JOY: {
                EmotionType.EXCITEMENT: 0.3,
                EmotionType.LOVE: 0.2,
                EmotionType.CALM: -0.2
            },
            EmotionType.EXCITEMENT: {
                EmotionType.JOY: 0.2,
                EmotionType.CURIOSITY: 0.3,
                EmotionType.ANXIETY: 0.1
            },
            EmotionType.ANGER: {
                EmotionType.SADNESS: 0.3,
                EmotionType.ANXIETY: 0.2,
                EmotionType.JOY: -0.5
            },
            EmotionType.SADNESS: {
                EmotionType.ANXIETY: 0.3,
                EmotionType.LOVE: -0.2
            },
            EmotionType.LOVE: {
                EmotionType.JOY: 0.3,
                EmotionType.CALM: 0.2,
                EmotionType.GRATITUDE: 0.3
            },
            EmotionType.FEAR: {
                EmotionType.ANXIETY: 0.5,
                EmotionType.SADNESS: 0.2
            },
            EmotionType.CURIOSITY: {
                EmotionType.EXCITEMENT: 0.3,
                EmotionType.JOY: 0.1
            }
        }
        
        # 情感表达库
        self.emotion_expressions = {
            EmotionType.JOY: [
                "欢快地摇尾巴",
                "蹦蹦跳跳地转圈",
                "发出愉悦的叫声",
                "扑到你怀里撒娇"
            ],
            EmotionType.EXCITEMENT: [
                "兴奋地跑来跑去",
                "不停地舔你的手",
                "尾巴摇得像小旗子",
                "急切地想和你玩耍"
            ],
            EmotionType.CALM: [
                "安静地趴在你身边",
                "闭着眼睛享受抚摸",
                "缓慢地摆动尾巴",
                "发出轻柔的呼噜声"
            ],
            EmotionType.ANXIETY: [
                "不安地踱步",
                "尾巴夹在两腿之间",
                "耳朵向后贴",
                "发出紧张的呜咽声"
            ],
            EmotionType.FEAR: [
                "蜷缩成一团",
                "躲到角落里",
                "毛发竖起",
                "发出害怕的叫声"
            ],
            EmotionType.ANGER: [
                "尾巴猛烈地摆动",
                "耳朵向后贴",
                "发出低吼",
                "避开你的触碰"
            ],
            EmotionType.SADNESS: [
                "无精打采地趴着",
                "尾巴下垂",
                "眼神空洞",
                "对玩耍失去兴趣"
            ],
            EmotionType.LOVE: [
                "温柔地舔你的手",
                "用头蹭你的腿",
                "蜷缩在你怀里",
                "跟着你到处走"
            ],
            EmotionType.CURIOSITY: [
                "歪着脑袋看你",
                "用鼻子嗅来嗅去",
                "尾巴高高竖起",
                "耳朵向前竖起"
            ],
            EmotionType.GRATITUDE: [
                "温柔地看着你",
                "轻轻舔你的脸",
                "安静地靠在你身边",
                "尾巴缓慢地摆动"
            ],
            EmotionType.PRIDE: [
                "昂首挺胸地走路",
                "尾巴高高竖起",
                "发出得意的叫声",
                "炫耀自己的技能"
            ],
            EmotionType.ENVY: [
                "盯着其他宠物看",
                "发出不满的声音",
                "试图吸引你的注意力",
                "尾巴快速摆动"
            ]
        }
        
        # 情感记忆
        self.emotion_memories = []
        self.max_memory_length = 50
        
        # 最近的情感状态
        self.recent_emotions = deque(maxlen=10)
    
    def trigger_emotion(self, emotion_type, intensity, trigger):
        """触发情感"""
        # 确保强度在有效范围内
        intensity = max(0.0, min(1.0, intensity))
        
        # 应用情感强度
        old_intensity = self.emotions[emotion_type]
        self.emotions[emotion_type] = min(1.0, self.emotions[emotion_type] + intensity)
        new_intensity = self.emotions[emotion_type]
        
        # 情感关联影响
        self._apply_emotion_connections(emotion_type, intensity)
        
        # 创建情感事件
        event = EmotionEvent(emotion_type, intensity, trigger)
        self.emotion_history.append(event)
        self.recent_emotions.append((emotion_type, new_intensity))
        
        # 记录触发因素
        self.emotion_triggers[emotion_type].append((trigger, intensity, datetime.now()))
        
        # 情感衰减（情感会随时间减弱）
        self._decay_emotions()
        
        # 形成情感记忆
        if intensity > 0.5:
            self._form_emotion_memory(emotion_type, intensity, trigger)
        
        return event
    
    def _apply_emotion_connections(self, emotion_type, intensity):
        """应用情感关联影响"""
        if emotion_type in self.emotion_connections:
            for connected_emotion, connection_strength in self.emotion_connections[emotion_type].items():
                influence = intensity * connection_strength
                if influence != 0:
                    new_intensity = self.emotions[connected_emotion] + influence
                    self.emotions[connected_emotion] = max(0.0, min(1.0, new_intensity))
    
    def _decay_emotions(self):
        """情感衰减"""
        decay_rate = 0.03  # 衰减速率
        for emotion_type in self.emotions:
            if emotion_type != EmotionType.CALM:  # 平静状态不衰减
                self.emotions[emotion_type] = max(0.05, self.emotions[emotion_type] - decay_rate)
        
        # 平静状态会自然恢复
        self.emotions[EmotionType.CALM] = min(0.8, self.emotions[EmotionType.CALM] + 0.03)
    
    def _form_emotion_memory(self, emotion_type, intensity, trigger):
        """形成情感记忆"""
        memory = {
            "emotion_type": emotion_type,
            "intensity": intensity,
            "trigger": trigger,
            "timestamp": datetime.now(),
            "recall_strength": intensity
        }
        self.emotion_memories.append(memory)
        
        # 限制记忆长度
        if len(self.emotion_memories) > self.max_memory_length:
            self.emotion_memories.pop(0)
    
    def get_dominant_emotion(self):
        """获取当前主导情感"""
        return max(self.emotions.items(), key=lambda x: x[1])[0]
    
    def get_emotional_state(self):
        """获取情感状态"""
        dominant = self.get_dominant_emotion()
        return {
            "dominant_emotion": dominant.value,
            "emotions": {k.value: v for k, v in self.emotions.items()},
            "recent_emotions": [e.to_dict() for e in list(self.emotion_history)[-5:]],
            "expression": self.get_emotion_expression(dominant),
            "mood": self.get_mood()
        }
    
    def get_emotion_expression(self, emotion_type):
        """获取情感表达"""
        if emotion_type in self.emotion_expressions:
            return random.choice(self.emotion_expressions[emotion_type])
        return "保持安静"
    
    def get_mood(self):
        """获取整体情绪状态"""
        joy = self.emotions[EmotionType.JOY]
        sadness = self.emotions[EmotionType.SADNESS]
        anger = self.emotions[EmotionType.ANGER]
        calm = self.emotions[EmotionType.CALM]
        
        if joy > 0.7:
            return "非常开心"
        elif joy > 0.4:
            return "开心"
        elif sadness > 0.6:
            return "悲伤"
        elif anger > 0.6:
            return "愤怒"
        elif calm > 0.7:
            return "平静"
        elif self.emotions[EmotionType.ANXIETY] > 0.6:
            return "焦虑"
        elif self.emotions[EmotionType.EXCITEMENT] > 0.7:
            return "兴奋"
        else:
            return "中性"
    
    def get_emotion_intensity(self, emotion_type):
        """获取特定情感的强度"""
        return self.emotions.get(emotion_type, 0.0)
    
    def recall_emotion_memory(self, trigger_similarity):
        """回忆情感记忆"""
        if not self.emotion_memories:
            return None
        
        # 按回忆强度排序
        sorted_memories = sorted(self.emotion_memories, key=lambda x: x["recall_strength"], reverse=True)
        
        # 随机选择一个强度较高的记忆
        strong_memories = [m for m in sorted_memories if m["recall_strength"] > 0.3]
        if strong_memories:
            memory = random.choice(strong_memories)
            # 减弱记忆强度
            memory["recall_strength"] *= 0.8
            return memory
        return None
    
    def update_emotional_state(self, time_passed):
        """更新情感状态（随时间）"""
        # 情感衰减
        decay_factor = time_passed / 60.0 * 0.05  # 每分钟衰减
        for emotion_type in self.emotions:
            if emotion_type != EmotionType.CALM:
                self.emotions[emotion_type] = max(0.05, self.emotions[emotion_type] - decay_factor)
        
        # 平静状态恢复
        self.emotions[EmotionType.CALM] = min(0.8, self.emotions[EmotionType.CALM] + decay_factor * 0.5)
    
    def to_dict(self):
        """序列化情感系统状态"""
        return {
            "emotions": {k.value: v for k, v in self.emotions.items()},
            "emotion_history": [e.to_dict() for e in self.emotion_history],
            "emotion_memories": [
                {
                    "emotion_type": m["emotion_type"].value,
                    "intensity": m["intensity"],
                    "trigger": m["trigger"],
                    "timestamp": m["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    "recall_strength": m["recall_strength"]
                }
                for m in self.emotion_memories
            ]
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
            self.emotion_history = deque([EmotionEvent.from_dict(e) for e in data["emotion_history"]], maxlen=200)
        
        if "emotion_memories" in data:
            self.emotion_memories = []
            for m in data["emotion_memories"]:
                try:
                    memory = {
                        "emotion_type": EmotionType(m["emotion_type"]),
                        "intensity": m["intensity"],
                        "trigger": m["trigger"],
                        "timestamp": datetime.strptime(m["timestamp"], "%Y-%m-%d %H:%M:%S"),
                        "recall_strength": m["recall_strength"]
                    }
                    self.emotion_memories.append(memory)
                except ValueError:
                    pass
