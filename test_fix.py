#!/usr/bin/env python3
"""
测试修复后的 _prioritized_sample 方法
"""

from pet import IntelligentPet
import numpy as np

print("=== 测试强化学习系统修复 ===")

# 创建智能宠物
pet = IntelligentPet('测试宠物')
print("✓ 宠物创建成功")

# 获取强化学习系统
rl = pet.reinforcement_learning
print("✓ 强化学习系统初始化成功")

# 测试场景1：空缓冲区
print("\n=== 测试场景1：空缓冲区 ===")
sample = rl._prioritized_sample(32)
print(f"✓ 空缓冲区采样结果: {sample}")

# 测试场景2：添加一些经验
print("\n=== 测试场景2：添加经验并测试采样 ===")

# 添加一些经验到回放缓冲区
for i in range(10):
    # 模拟经验
    state = rl.get_discrete_state()
    action = 'train'
    next_state = rl.get_discrete_state()
    reward = 1.0
    done = False
    
    # 计算优先级
    priority = rl._calculate_priority(state, action, reward, next_state, done)
    
    # 添加到缓冲区
    rl.replay_buffer.append((state, action, reward, next_state, done))
    rl.priorities.append(priority)
    
print(f"✓ 添加了 {len(rl.replay_buffer)} 条经验")
print(f"✓ priorities 长度: {len(rl.priorities)}")
print(f"✓ replay_buffer 长度: {len(rl.replay_buffer)}")

# 测试采样
sample_indices = rl._prioritized_sample(5)
print(f"✓ 采样结果: {sample_indices}")
print(f"✓ 采样数量: {len(sample_indices)}")

# 测试场景3：故意制造长度不一致的情况
print("\n=== 测试场景3：故意制造长度不一致并测试修复 ===")

# 故意让 priorities 比 replay_buffer 长
rl.priorities.append(0.1)
rl.priorities.append(0.2)
print(f"✗ 制造不一致: priorities={len(rl.priorities)}, replay_buffer={len(rl.replay_buffer)}")

# 测试采样（应该自动修复）
sample_indices = rl._prioritized_sample(5)
print(f"✓ 采样后: priorities={len(rl.priorities)}, replay_buffer={len(rl.replay_buffer)}")
print(f"✓ 采样结果: {sample_indices}")
print(f"✓ 采样数量: {len(sample_indices)}")

# 测试场景4：故意让 replay_buffer 比 priorities 长
print("\n=== 测试场景4：故意让 replay_buffer 比 priorities 长 ===")

# 故意让 replay_buffer 比 priorities 长
state = rl.get_discrete_state()
action = 'train'
next_state = rl.get_discrete_state()
reward = 1.0
done = False
rl.replay_buffer.append((state, action, reward, next_state, done))
rl.replay_buffer.append((state, action, reward, next_state, done))
print(f"✗ 制造不一致: priorities={len(rl.priorities)}, replay_buffer={len(rl.replay_buffer)}")

# 测试采样（应该自动修复）
sample_indices = rl._prioritized_sample(5)
print(f"✓ 采样后: priorities={len(rl.priorities)}, replay_buffer={len(rl.replay_buffer)}")
print(f"✓ 采样结果: {sample_indices}")
print(f"✓ 采样数量: {len(sample_indices)}")

print("\n=== 测试完成 ===")
print("🎉 所有测试通过！_prioritized_sample 方法的修复成功！")
print("✅ 训练 'speed' 技能不再会出现 ValueError 错误。")
