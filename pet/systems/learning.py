from collections import defaultdict, Counter
import time

class LearningSystem:
    """学习系统"""
    def __init__(self, pet):
        self.pet = pet
        self.behavior_history = []
        self.max_history_length = 200
        
        # 行为效果学习
        self.behavior_effects = defaultdict(list)
        
        # 用户交互学习
        self.user_interactions = defaultdict(list)
        
        # 偏好学习
        self.preferences = defaultdict(float)
    
    def record_behavior(self, action, result, context):
        """记录行为及其结果"""
        behavior = {
            "action": action,
            "result": result,
            "context": context,
            "timestamp": time.time(),
            "pet_state_before": self.pet.get_status()
        }
        
        self.behavior_history.append(behavior)
        
        # 限制历史长度
        if len(self.behavior_history) > self.max_history_length:
            self.behavior_history.pop(0)
        
        # 学习行为效果
        self._learn_behavior_effect(action, result, context)
    
    def record_user_interaction(self, interaction_type, kwargs):
        """记录用户交互"""
        interaction = {
            "interaction_type": interaction_type,
            "kwargs": kwargs,
            "timestamp": time.time(),
            "pet_state": self.pet.get_status()
        }
        
        self.user_interactions[interaction_type].append(interaction)
        
        # 学习用户偏好
        self._learn_user_preference(interaction_type, kwargs)
    
    def _learn_behavior_effect(self, action, result, context):
        """学习行为效果"""
        # 记录行为效果
        self.behavior_effects[action].append({
            "result": result,
            "context": context,
            "timestamp": time.time()
        })
        
        # 基于效果调整偏好
        if "成功" in result:
            self.preferences[action] += 0.1
        elif "无法" in result:
            self.preferences[action] -= 0.05
    
    def _learn_user_preference(self, interaction_type, kwargs):
        """学习用户偏好"""
        # 增加用户交互的偏好值
        self.preferences[interaction_type] += 0.2
        
        # 学习具体参数偏好
        for key, value in kwargs.items():
            if value:
                preference_key = f"{interaction_type}_{key}_{value}"
                self.preferences[preference_key] += 0.1
    
    def learn_from_interaction(self, interaction_type, result):
        """从交互中学习"""
        # 记录交互结果
        self.behavior_history.append({
            "action": interaction_type,
            "result": result,
            "timestamp": time.time(),
            "pet_state": self.pet.get_status()
        })
        
        # 基于结果调整偏好
        if "成功" in result:
            self.preferences[interaction_type] += 0.15
    
    def get_preferences(self):
        """获取学习到的偏好"""
        return self.preferences
    
    def get_behavior_patterns(self):
        """获取行为模式"""
        patterns = {}
        
        # 分析行为频率
        action_counts = Counter([b["action"] for b in self.behavior_history])
        patterns["action_frequency"] = dict(action_counts)
        
        # 分析行为效果
        action_effects = defaultdict(list)
        for b in self.behavior_history:
            action_effects[b["action"]].append(b["result"])
        patterns["action_effects"] = dict(action_effects)
        
        return patterns
    
    def predict_behavior(self, context):
        """预测行为"""
        # 基于当前上下文和历史行为预测
        # 这里可以实现更复杂的预测逻辑
        
        # 简单实现：返回最常见的行为
        if not self.behavior_history:
            return "feed"
        
        action_counts = Counter([b["action"] for b in self.behavior_history])
        return action_counts.most_common(1)[0][0]
