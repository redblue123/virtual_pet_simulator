#!/usr/bin/env python3
"""
测试所有优化和新功能
"""
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pet.base import Pet
from tasks import TaskSystem, TaskDifficulty
from achievements import AchievementSystem
from pet.systems.reinforcement import ReinforcementLearningSystem

def test_task_system():
    """测试任务系统"""
    print("=" * 60)
    print("测试任务系统")
    print("=" * 60)
    
    # 创建宠物实例
    pet = Pet("测试宠物", "猫咪")
    
    # 创建任务系统
    task_system = TaskSystem(pet)
    
    # 测试任务生成
    print("1. 测试任务生成:")
    tasks = task_system.get_active_tasks()
    print(f"   当前活跃任务数: {len(tasks)}")
    for task in tasks:
        print(f"   - {task.description} (难度: {task.difficulty.value})")
    
    # 测试任务进度更新
    print("\n2. 测试任务进度更新:")
    # 模拟喂食操作
    pet.hunger = 0  # 喂食成功
    from tasks import TaskType
    rewards = task_system.update_task_progress(TaskType.FEED, 1)
    print(f"   更新喂食任务进度，获得奖励: {rewards}")
    
    # 检查任务状态
    tasks = task_system.get_active_tasks()
    for task in tasks:
        if task.task_type == TaskType.FEED:
            print(f"   喂食任务进度: {task.progress}/{task.target}")
    
    # 测试任务完成
    print("\n3. 测试任务完成:")
    # 快速完成一个简单任务
    simple_task = next((t for t in tasks if t.difficulty == TaskDifficulty.EASY), None)
    if simple_task:
        print(f"   尝试完成任务: {simple_task.description}")
        # 直接更新进度到目标值
        simple_task.progress = simple_task.target
        simple_task.complete()
        print(f"   任务状态: {simple_task.status.value}")
    
    print("任务系统测试完成！")
    print("=" * 60)

def test_achievement_system():
    """测试成就系统"""
    print("\n" + "=" * 60)
    print("测试成就系统")
    print("=" * 60)
    
    # 创建宠物实例
    pet = Pet("测试宠物", "猫咪")
    
    # 创建成就系统
    achievement_system = AchievementSystem(pet)
    
    # 测试成就初始化
    print("1. 测试成就初始化:")
    achievements = achievement_system.get_achievements()
    print(f"   成就总数: {len(achievements)}")
    
    # 按类别统计成就
    categories = {}
    for achievement in achievements:
        categories[achievement.category.value] = categories.get(achievement.category.value, 0) + 1
    print("   成就分类:")
    for category, count in categories.items():
        print(f"   - {category}: {count}个")
    
    # 测试成就进度更新
    print("\n2. 测试成就进度更新:")
    # 模拟喂食操作10次
    for i in range(10):
        achievement_system.update_care_achievements("feed", 1)
    
    # 检查成就进度
    feed_achievements = [a for a in achievements if a.category.value == "照顾"]
    for achievement in feed_achievements:
        print(f"   {achievement.name}: {achievement.progress}/{achievement.requirement}")
    
    # 测试成就解锁
    print("\n3. 测试成就解锁:")
    unlocked_count = achievement_system.get_unlocked_count()
    recently_unlocked = achievement_system.get_recently_unlocked()
    if recently_unlocked:
        print("   最近解锁的成就:")
        for achievement in recently_unlocked:
            print(f"   - {achievement.name}: {achievement.description}")
    print(f"   总解锁成就数: {unlocked_count}")
    
    print("成就系统测试完成！")
    print("=" * 60)

def test_reinforcement_learning():
    """测试强化学习算法性能"""
    print("\n" + "=" * 60)
    print("测试强化学习算法性能")
    print("=" * 60)
    
    # 创建宠物实例
    pet = Pet("测试宠物", "猫咪")
    
    # 创建强化学习系统
    rl_system = ReinforcementLearningSystem(pet)
    
    # 测试状态获取性能
    print("1. 测试状态获取性能:")
    start_time = time.time()
    for _ in range(1000):
        state = rl_system.get_discrete_state()
    end_time = time.time()
    print(f"   1000次状态获取耗时: {end_time - start_time:.4f}秒")
    
    # 测试动作选择性能
    print("\n2. 测试动作选择性能:")
    start_time = time.time()
    for _ in range(1000):
        state = rl_system.get_discrete_state()
        action = rl_system.choose_action(state)
    end_time = time.time()
    print(f"   1000次动作选择耗时: {end_time - start_time:.4f}秒")
    
    # 测试学习性能
    print("\n3. 测试学习性能:")
    # 生成一些经验
    start_time = time.time()
    for _ in range(100):
        state = rl_system.get_discrete_state()
        action = rl_system.choose_action(state)
        # 模拟奖励
        reward = 1.0
        next_state = rl_system.get_discrete_state()
        done = False
        rl_system.learn(state, action, reward, next_state, done)
    end_time = time.time()
    print(f"   100次学习耗时: {end_time - start_time:.4f}秒")
    
    # 测试学习统计
    print("\n4. 测试学习统计:")
    stats = rl_system.get_learning_stats()
    print(f"   学习步数: {stats['learning_steps']}")
    print(f"   平均奖励: {stats['average_reward']:.4f}")
    print(f"   探索率: {stats['exploration_rate']:.4f}")
    print(f"   回放缓冲区大小: {stats['replay_buffer_size']}")
    print(f"   Q表大小: {stats['q_table_size']}")
    
    print("强化学习算法性能测试完成！")
    print("=" * 60)

def test_platform_compatibility():
    """测试跨平台兼容性"""
    print("\n" + "=" * 60)
    print("测试跨平台兼容性")
    print("=" * 60)
    
    from utils.platform import PlatformUtils
    
    print("1. 测试平台检测:")
    print(f"   当前平台: {PlatformUtils.get_platform()}")
    print(f"   是Windows: {PlatformUtils.is_windows()}")
    print(f"   是Linux: {PlatformUtils.is_linux()}")
    print(f"   是macOS: {PlatformUtils.is_macos()}")
    
    print("\n2. 测试清屏功能:")
    print("   清屏前...")
    time.sleep(1)
    PlatformUtils.clear_screen()
    print("   清屏后...")
    
    print("\n3. 测试路径操作:")
    test_path = PlatformUtils.join_path("test", "path")
    print(f"   拼接路径: {test_path}")
    
    print("跨平台兼容性测试完成！")
    print("=" * 60)

def main():
    """主测试函数"""
    print("开始测试所有优化和新功能...")
    print("=" * 60)
    
    # 测试任务系统
    test_task_system()
    
    # 测试成就系统
    test_achievement_system()
    
    # 测试强化学习算法性能
    test_reinforcement_learning()
    
    # 测试跨平台兼容性
    test_platform_compatibility()
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
