#!/usr/bin/env python3
"""
测试宠物自然睡眠恢复精力时是否会自动醒来
"""
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pet.base import Pet

def test_natural_sleep_wakeup():
    """测试自然睡眠恢复精力时是否会自动醒来"""
    print("=" * 60)
    print("测试宠物自然睡眠恢复精力时是否会自动醒来")
    print("=" * 60)
    
    # 创建宠物实例
    pet = Pet("测试宠物", "猫咪")
    
    # 让宠物睡觉
    print("\n1. 让宠物睡觉：")
    sleep_result = pet.sleep()
    print(f"   {sleep_result}")
    print(f"   睡眠状态：{pet.is_sleeping}")
    
    # 设置宠物精力值为50%（需要恢复50点精力）
    print("\n2. 设置宠物精力值为50%：")
    pet.energy = 50
    print(f"   精力值：{pet.energy:.1f}%")
    print(f"   睡眠状态：{pet.is_sleeping}")
    
    # 模拟时间流逝（4小时，每小时恢复15点精力，总共恢复60点，达到110%即100%）
    print("\n3. 模拟4小时时间流逝：")
    print(f"   模拟前：精力值 = {pet.energy:.1f}%, 睡眠状态 = {pet.is_sleeping}")
    
    # 手动调用_update_needs方法，模拟时间流逝
    pet._update_needs(4)  # 4小时
    
    print(f"   模拟后：精力值 = {pet.energy:.1f}%, 睡眠状态 = {pet.is_sleeping}")
    
    # 再次模拟时间流逝（确保精力值达到100%）
    print("\n4. 再次模拟2小时时间流逝：")
    pet._update_needs(2)  # 2小时
    print(f"   模拟后：精力值 = {pet.energy:.1f}%, 睡眠状态 = {pet.is_sleeping}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

def test_update_method():
    """测试update方法是否会正确唤醒宠物"""
    print("\n" + "=" * 60)
    print("测试update方法是否会正确唤醒宠物")
    print("=" * 60)
    
    # 创建宠物实例
    pet = Pet("测试宠物", "猫咪")
    
    # 让宠物睡觉
    print("\n1. 让宠物睡觉：")
    sleep_result = pet.sleep()
    print(f"   {sleep_result}")
    print(f"   睡眠状态：{pet.is_sleeping}")
    
    # 设置宠物精力值为60%，并设置last_update_time为1小时前
    print("\n2. 设置宠物状态：")
    pet.energy = 60
    pet.last_update_time = time.time() - 3600  # 1小时前
    pet.needs_update = True
    print(f"   精力值：{pet.energy:.1f}%")
    print(f"   睡眠状态：{pet.is_sleeping}")
    print(f"   需要更新：{pet.needs_update}")
    
    # 调用update方法
    print("\n3. 调用update方法：")
    print(f"   调用前：精力值 = {pet.energy:.1f}%, 睡眠状态 = {pet.is_sleeping}")
    pet.update()
    print(f"   调用后：精力值 = {pet.energy:.1f}%, 睡眠状态 = {pet.is_sleeping}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

def main():
    """主测试函数"""
    test_natural_sleep_wakeup()
    test_update_method()

if __name__ == "__main__":
    main()
