#!/usr/bin/env python3
import random
import time
from enum import Enum

class EnvironmentElementType(Enum):
    """环境元素类型枚举"""
    FOOD_BOWL = "food_bowl"  # 食物碗
    WATER_BOWL = "water_bowl"  # 水碗
    BED = "bed"  # 床
    TOY = "toy"  # 玩具
    SCRATCH_POST = "scratch_post"  # 猫抓板
    PLANT = "plant"  # 植物
    WINDOW = "window"  # 窗户
    DOOR = "door"  # 门
    SOFA = "sofa"  # 沙发
    TABLE = "table"  # 桌子

class EnvironmentElement:
    """环境元素类"""
    def __init__(self, element_id, element_type, name, description, status=None):
        self.element_id = element_id
        self.element_type = element_type
        self.name = name
        self.description = description
        self.status = status or {}
        self.last_interaction = None
        self.interaction_count = 0
    
    def interact(self, pet, interaction_type):
        """与环境元素互动"""
        # 记录互动
        self.last_interaction = time.time()
        self.interaction_count += 1
        
        # 根据环境元素类型和互动类型执行不同的互动
        if self.element_type == EnvironmentElementType.FOOD_BOWL:
            return self._interact_with_food_bowl(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.WATER_BOWL:
            return self._interact_with_water_bowl(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.BED:
            return self._interact_with_bed(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.TOY:
            return self._interact_with_toy(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.SCRATCH_POST:
            return self._interact_with_scratch_post(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.PLANT:
            return self._interact_with_plant(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.WINDOW:
            return self._interact_with_window(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.DOOR:
            return self._interact_with_door(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.SOFA:
            return self._interact_with_sofa(pet, interaction_type)
        elif self.element_type == EnvironmentElementType.TABLE:
            return self._interact_with_table(pet, interaction_type)
        
        return {"success": False, "message": "未知的环境元素类型"}
    
    def _interact_with_food_bowl(self, pet, interaction_type):
        """与食物碗互动"""
        if interaction_type == "eat":
            if pet.hunger > 0:
                food_amount = min(pet.hunger, 30)
                pet.hunger -= food_amount
                pet.happiness += 5
                # 触发情感
                if hasattr(pet, 'emotional_system'):
                    from pet.enums import EmotionType
                    pet.emotional_system.trigger_emotion(EmotionType.JOY, 0.3, "从食物碗进食")
                return {
                    "success": True,
                    "message": f"宠物从食物碗中进食，饥饿度减少了{food_amount}，变得更开心了！",
                    "effects": {"hunger": -food_amount, "happiness": 5}
                }
            else:
                return {
                    "success": False,
                    "message": "宠物不饿，不需要进食。"
                }
        elif interaction_type == "check":
            return {
                "success": True,
                "message": "食物碗里有食物。"
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_water_bowl(self, pet, interaction_type):
        """与水碗互动"""
        if interaction_type == "drink":
            # 检查宠物是否需要喝水
            needs_water = False
            if hasattr(pet, 'thirst'):
                needs_water = pet.thirst > 0
            else:
                # 如果没有thirst属性，根据hunger判断
                needs_water = pet.hunger > 30
            
            if needs_water:
                thirst_amount = min(pet.thirst, 25) if hasattr(pet, 'thirst') else 25
                if hasattr(pet, 'thirst'):
                    pet.thirst -= thirst_amount
                pet.happiness += 3
                # 触发情感
                if hasattr(pet, 'emotional_system'):
                    from pet.enums import EmotionType
                    pet.emotional_system.trigger_emotion(EmotionType.CALM, 0.2, "从水碗喝水")
                return {
                    "success": True,
                    "message": f"宠物从水碗中喝水，变得更舒适了！",
                    "effects": {"thirst": -thirst_amount, "happiness": 3}
                }
            else:
                return {
                    "success": False,
                    "message": "宠物不渴，不需要喝水。"
                }
        elif interaction_type == "check":
            return {
                "success": True,
                "message": "水碗里有水。"
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_bed(self, pet, interaction_type):
        """与床互动"""
        if interaction_type == "sleep":
            if pet.energy < 70:
                pet.sleep()
                # 触发情感
                if hasattr(pet, 'emotional_system'):
                    from pet.enums import EmotionType
                    pet.emotional_system.trigger_emotion(EmotionType.CALM, 0.4, "在床上睡觉")
                return {
                    "success": True,
                    "message": "宠物在床上睡着了，会恢复能量。",
                    "effects": {"energy": "恢复中"}
                }
            else:
                return {
                    "success": False,
                    "message": "宠物精力充沛，不需要睡觉。"
                }
        elif interaction_type == "rest":
            pet.energy = min(100, pet.energy + 10)
            pet.happiness += 2
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CALM, 0.3, "在床上休息")
            return {
                "success": True,
                "message": "宠物在床上休息了一会儿，精力恢复了一些。",
                "effects": {"energy": 10, "happiness": 2}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_toy(self, pet, interaction_type):
        """与玩具互动"""
        if interaction_type == "play":
            pet.happiness = min(100, pet.happiness + 15)
            pet.energy = max(0, pet.energy - 10)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.EXCITEMENT, 0.4, "玩玩具")
            return {
                "success": True,
                "message": "宠物玩得很开心，快乐度增加了！",
                "effects": {"happiness": 15, "energy": -10}
            }
        elif interaction_type == "explore":
            # 检查宠物是否有curiosity属性
            if hasattr(pet, 'curiosity'):
                pet.curiosity = min(100, pet.curiosity + 5)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CURIOSITY, 0.3, "探索玩具")
            return {
                "success": True,
                "message": "宠物对玩具产生了好奇心。",
                "effects": {"curiosity": 5}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_scratch_post(self, pet, interaction_type):
        """与猫抓板互动"""
        if interaction_type == "scratch":
            pet.happiness += 8
            pet.energy = max(0, pet.energy - 5)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CALM, 0.2, "使用猫抓板")
            return {
                "success": True,
                "message": "宠物使用了猫抓板，感到很满足。",
                "effects": {"happiness": 8, "energy": -5}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_plant(self, pet, interaction_type):
        """与植物互动"""
        if interaction_type == "explore":
            # 检查宠物是否有curiosity属性
            if hasattr(pet, 'curiosity'):
                pet.curiosity = min(100, pet.curiosity + 8)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CURIOSITY, 0.4, "探索植物")
            return {
                "success": True,
                "message": "宠物对植物产生了浓厚的兴趣，正在仔细观察。",
                "effects": {"curiosity": 8}
            }
        elif interaction_type == "touch":
            pet.happiness += 3
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CALM, 0.2, "触摸植物")
            return {
                "success": True,
                "message": "宠物轻轻触摸了植物，感到很有趣。",
                "effects": {"happiness": 3}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_window(self, pet, interaction_type):
        """与窗户互动"""
        if interaction_type == "look_out":
            # 检查宠物是否有curiosity属性
            if hasattr(pet, 'curiosity'):
                pet.curiosity = min(100, pet.curiosity + 10)
            pet.happiness += 5
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CURIOSITY, 0.5, "看窗外")
            return {
                "success": True,
                "message": "宠物看着窗外的景色，感到很好奇。",
                "effects": {"curiosity": 10, "happiness": 5}
            }
        elif interaction_type == "sunbathe":
            pet.energy = min(100, pet.energy + 15)
            pet.happiness += 8
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CALM, 0.4, "晒太阳")
            return {
                "success": True,
                "message": "宠物在窗户边晒太阳，感到很舒适，精力恢复了。",
                "effects": {"energy": 15, "happiness": 8}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_door(self, pet, interaction_type):
        """与门互动"""
        if interaction_type == "check":
            # 检查宠物是否有curiosity属性
            if hasattr(pet, 'curiosity'):
                pet.curiosity = min(100, pet.curiosity + 5)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CURIOSITY, 0.3, "检查门")
            return {
                "success": True,
                "message": "宠物检查了门，想知道门后面有什么。",
                "effects": {"curiosity": 5}
            }
        elif interaction_type == "scratch":
            pet.happiness += 3
            pet.energy = max(0, pet.energy - 3)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.EXCITEMENT, 0.2, "抓门")
            return {
                "success": True,
                "message": "宠物抓了抓门，似乎想出去。",
                "effects": {"happiness": 3, "energy": -3}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_sofa(self, pet, interaction_type):
        """与沙发互动"""
        if interaction_type == "rest":
            pet.energy = min(100, pet.energy + 8)
            pet.happiness += 5
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CALM, 0.3, "在沙发上休息")
            return {
                "success": True,
                "message": "宠物在沙发上休息，感到很舒适。",
                "effects": {"energy": 8, "happiness": 5}
            }
        elif interaction_type == "play":
            pet.happiness += 10
            pet.energy = max(0, pet.energy - 8)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.JOY, 0.3, "在沙发上玩耍")
            return {
                "success": True,
                "message": "宠物在沙发上玩耍，玩得很开心。",
                "effects": {"happiness": 10, "energy": -8}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def _interact_with_table(self, pet, interaction_type):
        """与桌子互动"""
        if interaction_type == "explore":
            # 检查宠物是否有curiosity属性
            if hasattr(pet, 'curiosity'):
                pet.curiosity = min(100, pet.curiosity + 7)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.CURIOSITY, 0.4, "探索桌子")
            return {
                "success": True,
                "message": "宠物在桌子上探索，发现了一些有趣的东西。",
                "effects": {"curiosity": 7}
            }
        elif interaction_type == "jump":
            pet.happiness += 5
            pet.energy = max(0, pet.energy - 5)
            # 触发情感
            if hasattr(pet, 'emotional_system'):
                from pet.enums import EmotionType
                pet.emotional_system.trigger_emotion(EmotionType.EXCITEMENT, 0.3, "跳上桌子")
            return {
                "success": True,
                "message": "宠物跳上了桌子，感到很兴奋。",
                "effects": {"happiness": 5, "energy": -5}
            }
        return {"success": False, "message": "无效的互动类型"}
    
    def get_status(self):
        """获取环境元素状态"""
        return {
            "element_id": self.element_id,
            "element_type": self.element_type.value,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "last_interaction": self.last_interaction,
            "interaction_count": self.interaction_count
        }
    
    def to_dict(self):
        """转换为字典"""
        return {
            "element_id": self.element_id,
            "element_type": self.element_type.value,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "last_interaction": self.last_interaction,
            "interaction_count": self.interaction_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建环境元素"""
        element_type = EnvironmentElementType(data["element_type"])
        return cls(
            element_id=data["element_id"],
            element_type=element_type,
            name=data["name"],
            description=data["description"],
            status=data.get("status", {})
        )

class EnvironmentSystem:
    """环境系统"""
    def __init__(self, pet):
        self.pet = pet
        self.elements = {}  # 环境元素字典，键为元素ID，值为环境元素对象
        self._initialize_default_elements()
    
    def _initialize_default_elements(self):
        """初始化默认环境元素"""
        default_elements = [
            EnvironmentElement(
                element_id="food_bowl_1",
                element_type=EnvironmentElementType.FOOD_BOWL,
                name="食物碗",
                description="宠物的食物碗，里面有食物。"
            ),
            EnvironmentElement(
                element_id="water_bowl_1",
                element_type=EnvironmentElementType.WATER_BOWL,
                name="水碗",
                description="宠物的水碗，里面有水。"
            ),
            EnvironmentElement(
                element_id="bed_1",
                element_type=EnvironmentElementType.BED,
                name="宠物床",
                description="宠物的舒适小床。"
            ),
            EnvironmentElement(
                element_id="toy_1",
                element_type=EnvironmentElementType.TOY,
                name="玩具球",
                description="宠物喜欢的玩具球。"
            ),
            EnvironmentElement(
                element_id="window_1",
                element_type=EnvironmentElementType.WINDOW,
                name="窗户",
                description="可以看到外面景色的窗户。"
            ),
            EnvironmentElement(
                element_id="sofa_1",
                element_type=EnvironmentElementType.SOFA,
                name="沙发",
                description="舒适的沙发，宠物喜欢在上面休息。"
            )
        ]
        
        for element in default_elements:
            self.elements[element.element_id] = element
    
    def add_element(self, element):
        """添加环境元素"""
        self.elements[element.element_id] = element
    
    def remove_element(self, element_id):
        """移除环境元素"""
        if element_id in self.elements:
            del self.elements[element_id]
            return True
        return False
    
    def get_element(self, element_id):
        """获取环境元素"""
        return self.elements.get(element_id)
    
    def get_all_elements(self):
        """获取所有环境元素"""
        return list(self.elements.values())
    
    def get_elements_by_type(self, element_type):
        """按类型获取环境元素"""
        return [element for element in self.elements.values() if element.element_type == element_type]
    
    def interact_with_element(self, element_id, interaction_type):
        """与环境元素互动"""
        if element_id in self.elements:
            element = self.elements[element_id]
            result = element.interact(self.pet, interaction_type)
            
            # 记录互动到宠物的历史
            if hasattr(self.pet, 'interaction_history'):
                self.pet.interaction_history.append({
                    "type": "environment",
                    "element_id": element_id,
                    "element_name": element.name,
                    "interaction_type": interaction_type,
                    "result": result,
                    "timestamp": time.time()
                })
            
            return result
        return {"success": False, "message": "环境元素不存在"}
    
    def update_environment(self, time_passed):
        """更新环境状态"""
        # 这里可以添加环境随时间变化的逻辑
        # 例如，食物碗中的食物会减少，水碗中的水会蒸发等
        pass
    
    def get_environment_summary(self):
        """获取环境摘要"""
        summary = {
            "total_elements": len(self.elements),
            "elements": [element.get_status() for element in self.elements.values()]
        }
        return summary
    
    def to_dict(self):
        """转换为字典"""
        return {
            "elements": [element.to_dict() for element in self.elements.values()]
        }
    
    def from_dict(self, data):
        """从字典加载"""
        elements_data = data.get("elements", [])
        self.elements = {}
        for element_data in elements_data:
            element = EnvironmentElement.from_dict(element_data)
            self.elements[element.element_id] = element
