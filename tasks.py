#!/usr/bin/env python3
import random
import time
from datetime import datetime
from enum import Enum

class TaskType(Enum):
    """任务类型枚举"""
    FEED = "喂食"
    PLAY = "玩耍"
    CLEAN = "清洁"
    TRAIN = "训练"
    SLEEP = "睡眠"
    PET = "抚摸"
    SPECIAL = "特殊"

class TaskDifficulty(Enum):
    """任务难度枚举"""
    EASY = "简单"
    MEDIUM = "中等"
    HARD = "困难"

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "待完成"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    FAILED = "失败"

class Task:
    """任务类"""
    def __init__(self, task_id, task_type, description, difficulty, target, reward, time_limit=None):
        self.task_id = task_id
        self.task_type = task_type
        self.description = description
        self.difficulty = difficulty
        self.target = target  # 任务目标值
        self.reward = reward  # 任务奖励
        self.time_limit = time_limit  # 时间限制（秒）
        self.status = TaskStatus.PENDING
        self.progress = 0
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
    
    def start(self):
        """开始任务"""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.IN_PROGRESS
            self.started_at = time.time()
            return True
        return False
    
    def update_progress(self, progress):
        """更新任务进度"""
        if self.status == TaskStatus.IN_PROGRESS:
            self.progress = min(progress, self.target)
            if self.progress >= self.target:
                self.complete()
            elif self.time_limit and time.time() - self.created_at > self.time_limit:
                self.fail()
            return True
        return False
    
    def complete(self):
        """完成任务"""
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.COMPLETED
            self.progress = self.target
            self.completed_at = time.time()
            return True
        return False
    
    def fail(self):
        """失败任务"""
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.FAILED
            self.completed_at = time.time()
            return True
        return False
    
    def is_expired(self):
        """检查任务是否过期"""
        if self.time_limit:
            return time.time() - self.created_at > self.time_limit and self.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED]
        return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "description": self.description,
            "difficulty": self.difficulty.value,
            "target": self.target,
            "reward": self.reward,
            "time_limit": self.time_limit,
            "status": self.status.value,
            "progress": self.progress,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建任务"""
        task = cls(
            task_id=data["task_id"],
            task_type=TaskType(data["task_type"]),
            description=data["description"],
            difficulty=TaskDifficulty(data["difficulty"]),
            target=data["target"],
            reward=data["reward"],
            time_limit=data.get("time_limit")
        )
        task.status = TaskStatus(data["status"])
        task.progress = data["progress"]
        task.created_at = data["created_at"]
        task.started_at = data.get("started_at")
        task.completed_at = data.get("completed_at")
        return task

class TaskSystem:
    """任务系统"""
    def __init__(self, pet):
        self.pet = pet
        self.tasks = []
        self.completed_tasks = []
        self.max_active_tasks = 3
        self.daily_tasks_generated = False
        self.last_daily_reset = time.time()
        self.task_counter = 0
        
        # 任务模板
        self.task_templates = {
            TaskType.FEED: [
                {"description": "喂食你的宠物", "difficulty": TaskDifficulty.EASY, "target": 1, "reward": {"experience": 10, "points": 5}},
                {"description": "连续喂食你的宠物3次", "difficulty": TaskDifficulty.MEDIUM, "target": 3, "reward": {"experience": 25, "points": 15}},
            ],
            TaskType.PLAY: [
                {"description": "和你的宠物玩耍", "difficulty": TaskDifficulty.EASY, "target": 1, "reward": {"experience": 12, "points": 6}},
                {"description": "连续和你的宠物玩耍2次", "difficulty": TaskDifficulty.MEDIUM, "target": 2, "reward": {"experience": 30, "points": 18}},
            ],
            TaskType.CLEAN: [
                {"description": "清洁你的宠物", "difficulty": TaskDifficulty.EASY, "target": 1, "reward": {"experience": 8, "points": 4}},
                {"description": "连续清洁你的宠物2次", "difficulty": TaskDifficulty.MEDIUM, "target": 2, "reward": {"experience": 20, "points": 12}},
            ],
            TaskType.TRAIN: [
                {"description": "训练你的宠物", "difficulty": TaskDifficulty.MEDIUM, "target": 1, "reward": {"experience": 15, "points": 8}},
                {"description": "连续训练你的宠物3次", "difficulty": TaskDifficulty.HARD, "target": 3, "reward": {"experience": 40, "points": 25}},
            ],
            TaskType.SLEEP: [
                {"description": "让你的宠物睡觉", "difficulty": TaskDifficulty.EASY, "target": 1, "reward": {"experience": 10, "points": 5}},
                {"description": "让你的宠物睡满8小时", "difficulty": TaskDifficulty.HARD, "target": 8, "reward": {"experience": 50, "points": 30}},
            ],
            TaskType.PET: [
                {"description": "抚摸你的宠物", "difficulty": TaskDifficulty.EASY, "target": 1, "reward": {"experience": 8, "points": 4}},
                {"description": "连续抚摸你的宠物5次", "difficulty": TaskDifficulty.MEDIUM, "target": 5, "reward": {"experience": 35, "points": 20}},
            ],
            TaskType.SPECIAL: [
                {"description": "让你的宠物保持快乐状态1小时", "difficulty": TaskDifficulty.HARD, "target": 60, "reward": {"experience": 60, "points": 40}},
                {"description": "让你的宠物达到100%清洁度", "difficulty": TaskDifficulty.MEDIUM, "target": 100, "reward": {"experience": 30, "points": 18}},
            ]
        }
    
    def generate_daily_tasks(self):
        """生成每日任务"""
        # 检查是否已经生成过今日任务
        today = datetime.now().date()
        last_reset_date = datetime.fromtimestamp(self.last_daily_reset).date()
        
        if today != last_reset_date or not self.daily_tasks_generated:
            # 清理过期任务
            self._cleanup_expired_tasks()
            
            # 生成新的每日任务
            new_tasks = []
            task_types = list(TaskType)
            
            # 确保每种类型至少有一个任务
            for task_type in [TaskType.FEED, TaskType.PLAY, TaskType.CLEAN]:
                template = random.choice(self.task_templates[task_type])
                task = Task(
                    task_id=self._generate_task_id(),
                    task_type=task_type,
                    description=template["description"],
                    difficulty=template["difficulty"],
                    target=template["target"],
                    reward=template["reward"],
                    time_limit=3600 * 24  # 24小时时间限制
                )
                new_tasks.append(task)
            
            # 添加一个随机任务
            random_task_type = random.choice(task_types)
            template = random.choice(self.task_templates[random_task_type])
            random_task = Task(
                task_id=self._generate_task_id(),
                task_type=random_task_type,
                description=template["description"],
                difficulty=template["difficulty"],
                target=template["target"],
                reward=template["reward"],
                time_limit=3600 * 24
            )
            new_tasks.append(random_task)
            
            # 添加到任务列表
            self.tasks.extend(new_tasks)
            self.daily_tasks_generated = True
            self.last_daily_reset = time.time()
            
            return new_tasks
        return []
    
    def generate_special_task(self):
        """生成特殊任务"""
        if len(self.tasks) < self.max_active_tasks:
            template = random.choice(self.task_templates[TaskType.SPECIAL])
            task = Task(
                task_id=self._generate_task_id(),
                task_type=TaskType.SPECIAL,
                description=template["description"],
                difficulty=template["difficulty"],
                target=template["target"],
                reward=template["reward"],
                time_limit=3600 * 12  # 12小时时间限制
            )
            self.tasks.append(task)
            return task
        return None
    
    def update_task_progress(self, task_type, progress_increment=1):
        """更新任务进度"""
        completed_tasks = []
        rewards = []
        
        for task in self.tasks:
            if task.task_type == task_type and task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]:
                # 开始任务（如果尚未开始）
                if task.status == TaskStatus.PENDING:
                    task.start()
                
                # 更新进度
                old_progress = task.progress
                task.update_progress(old_progress + progress_increment)
                
                # 检查任务是否完成
                if task.status == TaskStatus.COMPLETED:
                    completed_tasks.append(task)
                    rewards.append(task.reward)
        
        # 处理完成的任务
        for task in completed_tasks:
            self.tasks.remove(task)
            self.completed_tasks.append(task)
        
        return rewards
    
    def get_active_tasks(self):
        """获取活跃任务"""
        # 清理过期任务
        self._cleanup_expired_tasks()
        
        # 确保有足够的活跃任务
        if len(self.tasks) < 2:
            self.generate_daily_tasks()
        
        return self.tasks
    
    def get_completed_tasks(self, limit=10):
        """获取已完成的任务"""
        return self.completed_tasks[-limit:]
    
    def _cleanup_expired_tasks(self):
        """清理过期任务"""
        expired_tasks = []
        for task in self.tasks:
            if task.is_expired():
                task.fail()
                expired_tasks.append(task)
        
        for task in expired_tasks:
            self.tasks.remove(task)
            self.completed_tasks.append(task)
    
    def _generate_task_id(self):
        """生成任务ID"""
        self.task_counter += 1
        return f"task_{int(time.time())}_{self.task_counter}"
    
    def to_dict(self):
        """转换为字典"""
        return {
            "tasks": [task.to_dict() for task in self.tasks],
            "completed_tasks": [task.to_dict() for task in self.completed_tasks[-50:]],  # 只保存最近50个完成的任务
            "daily_tasks_generated": self.daily_tasks_generated,
            "last_daily_reset": self.last_daily_reset,
            "task_counter": self.task_counter
        }
    
    def from_dict(self, data):
        """从字典加载"""
        self.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        self.completed_tasks = [Task.from_dict(task_data) for task_data in data.get("completed_tasks", [])]
        self.daily_tasks_generated = data.get("daily_tasks_generated", False)
        self.last_daily_reset = data.get("last_daily_reset", time.time())
        self.task_counter = data.get("task_counter", 0)
