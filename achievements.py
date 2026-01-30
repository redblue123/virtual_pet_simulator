#!/usr/bin/env python3
import time
from enum import Enum

class AchievementCategory(Enum):
    """成就类别枚举"""
    CARE = "照顾"
    TRAINING = "训练"
    SOCIAL = "社交"
    EXPLORATION = "探索"
    SPECIAL = "特殊"

class AchievementStatus(Enum):
    """成就状态枚举"""
    LOCKED = "未解锁"
    IN_PROGRESS = "进行中"
    UNLOCKED = "已解锁"

class Achievement:
    """成就类"""
    def __init__(self, achievement_id, name, description, category, requirement, reward, icon=None):
        self.achievement_id = achievement_id
        self.name = name
        self.description = description
        self.category = category
        self.requirement = requirement  # 解锁要求
        self.reward = reward  # 解锁奖励
        self.icon = icon  # 成就图标
        self.status = AchievementStatus.LOCKED
        self.progress = 0
        self.unlocked_at = None
    
    def update_progress(self, progress):
        """更新成就进度"""
        old_progress = self.progress
        self.progress = min(progress, self.requirement)
        
        # 更新状态
        if self.status == AchievementStatus.LOCKED and self.progress > 0:
            self.status = AchievementStatus.IN_PROGRESS
        elif self.progress >= self.requirement:
            self.status = AchievementStatus.UNLOCKED
            self.unlocked_at = time.time()
        
        return self.progress > old_progress
    
    def is_unlocked(self):
        """检查成就是否已解锁"""
        return self.status == AchievementStatus.UNLOCKED
    
    def to_dict(self):
        """转换为字典"""
        return {
            "achievement_id": self.achievement_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "requirement": self.requirement,
            "reward": self.reward,
            "icon": self.icon,
            "status": self.status.value,
            "progress": self.progress,
            "unlocked_at": self.unlocked_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建成就"""
        achievement = cls(
            achievement_id=data["achievement_id"],
            name=data["name"],
            description=data["description"],
            category=AchievementCategory(data["category"]),
            requirement=data["requirement"],
            reward=data["reward"],
            icon=data.get("icon")
        )
        achievement.status = AchievementStatus(data["status"])
        achievement.progress = data["progress"]
        achievement.unlocked_at = data.get("unlocked_at")
        return achievement

class AchievementSystem:
    """成就系统"""
    def __init__(self, pet):
        self.pet = pet
        self.achievements = self._initialize_achievements()
        self.recently_unlocked = []
    
    def _initialize_achievements(self):
        """初始化成就列表"""
        achievements = []
        
        # 照顾类别成就
        achievements.extend([
            Achievement(
                achievement_id="care_1",
                name="初级饲养员",
                description="喂食你的宠物10次",
                category=AchievementCategory.CARE,
                requirement=10,
                reward={"experience": 100, "points": 50}
            ),
            Achievement(
                achievement_id="care_2",
                name="中级饲养员",
                description="喂食你的宠物50次",
                category=AchievementCategory.CARE,
                requirement=50,
                reward={"experience": 300, "points": 150}
            ),
            Achievement(
                achievement_id="care_3",
                name="高级饲养员",
                description="喂食你的宠物100次",
                category=AchievementCategory.CARE,
                requirement=100,
                reward={"experience": 500, "points": 300}
            ),
            Achievement(
                achievement_id="care_4",
                name="清洁大师",
                description="清洁你的宠物50次",
                category=AchievementCategory.CARE,
                requirement=50,
                reward={"experience": 250, "points": 125}
            ),
            Achievement(
                achievement_id="care_5",
                name="睡眠专家",
                description="让你的宠物睡觉20次",
                category=AchievementCategory.CARE,
                requirement=20,
                reward={"experience": 150, "points": 75}
            ),
        ])
        
        # 训练类别成就
        achievements.extend([
            Achievement(
                achievement_id="training_1",
                name="初级训练师",
                description="训练你的宠物10次",
                category=AchievementCategory.TRAINING,
                requirement=10,
                reward={"experience": 120, "points": 60}
            ),
            Achievement(
                achievement_id="training_2",
                name="中级训练师",
                description="训练你的宠物50次",
                category=AchievementCategory.TRAINING,
                requirement=50,
                reward={"experience": 350, "points": 175}
            ),
            Achievement(
                achievement_id="training_3",
                name="高级训练师",
                description="训练你的宠物100次",
                category=AchievementCategory.TRAINING,
                requirement=100,
                reward={"experience": 600, "points": 300}
            ),
            Achievement(
                achievement_id="training_4",
                name="技能大师",
                description="让你的宠物的所有技能达到10级",
                category=AchievementCategory.TRAINING,
                requirement=10,
                reward={"experience": 800, "points": 400}
            ),
        ])
        
        # 社交类别成就
        achievements.extend([
            Achievement(
                achievement_id="social_1",
                name="友好伙伴",
                description="和你的宠物玩耍20次",
                category=AchievementCategory.SOCIAL,
                requirement=20,
                reward={"experience": 150, "points": 75}
            ),
            Achievement(
                achievement_id="social_2",
                name="亲密伙伴",
                description="抚摸你的宠物50次",
                category=AchievementCategory.SOCIAL,
                requirement=50,
                reward={"experience": 250, "points": 125}
            ),
            Achievement(
                achievement_id="social_3",
                name="最佳朋友",
                description="和你的宠物的关系达到100",
                category=AchievementCategory.SOCIAL,
                requirement=100,
                reward={"experience": 500, "points": 250}
            ),
        ])
        
        # 特殊类别成就
        achievements.extend([
            Achievement(
                achievement_id="special_1",
                name="宠物诞生",
                description="创建你的第一个宠物",
                category=AchievementCategory.SPECIAL,
                requirement=1,
                reward={"experience": 50, "points": 25}
            ),
            Achievement(
                achievement_id="special_2",
                name="成长里程碑",
                description="你的宠物成长到成年",
                category=AchievementCategory.SPECIAL,
                requirement=1,
                reward={"experience": 300, "points": 150}
            ),
            Achievement(
                achievement_id="special_3",
                name="全能冠军",
                description="解锁所有成就",
                category=AchievementCategory.SPECIAL,
                requirement=1,
                reward={"experience": 2000, "points": 1000}
            ),
        ])
        
        return achievements
    
    def update_achievement_progress(self, achievement_type, progress):
        """更新成就进度"""
        unlocked_achievements = []
        rewards = []
        
        for achievement in self.achievements:
            if achievement_type in achievement.achievement_id:
                was_updated = achievement.update_progress(progress)
                if was_updated and achievement.is_unlocked():
                    unlocked_achievements.append(achievement)
                    rewards.append(achievement.reward)
        
        # 处理新解锁的成就
        for achievement in unlocked_achievements:
            self.recently_unlocked.append(achievement)
            if len(self.recently_unlocked) > 5:
                self.recently_unlocked.pop(0)
        
        return rewards
    
    def update_care_achievements(self, action_type, count=1):
        """更新照顾类成就"""
        rewards = []
        
        if action_type == "feed":
            rewards.extend(self.update_achievement_progress("care_1", count))
            rewards.extend(self.update_achievement_progress("care_2", count))
            rewards.extend(self.update_achievement_progress("care_3", count))
        elif action_type == "clean":
            rewards.extend(self.update_achievement_progress("care_4", count))
        elif action_type == "sleep":
            rewards.extend(self.update_achievement_progress("care_5", count))
        
        return rewards
    
    def update_training_achievements(self, count=1):
        """更新训练类成就"""
        rewards = []
        rewards.extend(self.update_achievement_progress("training_1", count))
        rewards.extend(self.update_achievement_progress("training_2", count))
        rewards.extend(self.update_achievement_progress("training_3", count))
        
        # 检查技能等级
        max_skill_level = max(self.pet.skills.values())
        self.update_achievement_progress("training_4", max_skill_level)
        
        return rewards
    
    def update_social_achievements(self, action_type, count=1):
        """更新社交类成就"""
        rewards = []
        
        if action_type == "play":
            rewards.extend(self.update_achievement_progress("social_1", count))
        elif action_type == "pet":
            rewards.extend(self.update_achievement_progress("social_2", count))
        
        # 检查关系值
        relationship = self.pet.relationship_with_owner
        self.update_achievement_progress("social_3", relationship)
        
        return rewards
    
    def update_special_achievements(self, event_type):
        """更新特殊类成就"""
        rewards = []
        
        if event_type == "pet_created":
            rewards.extend(self.update_achievement_progress("special_1", 1))
        elif event_type == "pet_adult":
            rewards.extend(self.update_achievement_progress("special_2", 1))
        
        # 检查是否解锁了所有成就
        unlocked_count = sum(1 for a in self.achievements if a.is_unlocked())
        if unlocked_count == len(self.achievements):
            rewards.extend(self.update_achievement_progress("special_3", 1))
        
        return rewards
    
    def get_achievements(self, category=None):
        """获取成就列表"""
        if category:
            return [a for a in self.achievements if a.category == category]
        return self.achievements
    
    def get_recently_unlocked(self):
        """获取最近解锁的成就"""
        return self.recently_unlocked
    
    def get_unlocked_count(self):
        """获取已解锁成就数量"""
        return sum(1 for a in self.achievements if a.is_unlocked())
    
    def get_total_count(self):
        """获取总成就数量"""
        return len(self.achievements)
    
    def to_dict(self):
        """转换为字典"""
        return {
            "achievements": [a.to_dict() for a in self.achievements],
            "recently_unlocked": [a.to_dict() for a in self.recently_unlocked]
        }
    
    def from_dict(self, data):
        """从字典加载"""
        achievements_data = data.get("achievements", [])
        self.achievements = [Achievement.from_dict(a) for a in achievements_data]
        
        recently_unlocked_data = data.get("recently_unlocked", [])
        self.recently_unlocked = [Achievement.from_dict(a) for a in recently_unlocked_data]
