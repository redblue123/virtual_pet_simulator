from collections import defaultdict
import random

class DecisionSystem:
    """决策系统"""
    def __init__(self, pet):
        self.pet = pet
        self.decision_history = []
        self.max_history_length = 50
        self.confidence_threshold = 0.7
    
    def make_decision(self, available_actions):
        """做出决策"""
        # 基于当前状态评估每个动作的价值
        action_values = {}
        for action in available_actions:
            action_values[action] = self._evaluate_action(action)
        
        # 选择价值最高的动作
        best_action = max(action_values.items(), key=lambda x: x[1])[0]
        confidence = action_values[best_action] / sum(action_values.values()) if sum(action_values.values()) > 0 else 0
        
        # 记录决策
        self.decision_history.append({
            "action": best_action,
            "confidence": confidence,
            "state": self.pet.get_status()
        })
        
        # 限制历史长度
        if len(self.decision_history) > self.max_history_length:
            self.decision_history.pop(0)
        
        return best_action, confidence
    
    def _evaluate_action(self, action):
        """评估动作的价值"""
        value = 0
        
        # 基于当前状态评估
        status = self.pet.get_status()
        
        if action == "feed":
            # 饥饿时喂食价值高
            hunger = float(status["hunger"].split("/")[0])
            value += hunger * 0.8
        elif action == "play":
            # 精力充足时玩耍价值高
            energy = float(status["energy"].split("/")[0])
            value += energy * 0.6
        elif action == "sleep":
            # 精力不足时睡觉价值高
            energy = float(status["energy"].split("/")[0])
            value += (100 - energy) * 0.7
        elif action == "clean":
            # 清洁度低时清洁价值高
            hygiene = float(status["hygiene"].split("/")[0])
            value += (100 - hygiene) * 0.5
        elif action == "train":
            # 精力充足时训练价值高
            energy = float(status["energy"].split("/")[0])
            value += energy * 0.4
        
        # 考虑性格偏好
        if hasattr(self.pet, "personality_traits"):
            for trait, strength in self.pet.personality_traits.items():
                if trait.value == "顽皮" and action == "play":
                    value += 20 * strength
                elif trait.value == "懒惰" and action == "sleep":
                    value += 20 * strength
                elif trait.value == "贪吃" and action == "feed":
                    value += 20 * strength
                elif trait.value == "爱干净" and action == "clean":
                    value += 20 * strength
        
        return value
    
    def predict_needs(self):
        """预测宠物需求"""
        status = self.pet.get_status()
        needs = []
        
        # 检查各项指标
        hunger = float(status["hunger"].split("/")[0])
        energy = float(status["energy"].split("/")[0])
        hygiene = float(status["hygiene"].split("/")[0])
        happiness = float(status["happiness"].split("/")[0])
        
        if hunger > 70:
            needs.append(("hunger", "高", 0.9))
        elif hunger > 40:
            needs.append(("hunger", "中", 0.6))
        
        if energy < 30:
            needs.append(("energy", "低", 0.8))
        elif energy < 60:
            needs.append(("energy", "中", 0.5))
        
        if hygiene < 30:
            needs.append(("hygiene", "低", 0.7))
        elif hygiene < 60:
            needs.append(("hygiene", "中", 0.4))
        
        if happiness < 30:
            needs.append(("happiness", "低", 0.6))
        
        # 按优先级排序
        needs.sort(key=lambda x: x[2], reverse=True)
        
        return needs
    
    def predict_next_action(self):
        """预测下一步动作"""
        available_actions = ["feed", "play", "sleep", "clean", "train"]
        best_action, confidence = self.make_decision(available_actions)
        return {
            "action": best_action,
            "confidence": confidence,
            "reason": self._get_action_reason(best_action)
        }
    
    def _get_action_reason(self, action):
        """获取动作的原因"""
        reasons = {
            "feed": "宠物可能饿了",
            "play": "宠物可能想玩耍",
            "sleep": "宠物可能累了",
            "clean": "宠物可能需要清洁",
            "train": "宠物可能需要训练"
        }
        return reasons.get(action, "宠物想做这个动作")
    
    def get_confidence(self):
        """获取当前决策信心"""
        if not self.decision_history:
            return 0.5
        return self.decision_history[-1]["confidence"]
