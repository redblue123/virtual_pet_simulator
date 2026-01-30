#!/usr/bin/env python3
import random

class MiniGames:
    def __init__(self):
        pass
    
    def play_guess_number(self):
        """猜数字游戏"""
        print("=" * 40)
        print("猜数字游戏")
        print("=" * 40)
        print("我想了一个1-100之间的数字，你有5次机会猜出它！")
        
        target_number = random.randint(1, 100)
        attempts = 0
        max_attempts = 5
        
        while attempts < max_attempts:
            try:
                guess = int(input(f"请输入你的猜测（{attempts + 1}/{max_attempts}）: "))
                attempts += 1
                
                if guess < target_number:
                    print("太小了！")
                elif guess > target_number:
                    print("太大了！")
                else:
                    print(f"恭喜你猜对了！答案就是 {target_number}！")
                    print(f"你用了 {attempts} 次机会。")
                    return True
            except ValueError:
                print("请输入有效的数字！")
        
        print(f"很遗憾，你没有在规定次数内猜对。答案是 {target_number}。")
        return False
    
    def play_rock_paper_scissors(self):
        """石头剪刀布游戏"""
        print("=" * 40)
        print("石头剪刀布游戏")
        print("=" * 40)
        print("规则：1. 石头 2. 剪刀 3. 布")
        
        choices = ["石头", "剪刀", "布"]
        player_score = 0
        computer_score = 0
        rounds = 3
        
        for i in range(rounds):
            print(f"\n第 {i + 1} 轮")
            
            # 玩家选择
            try:
                player_choice = int(input("请选择（1-3）: ")) - 1
                if player_choice not in [0, 1, 2]:
                    print("无效选择，本轮算你输！")
                    computer_score += 1
                    continue
            except ValueError:
                print("无效输入，本轮算你输！")
                computer_score += 1
                continue
            
            # 电脑选择
            computer_choice = random.randint(0, 2)
            
            print(f"你出了：{choices[player_choice]}")
            print(f"电脑出了：{choices[computer_choice]}")
            
            # 判断胜负
            if player_choice == computer_choice:
                print("平局！")
            elif (player_choice == 0 and computer_choice == 1) or \
                 (player_choice == 1 and computer_choice == 2) or \
                 (player_choice == 2 and computer_choice == 0):
                print("你赢了！")
                player_score += 1
            else:
                print("你输了！")
                computer_score += 1
        
        print("\n" + "=" * 40)
        print("游戏结束")
        print(f"你的得分：{player_score}")
        print(f"电脑得分：{computer_score}")
        
        if player_score > computer_score:
            print("恭喜你获得最终胜利！")
            return True
        elif player_score < computer_score:
            print("很遗憾，电脑获得了最终胜利！")
            return False
        else:
            print("最终平局！")
            return None
    
    def play_memory_game(self):
        """记忆力游戏"""
        print("=" * 40)
        print("记忆力游戏")
        print("=" * 40)
        print("记住屏幕上显示的数字，然后输入它们！")
        
        difficulty = 3
        score = 0
        
        while True:
            # 生成随机数字序列
            numbers = [random.randint(0, 9) for _ in range(difficulty)]
            print(f"\n记住这个序列：{' '.join(map(str, numbers))}")
            
            # 短暂显示后清屏
            import time
            time.sleep(2)
            from utils.platform import PlatformUtils
            PlatformUtils.clear_screen()
            
            # 玩家输入
            player_input = input("请输入你记住的序列（用空格分隔）: ")
            try:
                player_numbers = list(map(int, player_input.split()))
                if player_numbers == numbers:
                    print("正确！你真棒！")
                    score += 1
                    difficulty += 1
                    print(f"难度提升到 {difficulty}！")
                else:
                    print(f"错误！正确序列是：{' '.join(map(str, numbers))}")
                    break
            except ValueError:
                print("无效输入，请用空格分隔数字！")
                break
        
        print(f"\n游戏结束，你的得分是：{score}")
        return score
