import uart
import time
from pyPS4Controller.controller import Controller

uart_port_name = "/dev/ttyAMA0"
cp = uart.CommunicationProtocol(uart_port_name)

Speed = 0
Mode = 2
Acce = 0
Brake_P = 0

ID_RIGHT = 1
ID__LEFT = 2

SPEED_COEFFICIENT = 20
SPEED_5 = 50
SPEED_4 = 40
SPEED_3 = 30

controller_port_name = "/dev/input/js1"

# モーター初期化
cp.Control_Motor(0, ID_RIGHT, Acce, Brake_P)
cp.Control_Motor(0, ID__LEFT, Acce, Brake_P)

def motor_stop():
    cp.Control_Motor(0, ID_RIGHT, Acce, Brake_P)
    cp.Control_Motor(0, ID__LEFT, Acce, Brake_P)

def transf(raw):
    temp = (raw+32767)/65534
    # Filter values that are too weak for the motors to move
    if abs(temp) < 0.3:
        return 0
    # Return a value between 0.3 and 1.0
    else:
        return round(temp, 1)

def transf1(raw):
    temp = (abs(raw)+32767)/65534
    # Filter values that are too weak for the motors to move
    if abs(temp) < 0.3:
        return 0
    # Return a value between 0.3 and 1.0
    else:
        return round(-temp, 1)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    # 【＜－左】↓   ※－指定
    def on_L3_down(self, value):
        value = transf(value)

        # －指定するために－反転
        rpm = -int(value * SPEED_COEFFICIENT)
        cp.Control_Motor(rpm, ID__LEFT, Acce, Brake_P)
        print(str(value) + "/rpm:" + str(rpm))
            
    # 【＜－左】↑   ※＋指定
    def on_L3_up(self, value):
        value = transf1(value)
        
        # ＋指定するために－反転
        rpm = -int(value * SPEED_COEFFICIENT)
        cp.Control_Motor(rpm, ID__LEFT, Acce, Brake_P)
        print(str(value) + "/rpm:" + str(rpm))
        
    # 【＜－左】離し
    def on_L3_y_at_rest(self):
        cp.Control_Motor(0, ID__LEFT, Acce, Brake_P)
        print("on_L3_y_at_rest:L3")

    # 【右－＞】↓   ※＋指定
    def on_R3_down(self, value):
        value = transf(value)

        rpm = int(value * SPEED_COEFFICIENT)
        cp.Control_Motor(rpm, ID_RIGHT, Acce, Brake_P)
        print(str(value) + "/rpm:" + str(rpm))
            
    # 【右－＞】↑   ※－指定
    def on_R3_up(self, value):
        value = transf1(value)
        
        rpm = int(value * SPEED_COEFFICIENT)
        cp.Control_Motor(rpm, ID_RIGHT, Acce, Brake_P)
        print(str(value) + "/rpm:" + str(rpm))

    # 【右－＞】離し
    def on_R3_y_at_rest(self):
        cp.Control_Motor(0, ID_RIGHT, Acce, Brake_P)
        print("on_R3_y_at_rest:R3")

    # 【×】押し
    def on_x_press(self):
        cp.Control_Motor(SPEED_5, ID__LEFT, Acce, Brake_P)
        cp.Control_Motor(-SPEED_5, ID_RIGHT, Acce, Brake_P)
        print("on_x_press")

    # 【×】離し
    def on_x_release(self):
        motor_stop
        print("on_x_release")

    # 【□】押し
    def on_square_press(self):
        cp.Control_Motor(SPEED_4, ID__LEFT, Acce, Brake_P)
        cp.Control_Motor(-SPEED_4, ID_RIGHT, Acce, Brake_P)
        print("on_square_press")

    # 【□】離し
    def on_square_release(self):
        motor_stop
        print("on_square_release")

    # 【△】押し
    def on_triangle_press(self):
        cp.Control_Motor(SPEED_3, ID__LEFT, Acce, Brake_P)
        cp.Control_Motor(-SPEED_3, ID_RIGHT, Acce, Brake_P)
        print("on_tri_press")

    # 【△】離し
    def on_triangle_release(self):
        motor_stop
        print("on_tri_release")

    def on_R3_right(self, value):
        # nop
        print("on_Rx_right")

    def on_R3_left(self, value):
        # nop
        print("on_Rx_left")

controller = MyController(interface=controller_port_name, connecting_using_ds4drv=False)
controller.listen()
