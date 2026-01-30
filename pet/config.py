"""宠物配置文件"""

class PetConfig:
    """宠物配置类"""
    # 状态更新参数
    UPDATE_INTERVAL = 1  # 小时
    
    # 需求值更新速率
    HUNGER_RATE = 3.0  # 每小时饥饿增长
    ENERGY_RATE_ACTIVE = 2.0  # 活跃时每小时能量消耗
    ENERGY_RATE_SLEEP = 15.0  # 睡眠时每小时能量恢复
    HYGIENE_RATE = 1.0  # 每小时清洁度下降
    
    # 快乐度影响参数
    HAPPINESS_HUNGER_PENALTY = 0.5  # 饥饿时快乐度下降速率
    HAPPINESS_HUNGER_BONUS = 0.2  # 饱腹时快乐度上升速率
    HAPPINESS_HYGIENE_PENALTY = 0.3  # 脏时快乐度下降速率
    HAPPINESS_ENERGY_PENALTY = 0.4  # 疲劳时快乐度下降速率
    
    # 阈值
    HUNGER_THRESHOLD = 70  # 饥饿阈值
    ENERGY_THRESHOLD = 20  # 疲劳阈值
    HYGIENE_THRESHOLD = 30  # 脏阈值
    ENERGY_SLEEP_THRESHOLD = 50  # 睡眠阈值
    
    # 行为效果参数
    FEED_ENERGY_COST = 5  # 喂食消耗的能量
    PLAY_ENERGY_COST_BASE = 15  # 玩耍消耗的基础能量
    TRAIN_ENERGY_COST_BASE = 20  # 训练消耗的基础能量
    EXPLORE_ENERGY_COST = 15  # 探索消耗的能量
    REST_ENERGY_GAIN = 20  # 休息恢复的能量
    REST_HEALTH_GAIN = 5  # 休息恢复的健康值
    
    # 技能提升参数
    TRAIN_SKILL_GAIN = 1  # 训练提升的技能值
    EXPLORE_INTELLIGENCE_GAIN = 0.5  # 探索提升的智力值
    
    # 经验值参数
    PLAY_EXPERIENCE_GAIN = 10  # 玩耍获得的经验值
    TRAIN_EXPERIENCE_GAIN = 15  # 训练获得的经验值
    
    # 记忆参数
    MAX_MEMORY_LENGTH = 50  # 最大记忆长度
    
    # 自发行为参数
    SPONTANEOUS_ACTION_COOLDOWN = 30  # 自发行为冷却时间（秒）
    
    # 食物效果
    FOOD_EFFECTS = {
        "普通食物": {"hunger": -30, "happiness": 5, "weight": 0.1},
        "美味大餐": {"hunger": -50, "happiness": 15, "weight": 0.2},
        "健康食品": {"hunger": -25, "health": 10, "weight": 0.05},
        "零食": {"hunger": -10, "happiness": 10, "weight": 0.02}
    }
    
    # 游戏效果
    GAME_EFFECTS = {
        "普通游戏": {"energy": -15, "happiness": 20, "experience": 10},
        "捡球游戏": {"energy": -20, "happiness": 25, "skills": ["strength", "speed"]},
        "智力游戏": {"energy": -10, "happiness": 15, "skills": ["intelligence"]},
        "社交游戏": {"energy": -5, "happiness": 30, "skills": ["social"]}
    }
    
    # 清洁效果
    CLEAN_EFFECTS = {
        "毛发清理": {
            "hygiene_gain": 40,
            "happiness_gain": 10,
            "health_gain": 5,
            "emotion": "CALM",
            "emotion_intensity": 0.3,
            "description": "清理毛发",
            "memory": "被清理了毛发"
        },
        "刷牙": {
            "hygiene_gain": 20,
            "happiness_gain": 5,
            "health_gain": 15,
            "emotion": "ANXIETY",
            "emotion_intensity": 0.2,
            "description": "刷牙",
            "memory": "被刷了牙"
        },
        "洗澡": {
            "hygiene_gain": 60,
            "happiness_gain": 15,
            "health_gain": 10,
            "emotion": "EXCITEMENT",
            "emotion_intensity": 0.4,
            "description": "洗澡",
            "memory": "被洗了澡"
        },
        "修剪指甲": {
            "hygiene_gain": 15,
            "happiness_gain": 5,
            "health_gain": 3,
            "emotion": "ANXIETY",
            "emotion_intensity": 0.3,
            "description": "修剪指甲",
            "memory": "被修剪了指甲"
        }
    }
    
    # 性格影响因子
    PERSONALITY_FACTORS = {
        "HUNGRY": {
            "hunger_rate_multiplier": 1.5,
            "happiness_bonus": 5
        },
        "LAZY": {
            "energy_cost_multiplier": 1.5,
            "happiness_penalty": 5
        },
        "CLEAN": {
            "hygiene_rate_multiplier": 0.5,
            "hygiene_gain_multiplier": 1.3,
            "happiness_gain_multiplier": 1.5
        },
        "PLAYFUL": {
            "happiness_bonus": 10
        }
    }
    
    # 技能名称映射
    SKILL_NAMES = {
        "intelligence": "智力",
        "strength": "力量",
        "speed": "速度",
        "social": "社交"
    }
    
    # 可用颜色
    AVAILABLE_COLORS = ["白色", "棕色", "黑色", "斑点", "条纹", "金色", "银色", "蓝色", "红色", "紫色", "橘色", "梨花"]
    
    # 强化学习参数
    RL_LEARNING_RATE = 0.1
    RL_DISCOUNT_FACTOR = 0.9
    RL_EXPLORATION_RATE = 1.0
    RL_EXPLORATION_DECAY = 0.995
    RL_MIN_EXPLORATION = 0.1
    RL_BATCH_SIZE = 32
    RL_MAX_REPLAY_BUFFER_SIZE = 10000
    RL_ALPHA = 0.6  # 优先级指数
    RL_BETA = 0.4  # 重要性采样权重指数
    RL_BETA_INCREMENT = 0.001
    
    # 状态离散化参数
    STATE_BINS = {
        "hunger": [0, 30, 60, 100],
        "energy": [0, 30, 60, 100],
        "hygiene": [0, 30, 60, 100],
        "happiness": [0, 30, 60, 100],
        "health": [0, 30, 60, 100]
    }
    
    # 可能的动作
    RL_ACTIONS = ["feed", "play", "sleep", "clean", "train", "explore", "rest"]
