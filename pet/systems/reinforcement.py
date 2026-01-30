import numpy as np
import random
import json
from collections import defaultdict
from ..config import PetConfig

class ReinforcementLearningSystem:
    """强化学习系统"""
    def __init__(self, pet, learning_rate=None, discount_factor=None, exploration_rate=None, exploration_decay=None, min_exploration=None):
        self.pet = pet
        self.learning_rate = learning_rate or PetConfig.RL_LEARNING_RATE
        self.discount_factor = discount_factor or PetConfig.RL_DISCOUNT_FACTOR
        self.exploration_rate = exploration_rate or PetConfig.RL_EXPLORATION_RATE
        self.exploration_decay = exploration_decay or PetConfig.RL_EXPLORATION_DECAY
        self.min_exploration = min_exploration or PetConfig.RL_MIN_EXPLORATION
        
        # Q表 - 使用字典的字典结构，键为离散状态元组，值为动作到Q值的映射
        self.q_table = defaultdict(dict)
        self.q_table_2 = defaultdict(dict)  # 双Q学习
        
        # Q表优化参数
        self.q_table_compression_threshold = 1000  # 当Q表大小超过此阈值时进行压缩
        self.q_table_cleanup_interval = 1000  # 每学习多少步进行一次Q表清理
        
        # 经验回放
        self.replay_buffer = []
        self.max_replay_buffer_size = PetConfig.RL_MAX_REPLAY_BUFFER_SIZE
        self.batch_size = PetConfig.RL_BATCH_SIZE
        
        # 优先级经验回放
        self.priorities = []
        self.alpha = PetConfig.RL_ALPHA  # 优先级指数
        self.beta = PetConfig.RL_BETA  # 重要性采样权重指数
        self.beta_increment = PetConfig.RL_BETA_INCREMENT
        
        # 学习统计
        self.learning_steps = 0
        self.average_reward = 0
        self.total_reward = 0
        
        # 状态离散化参数
        self.state_bins = PetConfig.STATE_BINS
        
        # 可能的动作
        self.actions = PetConfig.RL_ACTIONS
        
        # 状态缓存 - 减少重复计算
        self._state_cache = {}
        self._last_status_time = 0
        self._status_cache_timeout = 0.1  # 状态缓存超时时间（秒）
    
    def get_discrete_state(self):
        """获取离散状态"""
        import time
        current_time = time.time()
        
        # 检查是否需要更新状态缓存
        if current_time - self._last_status_time > self._status_cache_timeout:
            status = self.pet.get_status()
            
            # 提取需要离散化的状态
            state = {
                "hunger": float(status["hunger"].split("/")[0]),
                "energy": float(status["energy"].split("/")[0]),
                "hygiene": float(status["hygiene"].split("/")[0]),
                "happiness": float(status["happiness"].split("/")[0]),
                "health": float(status["health"].split("/")[0])
            }
            
            # 离散化状态
            discrete_state = []
            for key, value in state.items():
                bins = self.state_bins[key]
                for i, bin_threshold in enumerate(bins):
                    if value <= bin_threshold:
                        discrete_state.append(i)
                        break
                else:
                    discrete_state.append(len(bins) - 1)
            
            # 转换为元组以便作为字典键
            discrete_state_tuple = tuple(discrete_state)
            
            # 更新缓存
            self._state_cache["discrete_state"] = discrete_state_tuple
            self._state_cache["continuous_state"] = state
            self._last_status_time = current_time
            
            return discrete_state_tuple
        else:
            # 使用缓存的状态
            return self._state_cache.get("discrete_state", tuple([0] * len(self.state_bins)))
    
    def choose_action(self, state):
        """选择动作"""
        # 探索与利用
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        else:
            # 利用Q表选择最优动作
            state_q = self.q_table.get(state)
            if state_q and state_q:
                # 优化：预先计算最大Q值的动作
                max_q = -float('inf')
                best_action = None
                for action, q_value in state_q.items():
                    if q_value > max_q:
                        max_q = q_value
                        best_action = action
                return best_action or random.choice(self.actions)
            else:
                return random.choice(self.actions)
    
    def calculate_reward(self, state, action, next_state):
        """计算奖励"""
        reward = 0
        
        # 1. 基于状态变化计算奖励
        # 计算各状态值的变化量
        hunger_change = next_state["hunger"] - state["hunger"]
        energy_change = next_state["energy"] - state["energy"]
        hygiene_change = next_state["hygiene"] - state["hygiene"]
        happiness_change = next_state["happiness"] - state["happiness"]
        health_change = next_state["health"] - state["health"]
        
        # 2. 负奖励：惩罚不良状态变化
        # 饥饿增加
        if hunger_change > 0:
            reward -= hunger_change * 0.1
        # 能量减少
        if energy_change < 0:
            reward += energy_change * 0.1  # 能量减少是负奖励
        # 清洁度减少
        if hygiene_change < 0:
            reward += hygiene_change * 0.05
        # 快乐度减少
        if happiness_change < 0:
            reward += happiness_change * 0.15
        # 健康度减少
        if health_change < 0:
            reward += health_change * 0.2
        
        # 3. 正奖励：奖励良好状态变化
        # 饥饿减少
        if hunger_change < 0:
            reward -= hunger_change * 0.1  # 饥饿减少是正奖励
        # 能量增加
        if energy_change > 0:
            reward += energy_change * 0.1
        # 清洁度增加
        if hygiene_change > 0:
            reward += hygiene_change * 0.05
        # 快乐度增加
        if happiness_change > 0:
            reward += happiness_change * 0.15
        # 健康度增加
        if health_change > 0:
            reward += health_change * 0.2
        
        # 4. 动作特定奖励：根据动作的有效性给予额外奖励
        if action == "feed" and hunger_change < 0:
            # 喂食成功减少饥饿
            reward += 1.0
        elif action == "sleep" and energy_change > 0:
            # 睡眠成功恢复能量
            reward += 1.5
        elif action == "clean" and hygiene_change > 0:
            # 清洁成功增加清洁度
            reward += 0.8
        elif action == "play" and happiness_change > 0:
            # 玩耍成功增加快乐度
            reward += 1.2
        elif action == "train":
            # 训练给予基础奖励
            reward += 0.5
        
        # 5. 状态奖励：良好状态给予额外奖励
        if next_state["hunger"] < 30 and next_state["energy"] > 70 and next_state["hygiene"] > 70:
            # 饥饿低、能量高、清洁度高的良好状态
            reward += 2.0
        
        return reward
    
    def learn(self, state, action, reward, next_state, done):
        """学习"""
        # 1. 确保状态是元组（以便作为字典键）
        if isinstance(state, list):
            state = tuple(state)
        if isinstance(next_state, list):
            next_state = tuple(next_state)
        
        # 2. 存储经验到回放缓冲区
        self._store_experience(state, action, reward, next_state, done)
        
        # 3. 经验回放学习：当回放缓冲区足够大时，从缓冲区中采样学习
        if len(self.replay_buffer) >= self.batch_size:
            self._learn_from_replay_buffer()
        
        # 4. 更新学习统计信息
        self.learning_steps += 1
        self.total_reward += reward
        self.average_reward = self.total_reward / self.learning_steps
        
        # 5. 衰减探索率：随着学习的进行，减少探索，增加利用
        self.exploration_rate = max(self.min_exploration, self.exploration_rate * self.exploration_decay)
        
        # 6. 增加beta值：随着学习的进行，增加重要性采样权重的影响
        self.beta = min(1.0, self.beta + self.beta_increment)
    
    def _store_experience(self, state, action, reward, next_state, done):
        """存储经验"""
        # 计算优先级
        priority = self._calculate_priority(state, action, reward, next_state, done)
        
        # 存储经验和优先级
        self.replay_buffer.append((state, action, reward, next_state, done))
        self.priorities.append(priority)
        
        # 限制回放缓冲区大小
        if len(self.replay_buffer) > self.max_replay_buffer_size:
            self.replay_buffer.pop(0)
            self.priorities.pop(0)
        
        # 优化：定期清理无效经验
        if len(self.replay_buffer) % 100 == 0:
            self._cleanup_invalid_experiences()
    
    def _calculate_priority(self, state, action, reward, next_state, done):
        """计算经验优先级"""
        # 确保状态是元组
        if isinstance(state, list):
            state = tuple(state)
        if isinstance(next_state, list):
            next_state = tuple(next_state)
        
        # 获取当前Q值
        current_q = self.q_table.get(state, {}).get(action, 0)
        
        # 计算目标Q值
        if done:
            target_q = reward
        else:
            # 双Q学习
            if next_state in self.q_table and self.q_table[next_state]:
                best_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
                target_q = reward + self.discount_factor * self.q_table_2.get(next_state, {}).get(best_action, 0)
            else:
                target_q = reward
        
        # 计算TD误差
        td_error = abs(target_q - current_q)
        
        # 优先级 = (|TD误差| + epsilon)^alpha
        epsilon = 1e-6
        priority = (td_error + epsilon) ** self.alpha
        
        return priority
    
    def _cleanup_invalid_experiences(self):
        """清理无效经验"""
        valid_experiences = []
        valid_priorities = []
        
        for exp, priority in zip(self.replay_buffer, self.priorities):
            state, action, reward, next_state, done = exp
            # 检查经验是否有效
            if (isinstance(state, (tuple, list)) and 
                isinstance(action, str) and 
                isinstance(reward, (int, float)) and 
                isinstance(next_state, (tuple, list)) and 
                isinstance(done, bool)):
                valid_experiences.append(exp)
                valid_priorities.append(priority)
        
        # 更新回放缓冲区和优先级
        self.replay_buffer = valid_experiences
        self.priorities = valid_priorities
    
    def _prioritized_sample(self):
        """优先级采样"""
        # 确保 priorities 和 replay_buffer 长度相同
        min_length = min(len(self.priorities), len(self.replay_buffer))
        if min_length < len(self.priorities):
            self.priorities = self.priorities[:min_length]
        if min_length < len(self.replay_buffer):
            self.replay_buffer = self.replay_buffer[:min_length]
        
        # 确保有足够的经验可采样
        if min_length < self.batch_size:
            # 经验不足时，返回所有经验
            samples = self.replay_buffer[:min_length]
            indices = list(range(min_length))
            weights = [1.0] * min_length
            return samples, indices, weights
        
        # 计算采样概率
        total_priority = sum(self.priorities)
        if total_priority == 0:
            # 所有优先级为0时，均匀采样
            probabilities = [1.0 / len(self.priorities)] * len(self.priorities)
        else:
            probabilities = [p / total_priority for p in self.priorities]
        
        # 采样
        indices = random.choices(range(len(self.replay_buffer)), weights=probabilities, k=self.batch_size)
        samples = [self.replay_buffer[i] for i in indices]
        
        # 计算重要性采样权重
        weights = []
        for i in indices:
            probability = probabilities[i]
            weight = (len(self.replay_buffer) * probability) ** (-self.beta)
            weights.append(weight)
        
        # 归一化权重
        if weights:
            max_weight = max(weights)
            weights = [w / max_weight for w in weights]
        
        return samples, indices, weights
    
    def _compress_q_table(self, q_table, threshold=0.1):
        """压缩Q表，删除低价值的条目
        
        Args:
            q_table (defaultdict): 要压缩的Q表
            threshold (float): Q值阈值，低于此值的条目将被删除
        
        Returns:
            defaultdict: 压缩后的Q表
        """
        compressed_table = defaultdict(dict)
        for state, actions in q_table.items():
            # 只保留Q值绝对值大于阈值的动作
            compressed_actions = {action: q_value for action, q_value in actions.items() if abs(q_value) > threshold}
            if compressed_actions:  # 只保留有有效动作的状态
                compressed_table[state] = compressed_actions
        return compressed_table
    
    def _cleanup_q_tables(self):
        """清理和压缩Q表"""
        # 压缩Q表
        self.q_table = self._compress_q_table(self.q_table)
        self.q_table_2 = self._compress_q_table(self.q_table_2)
    
    def _learn_from_replay_buffer(self):
        """从回放缓冲区学习"""
        # 优先级采样
        samples, indices, weights = self._prioritized_sample()
        
        for i, (state, action, reward, next_state, done) in enumerate(samples):
            # 确保状态是元组
            if isinstance(state, list):
                state = tuple(state)
            if isinstance(next_state, list):
                next_state = tuple(next_state)
            
            # 获取当前Q值
            current_q = self.q_table.get(state, {}).get(action, 0)
            current_q_2 = self.q_table_2.get(state, {}).get(action, 0)
            
            # 计算目标Q值
            if done:
                target_q = reward
                target_q_2 = reward
            else:
                # 双Q学习
                if next_state in self.q_table and self.q_table[next_state]:
                    best_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
                    target_q = reward + self.discount_factor * self.q_table_2.get(next_state, {}).get(best_action, 0)
                else:
                    target_q = reward
                
                if next_state in self.q_table_2 and self.q_table_2[next_state]:
                    best_action_2 = max(self.q_table_2[next_state], key=self.q_table_2[next_state].get)
                    target_q_2 = reward + self.discount_factor * self.q_table.get(next_state, {}).get(best_action_2, 0)
                else:
                    target_q_2 = reward
            
            # 更新Q表
            if state not in self.q_table:
                self.q_table[state] = {}
            if state not in self.q_table_2:
                self.q_table_2[state] = {}
            
            # 使用重要性采样权重
            weight = weights[i]
            self.q_table[state][action] = current_q + self.learning_rate * weight * (target_q - current_q)
            self.q_table_2[state][action] = current_q_2 + self.learning_rate * weight * (target_q_2 - current_q_2)
            
            # 更新优先级
            new_priority = self._calculate_priority(state, action, reward, next_state, done)
            self.priorities[indices[i]] = new_priority
        
        # 定期清理Q表
        if self.learning_steps % self.q_table_cleanup_interval == 0:
            self._cleanup_q_tables()
    
    def get_learning_stats(self):
        """获取学习统计"""
        return {
            "learning_steps": self.learning_steps,
            "average_reward": self.average_reward,
            "exploration_rate": self.exploration_rate,
            "replay_buffer_size": len(self.replay_buffer),
            "q_table_size": sum(len(v) for v in self.q_table.values())
        }
    
    def save_learning_data(self, file_path):
        """保存学习数据"""
        # 转换Q表为可序列化格式
        def convert_keys(obj):
            if isinstance(obj, dict):
                new_obj = {}
                for k, v in obj.items():
                    if isinstance(k, tuple):
                        new_obj[str(k)] = convert_keys(v)
                    else:
                        new_obj[k] = convert_keys(v)
                return new_obj
            return obj
        
        data = {
            "q_table": convert_keys(self.q_table),
            "q_table_2": convert_keys(self.q_table_2),
            "learning_steps": self.learning_steps,
            "average_reward": self.average_reward,
            "total_reward": self.total_reward,
            "exploration_rate": self.exploration_rate
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_learning_data(self, file_path):
        """加载学习数据"""
        import json
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 转换键为元组
            def list_to_tuple(obj):
                if isinstance(obj, list):
                    return tuple(list_to_tuple(item) for item in obj)
                return obj
            
            def convert_keys_back(obj):
                if isinstance(obj, dict):
                    new_obj = {}
                    for k, v in obj.items():
                        if k.startswith('(') and k.endswith(')'):
                            # 转换字符串键为元组
                            try:
                                key_tuple = tuple(map(int, k.strip('()').split(',')))
                                new_obj[key_tuple] = convert_keys_back(v)
                            except:
                                new_obj[k] = convert_keys_back(v)
                        else:
                            new_obj[k] = convert_keys_back(v)
                    return new_obj
                return obj
            
            # 恢复Q表
            self.q_table = defaultdict(dict, convert_keys_back(data.get("q_table", {})))
            self.q_table_2 = defaultdict(dict, convert_keys_back(data.get("q_table_2", {})))
            
            # 恢复学习统计
            self.learning_steps = data.get("learning_steps", 0)
            self.average_reward = data.get("average_reward", 0)
            self.total_reward = data.get("total_reward", 0)
            self.exploration_rate = data.get("exploration_rate", self.exploration_rate)
            
            return True
        except Exception as e:
            print(f"加载学习数据失败: {e}")
            return False
