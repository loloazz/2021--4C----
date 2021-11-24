import PySimpleGUI as sg

import socket, sys

from pyfiglet import Figlet


def printLogo():
    f = Figlet(font='starwars')
    print("欢迎进入Answer Glibly")
    print(f.renderText(("answer")))
    print("★-☆-★-☆-★-☆-★-☆-★-☆-★-☆-★-☆-★")
    print("★              选择模式               ★")
    print("★-☆-★-☆-★-☆-★-☆-★-☆-★-☆-★-☆-★")
    print("★             1.闲聊模式              ★")
    print("★                                   ★")
    print("★             2.古诗模式              ★")
    print("★                                   ★")
    print("★             3.英文模式              ★")
    print("★-☆-★-☆-★-☆-★-☆-★-☆-★-☆-★-☆-★")
    print("输入序号即可！")


def init_window():
    # 窗口信息
    layout = [[(sg.Text('Answer like a flow robot', size=[40, 1]))],
              [sg.Output(size=(80, 20))],
              [sg.Multiline(size=(70, 5),  do_not_clear=False),
               sg.Submit('发送', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
               sg.Button('退出', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]

              ]

    window = sg.Window('Chat Window', layout, font="黑体", default_element_size=(30, 2))
    return window


if __name__ == '__main__':
    # 打印logo
    printLogo()
    HOST = '127.0.0.1'  # 主机名
    PORT = 8998  # 端口
    ADDR = (HOST, PORT)
    BUFSIZE = 1024

    sock = socket.socket()
    sock.connect(ADDR)

    window = init_window()
    while True:

        event, value = window.read()

        sock.sendall(value[0].encode('utf-8'))  # 不要用send()  将要发送的信息转换为bytes格式，并发送
        data = sock.recv(BUFSIZE).decode('utf-8')  # 接收服务器返回的信息，并转化为字符格式

        if event == '发送':
            if len(value[0]) < 1:
                print("小马回答：" + "你输入的信息为空，请重新输入")  # 输出收到的信息

            else:

                print("主人： " + value[0])
                print("小马回答：" + data)  # 输出收到的信息
                print()

        if event == sg.WINDOW_CLOSED or event == "退出":
            break


    sock.close()
    window.close()
