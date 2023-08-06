# coding=<encoding name> ： # coding=utf-8
# 参数
# --------------------------------------------------------------------------------------------------------
# 屏幕宽度，高度
WIDTH, HEIGHT = 1300, 700
# TITLE
TITLE = '华光仿真器'
# ICON
ICON = 'hg.png'
# --------------------------------------------------------------------------------------------------------
# 角色，背景，赛道、障碍、物品或其他图像的名称与坐标或RGB(传感器不存放在这)
elements = {'actors': {1: ['actors/car', (360, 370)]},
            'interfaces': {0: ['interfaces/interface_none', (0, 0)],
                            1: ['interfaces/interface1', (0, 0)],
                            2: ['interfaces/interface2', (0, 0)]},
            'levels': {0: ['levels/level_none', (200, 6)],
                            1: ['levels/level1', (200, 6)],
                            2: ['levels/level2', (200, 6)]},
            'racetracks': {0: ['racetracks/none', (0, 0)],
                           1: ['racetracks/racetrack1', (300, 80)],
                           2: ['racetracks/racetrack2', (320, 150)]},
            'others': {0: ['others/none', (0, 0)],
                          1: ['others/obstacle1', (500, 500)],
                          2: ['others/obstacle2', (600, 400)]}
            }
# --------------------------------------------------------------------------------------------------------
# 仿真界面所有固定及关联坐标点
hardwarepos_pic_right = {1:(1235, 70), 2:(1235, 200), 3:(1235, 330), 4:(1235, 460), 5:(1235, 590)}
hardwarepos_name_right = {key:(1225, hardwarepos_pic_right[key][1] + 56)
                         for key,a in hardwarepos_pic_right.items()}
io_pwm_pos_right = {key:[(hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] - 45),
                         (hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] - 20)]
                          for key,b in hardwarepos_pic_right.items()}
return_data_pos_right = {key:[(hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] + 24),
                              (hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] + 48)]
                         for key,c in hardwarepos_pic_right.items()}
return_data_pos_right_other = {key:[(hardwarepos_pic_right[key][0] - 5, hardwarepos_pic_right[key][1] - 24),
                                    (hardwarepos_pic_right[key][0] - 5, hardwarepos_pic_right[key][1] + 24)]
                               for key,e in hardwarepos_pic_right.items()}
# 以下待开发使用
hardwarepos_pic_left= {1:(71, 55), 2: (71, 225), 3: (71, 380)}
hardwarepos_name_left = {'csb':(71, 55+65), 'motor': (71, 225+70), 'wheel': (71, 380+78)}
return_data_pos_left = {key:[(hardwarepos_pic_left[key][0] + 96, hardwarepos_pic_left[key][1] - 20),
                              (hardwarepos_pic_left[key][0] + 96, hardwarepos_pic_left[key][1] + 20)]
                         for key,d in hardwarepos_pic_left.items()}
# 文本框位置
other_pos = {'文本框':(96, 485), '当前温度':[(60, 510), (140, 510)], '当前湿度':[(60, 533), (140, 533)]}
# --------------------------------------------------------------------------------------------------------



