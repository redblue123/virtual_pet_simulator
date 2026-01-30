#!/usr/bin/env python3
import random
import time
from enum import Enum

class NPCPet:
    """NPC宠物类"""
    def __init__(self, name, species, pet_id=None):
        self.name = name
        self.species = species
        self.pet_id = pet_id or f"npc_{name.lower()}_{random.randint(1000, 9999)}"
        
        # 基本属性
        self.happiness = random.randint(50, 80)
        self.energy = random.randint(50, 80)
        self.hunger = random.randint(20, 50)
        self.health = random.randint(70, 100)
        self.hygiene = random.randint(60, 90)
        
        # 添加情感系统（简化版）
        class MockEmotionalSystem:
            def __init__(self, npc_pet):
                self.pet = npc_pet
                
            def trigger_emotion(self, emotion_type, intensity, trigger):
                # 简化版情感系统，仅记录情感触发
                pass
        
        self.emotional_system = MockEmotionalSystem(self)
        
        # 添加社交系统（简化版）
        class MockSocialSystem:
            def __init__(self, npc_pet):
                self.pet = npc_pet
                self.social_skills = {
                    "communication": random.randint(40, 70),
                    "empathy": random.randint(40, 70),
                    "conflict_resolution": random.randint(40, 70),
                    "cooperation": random.randint(40, 70)
                }
        
        self.social_system = MockSocialSystem(self)

class NPCManager:
    """NPC管理器类"""
    def __init__(self):
        self.npcs = []
        self._initialize_default_npcs()
    
    def _initialize_default_npcs(self):
        """初始化默认NPC宠物"""
        default_npcs = [
            NPCPet("小白", "狗狗"),
            NPCPet("小黑", "猫咪"),
            NPCPet("小灰", "兔子"),
            NPCPet("小花", "仓鼠"),
            NPCPet("小黄", "鹦鹉")
        ]
        self.npcs.extend(default_npcs)
    
    def get_all_npcs(self):
        """获取所有NPC宠物"""
        return self.npcs
    
    def get_npc_by_id(self, npc_id):
        """根据ID获取NPC宠物"""
        for npc in self.npcs:
            if npc.pet_id == npc_id:
                return npc
        return None
    
    def add_npc(self, npc):
        """添加新的NPC宠物"""
        self.npcs.append(npc)

class SocialInteractionType(Enum):
    """社交互动类型枚举"""
    GREET = "greet"  # 问候
    PLAY = "play"  # 玩耍
    SHARE = "share"  # 分享
    COMPETE = "compete"  # 竞争
    HELP = "help"  # 帮助
    IGNORE = "ignore"  # 忽略
    CONFLICT = "conflict"  # 冲突

class SocialRelationshipStatus(Enum):
    """社交关系状态枚举"""
    STRANGER = "stranger"  # 陌生人
    ACQUAINTANCE = "acquaintance"  # 熟人
    FRIEND = "friend"  # 朋友
    BEST_FRIEND = "best_friend"  # 最好的朋友
    RIVAL = "rival"  # 竞争对手
    ENEMY = "enemy"  # 敌人

class SocialEvent:
    """社交事件类"""
    def __init__(self, event_id, event_type, participants, timestamp=None, description=None):
        self.event_id = event_id
        self.event_type = event_type
        self.participants = participants  # 参与者列表
        self.timestamp = timestamp or time.time()
        self.description = description
        self.resolved = False
        self.outcome = None
    
    def resolve(self, outcome):
        """解决社交事件"""
        self.resolved = True
        self.outcome = outcome
    
    def to_dict(self):
        """转换为字典"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "participants": self.participants,
            "timestamp": self.timestamp,
            "description": self.description,
            "resolved": self.resolved,
            "outcome": self.outcome
        }

class SocialRelationship:
    """社交关系类"""
    def __init__(self, pet1_id, pet2_id, status=SocialRelationshipStatus.STRANGER, bond=0):
        self.pet1_id = pet1_id
        self.pet2_id = pet2_id
        self.status = status
        self.bond = bond  # 关系纽带值，范围0-100
        self.interaction_history = []
        self.last_interaction = None
    
    def update_bond(self, change):
        """更新关系纽带值"""
        self.bond = max(0, min(100, self.bond + change))
        self._update_status()
    
    def _update_status(self):
        """根据纽带值更新关系状态"""
        if self.bond < 0:
            self.status = SocialRelationshipStatus.ENEMY
        elif self.bond < 20:
            self.status = SocialRelationshipStatus.STRANGER
        elif self.bond < 40:
            self.status = SocialRelationshipStatus.ACQUAINTANCE
        elif self.bond < 70:
            self.status = SocialRelationshipStatus.FRIEND
        elif self.bond < 90:
            self.status = SocialRelationshipStatus.BEST_FRIEND
        else:
            self.status = SocialRelationshipStatus.BEST_FRIEND
    
    def add_interaction(self, interaction_type, outcome, timestamp=None):
        """添加互动记录"""
        interaction = {
            "interaction_type": interaction_type.value,
            "outcome": outcome,
            "timestamp": timestamp or time.time()
        }
        self.interaction_history.append(interaction)
        self.last_interaction = timestamp or time.time()
    
    def get_status(self):
        """获取关系状态"""
        return {
            "pet1_id": self.pet1_id,
            "pet2_id": self.pet2_id,
            "status": self.status.value,
            "bond": self.bond,
            "last_interaction": self.last_interaction
        }
    
    def to_dict(self):
        """转换为字典"""
        return {
            "pet1_id": self.pet1_id,
            "pet2_id": self.pet2_id,
            "status": self.status.value,
            "bond": self.bond,
            "interaction_history": self.interaction_history,
            "last_interaction": self.last_interaction
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建社交关系"""
        status = SocialRelationshipStatus(data["status"])
        relationship = cls(
            pet1_id=data["pet1_id"],
            pet2_id=data["pet2_id"],
            status=status,
            bond=data["bond"]
        )
        relationship.interaction_history = data.get("interaction_history", [])
        relationship.last_interaction = data.get("last_interaction")
        return relationship

class SocialSystem:
    """社交系统"""
    def __init__(self, pet):
        self.pet = pet
        self.relationships = {}  # 键为其他宠物ID，值为SocialRelationship对象
        self.events = []  # 社交事件列表
        self.social_skills = {
            "communication": 50,  # 沟通能力
            "empathy": 50,  # 同理心
            "conflict_resolution": 50,  # 冲突解决
            "cooperation": 50  # 合作能力
        }
        self.interaction_count = 0
        self.friends = []  # 朋友列表
        self.rivals = []  # 竞争对手列表
    
    def interact_with_other(self, other_pet, interaction_type):
        """与其他宠物互动"""
        # 确保other_pet有必要的属性
        if not hasattr(other_pet, 'pet_id'):
            other_pet.pet_id = f"pet_{id(other_pet)}"
        
        # 获取或创建关系
        relationship = self._get_or_create_relationship(other_pet.pet_id)
        
        # 根据互动类型执行不同的互动
        result = self._execute_interaction(other_pet, interaction_type, relationship)
        
        # 更新关系
        self._update_relationship(other_pet.pet_id, interaction_type, result)
        
        # 记录互动
        self.interaction_count += 1
        
        # 更新朋友和竞争对手列表
        self._update_social_lists()
        
        return result
    
    def _get_or_create_relationship(self, other_pet_id):
        """获取或创建与其他宠物的关系"""
        # 获取当前宠物的ID，如果没有pet_id属性，使用名称
        self_pet_id = getattr(self.pet, 'pet_id', self.pet.name)
        if other_pet_id not in self.relationships:
            self.relationships[other_pet_id] = SocialRelationship(self_pet_id, other_pet_id)
        return self.relationships[other_pet_id]
    
    def _execute_interaction(self, other_pet, interaction_type, relationship):
        """执行互动"""
        if interaction_type == SocialInteractionType.GREET:
            return self._greet(other_pet, relationship)
        elif interaction_type == SocialInteractionType.PLAY:
            return self._play(other_pet, relationship)
        elif interaction_type == SocialInteractionType.SHARE:
            return self._share(other_pet, relationship)
        elif interaction_type == SocialInteractionType.COMPETE:
            return self._compete(other_pet, relationship)
        elif interaction_type == SocialInteractionType.HELP:
            return self._help(other_pet, relationship)
        elif interaction_type == SocialInteractionType.IGNORE:
            return self._ignore(other_pet, relationship)
        elif interaction_type == SocialInteractionType.CONFLICT:
            return self._conflict(other_pet, relationship)
        return {"success": False, "message": "无效的互动类型"}
    
    def _greet(self, other_pet, relationship):
        """问候互动"""
        # 导入EmotionType枚举
        from pet.enums import EmotionType
        
        # 基于关系状态和社交技能决定结果
        success_chance = 0.7
        if relationship.status == SocialRelationshipStatus.FRIEND:
            success_chance = 0.9
        elif relationship.status == SocialRelationshipStatus.ENEMY:
            success_chance = 0.3
        
        if random.random() < success_chance:
            bond_change = 5
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.JOY, 0.2, "问候其他宠物")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.JOY, 0.2, "被其他宠物问候")
            
            return {
                "success": True,
                "message": f"宠物成功问候了{other_pet.name}，关系变得更好了！",
                "bond_change": bond_change,
                "effects": {"happiness": 5}
            }
        else:
            bond_change = -2
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.SADNESS, 0.2, "问候被忽略")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.ANXIETY, 0.1, "忽略其他宠物的问候")
            
            return {
                "success": False,
                "message": f"宠物的问候被{other_pet.name}忽略了，关系变得有些紧张。",
                "bond_change": bond_change,
                "effects": {"happiness": -3}
            }
    
    def _play(self, other_pet, relationship):
        """玩耍互动"""
        # 导入EmotionType枚举
        from pet.enums import EmotionType
        
        # 基于关系状态和社交技能决定结果
        success_chance = 0.6
        if relationship.status == SocialRelationshipStatus.FRIEND:
            success_chance = 0.8
        elif relationship.status == SocialRelationshipStatus.ENEMY:
            success_chance = 0.2
        
        if random.random() < success_chance:
            bond_change = 10
            relationship.update_bond(bond_change)
            
            # 更新双方的情感和状态
            self.pet.happiness = min(100, self.pet.happiness + 15)
            self.pet.energy = max(0, self.pet.energy - 10)
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.EXCITEMENT, 0.4, "与其他宠物玩耍")
            
            if hasattr(other_pet, 'happiness'):
                other_pet.happiness = min(100, other_pet.happiness + 15)
            if hasattr(other_pet, 'energy'):
                other_pet.energy = max(0, other_pet.energy - 10)
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.EXCITEMENT, 0.4, "与其他宠物玩耍")
            
            return {
                "success": True,
                "message": f"宠物和{other_pet.name}一起玩得很开心，关系变得更好了！",
                "bond_change": bond_change,
                "effects": {"happiness": 15, "energy": -10}
            }
        else:
            bond_change = -5
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.SADNESS, 0.3, "玩耍被拒绝")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.ANXIETY, 0.2, "拒绝玩耍邀请")
            
            return {
                "success": False,
                "message": f"{other_pet.name}拒绝了玩耍邀请，关系变得有些紧张。",
                "bond_change": bond_change,
                "effects": {"happiness": -5}
            }
    
    def _share(self, other_pet, relationship):
        """分享互动"""
        # 导入EmotionType枚举
        from pet.enums import EmotionType
        
        # 基于关系状态和社交技能决定结果
        success_chance = 0.5
        if relationship.status == SocialRelationshipStatus.FRIEND:
            success_chance = 0.8
        elif relationship.status == SocialRelationshipStatus.ENEMY:
            success_chance = 0.1
        
        if random.random() < success_chance:
            bond_change = 12
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.GRATITUDE, 0.3, "与其他宠物分享")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.GRATITUDE, 0.4, "被其他宠物分享")
            
            return {
                "success": True,
                "message": f"宠物成功与{other_pet.name}分享了东西，关系变得更好了！",
                "bond_change": bond_change,
                "effects": {"happiness": 8}
            }
        else:
            bond_change = -3
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.SADNESS, 0.2, "分享被拒绝")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.ANXIETY, 0.1, "拒绝分享")
            
            return {
                "success": False,
                "message": f"{other_pet.name}拒绝了分享，关系变得有些紧张。",
                "bond_change": bond_change,
                "effects": {"happiness": -3}
            }
    
    def _compete(self, other_pet, relationship):
        """竞争互动"""
        # 导入EmotionType枚举
        from pet.enums import EmotionType
        
        # 基于社交技能决定胜负
        self_skill = sum(self.social_skills.values()) / len(self.social_skills)
        other_skill = 50  # 默认技能值
        if hasattr(other_pet, 'social_system') and hasattr(other_pet.social_system, 'social_skills'):
            other_skill = sum(other_pet.social_system.social_skills.values()) / len(other_pet.social_system.social_skills)
        
        win_chance = self_skill / (self_skill + other_skill)
        if random.random() < win_chance:
            # 获胜
            bond_change = -2  # 竞争会稍微降低关系
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.PRIDE, 0.4, "在竞争中获胜")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.SADNESS, 0.3, "在竞争中失败")
            
            return {
                "success": True,
                "message": f"宠物在竞争中战胜了{other_pet.name}，感到很自豪！",
                "bond_change": bond_change,
                "effects": {"happiness": 10}
            }
        else:
            # 失败
            bond_change = -4  # 失败会更多地降低关系
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.SADNESS, 0.3, "在竞争中失败")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.PRIDE, 0.4, "在竞争中获胜")
            
            return {
                "success": False,
                "message": f"宠物在竞争中输给了{other_pet.name}，感到有些失落。",
                "bond_change": bond_change,
                "effects": {"happiness": -8}
            }
    
    def _help(self, other_pet, relationship):
        """帮助互动"""
        # 导入EmotionType枚举
        from pet.enums import EmotionType
        
        # 基于关系状态和社交技能决定结果
        success_chance = 0.6
        if relationship.status == SocialRelationshipStatus.FRIEND:
            success_chance = 0.9
        elif relationship.status == SocialRelationshipStatus.ENEMY:
            success_chance = 0.2
        
        if random.random() < success_chance:
            bond_change = 15
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.GRATITUDE, 0.3, "帮助其他宠物")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.GRATITUDE, 0.5, "被其他宠物帮助")
            
            return {
                "success": True,
                "message": f"宠物成功帮助了{other_pet.name}，关系变得更好了！",
                "bond_change": bond_change,
                "effects": {"happiness": 12}
            }
        else:
            bond_change = -3
            relationship.update_bond(bond_change)
            
            # 更新双方的情感
            if hasattr(self.pet, 'emotional_system'):
                self.pet.emotional_system.trigger_emotion(EmotionType.SADNESS, 0.2, "帮助被拒绝")
            if hasattr(other_pet, 'emotional_system'):
                other_pet.emotional_system.trigger_emotion(EmotionType.ANXIETY, 0.2, "拒绝帮助")
            
            return {
                "success": False,
                "message": f"{other_pet.name}拒绝了帮助，关系变得有些紧张。",
                "bond_change": bond_change,
                "effects": {"happiness": -4}
            }
    
    def _ignore(self, other_pet, relationship):
        """忽略互动"""
        # 导入EmotionType枚举
        from pet.enums import EmotionType
        
        bond_change = -8
        relationship.update_bond(bond_change)
        
        # 更新双方的情感
        if hasattr(other_pet, 'emotional_system'):
            other_pet.emotional_system.trigger_emotion(EmotionType.SADNESS, 0.4, "被其他宠物忽略")
        
        return {
            "success": True,
            "message": f"宠物忽略了{other_pet.name}，关系变得紧张。",
            "bond_change": bond_change,
            "effects": {}
        }
    
    def _conflict(self, other_pet, relationship):
        """冲突互动"""
        # 导入EmotionType枚举
        from pet.enums import EmotionType
        
        bond_change = -15
        relationship.update_bond(bond_change)
        
        # 更新双方的情感
        if hasattr(self.pet, 'emotional_system'):
            self.pet.emotional_system.trigger_emotion(EmotionType.ANGER, 0.4, "与其他宠物发生冲突")
        if hasattr(other_pet, 'emotional_system'):
            other_pet.emotional_system.trigger_emotion(EmotionType.ANGER, 0.4, "与其他宠物发生冲突")
        
        return {
            "success": True,
            "message": f"宠物与{other_pet.name}发生了冲突，关系变得很紧张。",
            "bond_change": bond_change,
            "effects": {"happiness": -10}
        }
    
    def _update_relationship(self, other_pet_id, interaction_type, result):
        """更新关系"""
        relationship = self.relationships.get(other_pet_id)
        if relationship:
            relationship.add_interaction(interaction_type, result)
    
    def _update_social_lists(self):
        """更新朋友和竞争对手列表"""
        self.friends = [pet_id for pet_id, rel in self.relationships.items() 
                      if rel.status in [SocialRelationshipStatus.FRIEND, SocialRelationshipStatus.BEST_FRIEND]]
        self.rivals = [pet_id for pet_id, rel in self.relationships.items() 
                      if rel.status in [SocialRelationshipStatus.RIVAL, SocialRelationshipStatus.ENEMY]]
    
    def get_relationship_status(self, other_pet_id):
        """获取与其他宠物的关系状态"""
        relationship = self.relationships.get(other_pet_id)
        if relationship:
            return relationship.get_status()
        return {"status": "stranger", "bond": 0}
    
    def get_all_relationships(self):
        """获取所有社交关系"""
        return [rel.get_status() for rel in self.relationships.values()]
    
    def get_friends(self):
        """获取朋友列表"""
        return self.friends
    
    def get_rivals(self):
        """获取竞争对手列表"""
        return self.rivals
    
    def generate_social_event(self, other_pet):
        """生成社交事件"""
        event_types = list(SocialInteractionType)
        event_type = random.choice(event_types)
        event_id = f"event_{int(time.time())}_{random.randint(1000, 9999)}"
        
        descriptions = {
            SocialInteractionType.GREET: f"{self.pet.name}遇到了{other_pet.name}，想要打招呼。",
            SocialInteractionType.PLAY: f"{self.pet.name}想要和{other_pet.name}一起玩耍。",
            SocialInteractionType.SHARE: f"{self.pet.name}想要和{other_pet.name}分享东西。",
            SocialInteractionType.COMPETE: f"{self.pet.name}想要和{other_pet.name}进行一场比赛。",
            SocialInteractionType.HELP: f"{self.pet.name}想要帮助{other_pet.name}。",
            SocialInteractionType.IGNORE: f"{self.pet.name}遇到了{other_pet.name}，但选择忽略。",
            SocialInteractionType.CONFLICT: f"{self.pet.name}与{other_pet.name}发生了小冲突。"
        }
        
        # 获取宠物ID，如果没有pet_id属性，使用名称
        self_pet_id = getattr(self.pet, 'pet_id', self.pet.name)
        other_pet_id = getattr(other_pet, 'pet_id', other_pet.name)
        
        event = SocialEvent(
            event_id=event_id,
            event_type=event_type,
            participants=[self_pet_id, other_pet_id],
            description=descriptions.get(event_type, "社交事件")
        )
        
        self.events.append(event)
        return event
    
    def resolve_social_event(self, event_id, outcome):
        """解决社交事件"""
        for event in self.events:
            if event.event_id == event_id:
                event.resolve(outcome)
                return True
        return False
    
    def get_recent_events(self, limit=10):
        """获取最近的社交事件"""
        sorted_events = sorted(self.events, key=lambda e: e.timestamp, reverse=True)
        return sorted_events[:limit]
    
    def update_social_skills(self, time_passed):
        """更新社交技能"""
        # 基于互动次数和时间更新社交技能
        skill_gain = min(0.1, self.interaction_count / 1000)
        for skill in self.social_skills:
            self.social_skills[skill] = min(100, self.social_skills[skill] + skill_gain)
    
    def get_social_summary(self):
        """获取社交摘要"""
        summary = {
            "total_relationships": len(self.relationships),
            "friends_count": len(self.friends),
            "rivals_count": len(self.rivals),
            "interaction_count": self.interaction_count,
            "social_skills": self.social_skills,
            "recent_events": [e.to_dict() for e in self.get_recent_events(5)]
        }
        return summary
    
    def to_dict(self):
        """转换为字典"""
        return {
            "relationships": {k: v.to_dict() for k, v in self.relationships.items()},
            "events": [e.to_dict() for e in self.events],
            "interaction_count": self.interaction_count,
            "social_skills": self.social_skills,
            "friends": self.friends,
            "rivals": self.rivals
        }
    
    def from_dict(self, data):
        """从字典加载"""
        relationships_data = data.get("relationships", {})
        self.relationships = {}
        for pet_id, rel_data in relationships_data.items():
            rel = SocialRelationship.from_dict(rel_data)
            self.relationships[pet_id] = rel
        
        events_data = data.get("events", [])
        self.events = []
        for event_data in events_data:
            event = SocialEvent(
                event_id=event_data["event_id"],
                event_type=SocialInteractionType(event_data["event_type"]),
                participants=event_data["participants"],
                timestamp=event_data.get("timestamp"),
                description=event_data.get("description")
            )
            event.resolved = event_data.get("resolved", False)
            event.outcome = event_data.get("outcome")
            self.events.append(event)
        
        self.interaction_count = data.get("interaction_count", 0)
        self.social_skills = data.get("social_skills", {
            "communication": 50,
            "empathy": 50,
            "conflict_resolution": 50,
            "cooperation": 50
        })
        self.friends = data.get("friends", [])
        self.rivals = data.get("rivals", [])
