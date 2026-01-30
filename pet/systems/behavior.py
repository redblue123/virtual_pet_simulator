import random
import time

class BehaviorSystem:
    """行为系统"""
    def __init__(self, pet):
        self.pet = pet
        self.behavior_history = []
        self.max_history_length = 100
        self.action_cooldowns = {}
    
    def get_action_rate(self):
        """获取行为频率"""
        if not self.behavior_history:
            return {}
        
        # 统计最近的行为频率
        recent_actions = [b["action"] for b in self.behavior_history[-50:]]
        action_counts = {}
        for action in recent_actions:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        total = len(recent_actions)
        return {k: v / total for k, v in action_counts.items()}
    
    def record_behavior(self, action, result, context):
        """记录行为"""
        behavior = {
            "action": action,
            "result": result,
            "context": context,
            "timestamp": time.time(),
            "pet_state": self.pet.get_status()
        }
        
        self.behavior_history.append(behavior)
        
        # 限制历史长度
        if len(self.behavior_history) > self.max_history_length:
            self.behavior_history.pop(0)
        
        # 更新冷却时间
        self.action_cooldowns[action] = time.time()
    
    def get_available_actions(self):
        """获取当前可用的行为"""
        available_actions = []
        
        # 检查各种行为的条件
        if not self.pet.is_sleeping:
            available_actions.append("feed")
            available_actions.append("play")
            available_actions.append("clean")
            available_actions.append("train")
        
        available_actions.append("sleep")
        
        return available_actions
    
    def get_random_action(self):
        """获取随机行为"""
        available_actions = self.get_available_actions()
        if not available_actions:
            return None
        return random.choice(available_actions)

class BehaviorTree:
    """行为树"""
    def __init__(self, root_node):
        self.root_node = root_node
    
    def execute(self, pet):
        """执行行为树"""
        return self.root_node.execute(pet)

class BehaviorTreeNode:
    """行为树节点基类"""
    def execute(self, pet):
        raise NotImplementedError

class CompositeNode(BehaviorTreeNode):
    """复合节点"""
    def __init__(self, children, name=""):
        self.children = children
        self.name = name

class SequenceNode(CompositeNode):
    """序列节点"""
    def execute(self, pet):
        for child in self.children:
            result = child.execute(pet)
            if result != "success":
                return result
        return "success"

class SelectorNode(CompositeNode):
    """选择节点"""
    def execute(self, pet):
        for child in self.children:
            result = child.execute(pet)
            if result == "success":
                return result
        return "failure"

class DecoratorNode(BehaviorTreeNode):
    """装饰节点"""
    def __init__(self, child, name=""):
        self.child = child
        self.name = name

class InverterNode(DecoratorNode):
    """取反节点"""
    def execute(self, pet):
        result = self.child.execute(pet)
        return "success" if result == "failure" else "failure"

class RepeaterNode(DecoratorNode):
    """重复节点"""
    def __init__(self, child, count=-1, name=""):
        super().__init__(child, name)
        self.count = count
    
    def execute(self, pet):
        if self.count == -1:
            # 无限重复
            while True:
                result = self.child.execute(pet)
                if result != "success":
                    return result
        else:
            # 有限重复
            for i in range(self.count):
                result = self.child.execute(pet)
                if result != "success":
                    return result
        return "success"

class ConditionNode(BehaviorTreeNode):
    """条件节点"""
    def __init__(self, condition_func, name=""):
        self.condition_func = condition_func
        self.name = name
    
    def execute(self, pet):
        return "success" if self.condition_func(pet) else "failure"

class ActionNode(BehaviorTreeNode):
    """动作节点"""
    def __init__(self, action_func, name=""):
        self.action_func = action_func
        self.name = name
    
    def execute(self, pet):
        result = self.action_func(pet)
        return "success" if result else "failure"

class BehaviorTreeBuilder:
    """行为树构建器"""
    @staticmethod
    def build_pet_behavior_tree():
        """构建宠物行为树"""
        # 构建行为树
        root = SelectorNode([
            # 高优先级：基本需求
            SequenceNode([
                ConditionNode(lambda pet: float(pet.get_status()["hunger"].split("/")[0]) > 70),
                ActionNode(lambda pet: pet.feed("普通食物"))
            ], "喂食序列"),
            
            SequenceNode([
                ConditionNode(lambda pet: float(pet.get_status()["energy"].split("/")[0]) < 30),
                ActionNode(lambda pet: pet.sleep())
            ], "睡眠序列"),
            
            SequenceNode([
                ConditionNode(lambda pet: float(pet.get_status()["hygiene"].split("/")[0]) < 30),
                ActionNode(lambda pet: pet.clean())
            ], "清洁序列"),
            
            # 中优先级：娱乐和训练
            SequenceNode([
                ConditionNode(lambda pet: float(pet.get_status()["energy"].split("/")[0]) > 50),
                SelectorNode([
                    ActionNode(lambda pet: pet.play("普通游戏")),
                    ActionNode(lambda pet: pet.train("intelligence"))
                ])
            ], "娱乐序列"),
            
            # 低优先级：探索和休息
            SelectorNode([
                ActionNode(lambda pet: pet._explore()),
                ActionNode(lambda pet: pet._rest())
            ], "探索休息序列")
        ], "根选择节点")
        
        return BehaviorTree(root)
