#!/usr/bin/env python3
import time
import sys
import os
from pet import VirtualPet, IntelligentPet
from ui import UI
from inventory import Inventory
from minigames import MiniGames

class VirtualPetSimulator:
    def __init__(self):
        self.ui = UI() # 1. 用户界面控制器
        self.inventory = None # 2. 物品栏系统（暂未初始化）
        self.minigames = MiniGames()
        self.running = True
        self.pet = None
    
    def start(self):
        """开始游戏"""
        self.ui.display_welcome() # 1. 显示欢迎界面
        self.initialize_pet()
        
        while self.running:
            self.update()
            self.render()
            self.handle_input()
            time.sleep(0.1)
    
    def initialize_pet(self):
        """初始化宠物"""
        # 检查是否有已保存的宠物
        saved_pets_dir = "data/pets"
        if not os.path.exists(saved_pets_dir):
            os.makedirs(saved_pets_dir)
        
        saved_pets = [f for f in os.listdir(saved_pets_dir) if f.endswith('.json') and f != 'pets.json']
        
        if saved_pets:
            print("发现已保存的宠物：")
            for i, pet_file in enumerate(saved_pets, 1):
                print(f"{i}. {pet_file[:-5]}")
            print(f"{len(saved_pets) + 1}. 创建新宠物")
            
            choice = input("请选择： ")
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(saved_pets):
                    # 加载已保存的宠物
                    pet_file = os.path.join(saved_pets_dir, saved_pets[choice_idx])
                    loaded_pet = VirtualPet.load_from_file(pet_file)
                    
                    # 询问是否升级为智能宠物
                    if isinstance(loaded_pet, VirtualPet) and not isinstance(loaded_pet, IntelligentPet):
                        upgrade_choice = input("是否将此宠物升级为智能宠物？(y/n): ")
                        if upgrade_choice.lower() == 'y':
                            # 创建新的智能宠物并复制属性
                            self.pet = IntelligentPet(name=loaded_pet.name, species=loaded_pet.species)
                            # 复制所有属性
                            self.pet.hunger = loaded_pet.hunger
                            self.pet.happiness = loaded_pet.happiness
                            self.pet.energy = loaded_pet.energy
                            self.pet.health = loaded_pet.health
                            self.pet.hygiene = loaded_pet.hygiene
                            self.pet.is_sleeping = loaded_pet.is_sleeping
                            self.pet.color = loaded_pet.color
                            self.pet.favorite_activities = loaded_pet.favorite_activities
                            self.pet.dislikes = loaded_pet.dislikes
                            self.pet.skills = loaded_pet.skills
                            self.pet.personality_traits = loaded_pet.personality_traits
                            self.pet.age_in_days = loaded_pet.age_in_days
                            self.pet.experience = loaded_pet.experience
                            self.pet.level = loaded_pet.level
                            self.pet.memories = loaded_pet.memories
                            self.pet.relationship_with_owner = loaded_pet.relationship_with_owner
                            self.pet.routine_preferences = loaded_pet.routine_preferences
                            self.pet.weight = loaded_pet.weight
                            self.pet.size = loaded_pet.size
                            self.pet.accessories = loaded_pet.accessories
                            self.pet.is_sick = loaded_pet.is_sick
                            self.pet.sickness_type = loaded_pet.sickness_type
                            self.pet.last_update_time = loaded_pet.last_update_time
                            self.pet.needs_update = loaded_pet.needs_update
                            self.pet.state = loaded_pet.state
                            self.pet.mood = loaded_pet.mood
                            self.pet.birthday = loaded_pet.birthday
                            print(f"✨ 宠物 {loaded_pet.name} 已成功升级为智能宠物！")
                        else:
                            self.pet = loaded_pet
                    else:
                        self.pet = loaded_pet
                    
                    # 初始化物品栏并传入宠物实例
                    self.inventory = Inventory(pet=self.pet)
                    return
            except ValueError:
                pass
        
        # 创建新宠物
        name = input("请输入宠物名称： ")
        species = input("请输入宠物种类： ")
        
        # 选择宠物类型
        pet_type = input("请选择宠物类型（1. 普通宠物 2. 智能宠物）: ")
        if pet_type == "2":
            self.pet = IntelligentPet(name=name, species=species)
        else:
            self.pet = VirtualPet(name=name, species=species)
        
        # 初始化物品栏并传入宠物实例
        self.inventory = Inventory(pet=self.pet)
    
    def update(self):
        """更新游戏状态"""
        if self.pet:
            self.pet.update()
    
    def render(self):
        """渲染游戏界面"""
        self.ui.clear_screen()
        if self.pet:
            self.ui.display_pet_status(self.pet)
        self.ui.display_menu()
    
    def handle_input(self):
        """处理用户输入"""
        choice = input("请选择操作: ")
        
        if choice == "1":
            # 喂食
            if self.pet:
                food_type = input("请选择食物类型（普通食物/美味大餐/健康食品/零食）: ")
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("feed", food_type=food_type)
                else:
                    result = self.pet.feed(food_type)
                print(result)
                input("按回车键继续...")
        elif choice == "2":
            # 玩耍
            if self.pet:
                game_type = input("请选择游戏类型（普通游戏/捡球游戏/智力游戏/社交游戏）: ")
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("play", game_type=game_type)
                else:
                    result = self.pet.play(game_type)
                print(result)
                input("按回车键继续...")
        elif choice == "3":
            # 睡觉
            if self.pet:
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("sleep")
                else:
                    result = self.pet.sleep()
                print(result)
                input("按回车键继续...")
        elif choice == "4":
            # 叫醒宠物
            if self.pet:
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("wake_up")
                else:
                    result = self.pet.wake_up()
                print(result)
                input("按回车键继续...")
        elif choice == "5":
            # 查看物品栏
            self.inventory.view_inventory()
        elif choice == "6":
            # 玩小游戏
            game_choice = input("请选择游戏（1. 猜数字 2. 石头剪刀布 3. 记忆力游戏）: ")
            if game_choice == "1":
                self.minigames.play_guess_number()
            elif game_choice == "2":
                self.minigames.play_rock_paper_scissors()
            elif game_choice == "3":
                self.minigames.play_memory_game()
            input("按回车键继续...")
        elif choice == "7":
            # 保存宠物
            if self.pet:
                save_path = f"data/pets/{self.pet.name}.json"
                self.pet.save_to_file(save_path)
                print(f"宠物 {self.pet.name} 已保存！")
                input("按回车键继续...")
        elif choice == "8":
            # 清洁宠物
            if self.pet:
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("clean")
                else:
                    result = self.pet.clean()
                print(result)
                input("按回车键继续...")
        elif choice == "9":
            # 训练宠物
            if self.pet:
                skill_type = input("请选择技能类型（intelligence/strength/speed/social）: ")
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("train", skill_type=skill_type)
                else:
                    result = self.pet.train(skill_type)
                print(result)
                input("按回车键继续...")
        elif choice == "10":
            # 更改宠物颜色
            if self.pet:
                available_colors = self.pet.get_available_colors()
                print(f"可用颜色：{', '.join(available_colors)}")
                new_color = input("请输入要更改的颜色： ")
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("change_color", new_color=new_color)
                else:
                    result = self.pet.change_color(new_color)
                print(result)
                input("按回车键继续...")
        elif choice == "11":
            # 退出游戏
            self.running = False
            self.ui.display_goodbye()
        else:
            print("无效选择，请重新输入！")
            input("按回车键继续...")

if __name__ == "__main__":
    game = VirtualPetSimulator()
    game.start()
