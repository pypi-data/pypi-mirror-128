# coding=<encoding name> ： # coding=utf-8
from fzq_scnu.constants import elements as E
# 所有关卡，及其参数
class Level_1:
    def __init__(self):
        self.interface = E['interfaces'][1] # 界面
        self.level = E['levels'][1] # 关卡背景
        self.racetrack = E['racetracks'][0] # 赛道
        self.actor = E['actors'][1] # 角色
        self.others = [] # 特殊物品

class Level_2:
    def __init__(self):
        self.interface = E['interfaces'][1] # 界面
        self.level = E['levels'][0] # 关卡背景
        self.racetrack = E['racetracks'][0] # 赛道
        self.actor = E['actors'][1] # 角色
        # self.others = [E['others'][1], E['others'][2]] # 特殊物品
        self.others = []

class Level_3:
    def __init__(self):
        self.interface = E['interfaces'][1]  # 界面
        self.level = E['levels'][0]  # 关卡背景
        self.racetrack = E['racetracks'][2]  # 赛道
        self.actor = E['actors'][1]  # 角色
        self.others = []

class Level_4:
    def __init__(self):
        self.interface = E['interfaces'][2]  # 界面
        self.level = E['levels'][0]  # 关卡背景
        self.racetrack = E['racetracks'][1]  # 赛道
        self.actor = E['actors'][1]  # 角色
        self.others = []