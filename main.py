#!/usr/bin/env python3
import time
import sys
import os
from pet import Pet as VirtualPet, IntelligentPet
from ui import UI
from inventory import Inventory
from minigames import MiniGames
from environment import EnvironmentSystem, EnvironmentElementType
from social import SocialSystem, SocialInteractionType

class VirtualPetSimulator:
    def __init__(self):
        self.ui = UI() # 1. 用户界面控制器
        self.inventory = None # 2. 物品栏系统（暂未初始化）
        self.minigames = MiniGames()
        self.running = True
        self.pet = None
        self.environment_system = None
        self.social_system = None
        self.npc_manager = None
    
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
        while True:
            # 检查是否有已保存的宠物
            saved_pets_dir = "data/pets"
            if not os.path.exists(saved_pets_dir):
                os.makedirs(saved_pets_dir)
            
            saved_pets = [f for f in os.listdir(saved_pets_dir) if f.endswith('.json') and f != 'pets.json' and not f.endswith('_rl.json')]
            
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
                        
                        # 检查是否存在强化学习数据文件，判断是否为智能宠物
                        rl_file = pet_file.replace('.json', '_rl.json')
                        is_intelligent = os.path.exists(rl_file)
                        
                        # 根据是否为智能宠物选择加载类
                        if is_intelligent:
                            loaded_pet = IntelligentPet.load_from_file(pet_file)
                            if isinstance(loaded_pet, str):
                                print(f"加载失败：{loaded_pet}")
                                print("请重新选择或创建新宠物。")
                                # 重新开始选择流程
                                continue
                            self.pet = loaded_pet
                            print(f"✨ 智能宠物 {loaded_pet.name} 已加载！")
                        else:
                            loaded_pet = VirtualPet.load_from_file(pet_file)
                            if isinstance(loaded_pet, str):
                                print(f"加载失败：{loaded_pet}")
                                print("请重新选择或创建新宠物。")
                                # 重新开始选择流程
                                continue
                            
                            # 询问是否升级为智能宠物
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
                                if hasattr(loaded_pet, 'favorite_activities'):
                                    self.pet.favorite_activities = loaded_pet.favorite_activities
                                if hasattr(loaded_pet, 'dislikes'):
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
                                if hasattr(loaded_pet, 'accessories'):
                                    self.pet.accessories = loaded_pet.accessories
                                self.pet.is_sick = loaded_pet.is_sick
                                self.pet.sickness_type = loaded_pet.sickness_type
                                self.pet.last_update_time = loaded_pet.last_update_time
                                self.pet.needs_update = loaded_pet.needs_update
                                self.pet.state = loaded_pet.state
                                self.pet.mood = loaded_pet.mood
                                if hasattr(loaded_pet, 'birthday'):
                                    self.pet.birthday = loaded_pet.birthday
                                print(f"✨ 宠物 {loaded_pet.name} 已成功升级为智能宠物！")
                            else:
                                self.pet = loaded_pet
                        
                        # 初始化物品栏并传入宠物实例
                        self.inventory = Inventory(pet=self.pet)
                        # 初始化环境系统
                        self.environment_system = EnvironmentSystem(pet=self.pet)
                        # 初始化社交系统
                        self.social_system = SocialSystem(pet=self.pet)
                        # 初始化NPC管理器
                        from social import NPCManager
                        self.npc_manager = NPCManager()
                        return
                    elif choice_idx == len(saved_pets):
                        # 创建新宠物
                        break
                except ValueError:
                    print("无效的输入，请重新选择！")
                    continue
            else:
                # 没有保存的宠物，直接创建新宠物
                break
        
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
        # 初始化环境系统
        self.environment_system = EnvironmentSystem(pet=self.pet)
        # 初始化社交系统
        self.social_system = SocialSystem(pet=self.pet)
        # 初始化NPC管理器
        from social import NPCManager
        self.npc_manager = NPCManager()
    
    def update(self):
        """更新游戏状态"""
        if self.pet:
            self.pet.update()
            # 更新环境系统
            if self.environment_system:
                self.environment_system.update_environment(0.1)  # 假设每次更新间隔0.1秒
            # 更新社交系统
            if self.social_system:
                self.social_system.update_social_skills(0.1)
    
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
                # 显示清洁类型选择菜单
                print("\n请选择清洁类型：")
                print("1. 毛发清理")
                print("2. 刷牙")
                print("3. 洗澡")
                print("4. 修剪指甲")
                clean_choice = input("请选择（1-4）: ")
                
                # 映射选择到清洁类型
                clean_types = {
                    "1": "毛发清理",
                    "2": "刷牙",
                    "3": "洗澡",
                    "4": "修剪指甲"
                }
                
                clean_type = clean_types.get(clean_choice, "毛发清理")
                
                if isinstance(self.pet, IntelligentPet):
                    result = self.pet.interact_with_user("clean", clean_type=clean_type)
                else:
                    result = self.pet.clean(clean_type)
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
            # 抚摸宠物
            if self.pet:
                duration = input("请选择抚摸时间（1-5秒）: ")
                try:
                    duration = int(duration)
                    duration = max(1, min(5, duration))
                    if isinstance(self.pet, IntelligentPet):
                        result = self.pet.interact_with_user("pet", duration=duration)
                    else:
                        result = self.pet.pet(duration=duration)
                    print(result)
                except ValueError:
                    print("无效的输入！")
                input("按回车键继续...")
        elif choice == "11":
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
        elif choice == "12":
            # 环境互动
            if self.environment_system:
                print("\n环境元素列表：")
                elements = self.environment_system.get_all_elements()
                for i, element in enumerate(elements, 1):
                    print(f"{i}. {element.name} ({element.description})")
                
                element_choice = input("请选择要互动的环境元素编号： ")
                try:
                    element_idx = int(element_choice) - 1
                    if 0 <= element_idx < len(elements):
                        selected_element = elements[element_idx]
                        print(f"\n可选互动：")
                        
                        # 根据环境元素类型显示可用的互动类型
                        if selected_element.element_type == EnvironmentElementType.FOOD_BOWL:
                            print("1. 进食")
                            print("2. 检查")
                        elif selected_element.element_type == EnvironmentElementType.WATER_BOWL:
                            print("1. 喝水")
                            print("2. 检查")
                        elif selected_element.element_type == EnvironmentElementType.BED:
                            print("1. 睡觉")
                            print("2. 休息")
                        elif selected_element.element_type == EnvironmentElementType.TOY:
                            print("1. 玩耍")
                            print("2. 探索")
                        elif selected_element.element_type == EnvironmentElementType.SCRATCH_POST:
                            print("1. 抓挠")
                        elif selected_element.element_type == EnvironmentElementType.PLANT:
                            print("1. 探索")
                            print("2. 触摸")
                        elif selected_element.element_type == EnvironmentElementType.WINDOW:
                            print("1. 看窗外")
                            print("2. 晒太阳")
                        elif selected_element.element_type == EnvironmentElementType.DOOR:
                            print("1. 检查")
                            print("2. 抓挠")
                        elif selected_element.element_type == EnvironmentElementType.SOFA:
                            print("1. 休息")
                            print("2. 玩耍")
                        elif selected_element.element_type == EnvironmentElementType.TABLE:
                            print("1. 探索")
                            print("2. 跳上")
                        
                        interaction_choice = input("请选择互动类型编号： ")
                        interaction_map = {
                            (EnvironmentElementType.FOOD_BOWL, "1"): "eat",
                            (EnvironmentElementType.FOOD_BOWL, "2"): "check",
                            (EnvironmentElementType.WATER_BOWL, "1"): "drink",
                            (EnvironmentElementType.WATER_BOWL, "2"): "check",
                            (EnvironmentElementType.BED, "1"): "sleep",
                            (EnvironmentElementType.BED, "2"): "rest",
                            (EnvironmentElementType.TOY, "1"): "play",
                            (EnvironmentElementType.TOY, "2"): "explore",
                            (EnvironmentElementType.SCRATCH_POST, "1"): "scratch",
                            (EnvironmentElementType.PLANT, "1"): "explore",
                            (EnvironmentElementType.PLANT, "2"): "touch",
                            (EnvironmentElementType.WINDOW, "1"): "look_out",
                            (EnvironmentElementType.WINDOW, "2"): "sunbathe",
                            (EnvironmentElementType.DOOR, "1"): "check",
                            (EnvironmentElementType.DOOR, "2"): "scratch",
                            (EnvironmentElementType.SOFA, "1"): "rest",
                            (EnvironmentElementType.SOFA, "2"): "play",
                            (EnvironmentElementType.TABLE, "1"): "explore",
                            (EnvironmentElementType.TABLE, "2"): "jump"
                        }
                        
                        interaction_type = interaction_map.get((selected_element.element_type, interaction_choice))
                        if interaction_type:
                            result = self.environment_system.interact_with_element(selected_element.element_id, interaction_type)
                            print(result["message"])
                        else:
                            print("无效的互动类型！")
                    else:
                        print("无效的选择！")
                except ValueError:
                    print("无效的输入！")
                input("按回车键继续...")
        elif choice == "13":
            # 社交系统
            if self.social_system:
                print("\n社交系统菜单：")
                print("1. 查看社交关系")
                print("2. 与NPC宠物互动")
                print("3. 与已保存宠物互动")
                print("4. 查看社交事件")
                social_choice = input("请选择操作： ")
                
                if social_choice == "1":
                    # 查看社交关系
                    relationships = self.social_system.get_all_relationships()
                    if relationships:
                        print("\n社交关系列表：")
                        for rel in relationships:
                            print(f"宠物：{rel['pet2_id']}，关系：{rel['status']}，纽带值：{rel['bond']}")
                    else:
                        print("还没有社交关系！")
                elif social_choice == "2":
                    # 与NPC宠物互动
                    if self.npc_manager:
                        npcs = self.npc_manager.get_all_npcs()
                        if npcs:
                            print("\n可用的NPC宠物：")
                            for i, npc in enumerate(npcs, 1):
                                print(f"{i}. {npc.name} ({npc.species})")
                            
                            npc_choice = input("请选择要互动的NPC编号： ")
                            try:
                                npc_idx = int(npc_choice) - 1
                                if 0 <= npc_idx < len(npcs):
                                    selected_npc = npcs[npc_idx]
                                    
                                    print("\n可选互动：")
                                    print("1. 问候")
                                    print("2. 玩耍")
                                    print("3. 分享")
                                    print("4. 竞争")
                                    print("5. 帮助")
                                    print("6. 忽略")
                                    print("7. 冲突")
                                    
                                    interaction_choice = input("请选择互动类型编号： ")
                                    interaction_map = {
                                        "1": SocialInteractionType.GREET,
                                        "2": SocialInteractionType.PLAY,
                                        "3": SocialInteractionType.SHARE,
                                        "4": SocialInteractionType.COMPETE,
                                        "5": SocialInteractionType.HELP,
                                        "6": SocialInteractionType.IGNORE,
                                        "7": SocialInteractionType.CONFLICT
                                    }
                                    
                                    interaction_type = interaction_map.get(interaction_choice)
                                    if interaction_type:
                                        result = self.social_system.interact_with_other(selected_npc, interaction_type)
                                        print(result["message"])
                                    else:
                                        print("无效的互动类型！")
                                else:
                                    print("无效的选择！")
                            except ValueError:
                                print("无效的输入！")
                        else:
                            print("没有可用的NPC宠物！")
                    else:
                        print("NPC管理器未初始化！")
                elif social_choice == "3":
                    # 与已保存宠物互动
                    # 检查是否有已保存的宠物
                    saved_pets_dir = "data/pets"
                    if os.path.exists(saved_pets_dir):
                        saved_pets = [f for f in os.listdir(saved_pets_dir) if f.endswith('.json') and f != 'pets.json' and not f.endswith('_rl.json')]
                        
                        # 过滤掉当前宠物
                        current_pet_name = self.pet.name if self.pet else ""
                        other_pets = [pet_file for pet_file in saved_pets if pet_file[:-5] != current_pet_name]
                        
                        if other_pets:
                            print("\n可用的已保存宠物：")
                            for i, pet_file in enumerate(other_pets, 1):
                                print(f"{i}. {pet_file[:-5]}")
                            
                            pet_choice = input("请选择要互动的宠物编号： ")
                            try:
                                pet_idx = int(pet_choice) - 1
                                if 0 <= pet_idx < len(other_pets):
                                    # 加载已保存的宠物
                                    pet_file = os.path.join(saved_pets_dir, other_pets[pet_idx])
                                    
                                    # 检查是否存在强化学习数据文件，判断是否为智能宠物
                                    rl_file = pet_file.replace('.json', '_rl.json')
                                    is_intelligent = os.path.exists(rl_file)
                                    
                                    # 根据是否为智能宠物选择加载类
                                    if is_intelligent:
                                        loaded_pet = IntelligentPet.load_from_file(pet_file)
                                        if not isinstance(loaded_pet, str):
                                            # 与加载的宠物互动
                                            print("\n可选互动：")
                                            print("1. 问候")
                                            print("2. 玩耍")
                                            print("3. 分享")
                                            print("4. 竞争")
                                            print("5. 帮助")
                                            print("6. 忽略")
                                            print("7. 冲突")
                                            
                                            interaction_choice = input("请选择互动类型编号： ")
                                            interaction_map = {
                                                "1": SocialInteractionType.GREET,
                                                "2": SocialInteractionType.PLAY,
                                                "3": SocialInteractionType.SHARE,
                                                "4": SocialInteractionType.COMPETE,
                                                "5": SocialInteractionType.HELP,
                                                "6": SocialInteractionType.IGNORE,
                                                "7": SocialInteractionType.CONFLICT
                                            }
                                            
                                            interaction_type = interaction_map.get(interaction_choice)
                                            if interaction_type:
                                                result = self.social_system.interact_with_other(loaded_pet, interaction_type)
                                                print(result["message"])
                                            else:
                                                print("无效的互动类型！")
                                        else:
                                            print(f"加载失败：{loaded_pet}")
                                    else:
                                        loaded_pet = VirtualPet.load_from_file(pet_file)
                                        if not isinstance(loaded_pet, str):
                                            # 与加载的宠物互动
                                            print("\n可选互动：")
                                            print("1. 问候")
                                            print("2. 玩耍")
                                            print("3. 分享")
                                            print("4. 竞争")
                                            print("5. 帮助")
                                            print("6. 忽略")
                                            print("7. 冲突")
                                            
                                            interaction_choice = input("请选择互动类型编号： ")
                                            interaction_map = {
                                                "1": SocialInteractionType.GREET,
                                                "2": SocialInteractionType.PLAY,
                                                "3": SocialInteractionType.SHARE,
                                                "4": SocialInteractionType.COMPETE,
                                                "5": SocialInteractionType.HELP,
                                                "6": SocialInteractionType.IGNORE,
                                                "7": SocialInteractionType.CONFLICT
                                            }
                                            
                                            interaction_type = interaction_map.get(interaction_choice)
                                            if interaction_type:
                                                result = self.social_system.interact_with_other(loaded_pet, interaction_type)
                                                print(result["message"])
                                            else:
                                                print("无效的互动类型！")
                                        else:
                                            print(f"加载失败：{loaded_pet}")
                                else:
                                    print("无效的选择！")
                            except ValueError:
                                print("无效的输入！")
                        else:
                            print("没有其他已保存的宠物！")
                    else:
                        print("没有已保存的宠物！")
                elif social_choice == "4":
                    # 查看社交事件
                    events = self.social_system.get_recent_events()
                    if events:
                        print("\n最近的社交事件：")
                        for event in events:
                            print(f"{event.description} - {'已解决' if event.resolved else '未解决'}")
                    else:
                        print("还没有社交事件！")
                else:
                    print("无效的选择！")
                input("按回车键继续...")
        elif choice == "14":
            # 退出游戏
            self.running = False
            self.ui.display_goodbye()
        else:
            print("无效选择，请重新输入！")
            input("按回车键继续...")

if __name__ == "__main__":
    game = VirtualPetSimulator()
    game.start()
