#!/usr/bin/env python3
import json
import os

class Inventory:
    def __init__(self, pet=None):
        self.items = []
        self.pet = pet
        self._load_items_data()
        self._initialize_inventory()
    
    def _load_items_data(self):
        """加载物品数据"""
        items_file = "data/items.json"
        if os.path.exists(items_file):
            try:
                with open(items_file, "r", encoding="utf-8") as f:
                    self.items_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.items_data = {}
        else:
            self.items_data = {}
    
    def _initialize_inventory(self):
        """初始化物品栏"""
        # 初始物品
        initial_items = [
            {"name": "食物", "description": "增加宠物的饥饿度"},
            {"name": "玩具", "description": "增加宠物的快乐度"},
            {"name": "枕头", "description": "增加宠物的精力值"}
        ]
        self.items.extend(initial_items)
    
    def view_inventory(self):
        """查看物品栏"""
        from ui import UI
        ui = UI()
        ui.clear_screen()
        
        print("物品栏")
        print("=" * 40)
        
        if not self.items:
            print("物品栏为空！")
        else:
            for i, item in enumerate(self.items, 1):
                print(f"{i}. {item['name']} - {item['description']}")
        
        print("=" * 40)
        print("0. 返回")
        
        choice = input("请选择要使用的物品（输入编号）: ")
        
        if choice == "0":
            return
        
        try:
            item_idx = int(choice) - 1
            if 0 <= item_idx < len(self.items):
                self.use_item(item_idx)
            else:
                print("无效选择！")
        except ValueError:
            print("无效输入！")
        
        input("按回车键继续...")
    
    def use_item(self, item_idx):
        """使用物品"""
        item = self.items[item_idx]
        print(f"你使用了 {item['name']}！")
        
        # 物品效果
        if self.pet:
            if item["name"] == "食物":
                self.pet.hunger = min(100, self.pet.hunger + 40)
                print("宠物的饥饿度增加了！")
            elif item["name"] == "玩具":
                self.pet.happiness = min(100, self.pet.happiness + 40)
                print("宠物的快乐度增加了！")
            elif item["name"] == "枕头":
                self.pet.energy = min(100, self.pet.energy + 40)
                print("宠物的精力值增加了！")
        else:
            print("没有宠物可以使用物品！")
        
        # 使用后移除物品
        self.items.pop(item_idx)
    
    def add_item(self, item_name, item_description):
        """添加物品"""
        new_item = {"name": item_name, "description": item_description}
        self.items.append(new_item)
        print(f"{item_name} 已添加到物品栏！")
    
    def remove_item(self, item_idx):
        """移除物品"""
        if 0 <= item_idx < len(self.items):
            removed_item = self.items.pop(item_idx)
            print(f"{removed_item['name']} 已从物品栏移除！")
        else:
            print("无效的物品索引！")
    
    def get_item_count(self):
        """获取物品数量"""
        return len(self.items)
