from enum import Enum

class PetState(Enum):
    """宠物状态枚举"""
    EGG = "蛋"
    BABY = "幼年"
    CHILD = "童年"
    TEEN = "青少年"
    ADULT = "成年"
    ELDER = "老年"

class PetMood(Enum):
    """宠物心情枚举"""
    ECSTATIC = "狂喜"
    HAPPY = "快乐"
    CONTENT = "满足"
    NEUTRAL = "一般"
    SAD = "悲伤"
    DEPRESSED = "抑郁"
    ANGRY = "生气"

class PetPersonality(Enum):
    """宠物性格类型"""
    PLAYFUL = "顽皮"      # 喜欢玩耍
    LAZY = "懒惰"        # 喜欢休息
    HUNGRY = "贪吃"      # 容易饿
    CLEAN = "爱干净"     # 讨厌脏乱
    AFFECTIONATE = "黏人" # 需要关注
    INDEPENDENT = "独立" # 喜欢独处
    CURIOUS = "好奇"     # 喜欢探索

class EmotionType(Enum):
    """情感类型枚举"""
    JOY = "愉悦"
    EXCITEMENT = "兴奋"
    CALM = "平静"
    ANXIETY = "焦虑"
    FEAR = "恐惧"
    ANGER = "愤怒"
    SADNESS = "悲伤"
    LOVE = "喜爱"
    CURIOSITY = "好奇"
    GRATITUDE = "感激"
    PRIDE = "自豪"
    ENVY = "嫉妒"
