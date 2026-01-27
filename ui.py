#!/usr/bin/env python3
import os

class UI:
    def __init__(self):
        self.ascii_art = {
            "welcome": """        
  /\_/\  
 ( o.o ) 
  > ^ <  
欢迎来到虚拟宠物模拟器！
            """,
            "pet": """        
  /\_/\  
 ( o.o ) 
  > ^ <  
            """,
            "goodbye": """        
  /\_/\  
 ( -.- ) 
  > ^ <  
再见，期待再次见到你！
            """
        }
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        """显示欢迎界面"""
        self.clear_screen()
        print(self.ascii_art["welcome"])
        print("=" * 40)
        print("虚拟宠物模拟器")
        print("=" * 40)
        input("按回车键开始...")
    
    def display_pet_status(self, pet):
        """显示宠物状态"""
        print(self.ascii_art["pet"])
        print(f"宠物名称: {pet.name}")
        print(f"宠物种类: {pet.species}")
        print(f"年龄: {pet.age_in_days} 天")
        print(f"状态: {pet.state.value}")
        print(f"心情: {pet.mood.value}")
        print(f"等级: {pet.level}")
        print(f"外观: {pet.color} {pet.size}")
        print("-" * 40)
        print(f"健康值: {self._get_status_bar(pet.health)}")
        print(f"饥饿度: {self._get_status_bar(pet.hunger)}")
        print(f"精力值: {self._get_status_bar(pet.energy)}")
        print(f"清洁度: {self._get_status_bar(pet.hygiene)}")
        print(f"快乐度: {self._get_status_bar(pet.happiness)}")
        print("-" * 40)
        
        # 显示技能
        print("技能:")
        for skill, level in pet.skills.items():
            skill_name = {
                "intelligence": "智力",
                "strength": "力量",
                "speed": "速度",
                "social": "社交"
            }.get(skill, skill)
            print(f"  {skill_name}: {level}")
        
        # 显示性格
        print("性格:")
        for trait, strength in pet.personality_traits.items():
            print(f"  {trait.value}: {strength:.1f}")
        
        # 显示特殊状态
        if pet.is_sleeping:
            print("特殊状态: 正在睡觉")
        if pet.is_sick:
            print(f"特殊状态: 生病 ({pet.sickness_type})")
        print("-" * 40)
    
    def display_menu(self):
        """显示菜单"""
        print("菜单选项:")
        print("1. 喂食")
        print("2. 玩耍")
        print("3. 睡觉")
        print("4. 叫醒宠物")
        print("5. 查看物品栏")
        print("6. 玩小游戏")
        print("7. 保存宠物")
        print("8. 清洁宠物")
        print("9. 训练宠物")
        print("10. 更改宠物颜色")
        print("11. 退出游戏")
        print("-" * 40)
    
    def display_goodbye(self):
        """显示再见界面"""
        self.clear_screen()
        print(self.ascii_art["goodbye"])
        print("=" * 40)
        print("感谢游玩虚拟宠物模拟器！")
        print("=" * 40)
    
    def _get_status_bar(self, value):
        """获取状态条"""
        bar_length = 20
        filled_length = int(bar_length * value / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"[{bar}] {int(value)}%"
    
    def display_inventory(self, inventory):
        """显示物品栏"""
        self.clear_screen()
        print("物品栏")
        print("=" * 40)
        
        if not inventory.items:
            print("物品栏为空！")
        else:
            for i, item in enumerate(inventory.items, 1):
                print(f"{i}. {item['name']} - {item['description']}")
        
        print("=" * 40)
        print("0. 返回")
    
    def display_minigame_result(self, result, score=None):
        """显示小游戏结果"""
        print("=" * 40)
        print(result)
        if score is not None:
            print(f"得分: {score}")
        print("=" * 40)
        input("按回车键继续...")
