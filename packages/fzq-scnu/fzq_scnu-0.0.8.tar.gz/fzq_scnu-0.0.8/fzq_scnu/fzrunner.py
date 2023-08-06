# coding=<encoding name> ： # coding=utf-8
# 项目名称：华光人工智能教育硬件仿真器
# 前项目组成员：lmq,hjh,wpz,czj,sjw
# --------------------------------------------------------------------------------------------------------
# 文件名：仿真器运行文件
# 作者：lmq(1代),hjh(2代)
# 版本：2代
# --------------------------------------------------------------------------------------------------------
import os, threading, sys, logging, traceback, math
import pygame
from pgzero import loaders
from pgzero.screen import Screen
from pgzero.actor import Actor
from pgzero.rect import Rect
from fzq_scnu import fzgpio, fzshijue1, tools, constants, levels, input
# --------------------------------------------------------------------------------------------------------
# 控制运行的标志，空字符为不运行，非空字符为运行
run = ''
# --------------------------------------------------------------------------------------------------------
# 换页，code线程结束控制
pagechange = {'left': 1, 'right': 1}
code_threading_is_over = {'over': 0}
# --------------------------------------------------------------------------------------------------------
# 主控
class Update(fzgpio.Mecanum_wheel):
    def __init__(self):
        super(Update, self).__init__()
        self.py_image = 'None'
        self.actor = Actor(LEVEL.actor[0])
        self.actor.pos = (LEVEL.actor[1])

    # 定义绘制文本的方法
    def draw_t(self, text, pos, color='black', fontname='fangsong.ttf', fontsize=17):
        screen.draw.text(text, center=pos, color=color, fontname=fontname, fontsize=fontsize)

    # 背景清空
    def draw_clear(self):
        screen.clear()
        screen.fill((244, 244, 244))

    # 背景绘制
    def draw_background(self):
        screen.blit(LEVEL.interface[0], LEVEL.interface[1])
        screen.blit(LEVEL.level[0], LEVEL.level[1])
        screen.blit(LEVEL.racetrack[0], LEVEL.racetrack[1])
        if len(LEVEL.others) >= 2:
            for other in range(len(LEVEL.others)):
                screen.blit(LEVEL.others[other][0], LEVEL.others[other][1])
        elif len(LEVEL.others) == 1:
            screen.blit(LEVEL.others[0][0], LEVEL.others[0][1])
        else:
            pass
        # 温湿度手动设置
        if fzgpio.transmit_right != None:
            for key, value in list(fzgpio.transmit_right.items()):
                result = fzgpio.tmp_hum.tmp_hum_input(value[2])
                if result:
                    InpurBox_temp.draw()
                    InpurBox_humi.draw()
                    if input.input_text['设置温度'] != '':
                        fzgpio.tmp_hum_data['temp'] = input.input_text['设置温度']
                    if input.input_text['设置湿度'] != '':
                        fzgpio.tmp_hum_data['humi'] = input.input_text['设置湿度']
        # 翻页按钮
        self.draw_t('上一页', (pageback_rect.x+pageback_rect.w/2, pageback_rect.y+pageback_rect.h/2))
        self.draw_t('下一页', (pageforward_rect.x+pageforward_rect.w/2, pageforward_rect.y+pageforward_rect.h/2))

    # 硬件图像刷新
    def draw_sensors(self):
        # 查看小车初始位置的像素点颜色
        # print(pygame.Surface.get_at(screen.surface, [360, 400]))
        # 实现翻页展示传感器画面
        if fzgpio.transmit_right != None:
            for key, value in list(fzgpio.transmit_right.items()):
                if key <= 5 and value[8] == 1 and pagechange['right'] == 1:
                    img = Actor('sensors/' + value[0])
                    img.pos = value[1]
                    img.draw()
                    self.draw_t(value[2], value[3])
                    fzgpio.servo.servo_angle_control(value[2], value[1], value[6][1])
                    for i in range(2):
                        self.draw_t(value[4][i], value[5][i])
                        self.draw_t(value[6][i], value[7][i])
                elif key >= 5 and key <= 10 and value[8] == 2 and pagechange['right'] == 2:
                    img = Actor('sensors/' + value[0])
                    img.pos = value[1]
                    img.draw()
                    self.draw_t(value[2], value[3])
                    fzgpio.servo.servo_angle_control(value[2], value[1], value[6][1])
                    for i in range(2):
                        self.draw_t(value[4][i], value[5][i])
                        self.draw_t(value[6][i], value[7][i])
                elif key >= 10 and key <= 15 and value[8] == 3 and pagechange['right'] == 3:
                    img = Actor('sensors/' + value[0])
                    img.pos = value[1]
                    img.draw()
                    self.draw_t(value[2], value[3])
                    fzgpio.servo.servo_angle_control(value[2], value[1], value[6][1])
                    for i in range(2):
                        self.draw_t(value[4][i], value[5][i])
                        self.draw_t(value[6][i], value[7][i])

        # 绘制当前温湿度并绘制
        if fzgpio.other_pos != None:
            if fzgpio.tmp_hum_data['temp'] != '' or fzgpio.tmp_hum_data['humi'] != '':
                # self.draw_t('可以设置当前温湿度', (InpurBox_temp_rect.x+80, InpurBox_temp_rect.y-10))
                fzgpio.text_box['temp_humi'] = {'文本框': constants.other_pos['文本框'],
                                                '当前温度：': constants.other_pos['当前温度'][0],
                                                fzgpio.tmp_hum_data['temp'] + '℃': constants.other_pos['当前温度'][1],
                                                '当前湿度：': constants.other_pos['当前湿度'][0],
                                                fzgpio.tmp_hum_data['humi'] + '%': constants.other_pos['当前湿度'][1]}
                for key, value in fzgpio.text_box.items():
                    for key1, value1 in value.items():
                        self.draw_t(key1, value1)

        # # 小车左红外绘制
        # screen.draw.circle((int(fzgpio.dict['Hongwai_pos']['hongwai_left_x']),
        #                            int(fzgpio.dict['Hongwai_pos']['hongwai_left_y'])), 20, color=(0, 0, 0))
        # # 小车右红外绘制
        # screen.draw.circle((int(fzgpio.dict['Hongwai_pos']['hongwai_right_x']),
        #                            int(fzgpio.dict['Hongwai_pos']['hongwai_right_y'])), 20, color=(0, 0, 0))

    # def cramer_draw(self):
    #     if self.py_image != 'None':
    #         screen.blit(self.py_image, (self.image_rect.x + 50, self.image_rect.y + 500))
    #         screen.blit('shijue//cramer_fill', (self.image_rect.x + 50, self.image_rect.y + 500))

    # 小车图像刷新
    def draw_car(self):
        if fzgpio.dict['actor'][0] == 1:
            self.actor.draw()
            # self.xunxian_run()

    # 获取红外像素点颜色
    def hongwai_position(self):
        # 获取小车左红外坐标处的像素颜色（RGBA）
        fzgpio.dict['car_pos_color_alpha']['left'] = \
            screen.surface.get_at((int(fzgpio.dict['Hongwai_pos']['hongwai_left_x']),
                                   int(fzgpio.dict['Hongwai_pos']['hongwai_left_y'])))
        # 获取小车右红外坐标处的像素颜色（RGBA）
        fzgpio.dict['car_pos_color_alpha']['right'] = \
            screen.surface.get_at((int(fzgpio.dict['Hongwai_pos']['hongwai_right_x']),
                                   int(fzgpio.dict['Hongwai_pos']['hongwai_right_y'])))

    # 摄像头获取仿真界面图像
    def cramer_update(self):
        self.cr_x = self.actor.center[0] - (self.actor.width / 2 + 55) * math.sin(math.radians(self.actor.angle))
        self.cr_y = self.actor.center[1] - (self.actor.height / 2 + 55) * math.cos(math.radians(self.actor.angle))
        self.screen_rect = screen.surface.get_rect()
        self.shijue_clip = self.screen_rect.clip((self.cr_x - 50, self.cr_y - 50), (100, 100))
        self.py_image, self.image_rect = tools.clip_image(self.shijue_clip)
        self.fzimage = tools.change_image(self.py_image, size=(200, 200))  # cv2类型的图像
        fzshijue1.dict['fzimage'] = self.fzimage

    # 小车运动刷新
    def update_car(self):
        if fzgpio.dict['actor'][0] == 1:
            self.actor_rect = Rect((self.actor.left, self.actor.top),
                                   (self.actor.width, self.actor.height))
            # 中间画面的大小，小车和物体的放置和运动不能超过此界限
            self.background_rect = Rect((200, 6), (900, 650))
            self.hongwai_rect = Rect((int(fzgpio.dict['Hongwai_pos']['hongwai_right_x']),
                                      int(fzgpio.dict['Hongwai_pos']['hongwai_right_y'])),
                                     (1, 1))
            if self.background_rect.contains(self.actor_rect) and self.background_rect.contains(self.hongwai_rect):
                self.car_contr_run()
                try:
                    self.hongwai_position()
                except Exception as result:
                    # 获取报错内容（获取后会导致报错内容不输出）
                    msg = traceback.format_exc()
                    logging.error(str(msg))
                    # 打印出报错内容
                    print(result)
                    sys.exit(0)
            else:
                pass

    # 运行监听
    def fzq_over(self):
        if fzgpio.dict['exit'] == True:
            sys.exit(0)

    # 子线程，这里写入新代码，子线程为仿真器画面展示的控制者
    def code(self):
        try:
            pass
        except Exception:
            msg = traceback.format_exc()
            logging.error(str(msg))
            print(msg)
            sys.exit(0)

    # 子线程控制，控制code线程
    def fzgo(self):
        # daemon参数为True，将子线程设置为守护线程，主线程结束，子线程跟着结束，进而使得进程立即结束
        # 设置daemon参数，最终目的是为了，在点击仿真界面右上角的叉叉关闭仿真器的时候，立即结束进程，避免主线程仍在等待子线程结束
        self.code_threading = threading.Thread(target=self.code, daemon=True)
        self.code_threading.start()
# --------------------------------------------------------------------------------------------------------
# 设置鼠标或按键事件 (监听)
def on_mouse_down(pos,button):
    # 点击鼠标右键给右边的硬件展示画面翻页
    if button == 1:
        if pageback_rect.collidepoint(pos[0], pos[1]):
            if pagechange['right'] > 1:
                pagechange['right'] -= 1
            else:
                pagechange['right'] = 3
        elif pageforward_rect.collidepoint(pos[0], pos[1]):
            if pagechange['right'] <= 2:
                pagechange['right'] += 1
            else:
                pagechange['right'] = 1
        # if pos[0]>=1160 and pos[1] <= 655:
        #     if pagechange['right'] <= 2:
        #         pagechange['right'] += 1
        #     else:
        #         pagechange['right'] = 1
        # elif pos[0]<=140 and pos[1] <= 470:
        #     if pagechange['left'] <= 2:
        #         pagechange['left'] += 1
        #     else:
        #         pagechange['left'] = 1
    # 鼠标点击输入框
    if InpurBox_temp_rect.collidepoint(pos[0], pos[1]):
        InpurBox_temp.active = True
    else:
        InpurBox_temp.active = False
    if InpurBox_humi_rect.collidepoint(pos[0], pos[1]):
        InpurBox_humi.active = True
    else:
        InpurBox_humi.active = False
def on_key_up():
    InpurBox_temp.count_time = 0
    InpurBox_humi.count_time = 0
# --------------------------------------------------------------------------------------------------------
# 仿真器运行
if run != '':
    import pgzrun
    # --------------------------------------------------------------------------------------------------------
    # 必须'def draw()'和'def update()',原设定就是如此,即无限循环执行draw()和update()
    # 当然，也可以在game.py里的PGZeroGame.mainloop()设置无限循环
    # 这里利用return返回调用的对象Update里面的draw(),update(),这样可以实现无限循环执行类中的方法
    # 最终目的是实现面向对象开发
    def draw():
        Update.draw_clear()
        Update.draw_background()
        Update.draw_sensors()
        # Update.cramer_draw()
        Update.draw_car()

    def update():
        Update.update_car()
        Update.cramer_update()
        Update.fzq_over()
    # --------------------------------------------------------------------------------------------------------
    # 设置根路径（也就是仿真所需要的图像路径，此处由change.py写入）
    # files_path = 'C:\\Users\\86137\\Documents\\python_code\\fzq_test\\files\\'
    files_path = ''
    loaders.set_root(files_path)
    # --------------------------------------------------------------------------------------------------------
    # 关卡设置：
    LEVEL = levels.Level_1()
    # --------------------------------------------------------------------------------------------------------
    # 获取储存日志的位置，记录报错内容
    files_path_logger = tools.path_processing(files_path, -2, 'txt\\')
    tools.Logging(files_path_logger)
    # --------------------------------------------------------------------------------------------------------
    # 窗口设置
    # screen : Screen
    screen = Screen(pygame.image.load(files_path + 'images\\interfaces\\interface_none.png'))
    WIDTH, HEIGHT = constants.WIDTH, constants.HEIGHT
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    TITLE = constants.TITLE
    icon_path = tools.path_processing(files_path, -1, 'data\\')
    ICON = icon_path + constants.ICON
    # --------------------------------------------------------------------------------------------------------
    # 输入框
    InpurBox_temp_rect = Rect(constants.other_pos['当前温度'][0][0] - 50, constants.other_pos['当前温度'][0][1] + 80, 170, 20)
    InpurBox_temp = input.InputBox(screen,
                                   rect=InpurBox_temp_rect,
                                   boxname='设置温度',
                                   rectcolor='black',
                                   fontname='fangsong.ttf',
                                   fontsize=18)
    InpurBox_humi_rect = Rect(constants.other_pos['当前湿度'][0][0] - 50, constants.other_pos['当前湿度'][0][1] + 100, 170, 20)
    InpurBox_humi = input.InputBox(screen,
                                   rect=InpurBox_humi_rect,
                                   boxname='设置湿度',
                                   rectcolor='black',
                                   fontname='fangsong.ttf',
                                   fontsize=18)
    # --------------------------------------------------------------------------------------------------------
    # 翻页框
    pageback_rect = Rect(1111, 660, 180 / 2, 35)
    pageforward_rect = Rect(1111 + (180 / 2) + 5, 660, 180 / 2, 35)
    # --------------------------------------------------------------------------------------------------------
    # 实例化对象
    Update = Update()
    # 启动子线程code（目的：利用子线程控制主线程的仿真画面）
    Update.fzgo()
    # --------------------------------------------------------------------------------------------------------
    # 开始运行
    # pgzrun.go()为死循环,也就是game.py里的PGZeroGame.mainloop()所设置的无限循环。
    pgzrun.go()
    # 以下语句只能在仿真器结束后执行。
    print('仿真器运行结束')
else:
    pass

