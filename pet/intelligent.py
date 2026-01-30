import time
from collections import defaultdict, Counter
from .base import Pet
from .config import PetConfig
from .systems.decision import DecisionSystem
from .systems.behavior import BehaviorSystem, BehaviorTreeBuilder
from .systems.learning import LearningSystem
from .systems.reinforcement import ReinforcementLearningSystem

class IntelligentPet(Pet):
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
        self.spontaneous_action_cooldown = PetConfig.SPONTANEOUS_ACTION_COOLDOWN  # 自发行为冷却时间（秒）
        
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
        
        # 防止递归调用：只在非递归调用时执行自发行为
        if not hasattr(self, '_updating') or not self._updating:
            if current_time - self.last_spontaneous_action > self.spontaneous_action_cooldown:
                self._updating = True
                try:
                    self.execute_spontaneous_action()
                    self.last_spontaneous_action = current_time
                finally:
                    self._updating = False
    
    def execute_spontaneous_action(self):
        """执行自发行为（使用强化学习和行为树）"""
        # 第二阶段：优先使用强化学习决策
        # 1. 获取当前的离散状态，用于强化学习决策
        state_before = self.reinforcement_learning.get_discrete_state()
        # 2. 使用强化学习系统选择一个动作
        action = self.reinforcement_learning.choose_action(state_before)
        
        if action:
            # 3. 执行选择的行为
            result = self._execute_action(action)
            
            # 4. 评估执行后的状态
            state_after = self.reinforcement_learning.get_discrete_state()
            
            # 5. 计算奖励 - 直接使用原始状态字典
            # 获取执行前后的详细状态，使用 force_update=False 避免不必要的更新
            status_before = self.get_status(force_update=False)
            status_after = self.get_status(force_update=False)
            # 提取需要的状态值（如饥饿、能量、清洁度等）
            state_dict_before = self._extract_state_values(status_before)
            state_dict_after = self._extract_state_values(status_after)
            # 使用强化学习系统计算奖励
            reward = self.reinforcement_learning.calculate_reward(
                state_dict_before, action, state_dict_after
            )
            
            # 6. 强化学习 - 根据执行结果更新Q-table
            self.reinforcement_learning.learn(state_before, action, reward, state_after, False)
            
            # 7. 记录行为结果到学习系统
            self.learning_system.record_behavior(action, result, {})
            
            return result
        else:
            # 备用：如果强化学习没有选择动作，使用行为树
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
            clean_type = kwargs.get("clean_type", "毛发清理")
            result = self.clean(clean_type)
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
            # 直接使用原始状态字典计算奖励
            status_before = self.get_status()
            status_after = self.get_status()
            # 提取需要的状态值
            state_dict_before = self._extract_state_values(status_before)
            state_dict_after = self._extract_state_values(status_after)
            reward = self.reinforcement_learning.calculate_reward(
                state_dict_before, rl_action, state_dict_after
            )
            self.reinforcement_learning.learn(state_before, rl_action, reward, state_after, False)
        
        return result
    
    def _extract_state_values(self, status):
        """从状态字典中提取需要的数值"""
        return {
            "hunger": float(status["hunger"].split("/")[0]),
            "energy": float(status["energy"].split("/")[0]),
            "hygiene": float(status["hygiene"].split("/")[0]),
            "happiness": float(status["happiness"].split("/")[0]),
            "health": float(status["health"].split("/")[0])
        }
    
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
