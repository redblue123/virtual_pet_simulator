import random
import json
import time
import os
from datetime import datetime, timedelta
from collections import defaultdict
from .enums import PetState, PetMood, PetPersonality, EmotionType
from .emotion import EmotionalSystem
from .config import PetConfig

class Pet:
    """基础宠物类"""
    def __init__(self, name="未命名", species="未知"):
        """初始化宠物"""
        self.name = name
        self.species = species
        self.birth_time = time.time()
        self.age_in_days = 0
        
        # 基本属性
        self.health = 100.0
        self.hunger = 0.0
        self.energy = 100.0
        self.hygiene = 100.0
        self.happiness = 50.0
        self.weight = 1.0
        self.size = "小"
        self.color = "白色"
        
        # 状态
        self.state = PetState.BABY
        self.mood = PetMood.NEUTRAL
        self.is_sleeping = False
        self.is_sick = False
        self.sickness_type = None
        self.sleep_start_time = None
        self.sleep_duration = 0
        
        # 技能
        self.skills = {
            "intelligence": 0,
            "strength": 0,
            "speed": 0,
            "social": 0
        }
        self.experience = 0
        self.level = 1
        
        # 性格特质
        self.personality_traits = {}
        self._generate_personality()
        
        # 关系
        self.relationship_with_owner = 50.0
        
        # 记忆
        self.memories = []
        self.max_memory_length = PetConfig.MAX_MEMORY_LENGTH
        
        # 日常偏好
        self.routine_preferences = defaultdict(int)
        
        # 情感系统
        self.emotional_system = EmotionalSystem(self)
        
        # 状态更新标志
        self.needs_update = True
        self.last_update_time = time.time()
    
    def _generate_personality(self):
        """生成宠物性格"""
        for trait in PetPersonality:
            if random.random() > 0.7:  # 30% 几率获得该性格
                self.personality_traits[trait] = random.uniform(0.6, 1.0)
    
    def update(self, current_time=None):
        """更新宠物状态
        
        Args:
            current_time (float, optional): 当前时间戳，默认为None，使用time.time()
        
        Returns:
            None
        
        Notes:
            - 当时间间隔大于等于1小时时，会更新宠物的需求值、年龄和心情
            - 更新后会重置last_update_time和needs_update标志
            - 添加了防止递归调用的机制
        """
        # 防止递归调用
        if hasattr(self, '_updating') and self._updating:
            return
        
        if current_time is None:
            current_time = time.time()
        
        # 计算经过的时间
        hours_passed = (current_time - self.last_update_time) / 3600
        
        # 只有当时间间隔大于等于1小时且需要更新时才执行更新操作
        if hours_passed >= 1 and self.needs_update:
            self._updating = True
            try:
                self._update_needs(hours_passed)
                self._update_age(hours_passed)
                self._update_mood()
                self.last_update_time = current_time
                self.needs_update = False
            finally:
                self._updating = False
    
    def _update_needs(self, hours_passed):
        """随时间更新需求值
        
        Args:
            hours_passed (float): 经过的小时数
        
        Returns:
            None
        
        Notes:
            - 更新饥饿度、能量、清洁度和快乐度
            - 根据宠物性格调整更新速率
            - 当宠物睡眠时，能量会恢复而不是消耗
            - 当能量达到100%时，宠物会自动醒来
        """
        # 饥饿增长（根据性格调整）
        hunger_rate = PetConfig.HUNGER_RATE
        
        # 贪吃性格饿得更快
        if PetPersonality.HUNGRY in self.personality_traits:
            hunger_rate *= PetConfig.PERSONALITY_FACTORS["HUNGRY"]["hunger_rate_multiplier"]
        
        self.hunger = min(100, self.hunger + hunger_rate * hours_passed)
        
        # 能量恢复或消耗
        if self.is_sleeping:
            # 睡眠时恢复能量
            energy_rate = PetConfig.ENERGY_RATE_SLEEP
            old_energy = self.energy
            self.energy = min(100, self.energy + energy_rate * hours_passed)
            
            # 当能量达到100%时自动醒来
            if self.energy >= 100:
                self.wake_up()
        else:
            # 活跃时消耗能量
            energy_rate = PetConfig.ENERGY_RATE_ACTIVE
            self.energy = max(0, self.energy - energy_rate * hours_passed)
        
        # 清洁度下降（除非爱干净性格）
        hygiene_rate = PetConfig.HYGIENE_RATE
        if PetPersonality.CLEAN in self.personality_traits:
            hygiene_rate *= PetConfig.PERSONALITY_FACTORS["CLEAN"]["hygiene_rate_multiplier"]
        
        self.hygiene = max(0, self.hygiene - hygiene_rate * hours_passed)
        
        # 快乐度受其他因素影响
        happiness_change = 0
        
        # 饥饿影响快乐
        if self.hunger > PetConfig.HUNGER_THRESHOLD:
            happiness_change -= PetConfig.HAPPINESS_HUNGER_PENALTY * hours_passed
        elif self.hunger < PetConfig.HYGIENE_THRESHOLD:
            happiness_change += PetConfig.HAPPINESS_HUNGER_BONUS * hours_passed
        
        # 清洁度影响快乐
        if self.hygiene < PetConfig.HYGIENE_THRESHOLD:
            happiness_change -= PetConfig.HAPPINESS_HYGIENE_PENALTY * hours_passed
        
        # 能量影响快乐
        if self.energy < PetConfig.ENERGY_THRESHOLD:
            happiness_change -= PetConfig.HAPPINESS_ENERGY_PENALTY * hours_passed
        
        # 应用快乐度变化
        self.happiness = max(0, min(100, self.happiness + happiness_change))
    
    def _update_age(self, hours_passed):
        """更新年龄
        
        Args:
            hours_passed (float): 经过的小时数
        
        Returns:
            None
        
        Notes:
            - 将小时数转换为天数并更新宠物年龄
            - 根据年龄自动更新宠物状态：
              - 0-1天: 幼年 (BABY)
              - 1-7天: 童年 (CHILD)
              - 7-14天: 青少年 (TEEN)
              - 14-30天: 成年 (ADULT)
              - 30天以上: 老年 (ELDER)
        """
        days_passed = hours_passed / 24
        self.age_in_days += days_passed
        
        # 根据年龄更新状态
        if self.age_in_days < 1:
            self.state = PetState.BABY
        elif self.age_in_days < 7:
            self.state = PetState.CHILD
        elif self.age_in_days < 14:
            self.state = PetState.TEEN
        elif self.age_in_days < 30:
            self.state = PetState.ADULT
        else:
            self.state = PetState.ELDER
    
    def _update_mood(self):
        """更新心情
        
        Returns:
            None
        
        Notes:
            - 基于快乐度计算基础心情：
              - 90+ 快乐度: 狂喜 (ECSTATIC)
              - 70-90 快乐度: 快乐 (HAPPY)
              - 50-70 快乐度: 满足 (CONTENT)
              - 30-50 快乐度: 中性 (NEUTRAL)
              - 10-30 快乐度: 悲伤 (SAD)
              - 0-10 快乐度: 沮丧 (DEPRESSED)
            - 健康状况会影响心情：健康值低于30时，心情会变为悲伤
            - 情感系统会影响心情：当主导情绪为愤怒时，心情会变为愤怒
        """
        # 基于快乐度和其他因素计算心情
        if self.happiness > 90:
            self.mood = PetMood.ECSTATIC
        elif self.happiness > 70:
            self.mood = PetMood.HAPPY
        elif self.happiness > 50:
            self.mood = PetMood.CONTENT
        elif self.happiness > 30:
            self.mood = PetMood.NEUTRAL
        elif self.happiness > 10:
            self.mood = PetMood.SAD
        else:
            self.mood = PetMood.DEPRESSED
        
        # 健康状况影响心情
        if self.health < 30:
            self.mood = PetMood.SAD
        
        # 情感系统影响心情
        dominant_emotion = self.emotional_system.get_dominant_emotion()
        if dominant_emotion == EmotionType.ANGER:
            self.mood = PetMood.ANGRY
    
    def _add_memory(self, memory):
        """添加记忆
        
        Args:
            memory (str): 记忆内容
        
        Returns:
            None
        
        Notes:
            - 记忆会以 (时间戳, 内容) 的形式存储
            - 当记忆数量超过 max_memory_length 时，会删除最旧的记忆
        """
        self.memories.append((time.time(), memory))
        if len(self.memories) > self.max_memory_length:
            self.memories.pop(0)
    
    def feed(self, food_type="普通食物"):
        """喂食宠物
        
        Args:
            food_type (str, optional): 食物类型，默认为"普通食物"
                可选值："普通食物", "美味大餐", "健康食品", "零食"
        
        Returns:
            str: 喂食结果消息
        
        Notes:
            - 如果宠物正在睡觉，会先唤醒宠物，喂食后再继续睡觉
            - 不同食物类型有不同的效果：
              - 普通食物：减少30饥饿，增加5快乐，增加0.1体重
              - 美味大餐：减少50饥饿，增加15快乐，增加0.2体重
              - 健康食品：减少25饥饿，增加10健康，增加0.05体重
              - 零食：减少10饥饿，增加10快乐，增加0.02体重
            - 贪吃性格的宠物会获得额外的快乐
            - 喂食后会检查精力值，如果小于50%，宠物会去睡觉
        """
        # 检查宠物是否在睡觉
        was_sleeping = self.is_sleeping
        wake_result = ""
        
        if was_sleeping:
            # 唤醒宠物
            wake_result = self.wake_up()
        
        effect = PetConfig.FOOD_EFFECTS.get(food_type, PetConfig.FOOD_EFFECTS["普通食物"])
        
        # 应用效果
        self.hunger = max(0, self.hunger + effect["hunger"])
        self.happiness = min(100, self.happiness + effect.get("happiness", 0))
        self.health = min(100, self.health + effect.get("health", 0))
        self.weight += effect.get("weight", 0)
        
        # 贪吃性格额外快乐
        if PetPersonality.HUNGRY in self.personality_traits:
            self.happiness += 5
        
        # 触发情感
        self.emotional_system.trigger_emotion(EmotionType.JOY, 0.3, f"吃了{food_type}")
        if PetPersonality.HUNGRY in self.personality_traits:
            self.emotional_system.trigger_emotion(EmotionType.LOVE, 0.2, "主人喂食")
        
        self._add_memory(f"吃了{self.name}一份{food_type}")
        
        # 记录喂食偏好
        self.routine_preferences["feed"] += 1
        
        # 检查是否需要继续睡觉
        continue_sleep_result = ""
        if was_sleeping:
            # 如果之前在睡觉，吃完饭再继续睡觉
            continue_sleep_result = self.sleep()
        else:
            # 检查精力值，如果小于50%，则去睡觉
            continue_sleep_result = self._check_energy_and_sleep()
        
        # 构建返回消息
        result_message = f"喂食成功！{self.name}看起来很开心"
        if wake_result:
            result_message = f"{wake_result}\n{result_message}"
        if continue_sleep_result:
            result_message = f"{result_message}\n{continue_sleep_result}"
        
        return result_message
    
    def play(self, game_type="普通游戏"):
        """和宠物玩耍
        
        Args:
            game_type (str, optional): 游戏类型，默认为"普通游戏"
                可选值："普通游戏", "捡球游戏", "智力游戏", "社交游戏"
        
        Returns:
            str: 玩耍结果消息
        
        Notes:
            - 如果宠物正在睡觉，无法玩耍
            - 如果宠物能量低于20，无法玩耍
            - 不同游戏类型有不同的效果：
              - 普通游戏：消耗15能量，增加20快乐，获得10经验
              - 捡球游戏：消耗20能量，增加25快乐，提升力量和速度技能
              - 智力游戏：消耗10能量，增加15快乐，提升智力技能
              - 社交游戏：消耗5能量，增加30快乐，提升社交技能
            - 顽皮性格的宠物会获得额外的快乐
            - 懒惰性格的宠物会消耗更多的能量
            - 玩耍后会检查精力值，如果小于50%，宠物会去睡觉
        """
        if self.is_sleeping:
            return "宠物正在睡觉，无法玩耍"
        
        if self.energy < PetConfig.ENERGY_THRESHOLD:
            return "宠物太累了，需要休息"
        
        effect = PetConfig.GAME_EFFECTS.get(game_type, PetConfig.GAME_EFFECTS["普通游戏"])
        
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
        
        # 触发情感
        self.emotional_system.trigger_emotion(EmotionType.EXCITEMENT, 0.4, f"玩了{game_type}")
        self.emotional_system.trigger_emotion(EmotionType.JOY, 0.3, "玩耍")
        if PetPersonality.PLAYFUL in self.personality_traits:
            self.emotional_system.trigger_emotion(EmotionType.CURIOSITY, 0.2, "想继续玩")
        
        self._add_memory(f"玩了{game_type}游戏")
        
        # 记录游戏偏好
        self.routine_preferences["play"] += 1
        
        # 检查精力值，如果小于50%，则去睡觉
        sleep_result = self._check_energy_and_sleep()
        if sleep_result:
            return f"玩耍成功！{self.name}玩得很开心\n{sleep_result}"
        
        return f"玩耍成功！{self.name}玩得很开心"
    
    def clean(self, clean_type="毛发清理"):
        """清洁宠物
        
        Args:
            clean_type (str, optional): 清洁类型，默认为"毛发清理"
                可选值："毛发清理", "刷牙", "洗澡", "修剪指甲"
        
        Returns:
            str: 清洁结果消息
        
        Notes:
            - 如果宠物正在睡觉，无法清洁
            - 不同清洁类型有不同的效果：
              - 毛发清理：增加40清洁度，10快乐度，5健康度
              - 刷牙：增加20清洁度，5快乐度，15健康度
              - 洗澡：增加60清洁度，15快乐度，10健康度
              - 修剪指甲：增加15清洁度，5快乐度，3健康度
            - 爱干净性格的宠物会获得额外的清洁度和快乐度
            - 清洁后会检查精力值，如果小于50%，宠物会去睡觉
        """
        if self.is_sleeping:
            return "宠物正在睡觉，无法清洁"
        
        # 获取当前清洁类型的效果
        effect = PetConfig.CLEAN_EFFECTS.get(clean_type, PetConfig.CLEAN_EFFECTS["毛发清理"])
        
        # 应用效果
        hygiene_gain = effect["hygiene_gain"]
        happiness_gain = effect["happiness_gain"]
        health_gain = effect["health_gain"]
        
        # 爱干净性格更享受清洁
        if PetPersonality.CLEAN in self.personality_traits:
            hygiene_gain *= PetConfig.PERSONALITY_FACTORS["CLEAN"]["hygiene_gain_multiplier"]
            happiness_gain *= PetConfig.PERSONALITY_FACTORS["CLEAN"]["happiness_gain_multiplier"]
        
        # 应用清洁效果
        self.hygiene = min(100, self.hygiene + hygiene_gain)
        self.happiness = min(100, self.happiness + happiness_gain)
        self.health = min(100, self.health + health_gain)
        
        # 触发情感
        from .enums import EmotionType
        emotion_type = getattr(EmotionType, effect["emotion"])
        self.emotional_system.trigger_emotion(emotion_type, effect["emotion_intensity"], effect["description"])
        
        # 爱干净性格额外触发快乐情感
        if PetPersonality.CLEAN in self.personality_traits:
            self.emotional_system.trigger_emotion(EmotionType.JOY, 0.4, "享受清洁")
        
        # 添加记忆
        self._add_memory(effect["memory"])
        
        # 生成清洁结果消息
        result_message = ""
        if PetPersonality.CLEAN in self.personality_traits:
            result_message = f"{clean_type}成功！{self.name}享受了这次清洁，现在看起来很整洁"
        else:
            result_message = f"{clean_type}成功！{self.name}现在干净多了"
        
        # 检查精力值，如果小于50%，则去睡觉
        sleep_result = self._check_energy_and_sleep()
        if sleep_result:
            return f"{result_message}\n{sleep_result}"
        
        return result_message
    
    def sleep(self):
        """让宠物睡觉
        
        Returns:
            str: 睡觉结果消息
        
        Notes:
            - 如果宠物已经在睡觉，会返回相应提示
            - 设置宠物状态为睡眠中
            - 记录开始睡觉的时间
            - 初始化睡眠时长为0
            - 根据性格调整睡眠行为（懒惰性格会提示可能睡很久）
            - 触发平静情感
            - 添加睡眠记忆
        """
        if self.is_sleeping:
            return "宠物已经在睡觉了"
        
        self.is_sleeping = True
        self.sleep_start_time = time.time()
        self.sleep_duration = 0
        
        # 根据性格调整睡眠行为
        sleep_message = f"{self.name}开始睡觉了，晚安！"
        if PetPersonality.LAZY in self.personality_traits:
            sleep_message += f" (懒惰的{self.name}可能会睡很久哦)"
        
        # 触发情感
        self.emotional_system.trigger_emotion(EmotionType.CALM, 0.5, "开始睡觉")
        
        self._add_memory("去睡觉了")
        
        return sleep_message
    
    def wake_up(self):
        """唤醒宠物
        
        Returns:
            str: 唤醒结果消息
        
        Notes:
            - 如果宠物已经醒着，会返回相应提示
            - 设置宠物状态为清醒
            - 计算睡眠时长（如果有记录开始睡觉的时间）
            - 重置开始睡觉的时间为None
            - 根据睡眠时长恢复能量（每小时恢复15能量，最多恢复30能量）
            - 触发快乐情感
            - 根据恢复的能量多少生成不同的唤醒消息
            - 添加唤醒记忆
        """
        if not self.is_sleeping:
            return "宠物已经醒着了"
        
        self.is_sleeping = False
        if self.sleep_start_time:
            self.sleep_duration = time.time() - self.sleep_start_time
        self.sleep_start_time = None
        
        # 唤醒时的能量恢复
        energy_gained = min(30, (self.sleep_duration / 3600) * 15)
        self.energy = min(100, self.energy + energy_gained)
        
        # 触发情感
        self.emotional_system.trigger_emotion(EmotionType.JOY, 0.3, "醒来")
        
        wake_message = f"{self.name}睡眼惺忪地醒来了"
        if energy_gained > 20:
            wake_message = f"{self.name}精神饱满地醒来了！"
        
        self._add_memory("醒来了")
        
        return wake_message
    
    def train(self, skill_type="intelligence"):
        """训练宠物技能
        
        Args:
            skill_type (str, optional): 技能类型，默认为"intelligence"
                可选值："intelligence" (智力), "strength" (力量), "speed" (速度), "social" (社交)
        
        Returns:
            str: 训练结果消息
        
        Notes:
            - 如果宠物正在睡觉，无法训练
            - 如果宠物能量低于30，无法训练
            - 如果技能类型不存在，返回错误信息
            - 训练消耗能量（基础值：20）
            - 提升技能等级（基础值：1.0）
            - 获得经验（基础值：10）
            - 增加快乐度（5点）
            - 懒惰性格会增加能量消耗并减少快乐度
            - 触发好奇情感
            - 懒惰性格额外触发焦虑情感
            - 添加训练记忆
            - 检查精力值，如果小于50%，宠物会去睡觉
        """
        try:
            if self.is_sleeping:
                return "宠物正在睡觉，无法训练"
            
            if self.energy < 30:
                return "宠物太累了，无法训练"
            
            if skill_type not in self.skills:
                return f"无效的技能类型：{skill_type}"
            
            # 训练消耗和效果
            energy_cost = PetConfig.TRAIN_ENERGY_COST_BASE
            skill_gain = PetConfig.TRAIN_SKILL_GAIN
            
            # 根据性格调整
            if PetPersonality.LAZY in self.personality_traits:
                energy_cost *= PetConfig.PERSONALITY_FACTORS["LAZY"]["energy_cost_multiplier"]
                self.happiness -= PetConfig.PERSONALITY_FACTORS["LAZY"]["happiness_penalty"]
            
            self.energy = max(0, self.energy - energy_cost)
            self.skills[skill_type] += skill_gain
            self.experience += PetConfig.TRAIN_EXPERIENCE_GAIN
            self.happiness += 5
            
            # 触发情感
            self.emotional_system.trigger_emotion(EmotionType.CURIOSITY, 0.3, "学习新技能")
            if PetPersonality.LAZY in self.personality_traits:
                self.emotional_system.trigger_emotion(EmotionType.ANXIETY, 0.2, "不想训练")
            
            skill_names = {
                "intelligence": "智力",
                "strength": "力量",
                "speed": "速度",
                "social": "社交"
            }
            
            # 获取技能名称，如果不存在则使用原始技能类型
            skill_name = skill_names.get(skill_type, skill_type)
            self._add_memory(f"进行了{skill_name}训练")
            
            # 检查精力值，如果小于50%，则去睡觉
            sleep_result = self._check_energy_and_sleep()
            if sleep_result:
                return f"训练成功！{self.name}的{skill_name}提升了\n{sleep_result}"
            
            return f"训练成功！{self.name}的{skill_name}提升了"
        except Exception as e:
            return f"训练失败：{str(e)}"
    
    def change_color(self, new_color):
        """更改宠物毛发颜色
        
        Args:
            new_color (str): 新的毛发颜色
                可选值：根据 PetConfig.AVAILABLE_COLORS 配置
        
        Returns:
            str: 颜色更改结果消息
        
        Notes:
            - 如果宠物正在睡觉，无法更改颜色
            - 如果颜色不在可用列表中，返回错误信息并显示可用颜色
            - 记录旧颜色
            - 设置新颜色
            - 触发兴奋情感
            - 添加颜色更改记忆
        """
        try:
            if self.is_sleeping:
                return "宠物正在睡觉，无法更改颜色"
            
            if not isinstance(new_color, str):
                return "无效的颜色：颜色必须是字符串"
            
            if new_color not in PetConfig.AVAILABLE_COLORS:
                return f"无效的颜色。可用颜色：{', '.join(PetConfig.AVAILABLE_COLORS)}"
            
            old_color = self.color
            self.color = new_color
            
            # 触发情感
            self.emotional_system.trigger_emotion(EmotionType.EXCITEMENT, 0.3, "改变颜色")
            
            self._add_memory(f"颜色从{old_color}变成了{new_color}")
            
            return f"{self.name}的颜色已更改为{new_color}"
        except Exception as e:
            return f"更改颜色失败：{str(e)}"
    
    def get_status(self, force_update=False):
        """获取宠物状态摘要
        
        Args:
            force_update (bool, optional): 是否强制更新状态，默认为False
        
        Returns:
            dict: 宠物状态字典，包含以下字段：
                - name: 宠物名称
                - species: 宠物种类
                - age: 年龄（天数）
                - state: 状态
                - mood: 心情
                - level: 等级
                - health: 健康值
                - hunger: 饥饿值
                - energy: 能量值
                - hygiene: 清洁度
                - happiness: 快乐度
                - weight: 体重
                - relationship: 与主人的关系值
                - is_sleeping: 是否在睡觉
                - is_sick: 是否生病
                - sickness:  sickness类型或"健康"
                - personality: 性格特征列表
                - skills: 技能列表
                - color: 毛发颜色
                - size: 体型大小
                - 如果宠物在睡觉，还会包含睡眠状态信息
        
        Notes:
            - 只有在需要更新或强制更新时才会调用update()方法
            - 这样可以避免不必要的状态更新，提高性能
        """
        # 只有在需要更新或强制更新时才执行更新操作
        if force_update or self.needs_update:
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
        
        # 添加睡眠状态信息
        if self.is_sleeping:
            sleep_info = self.get_sleep_status()
            status.update(sleep_info)
        
        return status
    
    def get_sleep_status(self):
        """获取睡眠状态信息"""
        if not self.is_sleeping:
            return {}
        
        # 计算已睡眠时长
        sleep_duration = 0
        if self.sleep_start_time:
            sleep_duration = (time.time() - self.sleep_start_time) / 3600  # 转换为小时
        
        # 计算预计醒来时间
        energy_needed = 100 - self.energy
        hours_needed = energy_needed / 15.0  # 每小时恢复15点能量
        hours_needed = max(0.1, hours_needed)
        
        return {
            "sleep_duration": f"{sleep_duration:.1f}小时",
            "estimated_wake_up_time": f"约{hours_needed:.1f}小时后"
        }
    
    def save_to_file(self, file_path):
        """保存宠物数据到文件"""
        try:
            data = {
                "name": self.name,
                "species": self.species,
                "birth_time": self.birth_time,
                "age_in_days": self.age_in_days,
                "health": self.health,
                "hunger": self.hunger,
                "energy": self.energy,
                "hygiene": self.hygiene,
                "happiness": self.happiness,
                "weight": self.weight,
                "size": self.size,
                "color": self.color,
                "state": self.state.value,
                "mood": self.mood.value,
                "is_sleeping": self.is_sleeping,
                "is_sick": self.is_sick,
                "sickness_type": self.sickness_type,
                "sleep_start_time": self.sleep_start_time,
                "sleep_duration": self.sleep_duration,
                "skills": self.skills,
                "experience": self.experience,
                "level": self.level,
                "personality_traits": {t.value: v for t, v in self.personality_traits.items()},
                "relationship_with_owner": self.relationship_with_owner,
                "memories": self.memories,
                "routine_preferences": dict(self.routine_preferences),
                "emotional_system": self.emotional_system.to_dict()
            }
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return f"宠物 {self.name} 已保存到 {file_path}"
        except OSError as e:
            return f"保存失败：无法写入文件 - {str(e)}"
        except PermissionError as e:
            return f"保存失败：权限不足 - {str(e)}"
        except TypeError as e:
            return f"保存失败：数据无法序列化 - {str(e)}"
        except Exception as e:
            return f"保存失败：未知错误 - {str(e)}"
    
    @classmethod
    def load_from_file(cls, file_path):
        """从文件加载宠物数据"""
        try:
            if not os.path.exists(file_path):
                return f"加载失败：文件不存在 - {file_path}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查必要字段
            if "name" not in data or "species" not in data:
                return f"加载失败：文件格式错误，缺少必要字段"
            
            pet = cls(data["name"], data["species"])
            pet.birth_time = data.get("birth_time", time.time())
            pet.age_in_days = data.get("age_in_days", 0)
            pet.health = data.get("health", 100.0)
            pet.hunger = data.get("hunger", 0.0)
            pet.energy = data.get("energy", 100.0)
            pet.hygiene = data.get("hygiene", 100.0)
            pet.happiness = data.get("happiness", 50.0)
            pet.weight = data.get("weight", 1.0)
            pet.size = data.get("size", "小")
            pet.color = data.get("color", "白色")
            
            # 安全加载枚举值
            try:
                pet.state = PetState(data.get("state", "BABY"))
            except ValueError:
                pet.state = PetState.BABY
            
            try:
                pet.mood = PetMood(data.get("mood", "NEUTRAL"))
            except ValueError:
                pet.mood = PetMood.NEUTRAL
            
            pet.is_sleeping = data.get("is_sleeping", False)
            pet.is_sick = data.get("is_sick", False)
            pet.sickness_type = data.get("sickness_type", None)
            pet.sleep_start_time = data.get("sleep_start_time", None)
            pet.sleep_duration = data.get("sleep_duration", 0)
            pet.skills = data.get("skills", {"intelligence": 0, "strength": 0, "speed": 0, "social": 0})
            pet.experience = data.get("experience", 0)
            pet.level = data.get("level", 1)
            
            # 安全加载性格特征
            try:
                pet.personality_traits = {PetPersonality(t): v for t, v in data.get("personality_traits", {}).items()}
            except ValueError:
                pet.personality_traits = {}
            
            pet.relationship_with_owner = data.get("relationship_with_owner", 50.0)
            pet.memories = data.get("memories", [])
            pet.routine_preferences = defaultdict(int, data.get("routine_preferences", {}))
            
            # 恢复情感系统
            if "emotional_system" in data:
                try:
                    pet.emotional_system.from_dict(data["emotional_system"])
                except Exception as e:
                    print(f"警告：情感系统恢复失败 - {str(e)}")
            
            return pet
        except OSError as e:
            return f"加载失败：无法读取文件 - {str(e)}"
        except PermissionError as e:
            return f"加载失败：权限不足 - {str(e)}"
        except json.JSONDecodeError as e:
            return f"加载失败：文件格式错误 - {str(e)}"
        except Exception as e:
            return f"加载失败：未知错误 - {str(e)}"
    
    def _explore(self):
        """探索环境"""
        if self.energy < 15:
            return f"{self.name}：'我太累了，不想动'"
        
        energy_cost = PetConfig.EXPLORE_ENERGY_COST
        happiness_gain = 10
        intelligence_gain = PetConfig.EXPLORE_INTELLIGENCE_GAIN
        
        self.energy = max(0, self.energy - energy_cost)
        self.happiness = min(100, self.happiness + happiness_gain)
        self.skills["intelligence"] += intelligence_gain
        
        # 检查精力值，如果小于50%，则去睡觉
        sleep_result = self._check_energy_and_sleep()
        if sleep_result:
            return f"{self.name}正在好奇地探索周围环境\n{sleep_result}"
        
        return f"{self.name}正在好奇地探索周围环境"
    
    def _rest(self):
        """休息恢复"""
        energy_gain = PetConfig.REST_ENERGY_GAIN
        health_gain = PetConfig.REST_HEALTH_GAIN
        
        self.energy = min(100, self.energy + energy_gain)
        self.health = min(100, self.health + health_gain)
        
        # 检查精力值，如果小于50%，则去睡觉
        sleep_result = self._check_energy_and_sleep()
        if sleep_result:
            return f"{self.name}正在休息恢复精力\n{sleep_result}"
        
        return f"{self.name}正在休息恢复精力"
    
    def _check_energy_and_sleep(self):
        """检查精力值，如果小于50%，则去睡觉"""
        if not self.is_sleeping and self.energy < PetConfig.ENERGY_SLEEP_THRESHOLD:
            return self.sleep()
        return ""
