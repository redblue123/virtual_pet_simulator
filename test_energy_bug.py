#!/usr/bin/env python3
"""
测试宠物精力值达到100%但仍然在睡觉的问题
"""
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pet.base import Pet

def test_energy_100_still_sleeping():
    """测试宠物精力值达到100%但仍然在睡觉的问题"""
    print("=" * 60)
    print("测试宠物精力值达到100%但仍然在睡觉的问题")
    print("=" * 60)
    
    # 测试场景1：直接设置精力值为100%
    print("\n测试场景1：直接设置精力值为100%")
    pet1 = Pet("测试宠物1", "猫咪")
    pet1.sleep()
    print(f"   宠物入睡：{pet1.is_sleeping}")
    
    # 直接设置精力值为100%
    pet1.energy = 100
    print(f"   设置精力值为100%后：")
    print(f"   精力值：{pet1.energy:.1f}%")
    print(f"   睡眠状态：{pet1.is_sleeping}")
    
    # 调用update方法
    print(f"   调用update方法后：")
    pet1.last_update_time = time.time() - 3600  # 1小时前
    pet1.needs_update = True
    pet1.update()
    print(f"   精力值：{pet1.energy:.1f}%")
    print(f"   睡眠状态：{pet1.is_sleeping}")
    
    # 测试场景2：使用枕头后精力值达到100%
    print("\n测试场景2：使用枕头后精力值达到100%")
    pet2 = Pet("测试宠物2", "猫咪")
    pet2.sleep()
    print(f"   宠物入睡：{pet2.is_sleeping}")
    
    # 设置精力值为70%，使用枕头后达到110%即100%
    pet2.energy = 70
    print(f"   初始精力值：{pet2.energy:.1f}%")
    
    # 模拟使用枕头
    pet2.energy = min(100, pet2.energy + 40)
    print(f"   使用枕头后精力值：{pet2.energy:.1f}%")
    print(f"   睡眠状态：{pet2.is_sleeping}")
    
    # 手动检查是否需要唤醒
    if pet2.is_sleeping and pet2.energy >= 100:
        result = pet2.wake_up()
        print(f"   手动唤醒结果：{result}")
        print(f"   唤醒后睡眠状态：{pet2.is_sleeping}")
    
    # 测试场景3：自然睡眠恢复精力到100%
    print("\n测试场景3：自然睡眠恢复精力到100%")
    pet3 = Pet("测试宠物3", "猫咪")
    pet3.sleep()
    print(f"   宠物入睡：{pet3.is_sleeping}")
    
    # 设置精力值为85%，1小时睡眠后达到100%
    pet3.energy = 85
    print(f"   初始精力值：{pet3.energy:.1f}%")
    
    # 模拟1小时睡眠
    pet3._update_needs(1)
    print(f"   1小时睡眠后精力值：{pet3.energy:.1f}%")
    print(f"   睡眠状态：{pet3.is_sleeping}")
    
    # 测试场景4：多次使用枕头
    print("\n测试场景4：多次使用枕头")
    pet4 = Pet("测试宠物4", "猫咪")
    pet4.sleep()
    print(f"   宠物入睡：{pet4.is_sleeping}")
    
    # 设置精力值为50%
    pet4.energy = 50
    print(f"   初始精力值：{pet4.energy:.1f}%")
    
    # 第一次使用枕头
    pet4.energy = min(100, pet4.energy + 40)
    print(f"   第一次使用枕头后：精力值={pet4.energy:.1f}%, 睡眠={pet4.is_sleeping}")
    
    # 第二次使用枕头
    pet4.energy = min(100, pet4.energy + 40)
    print(f"   第二次使用枕头后：精力值={pet4.energy:.1f}%, 睡眠={pet4.is_sleeping}")
    
    # 手动唤醒
    if pet4.is_sleeping and pet4.energy >= 100:
        result = pet4.wake_up()
        print(f"   手动唤醒结果：{result}")
        print(f"   唤醒后：睡眠={pet4.is_sleeping}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

def test_wake_up_logic():
    """测试唤醒逻辑"""
    print("\n" + "=" * 60)
    print("测试唤醒逻辑")
    print("=" * 60)
    
    pet = Pet("测试宠物", "猫咪")
    
    # 测试1：宠物醒着时
    print("\n测试1：宠物醒着时")
    result = pet.wake_up()
    print(f"   结果：{result}")
    print(f"   睡眠状态：{pet.is_sleeping}")
    
    # 测试2：宠物睡着时
    print("\n测试2：宠物睡着时")
    pet.sleep()
    print(f"   入睡后：{pet.is_sleeping}")
    
    result = pet.wake_up()
    print(f"   唤醒结果：{result}")
    print(f"   唤醒后：{pet.is_sleeping}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

def main():
    """主测试函数"""
    test_energy_100_still_sleeping()
    test_wake_up_logic()

if __name__ == "__main__":
    main()
