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

controller_port_name = "/dev/input/js1"


# Speed = 10
# cp.Control_Motor(Speed, 1, Acce, Brake_P)
# Speed = -10
# cp.Control_Motor(Speed, 2, Acce, Brake_P)

# time.sleep(5)
# print('\t$$Finish')

Speed = 0
cp.Control_Motor(Speed, 1, Acce, Brake_P)
cp.Control_Motor(Speed, 2, Acce, Brake_P)

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
        return round(temp, 1)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    # 【＜－左】↓   ※－指定
    def on_L3_down(self, value):
        value = transf(value)
        cp.Control_Motor(-50, ID__LEFT, Acce, Brake_P)
        print(value)
            
    # 【＜－左】↑   ※＋指定
    def on_L3_up(self, value):
        value = transf1(value)
        cp.Control_Motor(50, ID__LEFT, Acce, Brake_P)
        print(value)
        
    # 【＜－左】離し
    def on_L3_y_at_rest(self):
        cp.Control_Motor(0, ID__LEFT, Acce, Brake_P)
        print("on_L3_y_at_rest:L3")

    # 【右－＞】↓   ※＋指定
    def on_R3_down(self, value):
        value = transf(value)
        cp.Control_Motor(50, ID_RIGHT, Acce, Brake_P)
        print(value)
            
    # 【右－＞】↑   ※－指定
    def on_R3_up(self, value):
        value = transf1(value)
        cp.Control_Motor(-50, ID_RIGHT, Acce, Brake_P)
        print(value)

    # 【右－＞】離し
    def on_R3_y_at_rest(self):
        cp.Control_Motor(0, ID_RIGHT, Acce, Brake_P)
        print("on_R3_y_at_rest:R3")


    def on_x_press(self):
        print("on_x_press")
        # nop

    def on_x_release(self):
        print("on_x_release")
        # nop

    def on_R3_right(self, value):
        print("on_Rx_right")
        # nop

    def on_R3_left(self, value):
        print("on_Rx_left")
        # nop


controller = MyController(interface=controller_port_name, connecting_using_ds4drv=False)
controller.listen()
