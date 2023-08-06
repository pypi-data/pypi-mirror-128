# coding=<encoding name> ： # coding=utf-8
import math, time, sys, threading, logging, traceback
from pgzero.actor import Actor
from fzq_scnu import constants, input
'''
！！！
已有background_rect为Rect((200, 6), (900, 650))。
待完成项：超声波的距离计算（可能需要设置障碍物）；
红外被遮挡（可利用rect碰撞,目前使用颜色检测）；
'''

# --------------------------------------------------------------------------------------------------------
# 仿真界面所有固定及关联坐标点
hardwarepos_pic_right = constants.hardwarepos_pic_right
hardwarepos_name_right = constants.hardwarepos_name_right
io_pwm_pos_right = constants.io_pwm_pos_right
return_data_pos_right = constants.return_data_pos_right
return_data_pos_right_other = constants.return_data_pos_right_other
#
hardwarepos_pic_left= constants.hardwarepos_pic_left
hardwarepos_name_left = constants.hardwarepos_name_left
return_data_pos_left = constants.return_data_pos_left
#
other_pos = constants.other_pos
tmp_hum_data = {'temp': '', 'humi': ''}
# --------------------------------------------------------------------------------------------------------
# 需要使用到的所有全局数据
dict = {'exit': False,
        'count': {'io': [0,[],9],'pwm': [0,[],4], 'uw': [0,[],2]},
        'num_count': 0,
        'actor': [0, {'contr_fb': 0, 'contr_lr': 0, 'contr_tn': 0}],
        'before_xunxian': 0,
        'xunxian': 0,
        'xunxian_stop': 0,
        'Hongwai_pos': {'open': 0, 'left': '', 'right': '',
                    'hongwai_left_x': 0, 'hongwai_left_y': 0,
                    'hongwai_right_x': 0, 'hongwai_right_y': 0},
        'car_pos_color_alpha': {'left': (255,255,255,255), 'right': (255,255,255,255)}
        }
hongwai_quantity = {'left': ['none', 'none'], 'right': ['none', 'none']}
# --------------------------------------------------------------------------------------------------------
# 该字典用于传递给仿真器运行文件所需要的数据
transmit_right = {}
transmit_left = {}
text_box = {}
# --------------------------------------------------------------------------------------------------------
# io口或pwm口的分配，及相应的报错
class gpio_distribute():
    def __init__(self, io_pwm_uw_num=None, io_pwm_uw='io'):
        self.io_pwm_uw_num = io_pwm_uw_num
        self.io_pwm_uw = io_pwm_uw

    def raise_exception(self):
        try:
            page_info_r = self.count_right()
            return page_info_r
        except Exception as result:
            msg = traceback.format_exc()
            logging.error(str(msg))
            print(result)
            # 传参给主线程，告诉它立即结束，传完后立即执行sys.exit(0)，退出子线程，
            # 这样可以完美避免子线程在进程结束的最后0.5秒内仍在运行
            dict['exit'] = True
            sys.exit(0)

    def count_left(self):
        # 待开发
        pass

    def count_right(self):
        assert type(self.io_pwm_uw_num) == int, \
            '未能检测到该{}{}号口,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)
        if self.io_pwm_uw == 'io' or self.io_pwm_uw == 'pwm':
            assert self.io_pwm_uw_num in [i for i in range(dict['count'][self.io_pwm_uw][2])], \
                '未能检测到该{}{}号口,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)
        elif self.io_pwm_uw == 'uw':
            assert self.io_pwm_uw_num in [i+1 for i in range(dict['count'][self.io_pwm_uw][2])], \
                '未能检测到该{}{}号口,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)
        assert self.io_pwm_uw_num not in dict['count'][self.io_pwm_uw][1], \
           '该{}{}号口已被占用,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)
        dict['count'][self.io_pwm_uw][0] += 1
        dict['count'][self.io_pwm_uw][1].append(self.io_pwm_uw_num)
        # 给右侧的展示的仿真图像分配坐标和页数
        if dict['count']['io'][0] + dict['count']['pwm'][0] + dict['count']['uw'][0] <= 5:
            dict['num_count'] += 1
            # 展示前五个硬件，分配坐标点，指定页数1展示
            page_info = (dict['num_count'], hardwarepos_pic_right[dict['num_count']], 1)
            return page_info
        elif dict['count']['io'][0] + dict['count']['pwm'][0] + dict['count']['uw'][0] <= 10:
            dict['num_count'] += 1
            # 展示中间五个硬件，分配坐标点，指定页数2展示
            page_info = (dict['num_count']-5, hardwarepos_pic_right[dict['num_count']-5], 2)
            return page_info
        elif dict['count']['io'][0] + dict['count']['pwm'][0] + dict['count']['uw'][0] <= 15:
            dict['num_count'] += 1
            # 展示后五个硬件，分配坐标点，指定页数3展示
            page_info = (dict['num_count']-10, hardwarepos_pic_right[dict['num_count']-10], 3)
            return page_info
# --------------------------------------------------------------------------------------------------------
# 进行统一操作，目的是在字典transmit中放入需要传递的所有可以用于绘制文字、图像等的参数
    @staticmethod
    def message(hardwarepos_pic_name,hardwarepos_name,io_pwm,io_pwm_num,text1,text2,page_info):
        # 储存图像名，显示图像名，接口类型，接口位，文本1，文本2，页面展示消息，
        name_position = hardwarepos_name_right[page_info[0]]
        io_pwm_position = io_pwm_pos_right[page_info[0]]
        # if hardwarepos_name == 'IO' or hardwarepos_name == 'PWM':
        #     return_datas_position = return_data_pos_right_other[page_info[0]]
        # else:
        return_datas_position = return_data_pos_right[page_info[0]]
        transmit_right[dict['num_count']] = [hardwarepos_pic_name, page_info[1],
                                             hardwarepos_name,
                                             name_position,
                                             [io_pwm, str(io_pwm_num)],
                                             io_pwm_position,
                                             [text1, text2],
                                             return_datas_position,
                                             page_info[2]]
# --------------------------------------------------------------------------------------------------------
# 主要
# gpio改为fzgpio
class io():
    def __init__(self, io_num=None):
        self.gpioio = io_num
        self.io_img_name = 'low'
        if self.gpioio != None:
            page_info = gpio_distribute(self.gpioio, 'io').raise_exception()
            gpio_distribute.message(self.io_img_name, 'IO', 'IO', self.gpioio, ' ', ' ', page_info)
            self.iocount = dict['num_count']
        self.ioin = 404
        self.inorout = '未设置输入输出模式'
        self.dianping = '未设置高低电平'

    def setinout(self, inorout):
        self.inorout = inorout
        if self.inorout == 'IN':
            transmit_right[self.iocount][6][0]= 'IN'
        elif self.inorout == 'OUT':
            transmit_right[self.iocount][6][0]= 'OUT'
        else:
            dict['exit'] = True
            print('未设置输入输出模式或是未知错误')
            sys.exit(0)

    def setioout(self, dianping):
        self.dianping = dianping
        if transmit_right[self.iocount][6][0]== 'OUT':
            # GPIO输出高or低电平
            if self.dianping == 'HIGH':
                transmit_right[self.iocount][6][1]= 'HIGH'
                transmit_right[self.iocount][0] = 'high'
            elif self.dianping == 'LOW':
                transmit_right[self.iocount][6][1]= 'LOW'
                transmit_right[self.iocount][0] = 'low'
            else:
                dict['exit'] = True
                print('未设置高低电平或是未知错误')
                sys.exit(0)
        else:
            dict['exit'] = True
            print('IO口未设置为输出模式,请检查')
            sys.exit(0)

    def getioin(self):
        if transmit_right[self.iocount][6][0] == 'IN':
            self.ioin = 0
            transmit_right[self.iocount][0] = 'low'
        else:
            self.ioin = 1
            transmit_right[self.iocount][0] = 'high'

    def cleanio(self):
        self.ioin = 404
        self.inorout = '未设置输入输出模式'
        self.dianping = '未设置高低电平'
        transmit_right[self.iocount][6][0] = ' '
        transmit_right[self.iocount][6][1] = ' '

class io2pwm():
    def __init__(self, io_num=None, freq=50, duty=50):
        self.iopwm_io = io_num
        self.iopwm_img_name = 'low'
        if self.iopwm_io != None:
            page_info = gpio_distribute(self.iopwm_io, 'io').raise_exception()
            gpio_distribute.message(self.iopwm_img_name, 'IO', 'IO', self.iopwm_io, ' ', ' ', page_info)
            self.iopwmcount = dict['num_count']
        self.iopwm_freq = freq
        self.iopwm_duty = duty

    def start(self):
        transmit_right[self.iopwmcount][6][0] = '' + str(self.iopwm_freq) + 'Hz'
        transmit_right[self.iopwmcount][6][1] = str(self.iopwm_duty) + '%'
        transmit_right[self.iopwmcount][0] = 'pwm50'

    def set_freq(self, pwm_freq):
        self.iopwm_freq = pwm_freq
        transmit_right[self.iopwmcount][6][0] = '' + str(self.iopwm_freq) + 'Hz'

    def set_duty(self, pwm_duty):
        self.iopwm_duty = pwm_duty
        transmit_right[self.iopwmcount][6][1] = '' + str(self.iopwm_duty) + '%'
        if self.iopwm_duty < 50:
            transmit_right[self.iopwmcount][0] = 'pwm25'
        elif self.iopwm_duty > 50:
            transmit_right[self.iopwmcount][0] = 'pwm75'

    def end(self):
        transmit_right[self.iopwmcount][6][0] = '' + '0' + 'Hz'
        transmit_right[self.iopwmcount][6][1] = '' + '0' + '%'

class PWM():
    def __init__(self, pwm_io=None):
        self.pwm_io = pwm_io
        self.pwm_img_name = 'low'
        if self.pwm_io != None:
            page_info = gpio_distribute(self.pwm_io, 'pwm').raise_exception()
            gpio_distribute.message(self.pwm_img_name, 'PWM', 'PWM', self.pwm_io, ' ', ' ', page_info)
            self.pwmcount = dict['num_count']
        self.pwm_duty = 50
        self.pwm_freq = 262

    def pwm_start(self):
        transmit_right[self.pwmcount][6][0] = '' + str(self.pwm_freq) + 'Hz'
        transmit_right[self.pwmcount][6][1] = str(self.pwm_duty) + '%'
        transmit_right[self.pwmcount][0] = 'pwm50'

    def change_duty(self, duty):
        self.pwm_duty = duty
        transmit_right[self.pwmcount][6][1] = '' + str(self.pwm_duty) + '%'
        if self.pwm_duty < 50:
            transmit_right[self.pwmcount][0] = 'pwm25'
        elif self.pwm_duty > 50:
            transmit_right[self.pwmcount][0] = 'pwm75'

    def change_freq(self, freq):
        self.pwm_freq = freq
        transmit_right[self.pwmcount][6][0] = '' + str(self.pwm_freq) + 'Hz'

    def pwm_stop(self):
        transmit_right[self.pwmcount][6][0] = '' + '0' + 'Hz'
        transmit_right[self.pwmcount][6][1] = '' + '0' + '%'

class csb():
    def __init__(self, uw_num=None):
        self.csbuw = uw_num
        self.csb_img_name = 'chaos'
        if self.csbuw != None:
            page_info = gpio_distribute(self.csbuw, 'uw').raise_exception()
            gpio_distribute.message(self.csb_img_name, '超声波传感器', 'UW', self.csbuw, '关', ' ', page_info)
            self.csbcount = dict['num_count']
        # self.trig_p = uw_num
        # self.echo_p = uw_num
        self.dis = 0
        self.csb_while = True

    # 子线程目的：实现超声波传感器开启后的动画效果
    def csb_theading(self):
        imgs_name = ['chaos1', 'chaos2', 'chaos3', 'chaos4', 'chaos5', 'chaos6', 'chaos7', 'chaos8']
        while True:
            for img in imgs_name:
                if self.csb_while == True:
                    transmit_right[self.csbcount][6][0] = '开'
                    transmit_right[self.csbcount][0] = img
                    time.sleep(1)
                else:
                    sys.exit(0)

    def get_distance(self):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!待更新
        print('超声波传感器待更新')
        self.dis = 20
        self.beep_while = True
        self.beep_thead = threading.Thread(target=self.csb_theading, daemon=True)
        self.beep_thead.start()

class beep():
    def __init__(self, beepio=None):
        self.beepio = beepio
        self.beep_img_name = 'beep'
        if self.beepio != None:
            page_info = gpio_distribute(self.beepio, 'io').raise_exception()
            gpio_distribute.message(self.beep_img_name, '蜂鸣器', 'IO', self.beepio, '关', ' ', page_info)
            self.beepcount = dict['num_count']
        # self.data = 0
        self.beep_while = True

    # 子线程目的：实现蜂鸣器开启后的动画效果
    def beep_theading(self):
        imgs_name = ['beep1', 'beep2', 'beep3']
        while True:
            for img in imgs_name:
                if self.beep_while == True:
                    transmit_right[self.beepcount][6][0] = '开'
                    transmit_right[self.beepcount][0] = img
                    time.sleep(1)
                else:
                    sys.exit(0)

    def beep_s(self, seconds=1):
        self.beep_while = True
        self.beep_thead = threading.Thread(target=self.beep_theading, daemon=True)
        time.sleep(seconds)
        self.beep_thead.start()

    def open_b(self):
        self.beep_while = True
        self.beep_thead = threading.Thread(target=self.beep_theading, daemon=True)
        self.beep_thead.start()

    def close_b(self):
        self.beep_while = False
        transmit_right[self.beepcount][6][0] = '关'
        transmit_right[self.beepcount][0] = 'beep'

class led():
    def __init__(self, ledio=None):
        self.ledio = ledio
        self.led_img_name = 'led_off1'
        if self.ledio != None:
            page_info = gpio_distribute(self.ledio, 'io').raise_exception()
            gpio_distribute.message(self.led_img_name, 'Led', 'IO', self.ledio, '灭', '', page_info)
            self.ledcount = dict['num_count']

    def openled(self):
        transmit_right[self.ledcount][0]= 'led_on1'
        transmit_right[self.ledcount][6][0]= '亮'

    def closeled(self):
        transmit_right[self.ledcount][0]= 'led_off1'
        transmit_right[self.ledcount][6][0] = '灭'

class tmp_hum():
    def __init__(self, t_h_io=None):
        self.tmp_io = t_h_io
        self.tmp_hum_img_name = 'wsdu1'
        if self.tmp_io != None:
            page_info = gpio_distribute(self.tmp_io, 'io').raise_exception()
            gpio_distribute.message(self.tmp_hum_img_name, '温湿度传感器', 'IO', self.tmp_io, '关', '', page_info)
            self.tmp_humcount = dict['num_count']
        self.temp = None
        self.humi = None

    def getTemp_Humi(self):
        # ！！！！！！！！！！！！！！！！！！待更新
        self.temp, self.humi = 26, 30
        if self.temp or self.humi:
            if input.input_text['设置温度'] != '' or input.input_text['设置温度'] != '':
                self.temp = input.input_text['设置温度']
                self.humi = input.input_text['设置温度']
            else:
                tmp_hum_data['temp'] = str(self.temp)
                tmp_hum_data['humi'] = str(self.humi)
                text_box['temp_humi'] = {'文本框': other_pos['文本框'],
                                         '当前温度：': other_pos['当前温度'][0],
                                         tmp_hum_data['temp'] + '℃': other_pos['当前温度'][1],
                                         '当前湿度：': other_pos['当前湿度'][0],
                                         tmp_hum_data['humi'] + '%': other_pos['当前湿度'][1]}
            transmit_right[self.tmp_humcount][6][0] = '开'
        else:
            print("温湿度传感器：获取温湿度失败")

    @staticmethod
    def tmp_hum_input(hardwarepos_name):
        if hardwarepos_name == '温湿度传感器':
            return True

class hongwai():
    def __init__(self, hongwaiio = None, position = '左'):
        # 默认先使用左红外
        self.hongwaiio = hongwaiio
        self.position = position
        self.hongwai_img_name = 'hongwai0'
        if self.hongwaiio != None:
            if hongwai_quantity['left'][0] == 'none':
                page_info = gpio_distribute(self.hongwaiio, 'io').raise_exception()
                gpio_distribute.message(self.hongwai_img_name, '红外传感器', 'IO', self.hongwaiio, 'IN', '0', page_info)
                self.hongwaicount = dict['num_count']
                hongwai_quantity['left'][0] = 'true'
                hongwai_quantity['left'][1] = str(self.hongwaicount)
                # 启动子线程
                self.hongwai_thead = threading.Thread(target=self.hongwai_threading, daemon=True)
                self.hongwai_thead.start()
            elif hongwai_quantity['right'][0] == 'none':
                page_info = gpio_distribute(self.hongwaiio, 'io').raise_exception()
                gpio_distribute.message(self.hongwai_img_name, '红外传感器', 'IO', self.hongwaiio, 'IN', '0', page_info)
                self.hongwaicount = dict['num_count']
                hongwai_quantity['right'][0] = 'true'
                hongwai_quantity['right'][1] = str(self.hongwaicount)
                # 启动子线程
                self.hongwai_thead = threading.Thread(target=self.hongwai_threading, daemon=True)
                self.hongwai_thead.start()
            else:
                print('红外数量上限是两个')
        self.lr = None
        self.data = 0
        self.ioin = 0
        self.timewait = 0.08

    # 用户手动调用，需要反复调用才能持续显示返回值
    def get_return(self):
        if dict['actor'][0] == 1:
            imgs_name = ['hongwai1', 'hongwai2']
            if hongwai_quantity['left'][0] == 'true' and hongwai_quantity['left'][1] == str(self.hongwaicount):
                self.lr = 'left'
            elif hongwai_quantity['right'][0] == 'true' and hongwai_quantity['right'][1] == str(self.hongwaicount):
                self.lr = 'right'
            if self.lr:
                a = 0
                # 注意：此处必须延时，不然更不上主线程（或者说是主线程里面的子线程code）里面的for循环速度
                time.sleep(self.timewait)
                self.timewait = 0.03
                for i in range(3):
                    if dict['car_pos_color_alpha'][self.lr][i] == 255:
                        a += 1
                if a == 3:
                    # dict['Hongwai_pos'][lr] = 0
                    transmit_right[self.hongwaicount][0] = imgs_name[1]
                    transmit_right[self.hongwaicount][6][1] = '0'
                    self.data = eval(transmit_right[self.hongwaicount][6][1])
                else:
                    # dict['Hongwai_pos'][lr] = 1
                    transmit_right[self.hongwaicount][0] = imgs_name[0]
                    transmit_right[self.hongwaicount][6][1] = '1'
                    self.data = eval(transmit_right[self.hongwaicount][6][1])
        else:
            print('使用红外，请先初始化小车')

    # 子线程目的：等待一会后，红外不亮，返回值归空
    def hongwai_threading(self):
        time.sleep(1)
        transmit_right[self.hongwaicount][0] = 'hongwai0'

    # 只供麦克纳姆小车调用（有左右红外区分）
    # def get_return_2(self):
    #     imgs_name = ['hongwai1', 'hongwai2']
    #     if self.position == '左':
    #         a = 0
    #         for i in range(3):
    #             if dict['car_pos_color_alpha']['left'][i] >= 170 and dict['car_pos_color_alpha']['left'][i] <= 175:
    #                 a +=1
    #         if a >= 2:
    #             dict['Hongwai_pos']['left'] = 0
    #             self.data = 0
    #             transmit_right[self.hongwaicount][0] = imgs_name[1]
    #             transmit_right[self.hongwaicount][6][1] = '左:0'
    #         else:
    #             dict['Hongwai_pos']['left'] = 1
    #             self.data = 1
    #             transmit_right[self.hongwaicount][0] = imgs_name[0]
    #             transmit_right[self.hongwaicount][6][1] = '左:1'
    #     elif self.position == '右':
    #         b = 0
    #         for i in range(3):
    #             if dict['car_pos_color_alpha']['right'][i] >= 170 and dict['car_pos_color_alpha']['right'][i] <= 175:
    #                 b += 1
    #         if b >= 2:
    #             dict['Hongwai_pos']['right'] = 0
    #             transmit_right[self.hongwaicount][0] = imgs_name[1]
    #             transmit_right[self.hongwaicount][6][1] = '右:0'
    #         else:
    #             dict['Hongwai_pos']['right'] = 1
    #             transmit_right[self.hongwaicount][0] = imgs_name[0]
    #             transmit_right[self.hongwaicount][6][1] = '右:1'

    # 用户调用
    def getioin(self):
        if '0' in transmit_right[self.hongwaicount][6][1]:
            self.ioin = 0
        elif '1' in transmit_right[self.hongwaicount][6][1]:
            self.ioin = 1

class servo():
    def __init__(self, servo_io=None):
        self.servoio = servo_io
        self.servo_img_name = 'steering_engine'
        if self.servoio != None:
            page_info = gpio_distribute(self.servoio, 'io').raise_exception()
            gpio_distribute.message(self.servo_img_name, '舵机', 'IO', self.servoio, '开', '', page_info)
            self.servoiocount = dict['num_count']
        self.duty = 0

    def setServoAngle(self, angle):  # 设置舵机角度
        self.servo_angle = angle
        transmit_right[self.servoiocount][6][1] = ' ' + str(self.servo_angle) + '°'

    @staticmethod
    def servo_angle_control(hardwarepos_name, hardwarepos_pos, servo_angle):
        if hardwarepos_name == '舵机':
            img_name = 'sensors/steering_engine0'
            hardwarepos_pos = hardwarepos_pos
            servo_angle = int(eval(servo_angle.strip('°').strip(' ')))
            img = Actor(img_name)
            img.pos = hardwarepos_pos
            img.angle = servo_angle
            img.draw()

# 主角
class Mecanum_wheel():
    def __init__(self):
        self.actor = Actor('actors/car')
        self.actor.pos = (360, 370)
        # 初始化时，计算小车左右红外的位置
        self.car_hongwai()
        self.car_speed = {'car_go': 0, 'car_back': 0,
                          'car_turn_l': 0, 'car_turn_r': 0,
                          'car_across_l': 0, 'car_across_r': 0}

    def car_hongwai(self):
        # 旋转度数在0~90之间时，为原有的基准6 / 11乘上（0.7 + 0.2*|cos（2θ）|)，以达到红外不外移的目的
        weitiao = 0.68 + 0.28 * (math.fabs(math.cos(2*math.radians(self.actor.angle))))**3
        # 计算红外位置
        dict['Hongwai_pos']['hongwai_left_x'] = self.actor.x - self.actor.height * (6 / 11 * weitiao) * math.sin(
            math.radians(self.actor.angle)) - 6 * math.cos(math.radians(self.actor.angle)) - 1 / 2
        dict['Hongwai_pos']['hongwai_left_y'] = self.actor.y - self.actor.height * (6 / 11 * weitiao) * math.cos(
            math.radians(self.actor.angle)) + 6 * math.sin(math.radians(self.actor.angle)) - 1 / 2
        dict['Hongwai_pos']['hongwai_right_x'] = self.actor.x - self.actor.height * (6 / 11 * weitiao) * math.sin(
            math.radians(self.actor.angle)) + 6 * math.cos(math.radians(self.actor.angle)) - 1 / 2
        dict['Hongwai_pos']['hongwai_right_y'] = self.actor.y - self.actor.height * (6 / 11 * weitiao) * math.cos(
            math.radians(self.actor.angle)) - 6 * math.sin(math.radians(self.actor.angle)) - 1 / 2


    # 初始化小车，用户直接调用
    def uart_init(self):
        if dict['actor'][0] == 0:
            dict['actor'][0] = 1
        elif dict['actor'][0] == 1:
            print('已经初始化了麦克纳姆小车，无需再初始化')
            dict['exit'] = True

    # 设置小车速度的所有方法，用户直接调用
    def stop(self):
        self.car_speed['car_go'] = 0
        self.car_speed['car_back'] = 0
        self.car_speed['car_across_l'] = 0
        self.car_speed['car_across_r'] = 0
        self.car_speed['car_turn_l'] = 0
        self.car_speed['car_turn_r'] = 0
        self.car_contr()

    def car_go(self):
        self.car_contr()

    def car_across_l(self):
        self.car_contr()

    def car_turn_l(self):
        self.car_contr()

    def car_back(self):
        self.car_contr()

    def car_across_r(self):
        self.car_contr()

    def car_turn_r(self):
        self.car_contr()

    # 各个方向的速度计算
    def car_contr(self):
        if dict['actor'][0] == 1:
            dict['actor'][1]['contr_fb'] = self.car_speed['car_go']-self.car_speed['car_back']
            dict['actor'][1]['contr_lr'] = self.car_speed['car_across_l']-self.car_speed['car_across_r']
            dict['actor'][1]['contr_tn'] = self.car_speed['car_turn_l']-self.car_speed['car_turn_r']

    # -------------------------------------------------------
    # car_contr_run是在仿真器运行文件里面刷新的方法
    def car_contr_run(self,t=0.0075):
        if dict['actor'][0] == 1:
            fb = dict['actor'][1]['contr_fb']
            lr = dict['actor'][1]['contr_lr']
            tn = dict['actor'][1]['contr_tn']
            # 坐标计算，实现移动
            self.actor.x -= fb * math.sin(math.radians(self.actor.angle)) * t
            self.actor.y -= fb * math.cos(math.radians(self.actor.angle)) * t
            self.actor.x -= lr * math.cos(math.radians(self.actor.angle)) * t
            self.actor.y -= -lr * math.sin(math.radians(self.actor.angle)) * t
            self.actor.angle += tn * t
            self.actor.pos = (self.actor.x, self.actor.y)
            # 时时刻刻计算小车左右红外的位置
            self.car_hongwai()
    # # -------------------------------------------------------
    # # 巡线必须先初始化左右两个红外，初始化后，不能更改小车红外io设置。用户直接调用
    # def before_xunxian(self, io_l, io_r):
    #     global io_le, io_ri
    #     io_le = io_l
    #     io_ri = io_r
    #     dict['before_xunxian'] = 1
    #
    # # -------------------------------------------------------
    # # 命令开始巡线，用户直接调用
    # def xunxian(self):
    #     try:
    #         assert dict['before_xunxian'] == 1 or dict['before_xunxian'] == 2, "未设置巡线用的左右红外"
    #         dict['xunxian'] = 1
    #         dict['xunxian_stop'] = 0
    #         print('开始巡线')
    #         while dict['xunxian'] ==1 and dict['xunxian_stop'] == 0:
    #             pass
    #         dict['xunxian'] = 0
    #         print('巡线结束')
    #     except Exception as result:
    #         msg = traceback.format_exc()
    #         logging.error(str(msg))
    #         print(result)
    #         sys.exit(0)
    # # -------------------------------------------------------
    # # xunxian_run是真正在仿真器运行文件里面刷新的函数
    # def xunxian_run(self):
    #     if dict['xunxian'] == 1 and dict['before_xunxian'] == 1:
    #         self.hw_l = hongwai(io_le, '左')
    #         self.hw_r = hongwai(io_ri, '右')
    #         dict['before_xunxian'] = 2
    #     elif dict['xunxian'] == 1 and dict['before_xunxian'] == 2:
    #         self.hw_l.get_return_2()
    #         self.hw_r.get_return_2()
    #         # 左转
    #         if dict['Hongwai_pos']['right'] == 1 and dict['Hongwai_pos']['left'] == 0:
    #             # self.car_contr(0, -100, 200)
    #             dict['actor'][1]['contr_fb'] = 0
    #             dict['actor'][1]['contr_lr'] = -50
    #             dict['actor'][1]['contr_tn'] = 200
    #             # self.car_contr(0, -100, 300)
    #         # 右转
    #         elif dict['Hongwai_pos']['right'] == 0 and dict['Hongwai_pos']['left'] == 1:
    #             # self.car_contr(0, 100, -200)
    #             dict['actor'][1]['contr_fb'] = 0
    #             dict['actor'][1]['contr_lr'] = 50
    #             dict['actor'][1]['contr_tn'] = -200
    #             # self.car_contr(0, 100, -300)
    #         # 前进
    #         elif dict['Hongwai_pos']['right'] == 0 and dict['Hongwai_pos']['left'] == 0:
    #             # self.car_contr(100, 0, 0)
    #             dict['actor'][1]['contr_fb'] = 100
    #             dict['actor'][1]['contr_lr'] = 0
    #             dict['actor'][1]['contr_tn'] = 0
    #         # 停止
    #         elif dict['Hongwai_pos']['right'] == 1 and dict['Hongwai_pos']['left'] == 1:
    #             dict['actor'][1]['contr_fb'] = 0
    #             dict['actor'][1]['contr_lr'] = 0
    #             dict['actor'][1]['contr_tn'] = 0
    #             dict['xunxian_stop'] = 1
    #             transmit_right[self.hw_l.hongwaicount][0] = 'hongwai0'
    #             transmit_right[self.hw_l.hongwaicount][6][1] = ' '
    #             transmit_right[self.hw_r.hongwaicount][0] = 'hongwai0'
    #             transmit_right[self.hw_r.hongwaicount][6][1] = ' '
    #     else:
    #         pass


