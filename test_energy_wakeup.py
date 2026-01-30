#!/usr/bin/env python3
"""
测试宠物精力值达到100%时是否会自动醒来
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pet.base import Pet

class Inventory:
    """简化的物品栏类，用于测试"""
    def __init__(self, pet):
        self.pet = pet
        self.items = [{"name": "枕头"}]
    
    def use_pillow(self):
        """使用枕头"""
        print(f"使用枕头前：精力值 = {self.pet.energy:.1f}%, 睡眠状态 = {self.pet.is_sleeping}")
        
        # 增加精力值
        old_energy = self.pet.energy
        self.pet.energy = min(100, self.pet.energy + 40)
        print(f"使用枕头后：精力值 = {self.pet.energy:.1f}%, 睡眠状态 = {self.pet.is_sleeping}")
        
        # 检查是否需要唤醒
        if self.pet.is_sleeping and self.pet.energy >= 100:
            result = self.pet.wake_up()
            print(f"唤醒结果：{result}")
            print(f"唤醒后：睡眠状态 = {self.pet.is_sleeping}")

def test_energy_wakeup():
    """测试精力值达到100%时是否会自动醒来"""
    print("=" * 60)
    print("测试宠物精力值达到100%时是否会自动醒来")
    print("=" * 60)
    
    # 创建宠物实例
    pet = Pet("测试宠物", "猫咪")
    
    # 让宠物睡觉
    print("\n1. 让宠物睡觉：")
    sleep_result = pet.sleep()
    print(f"   {sleep_result}")
    print(f"   睡眠状态：{pet.is_sleeping}")
    
    # 设置宠物精力值为70%（使用一个枕头后会达到110%，即100%）
    print("\n2. 设置宠物精力值为70%：")
    pet.energy = 70
    print(f"   精力值：{pet.energy:.1f}%")
    print(f"   睡眠状态：{pet.is_sleeping}")
    
    # 使用枕头
    print("\n3. 使用枕头：")
    inventory = Inventory(pet)
    inventory.use_pillow()
    
    # 再次使用枕头（确保精力值达到100%）
    print("\n4. 再次使用枕头：")
    inventory.use_pillow()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_energy_wakeup()
