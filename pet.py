# pet.py - 虚拟宠物类
import random
import json
import time
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
from collections import defaultdict, Counter

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

class VirtualPet:
    def __init__(self, name="未命名", species="未知"):
        # 基础信息
        self.name = name
        self.species = species  # 可扩展为不同物种
        self.birthday = datetime.now()
        self.age_in_days = 0
        
        # 状态系统
        self.state = PetState.EGG
        self.mood = PetMood.NEUTRAL
        self.health = 100.0
        self.hunger = 0.0        # 0-100，越高越饿
        self.energy = 100.0      # 0-100
        self.hygiene = 100.0     # 0-100，越低越脏
        self.happiness = 50.0    # 0-100
        self.weight = 1.0        # 公斤
        
        # 性格系统（随机生成或遗传）
        self.personality_traits = self._generate_personality()
        self.favorite_activities = []
        self.dislikes = []
        
        # 成长系统
        self.experience = 0
        self.level = 1
        self.skills = {
            "intelligence": 1,   # 智力
            "strength": 1,       # 力量
            "speed": 1,          # 速度
            "social": 1,         # 社交
        }
        
        # 记忆与关系
        self.memories = []       # 重大事件记忆
        self.relationship_with_owner = 50  # 0-100
        self.routine_preferences = defaultdict(int)
        
        # 外观特征（随机生成）
        self.color = random.choice(["白色", "棕色", "黑色", "斑点", "条纹"])
        self.size = "微小"
        self.accessories = []    # 装饰品
        
        # 时间追踪
        self.last_update_time = time.time()
        self.needs_update = True
        
        # 特殊状态
        self.is_sleeping = False
        self.is_sick = False
        self.sickness_type = None
        
        print(f"✨ 新宠物 {name} 诞生了！")
    
    def _generate_personality(self):
        """生成随机性格组合"""
        all_traits = list(PetPersonality)
        # 随机选择2-3个主要性格特征
        num_traits = random.randint(2, 3)
        selected = random.sample(all_traits, num_traits)
        
        # 为每个特征分配强度
        traits = {}
        for trait in selected:
            traits[trait] = random.uniform(0.7, 1.0)
        
        # 可能有一个弱特征
        if random.random() < 0.3:
            weak_trait = random.choice([t for t in all_traits if t not in selected])
            traits[weak_trait] = random.uniform(0.3, 0.5)
        
        return traits
    
    def update(self, current_time=None):
        """更新宠物状态（随时间变化）"""
        if current_time is None:
            current_time = time.time()
        
        # 计算时间差（秒）
        time_passed = current_time - self.last_update_time
        hours_passed = time_passed / 3600  # 转换为小时
        
        # 防止时间跳跃过大
        if hours_passed > 24:
            hours_passed = 24
        
        # 更新基本需求（每小时变化）
        self._update_needs(hours_passed)
        
        # 更新年龄
        self._update_age()
        
        # 更新心情
        self._update_mood()
        
        # 检查健康状态
        self._check_health()
        
        # 更新成长状态
        self._update_growth()
        
        self.last_update_time = current_time
        self.needs_update = False
    
    def _update_needs(self, hours_passed):
        """随时间更新需求值"""
        # 饥饿增长（根据性格调整）
        hunger_rate = 3.0  # 每小时饥饿增长
        
        # 贪吃性格饿得更快
        if PetPersonality.HUNGRY in self.personality_traits:
            hunger_rate *= 1.5
        
        self.hunger = min(100, self.hunger + hunger_rate * hours_passed)
        
        # 能量恢复或消耗
        if self.is_sleeping:
            # 睡眠时恢复能量
            energy_rate = 15.0  # 每小时恢复
            self.energy = min(100, self.energy + energy_rate * hours_passed)
        else:
            # 活跃时消耗能量
            energy_rate = 2.0  # 每小时消耗
            self.energy = max(0, self.energy - energy_rate * hours_passed)
        
        # 清洁度下降（除非爱干净性格）
        hygiene_rate = 1.0
        if PetPersonality.CLEAN in self.personality_traits:
            hygiene_rate *= 0.5  # 爱干净的宠物脏得慢
        
        self.hygiene = max(0, self.hygiene - hygiene_rate * hours_passed)
        
        # 快乐度受其他因素影响
        happiness_change = 0
        
        # 饥饿影响快乐
        if self.hunger > 70:
            happiness_change -= 0.5 * hours_passed
        elif self.hunger < 30:
            happiness_change += 0.2 * hours_passed
        
        # 清洁度影响快乐
        if self.hygiene < 30:
            happiness_change -= 0.3 * hours_passed
        
        # 能量影响快乐
        if self.energy < 20:
            happiness_change -= 0.4 * hours_passed
        
        # 性格影响
        if PetPersonality.PLAYFUL in self.personality_traits and self.energy > 50:
            # 精力充沛的顽皮宠物更快乐
            happiness_change += 0.1 * hours_passed
        
        self.happiness = max(0, min(100, self.happiness + happiness_change))
    
    def _update_age(self):
        """更新年龄和生命周期阶段"""
        age_delta = datetime.now() - self.birthday
        self.age_in_days = age_delta.days
        
        # 根据年龄更新生命阶段
        if self.age_in_days < 2:
            self.state = PetState.EGG
        elif self.age_in_days < 10:
            self.state = PetState.BABY
        elif self.age_in_days < 30:
            self.state = PetState.CHILD
        elif self.age_in_days < 90:
            self.state = PetState.TEEN
        elif self.age_in_days < 365:
            self.state = PetState.ADULT
        else:
            self.state = PetState.ELDER
        
        # 更新大小
        size_map = {
            PetState.EGG: "微小",
            PetState.BABY: "很小",
            PetState.CHILD: "小",
            PetState.TEEN: "中等",
            PetState.ADULT: "大",
            PetState.ELDER: "大"
        }
        self.size = size_map.get(self.state, "中等")
    
    def _update_mood(self):
        """根据状态计算当前心情"""
        mood_score = 0
        
        # 健康影响
        mood_score += self.health / 2
        
        # 快乐度影响
        mood_score += self.happiness
        
        # 饥饿影响
        if self.hunger > 80:
            mood_score -= 30
        elif self.hunger > 50:
            mood_score -= 15
        
        # 清洁度影响
        if self.hygiene < 20:
            mood_score -= 20
        
        # 能量影响
        if self.energy < 10:
            mood_score -= 25
        
        # 关系影响
        mood_score += self.relationship_with_owner * 0.5
        
        # 确定心情等级
        if mood_score >= 180:
            self.mood = PetMood.ECSTATIC
        elif mood_score >= 150:
            self.mood = PetMood.HAPPY
        elif mood_score >= 120:
            self.mood = PetMood.CONTENT
        elif mood_score >= 80:
            self.mood = PetMood.NEUTRAL
        elif mood_score >= 50:
            self.mood = PetMood.SAD
        elif mood_score >= 20:
            self.mood = PetMood.DEPRESSED
        else:
            self.mood = PetMood.ANGRY
    
    def _check_health(self):
        """检查健康状态"""
        health_penalty = 0
        
        # 极端饥饿伤害健康
        if self.hunger > 90:
            health_penalty += 0.5
        
        # 肮脏环境导致生病
        if self.hygiene < 10:
            health_penalty += 0.3
        
        # 长期不快乐影响健康
        if self.happiness < 20:
            health_penalty += 0.2
        
        # 应用健康变化
        self.health = max(0, self.health - health_penalty)
        
        # 检查是否生病
        if not self.is_sick:
            sick_chance = 0
            if self.hygiene < 15:
                sick_chance += 0.1
            if self.health < 30:
                sick_chance += 0.2
            if self.happiness < 20:
                sick_chance += 0.1
            
            if random.random() < sick_chance:
                self._get_sick()
        else:
            # 如果正在生病，恢复或恶化
            recovery_chance = 0.1
            if self.health > 70 and self.hygiene > 50:
                recovery_chance = 0.3
            
            if random.random() < recovery_chance:
                self._recover_from_sickness()
    
    def _get_sick(self):
        """宠物生病"""
        sickness_types = ["感冒", "消化不良", "皮肤病", "疲劳"]
        self.sickness_type = random.choice(sickness_types)
        self.is_sick = True
        self.health -= 10
        self._add_memory(f"生病了（{self.sickness_type}）")
    
    def _recover_from_sickness(self):
        """从疾病中恢复"""
        self.is_sick = False
        self.sickness_type = None
        self._add_memory("从疾病中恢复了")
    
    def _update_growth(self):
        """更新成长和技能"""
        # 根据活动增加经验
        if self.happiness > 60:
            self.experience += 1
        
        # 升级检查
        exp_needed = self.level * 100
        if self.experience >= exp_needed:
            self.level_up()
    
    def level_up(self):
        """升级宠物"""
        self.level += 1
        self.experience = 0
        
        # 随机提升一个技能
        skill_to_up = random.choice(list(self.skills.keys()))
        self.skills[skill_to_up] += 1
        
        # 恢复一些状态
        self.health = min(100, self.health + 20)
        self.happiness = min(100, self.happiness + 30)
        
        self._add_memory(f"升到了 {self.level} 级！{skill_to_up} 提升了")
    
    def _add_memory(self, memory_text):
        """添加记忆"""
        memory = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "text": memory_text,
            "age": self.age_in_days
        }
        self.memories.append(memory)
        
        # 限制记忆数量
        if len(self.memories) > 50:
            self.memories = self.memories[-50:]
    
    # ========== 玩家交互方法 ==========
    
    def feed(self, food_type="普通食物"):
        """喂食宠物"""
        if self.is_sleeping:
            return "宠物正在睡觉，无法喂食"
        
        food_effects = {
            "普通食物": {"hunger": -30, "happiness": 5, "weight": 0.1},
            "美味大餐": {"hunger": -50, "happiness": 15, "weight": 0.2},
            "健康食品": {"hunger": -25, "health": 10, "weight": 0.05},
            "零食": {"hunger": -10, "happiness": 10, "weight": 0.02}
        }
        
        effect = food_effects.get(food_type, food_effects["普通食物"])
        
        # 应用效果
        self.hunger = max(0, self.hunger + effect["hunger"])
        self.happiness = min(100, self.happiness + effect.get("happiness", 0))
        self.health = min(100, self.health + effect.get("health", 0))
        self.weight += effect.get("weight", 0)
        
        # 贪吃性格额外快乐
        if PetPersonality.HUNGRY in self.personality_traits:
            self.happiness += 5
        
        self._add_memory(f"吃了{self.name}一份{food_type}")
        
        # 记录喂食偏好
        self.routine_preferences["feed"] += 1
        
        return f"喂食成功！{self.name}看起来很开心"
    
    def play(self, game_type="普通游戏"):
        """和宠物玩耍"""
        if self.is_sleeping:
            return "宠物正在睡觉，无法玩耍"
        
        if self.energy < 20:
            return "宠物太累了，需要休息"
        
        game_effects = {
            "普通游戏": {"energy": -15, "happiness": 20, "experience": 10},
            "捡球游戏": {"energy": -20, "happiness": 25, "skills": ["strength", "speed"]},
            "智力游戏": {"energy": -10, "happiness": 15, "skills": ["intelligence"]},
            "社交游戏": {"energy": -5, "happiness": 30, "skills": ["social"]}
        }
        
        effect = game_effects.get(game_type, game_effects["普通游戏"])
        
        # 应用效果
        self.energy = max(0, self.energy + effect["energy"])
        self.happiness = min(100, self.happiness + effect["happiness"])
        self.experience += effect.get("experience", 0)
        
        # 提升技能
        for skill in effect.get("skills", []):
            self.skills[skill] += 0.5
        
        # 顽皮性格额外快乐
        if PetPersonality.PLAYFUL in self.personality_traits:
            self.happiness += 10
        
        # 懒惰性格消耗更多能量
        if PetPersonality.LAZY in self.personality_traits:
            self.energy -= 5
        
        self._add_memory(f"玩了{game_type}游戏")
        
        # 记录游戏偏好
        self.routine_preferences["play"] += 1
        
        return f"玩耍成功！{self.name}玩得很开心"
    
    def clean(self):
        """清洁宠物"""
        if self.is_sleeping:
            return "宠物正在睡觉，无法清洁"
        
        hygiene_gain = 50
        
        # 爱干净性格更享受清洁
        if PetPersonality.CLEAN in self.personality_traits:
            hygiene_gain = 70
            self.happiness += 20
        else:
            self.happiness += 5
        
        self.hygiene = min(100, self.hygiene + hygiene_gain)
        
        # 清洁有助于健康
        if self.is_sick and self.sickness_type == "皮肤病":
            self.health += 10
        
        self._add_memory("被清洁了")
        
        return f"清洁成功！{self.name}现在很干净"
    
    def sleep(self):
        """让宠物睡觉"""
        if self.is_sleeping:
            return "宠物已经在睡觉了"
        
        self.is_sleeping = True
        self._add_memory("去睡觉了")
        
        return f"{self.name}开始睡觉了，晚安！"
    
    def wake_up(self):
        """叫醒宠物"""
        if not self.is_sleeping:
            return "宠物已经醒着了"
        
        self.is_sleeping = False
        
        # 醒来后的心情受睡眠质量影响
        if self.energy > 80:
            self.happiness += 10
            wake_message = f"{self.name}精神饱满地醒来了！"
        else:
            wake_message = f"{self.name}睡眼惺忪地醒来了"
        
        self._add_memory("醒来了")
        return wake_message
    
    def treat_sickness(self, medicine="普通药物"):
        """治疗宠物疾病"""
        if not self.is_sick:
            return "宠物没有生病"
        
        medicine_effects = {
            "普通药物": {"health": 30, "recovery_chance": 0.5},
            "特效药": {"health": 50, "recovery_chance": 0.8},
            "自然疗法": {"health": 20, "happiness": 10, "recovery_chance": 0.4}
        }
        
        effect = medicine_effects.get(medicine, medicine_effects["普通药物"])
        
        self.health = min(100, self.health + effect["health"])
        self.happiness += effect.get("happiness", 0)
        
        # 检查是否恢复
        if random.random() < effect["recovery_chance"]:
            self._recover_from_sickness()
            result = f"治疗成功！{self.name}从{self.sickness_type}中恢复了"
        else:
            result = f"治疗有些效果，但{self.name}还需要休息"
        
        self._add_memory("接受了治疗")
        return result
    
    def train(self, skill_type="intelligence"):
        """训练宠物技能"""
        if self.is_sleeping:
            return "宠物正在睡觉，无法训练"
        
        if self.energy < 30:
            return "宠物太累了，无法训练"
        
        if skill_type not in self.skills:
            return f"无效的技能类型：{skill_type}"
        
        # 训练消耗和效果
        energy_cost = 20
        skill_gain = 1
        
        # 根据性格调整
        if PetPersonality.LAZY in self.personality_traits:
            energy_cost += 10
            self.happiness -= 5
        
        self.energy = max(0, self.energy - energy_cost)
        self.skills[skill_type] += skill_gain
        self.experience += 15
        self.happiness += 5
        
        skill_names = {
            "intelligence": "智力",
            "strength": "力量",
            "speed": "速度",
            "social": "社交"
        }
        
        self._add_memory(f"进行了{skill_names[skill_type]}训练")
        
        return f"训练成功！{self.name}的{skill_names[skill_type]}提升了"
    
    def change_color(self, new_color):
        """更改宠物毛发颜色"""
        if self.is_sleeping:
            return "宠物正在睡觉，无法更改颜色"
        
        available_colors = ["白色", "棕色", "黑色", "斑点", "条纹", "金色", "银色", "蓝色", "红色", "紫色", "橘色", "梨花"]
        
        if new_color not in available_colors:
            return f"无效的颜色。可用颜色：{', '.join(available_colors)}"
        
        old_color = self.color
        self.color = new_color
        self._add_memory(f"毛发颜色从{old_color}变成了{new_color}")
        
        return f"颜色更改成功！{self.name}现在是{new_color}的了"
    
    def get_available_colors(self):
        """获取可用的颜色列表"""
        return ["白色", "棕色", "黑色", "斑点", "条纹", "金色", "银色", "蓝色", "红色", "紫色", "橘色", "梨花"]
    
    def get_status(self):
        """获取宠物状态摘要"""
        needs_update = self.needs_update
        if needs_update:
            self.update()
        
        status = {
            "name": self.name,
            "species": self.species,
            "age": f"{self.age_in_days}天",
            "state": self.state.value,
            "mood": self.mood.value,
            "level": self.level,
            "health": f"{self.health:.1f}/100",
            "hunger": f"{self.hunger:.1f}/100",
            "energy": f"{self.energy:.1f}/100",
            "hygiene": f"{self.hygiene:.1f}/100",
            "happiness": f"{self.happiness:.1f}/100",
            "weight": f"{self.weight:.1f}kg",
            "relationship": f"{self.relationship_with_owner:.1f}/100",
            "is_sleeping": self.is_sleeping,
            "is_sick": self.is_sick,
            "sickness": self.sickness_type if self.is_sick else "健康",
            "personality": [f"{t.value}({s:.1f})" for t, s in self.personality_traits.items()],
            "skills": self.skills,
            "color": self.color,
            "size": self.size
        }
        
        return status
    
    def get_needs_summary(self):
        """获取需求摘要（用于UI显示）"""
        needs = []
        
        if self.hunger > 70:
            needs.append(("饥饿", "高"))
        elif self.hunger > 40:
            needs.append(("饥饿", "中"))
        
        if self.energy < 30:
            needs.append(("疲劳", "高"))
        elif self.energy < 60:
            needs.append(("疲劳", "中"))
        
        if self.hygiene < 30:
            needs.append(("清洁", "高"))
        elif self.hygiene < 60:
            needs.append(("清洁", "中"))
        
        if self.happiness < 30:
            needs.append(("不开心", "高"))
        elif self.happiness < 60:
            needs.append(("不开心", "中"))
        
        if self.health < 50:
            needs.append(("健康", "警告"))
        
        return needs
    
    def save_to_file(self, filename):
        """保存宠物数据到文件"""
        data = {
            "name": self.name,
            "species": self.species,
            "birthday": self.birthday.isoformat(),
            "age_in_days": self.age_in_days,
            "state": self.state.value,
            "mood": self.mood.value,
            "health": self.health,
            "hunger": self.hunger,
            "energy": self.energy,
            "hygiene": self.hygiene,
            "happiness": self.happiness,
            "weight": self.weight,
            "personality_traits": {k.value: v for k, v in self.personality_traits.items()},
            "experience": self.experience,
            "level": self.level,
            "skills": self.skills,
            "memories": self.memories,
            "relationship_with_owner": self.relationship_with_owner,
            "routine_preferences": dict(self.routine_preferences),
            "color": self.color,
            "size": self.size,
            "is_sleeping": self.is_sleeping,
            "is_sick": self.is_sick,
            "sickness_type": self.sickness_type,
            "last_update_time": self.last_update_time,
            "accessories": self.accessories,
            "needs_update": self.needs_update
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 保存强化学习数据（如果有）
        if hasattr(self, 'reinforcement_learning'):
            rl_filename = filename.replace('.json', '_rl.json')
            self.reinforcement_learning.save_learning_data(rl_filename)
        
        return True
    
    @classmethod
    def load_from_file(cls, filename):
        """从文件加载宠物数据"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 创建新宠物
        pet = cls(name=data["name"], species=data["species"])
        pet.birthday = datetime.fromisoformat(data["birthday"])
        pet.age_in_days = data["age_in_days"]
        
        # 恢复状态
        pet.state = PetState(data["state"])
        pet.mood = PetMood(data["mood"])
        pet.health = data["health"]
        pet.hunger = data["hunger"]
        pet.energy = data["energy"]
        pet.hygiene = data["hygiene"]
        pet.happiness = data["happiness"]
        pet.weight = data["weight"]
        
        # 恢复性格
        pet.personality_traits = {
            PetPersonality(k): v for k, v in data["personality_traits"].items()
        }
        
        # 恢复成长数据
        pet.experience = data["experience"]
        pet.level = data["level"]
        pet.skills = data["skills"]
        pet.memories = data["memories"]
        pet.relationship_with_owner = data["relationship_with_owner"]
        
        # 恢复偏好
        pet.routine_preferences = defaultdict(int, data.get("routine_preferences", {}))
        
        # 恢复外观
        pet.color = data["color"]
        pet.size = data["size"]
        pet.accessories = data.get("accessories", [])
        
        # 恢复特殊状态
        pet.is_sleeping = data["is_sleeping"]
        pet.is_sick = data["is_sick"]
        pet.sickness_type = data["sickness_type"]
        
        # 恢复时间
        pet.last_update_time = data["last_update_time"]
        pet.needs_update = data.get("needs_update", True)
        
        # 加载强化学习数据（如果有）
        if hasattr(pet, 'reinforcement_learning'):
            rl_filename = filename.replace('.json', '_rl.json')
            if os.path.exists(rl_filename):
                pet.reinforcement_learning.load_learning_data(rl_filename)
        
        # 立即更新状态
        pet.update()
        
        print(f"✨ 已加载宠物: {pet.name} (等级 {pet.level})")
        return pet


class IntelligentPet(VirtualPet): # 核心功能：让宠物能够自发行为和从交互中学习
    """智能宠物类 - 第二阶段强化学习智能体"""
    def __init__(self, name="未命名", species="未知"):
        super().__init__(name, species)
        
        # 智能体相关属性
        self.decision_system = DecisionSystem(self)
        self.behavior_system = BehaviorSystem(self)
        self.learning_system = LearningSystem(self)
        
        # 第二阶段：强化学习系统
        self.reinforcement_learning = ReinforcementLearningSystem(self)
        
        # 第二阶段：行为树系统
        self.behavior_tree = BehaviorTreeBuilder.build_pet_behavior_tree()
        
        # 主动行为相关
        self.last_spontaneous_action = time.time()
        self.spontaneous_action_cooldown = 30  # 自发行为冷却时间（秒）
        
        # 用户偏好记录
        self.user_preferences = defaultdict(Counter)
        
        print(f"🧠 智能宠物 {name} 已激活！")
        print(f"🚀 强化学习系统已启动！")
        print(f"🌳 行为树系统已初始化！")
    
    def update(self, current_time=None):
        """更新宠物状态，包括智能体决策"""
        super().update(current_time)
        
        # 检查是否需要执行自发行为
        if current_time is None:
            current_time = time.time()
        
        if current_time - self.last_spontaneous_action > self.spontaneous_action_cooldown:
            self.execute_spontaneous_action()
            self.last_spontaneous_action = current_time
    
    def execute_spontaneous_action(self):
        """执行自发行为（使用强化学习和行为树）"""
        # 第二阶段：优先使用强化学习决策
        state_before = self.reinforcement_learning.get_discrete_state()
        action = self.reinforcement_learning.choose_action(state_before)
        
        if action:
            # 执行行为
            result = self._execute_action(action)
            
            # 评估执行后的状态
            state_after = self.reinforcement_learning.get_discrete_state()
            
            # 计算奖励
            reward = self.reinforcement_learning.calculate_reward(
                dict(state_before), action, dict(state_after)
            )
            
            # 强化学习
            self.reinforcement_learning.learn(state_before, action, reward, state_after, False)
            
            # 记录行为结果
            self.learning_system.record_behavior(action, result, {})
            
            return result
        else:
            # 备用：使用行为树
            return self.execute_behavior_tree_action()
    
    def execute_behavior_tree_action(self):
        """执行行为树动作"""
        status = self.behavior_tree.execute(self)
        return f"行为树执行状态: {status}"
    
    def _execute_action(self, action):
        """执行具体行为"""
        if action == "feed":
            return self.feed("普通食物")
        elif action == "play":
            return self.play("普通游戏")
        elif action == "sleep":
            return self.sleep()
        elif action == "clean":
            return self.clean()
        elif action == "train":
            return self.train("intelligence")
        elif action == "explore":
            return self._explore()
        elif action == "rest":
            return self._rest()
        else:
            return f"执行行为: {action}"
    
    def _explore(self):
        """探索环境"""
        if self.energy < 15:
            return f"{self.name}：'我太累了，不想动'"
        
        energy_cost = 15
        happiness_gain = 10
        intelligence_gain = 0.5
        
        self.energy = max(0, self.energy - energy_cost)
        self.happiness = min(100, self.happiness + happiness_gain)
        self.skills["intelligence"] += intelligence_gain
        
        return f"{self.name}正在好奇地探索周围环境"
    
    def _rest(self):
        """休息恢复"""
        energy_gain = 20
        health_gain = 5
        
        self.energy = min(100, self.energy + energy_gain)
        self.health = min(100, self.health + health_gain)
        
        return f"{self.name}正在休息恢复精力"
    
    def interact_with_user(self, interaction_type, **kwargs):
        """与用户交互并学习"""
        # 执行传统交互
        if interaction_type == "feed":
            food_type = kwargs.get("food_type", "普通食物")
            result = self.feed(food_type)
        elif interaction_type == "play":
            game_type = kwargs.get("game_type", "普通游戏")
            result = self.play(game_type)
        elif interaction_type == "sleep":
            result = self.sleep()
        elif interaction_type == "wake_up":
            result = self.wake_up()
        elif interaction_type == "clean":
            result = self.clean()
        elif interaction_type == "train":
            skill_type = kwargs.get("skill_type", "intelligence")
            result = self.train(skill_type)
        elif interaction_type == "change_color":
            new_color = kwargs.get("new_color", "白色")
            result = self.change_color(new_color)
        else:
            result = "未知交互类型"
        
        # 记录用户交互偏好
        self.learning_system.record_user_interaction(interaction_type, kwargs)
        
        # 学习系统更新
        self.learning_system.learn_from_interaction(interaction_type, result)
        
        # 第二阶段：强化学习更新
        state_before = self.reinforcement_learning.get_discrete_state()
        # 将用户交互映射到强化学习动作
        rl_action = self._map_interaction_to_rl_action(interaction_type)
        if rl_action:
            state_after = self.reinforcement_learning.get_discrete_state()
            reward = self.reinforcement_learning.calculate_reward(
                dict(state_before), rl_action, dict(state_after)
            )
            self.reinforcement_learning.learn(state_before, rl_action, reward, state_after, False)
        
        return result
    
    def _map_interaction_to_rl_action(self, interaction_type):
        """将用户交互映射到强化学习动作"""
        mapping = {
            "feed": "feed",
            "play": "play",
            "sleep": "sleep",
            "wake_up": "explore",  # 醒来后探索
            "clean": "clean",
            "train": "train"
        }
        return mapping.get(interaction_type)
    
    def get_intelligent_status(self):
        """获取智能体状态"""
        base_status = self.get_status()
        
        # 添加智能体相关信息
        intelligent_status = {
            "decision_confidence": self.decision_system.get_confidence(),
            "predicted_needs": self.decision_system.predict_needs(),
            "learned_preferences": dict(self.learning_system.get_preferences()),
            "spontaneous_action_rate": self.behavior_system.get_action_rate(),
            "next_action_prediction": self.decision_system.predict_next_action(),
            # 第二阶段：强化学习信息
            "reinforcement_learning": self.reinforcement_learning.get_learning_stats()
        }
        
        base_status.update(intelligent_status)
        return base_status
    
    def get_learning_progress(self):
        """获取学习进度"""
        return {
            "exploration_rate": self.reinforcement_learning.exploration_rate,
            "average_reward": self.reinforcement_learning.average_reward,
            "learning_steps": self.reinforcement_learning.learning_steps,
            "q_table_size": sum(len(v) for v in self.reinforcement_learning.q_table.values())
        }
    
    def beg_for_food(self):
        """向主人乞讨食物"""
        self.happiness += 5  # 乞讨行为增加一点快乐
        return f"{self.name}：'我饿了，想吃东西！'"
    
    def groom(self):
        """自我清洁"""
        hygiene_gain = 15
        self.hygiene = min(100, self.hygiene + hygiene_gain)
        self.happiness += 5
        return f"{self.name}正在舔毛清洁自己"
    
    def spontaneous_play(self):
        """自发玩耍"""
        if self.energy < 20:
            return f"{self.name}：'我太累了，想休息'"
        
        energy_cost = 10
        happiness_gain = 15
        
        self.energy = max(0, self.energy - energy_cost)
        self.happiness = min(100, self.happiness + happiness_gain)
        
        return f"{self.name}正在开心地玩耍"


class DecisionSystem:
    """决策系统 - 基于规则的决策逻辑"""
    def __init__(self, pet):
        self.pet = pet
        self.decision_history = []
        self.confidence_level = 0.5
    
    def evaluate_state(self):
        """评估当前状态"""
        needs = self.pet.get_needs_summary()
        
        # 优先级评估
        priority_needs = {
            "health": 0,
            "hunger": 0,
            "energy": 0,
            "hygiene": 0,
            "happiness": 0
        }
        
        # 健康优先级
        if self.pet.health < 30:
            priority_needs["health"] = 5
        elif self.pet.health < 60:
            priority_needs["health"] = 3
        
        # 饥饿优先级
        if self.pet.hunger > 80:
            priority_needs["hunger"] = 4
        elif self.pet.hunger > 60:
            priority_needs["hunger"] = 2
        
        # 精力优先级
        if self.pet.energy < 20:
            priority_needs["energy"] = 4
        elif self.pet.energy < 40:
            priority_needs["energy"] = 2
        
        # 清洁优先级
        if self.pet.hygiene < 20:
            priority_needs["hygiene"] = 3
        elif self.pet.hygiene < 40:
            priority_needs["hygiene"] = 1
        
        # 快乐优先级
        if self.pet.happiness < 20:
            priority_needs["happiness"] = 3
        elif self.pet.happiness < 40:
            priority_needs["happiness"] = 1
        
        # 特殊状态
        if self.pet.is_sick:
            priority_needs["health"] = max(priority_needs["health"], 5)
        
        if self.pet.is_sleeping:
            priority_needs["energy"] = 0  # 睡觉时不考虑精力
        
        return {
            "needs": needs,
            "priority_needs": priority_needs,
            "current_state": self.pet.state.value,
            "mood": self.pet.mood.value,
            "is_sleeping": self.pet.is_sleeping,
            "is_sick": self.pet.is_sick
        }
    
    def make_decision(self, state_evaluation):
        """基于状态做出决策"""
        if self.pet.is_sleeping:
            # 检查是否需要醒来
            if self.pet.energy > 90:
                return "wake_up"
            return None
        
        # 基于优先级需求做出决策
        priority_needs = state_evaluation["priority_needs"]
        highest_priority = max(priority_needs.items(), key=lambda x: x[1])
        
        if highest_priority[1] == 0:
            # 所有需求都得到满足，随机选择一个愉悦行为
            return random.choice(["play", "explore"])
        
        # 根据最高优先级需求选择行为
        if highest_priority[0] == "health":
            if self.pet.is_sick:
                return "rest"
            else:
                return "rest"
        elif highest_priority[0] == "hunger":
            return "beg_for_food"
        elif highest_priority[0] == "energy":
            return "sleep"
        elif highest_priority[0] == "hygiene":
            return "groom"
        elif highest_priority[0] == "happiness":
            return "play"
        
        return "explore"
    
    def get_confidence(self):
        """获取决策信心"""
        # 基于状态评估的确定性计算信心
        return min(1.0, self.confidence_level + len(self.decision_history) * 0.01)
    
    def predict_needs(self):
        """预测未来需求"""
        # 基于当前状态和历史模式预测需求
        predictions = []
        
        if self.pet.hunger > 60:
            predictions.append("hunger")
        if self.pet.energy < 40:
            predictions.append("energy")
        if self.pet.hygiene < 40:
            predictions.append("hygiene")
        
        return predictions
    
    def predict_next_action(self):
        """预测下一个行为"""
        state_evaluation = self.evaluate_state()
        return self.make_decision(state_evaluation)


class BehaviorSystem:
    """行为系统 - 执行自主行为"""
    def __init__(self, pet):
        self.pet = pet
        self.action_history = []
        self.action_success_rate = defaultdict(float)
    
    def execute_action(self, action):
        """执行选定的行为"""
        if action is None:
            return "无行为执行"
        
        # 记录行为
        self.action_history.append((action, time.time()))
        
        # 执行行为
        if action == "wake_up":
            return self.pet.wake_up()
        elif action == "sleep":
            return self.pet.sleep()
        elif action == "beg_for_food":
            return self._beg_for_food()
        elif action == "groom":
            return self._groom()
        elif action == "play":
            return self._spontaneous_play()
        elif action == "rest":
            return self._rest()
        elif action == "explore":
            return self._explore()
        
        return f"执行行为: {action}"
    
    def _beg_for_food(self):
        """向主人乞讨食物"""
        self.pet.happiness += 5  # 乞讨行为增加一点快乐
        return f"{self.pet.name}：'我饿了，想吃东西！'"
    
    def _groom(self):
        """自我清洁"""
        hygiene_gain = 15
        self.pet.hygiene = min(100, self.pet.hygiene + hygiene_gain)
        self.pet.happiness += 5
        return f"{self.pet.name}正在舔毛清洁自己"
    
    def _spontaneous_play(self):
        """自发玩耍"""
        if self.pet.energy < 20:
            return f"{self.pet.name}：'我太累了，想休息'"
        
        energy_cost = 10
        happiness_gain = 15
        
        self.pet.energy = max(0, self.pet.energy - energy_cost)
        self.pet.happiness = min(100, self.pet.happiness + happiness_gain)
        
        return f"{self.pet.name}正在开心地玩耍"
    
    def _rest(self):
        """休息恢复"""
        energy_gain = 20
        health_gain = 5
        
        self.pet.energy = min(100, self.pet.energy + energy_gain)
        self.pet.health = min(100, self.pet.health + health_gain)
        
        return f"{self.pet.name}正在休息恢复精力"
    
    def _explore(self):
        """探索环境"""
        if self.pet.energy < 15:
            return f"{self.pet.name}：'我太累了，不想动'"
        
        energy_cost = 15
        happiness_gain = 10
        intelligence_gain = 0.5
        
        self.pet.energy = max(0, self.pet.energy - energy_cost)
        self.pet.happiness = min(100, self.pet.happiness + happiness_gain)
        self.pet.skills["intelligence"] += intelligence_gain
        
        return f"{self.pet.name}正在好奇地探索周围环境"
    
    def get_action_rate(self):
        """获取行为频率"""
        # 计算最近行为频率
        recent_actions = [a for a, t in self.action_history if time.time() - t < 3600]
        return len(recent_actions) / 60.0  # 每小时行为数


class LearningSystem:
    """学习系统 - 记录用户偏好和行为模式"""
    def __init__(self, pet):
        self.pet = pet
        self.interaction_history = []
        self.behavior_effects = defaultdict(list)
        self.time_based_preferences = defaultdict(Counter)
    
    def record_user_interaction(self, interaction_type, kwargs):
        """记录用户交互"""
        timestamp = time.time()
        hour = datetime.fromtimestamp(timestamp).hour
        
        self.interaction_history.append({
            "type": interaction_type,
            "kwargs": kwargs,
            "timestamp": timestamp,
            "hour": hour
        })
        
        # 记录时间偏好
        self.time_based_preferences[hour][interaction_type] += 1
        
        # 记录具体偏好
        if interaction_type == "feed" and "food_type" in kwargs:
            self.pet.user_preferences["food"][kwargs["food_type"]] += 1
        elif interaction_type == "play" and "game_type" in kwargs:
            self.pet.user_preferences["game"][kwargs["game_type"]] += 1
        elif interaction_type == "train" and "skill_type" in kwargs:
            self.pet.user_preferences["skill"][kwargs["skill_type"]] += 1
    
    def record_behavior(self, action, result, state_evaluation):
        """记录行为结果"""
        self.behavior_effects[action].append({
            "result": result,
            "state_before": state_evaluation,
            "timestamp": time.time()
        })
    
    def learn_from_interaction(self, interaction_type, result):
        """从交互中学习"""
        # 简单的强化学习 - 基于结果调整偏好
        if "成功" in result or "开心" in result:
            # 正面结果，增加该行为偏好
            self.pet.routine_preferences[interaction_type] += 2
        elif "无法" in result or "太累" in result:
            # 负面结果，减少该行为偏好
            if self.pet.routine_preferences[interaction_type] > 0:
                self.pet.routine_preferences[interaction_type] -= 1
    
    def get_preferences(self):
        """获取学习到的偏好"""
        preferences = {}
        
        # 食物偏好
        if self.pet.user_preferences["food"]:
            preferences["food"] = dict(self.pet.user_preferences["food"])
        
        # 游戏偏好
        if self.pet.user_preferences["game"]:
            preferences["game"] = dict(self.pet.user_preferences["game"])
        
        # 技能训练偏好
        if self.pet.user_preferences["skill"]:
            preferences["skill"] = dict(self.pet.user_preferences["skill"])
        
        # 时间偏好
        time_preferences = {}
        for hour, counts in self.time_based_preferences.items():
            if counts:
                time_preferences[hour] = dict(counts)
        
        if time_preferences:
            preferences["time"] = time_preferences
        
        return preferences
    
    def predict_user_action(self, hour=None):
        """预测用户可能的行为"""
        if hour is None:
            hour = datetime.now().hour
        
        # 基于时间的行为预测
        if hour in self.time_based_preferences:
            most_common = self.time_based_preferences[hour].most_common(1)
            if most_common:
                return most_common[0][0]
        
        # 基于历史频率的预测
        if self.interaction_history:
            recent_interactions = [i["type"] for i in self.interaction_history[-10:]]
            if recent_interactions:
                return Counter(recent_interactions).most_common(1)[0][0]
        
        return None


class ReinforcementLearningSystem:
    """强化学习系统 - 基于Q-learning的智能决策"""
    def __init__(self, pet, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995, min_exploration=0.1):
        self.pet = pet
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration = min_exploration
        
        # Q-table 存储
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # 经验回放缓存
        self.replay_buffer = []
        self.buffer_size = 1000
        
        # 状态离散化参数
        self.state_bins = {
            "health": [0, 30, 60, 100],
            "hunger": [0, 30, 60, 100],
            "energy": [0, 30, 60, 100],
            "hygiene": [0, 30, 60, 100],
            "happiness": [0, 30, 60, 100]
        }
        
        # 动作空间
        self.actions = ["feed", "play", "sleep", "clean", "train", "explore", "rest"]
        
        # 学习统计
        self.learning_steps = 0
        self.total_reward = 0
        self.average_reward = 0
        
        print("🧠 强化学习系统已初始化！")
    
    def get_discrete_state(self):
        """获取离散化的状态"""
        state = {
            "health": self._discretize_value(self.pet.health, self.state_bins["health"]),
            "hunger": self._discretize_value(self.pet.hunger, self.state_bins["hunger"]),
            "energy": self._discretize_value(self.pet.energy, self.state_bins["energy"]),
            "hygiene": self._discretize_value(self.pet.hygiene, self.state_bins["hygiene"]),
            "happiness": self._discretize_value(self.pet.happiness, self.state_bins["happiness"]),
            "is_sleeping": int(self.pet.is_sleeping),
            "is_sick": int(self.pet.is_sick)
        }
        
        # 转换为元组以便作为字典键
        return tuple(sorted(state.items()))
    
    def _discretize_value(self, value, bins):
        """将连续值离散化"""
        for i, bin_threshold in enumerate(bins):
            if value <= bin_threshold:
                return i
        return len(bins) - 1
    
    def choose_action(self, state):
        """基于ε-贪婪策略选择动作"""
        # 探索
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        # 利用
        else:
            q_values = self.q_table[state]
            if q_values:
                return max(q_values, key=q_values.get)
            else:
                return random.choice(self.actions)
    
    def calculate_reward(self, state_before, action, state_after):
        """计算奖励"""
        reward = 0
        
        # 基础奖励：维持良好状态
        if state_after["health"] >= 3:
            reward += 1.0
        if state_after["hunger"] <= 1:
            reward += 1.0
        if state_after["energy"] >= 3:
            reward += 0.5
        if state_after["hygiene"] >= 3:
            reward += 0.5
        if state_after["happiness"] >= 3:
            reward += 1.0
        
        # 惩罚：不良状态
        if state_after["health"] <= 0:
            reward -= 2.0
        if state_after["hunger"] >= 3:
            reward -= 1.5
        if state_after["energy"] <= 0:
            reward -= 1.0
        if state_after["hygiene"] <= 0:
            reward -= 0.5
        if state_after["happiness"] <= 0:
            reward -= 1.0
        
        # 特殊状态奖励/惩罚
        if state_after["is_sick"]:
            reward -= 2.0
        if state_after["is_sleeping"] and state_after["energy"] < 3:
            reward += 0.5
        
        # 动作特定奖励
        if action == "feed" and state_after["hunger"] < state_before["hunger"]:
            reward += 1.0
        if action == "play" and state_after["happiness"] > state_before["happiness"]:
            reward += 0.8
        if action == "sleep" and state_after["energy"] > state_before["energy"]:
            reward += 0.6
        if action == "clean" and state_after["hygiene"] > state_before["hygiene"]:
            reward += 0.4
        if action == "train" and any(skill > 1 for skill in self.pet.skills.values()):
            reward += 0.3
        if action == "explore":
            reward += 0.2
        if action == "rest" and state_after["health"] > state_before["health"]:
            reward += 0.5
        
        return reward
    
    def learn(self, state_before, action, reward, state_after, done):
        """执行Q-learning学习"""
        # 存储经验
        self.replay_buffer.append((state_before, action, reward, state_after, done))
        
        # 限制缓冲区大小
        if len(self.replay_buffer) > self.buffer_size:
            self.replay_buffer.pop(0)
        
        # 从缓冲区采样批次
        batch_size = min(32, len(self.replay_buffer))
        batch = random.sample(self.replay_buffer, batch_size)
        
        for s, a, r, s_next, d in batch:
            # 计算目标Q值
            if d:
                target_q = r
            else:
                next_max_q = max(self.q_table[s_next].values()) if self.q_table[s_next] else 0
                target_q = r + self.discount_factor * next_max_q
            
            # 更新Q值
            current_q = self.q_table[s].get(a, 0)
            new_q = current_q + self.learning_rate * (target_q - current_q)
            self.q_table[s][a] = new_q
        
        # 衰减探索率
        self.exploration_rate = max(self.min_exploration, self.exploration_rate * self.exploration_decay)
        
        # 更新学习统计
        self.learning_steps += 1
        self.total_reward += reward
        self.average_reward = self.total_reward / self.learning_steps
        
        return reward
    
    def get_learning_stats(self):
        """获取学习统计信息"""
        return {
            "learning_steps": self.learning_steps,
            "total_reward": self.total_reward,
            "average_reward": self.average_reward,
            "exploration_rate": self.exploration_rate,
            "buffer_size": len(self.replay_buffer),
            "q_table_size": sum(len(v) for v in self.q_table.values())
        }
    
    def save_learning_data(self, filename):
        """保存学习数据"""
        data = {
            "q_table": {str(k): v for k, v in self.q_table.items()},
            "learning_steps": self.learning_steps,
            "total_reward": self.total_reward,
            "exploration_rate": self.exploration_rate,
            "replay_buffer": self.replay_buffer
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def load_learning_data(self, filename):
        """加载学习数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 恢复Q-table
            self.q_table = defaultdict(lambda: defaultdict(float))
            for state_str, actions in data.get("q_table", {}).items():
                # 解析状态字符串
                state = eval(state_str)
                self.q_table[state] = defaultdict(float, actions)
            
            # 恢复其他参数
            self.learning_steps = data.get("learning_steps", 0)
            self.total_reward = data.get("total_reward", 0)
            self.exploration_rate = data.get("exploration_rate", self.exploration_rate)
            self.replay_buffer = data.get("replay_buffer", [])
            
            print("🧠 学习数据加载成功！")
            return True
        except Exception as e:
            print(f"❌ 加载学习数据失败: {e}")
            return False


# 行为树系统
class BehaviorTreeNode:
    """行为树节点基类"""
    def __init__(self, name=""):
        self.name = name
    
    def execute(self, pet):
        """执行节点"""
        raise NotImplementedError

class BehaviorTreeStatus:
    """行为树状态"""
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"

class CompositeNode(BehaviorTreeNode):
    """组合节点基类"""
    def __init__(self, name=""):
        super().__init__(name)
        self.children = []
    
    def add_child(self, child):
        """添加子节点"""
        self.children.append(child)
        return self

class SequenceNode(CompositeNode):
    """序列节点 - 按顺序执行子节点，直到一个失败"""
    def execute(self, pet):
        for child in self.children:
            status = child.execute(pet)
            if status != BehaviorTreeStatus.SUCCESS:
                return status
        return BehaviorTreeStatus.SUCCESS

class SelectorNode(CompositeNode):
    """选择节点 - 按顺序执行子节点，直到一个成功"""
    def execute(self, pet):
        for child in self.children:
            status = child.execute(pet)
            if status != BehaviorTreeStatus.FAILURE:
                return status
        return BehaviorTreeStatus.FAILURE

class ParallelNode(CompositeNode):
    """并行节点 - 同时执行所有子节点"""
    def __init__(self, name="", success_threshold=1):
        super().__init__(name)
        self.success_threshold = success_threshold
    
    def execute(self, pet):
        success_count = 0
        failure_count = 0
        
        for child in self.children:
            status = child.execute(pet)
            if status == BehaviorTreeStatus.SUCCESS:
                success_count += 1
            elif status == BehaviorTreeStatus.FAILURE:
                failure_count += 1
        
        if success_count >= self.success_threshold:
            return BehaviorTreeStatus.SUCCESS
        elif failure_count == len(self.children):
            return BehaviorTreeStatus.FAILURE
        else:
            return BehaviorTreeStatus.RUNNING

class DecoratorNode(BehaviorTreeNode):
    """装饰节点基类"""
    def __init__(self, child, name=""):
        super().__init__(name)
        self.child = child

class InverterNode(DecoratorNode):
    """取反节点 - 反转子节点的结果"""
    def execute(self, pet):
        status = self.child.execute(pet)
        if status == BehaviorTreeStatus.SUCCESS:
            return BehaviorTreeStatus.FAILURE
        elif status == BehaviorTreeStatus.FAILURE:
            return BehaviorTreeStatus.SUCCESS
        else:
            return status

class RepeaterNode(DecoratorNode):
    """重复节点 - 重复执行子节点"""
    def __init__(self, child, count=-1, name=""):
        super().__init__(child, name)
        self.count = count  # -1 表示无限重复
        self.current_count = 0
    
    def execute(self, pet):
        if self.count == -1 or self.current_count < self.count:
            status = self.child.execute(pet)
            if status != BehaviorTreeStatus.RUNNING:
                self.current_count += 1
            return BehaviorTreeStatus.RUNNING
        else:
            self.current_count = 0
            return BehaviorTreeStatus.SUCCESS

class SucceederNode(DecoratorNode):
    """成功节点 - 总是返回成功"""
    def execute(self, pet):
        self.child.execute(pet)
        return BehaviorTreeStatus.SUCCESS

class ConditionNode(BehaviorTreeNode):
    """条件节点 - 检查条件"""
    def __init__(self, condition_func, name=""):
        super().__init__(name)
        self.condition_func = condition_func
    
    def execute(self, pet):
        if self.condition_func(pet):
            return BehaviorTreeStatus.SUCCESS
        else:
            return BehaviorTreeStatus.FAILURE

class ActionNode(BehaviorTreeNode):
    """行为节点 - 执行具体行为"""
    def __init__(self, action_func, name=""):
        super().__init__(name)
        self.action_func = action_func
    
    def execute(self, pet):
        result = self.action_func(pet)
        if result:
            return BehaviorTreeStatus.SUCCESS
        else:
            return BehaviorTreeStatus.FAILURE

class BehaviorTree:
    """行为树"""
    def __init__(self, root_node):
        self.root = root_node
    
    def execute(self, pet):
        """执行行为树"""
        return self.root.execute(pet)

class BehaviorTreeBuilder:
    """行为树构建器"""
    @staticmethod
    def build_pet_behavior_tree():
        """构建宠物行为树"""
        # 健康检查序列
        health_check = SequenceNode("健康检查")
        health_check.add_child(ConditionNode(lambda p: p.health < 30, "健康低于30"))
        health_check.add_child(ActionNode(lambda p: p.rest(), "休息恢复"))
        
        # 饥饿检查序列
        hunger_check = SequenceNode("饥饿检查")
        hunger_check.add_child(ConditionNode(lambda p: p.hunger > 70, "饥饿高于70"))
        hunger_check.add_child(ActionNode(lambda p: p.beg_for_food(), "乞讨食物"))
        
        # 能量检查序列
        energy_check = SequenceNode("能量检查")
        energy_check.add_child(ConditionNode(lambda p: p.energy < 20, "能量低于20"))
        energy_check.add_child(ActionNode(lambda p: p.sleep(), "睡觉恢复"))
        
        # 清洁检查序列
        hygiene_check = SequenceNode("清洁检查")
        hygiene_check.add_child(ConditionNode(lambda p: p.hygiene < 30, "清洁低于30"))
        hygiene_check.add_child(ActionNode(lambda p: p.groom(), "自我清洁"))
        
        # 快乐检查序列
        happiness_check = SequenceNode("快乐检查")
        happiness_check.add_child(ConditionNode(lambda p: p.happiness < 30, "快乐低于30"))
        happiness_check.add_child(ActionNode(lambda p: p.spontaneous_play(), "自发玩耍"))
        
        # 主要行为选择器
        main_selector = SelectorNode("主要行为选择")
        main_selector.add_child(health_check)
        main_selector.add_child(hunger_check)
        main_selector.add_child(energy_check)
        main_selector.add_child(hygiene_check)
        main_selector.add_child(happiness_check)
        
        # 探索行为
        exploration = SequenceNode("探索行为")
        exploration.add_child(ConditionNode(lambda p: p.energy > 40, "能量高于40"))
        exploration.add_child(ActionNode(lambda p: p.explore(), "探索环境"))
        
        # 最终行为选择器
        final_selector = SelectorNode("最终行为选择")
        final_selector.add_child(main_selector)
        final_selector.add_child(exploration)
        final_selector.add_child(ActionNode(lambda p: p.rest(), "默认休息"))
        
        return BehaviorTree(final_selector)