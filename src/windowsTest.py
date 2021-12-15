import PySimpleGUI as sg

layout = [[(sg.Text('Answer like a flow robot', size=[40, 1]))],
          [sg.Output(size=(80, 20))],
          [sg.Multiline(size=(70, 5), enter_submits=True, do_not_clear=False),
           sg.Button('发送', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
           sg.Button('退出', button_color=(sg.YELLOWS[0], sg.GREENS[0])),
           sg.ReadButton('Speak')]

          ]

window = sg.Window('Chat Window', layout, font="黑体", default_element_size=(30, 2))

while True:

    event, value = window.read()

    # sock.sendall(value[0].encode('utf-8'))  # 不要用send()  将要发送的信息转换为bytes格式，并发送
    # data = sock.recv(BUFSIZE).decode('utf-8')  # 接收服务器返回的信息，并转化为字符格式

    if event == '发送':
        if len(value[0]) < 1:
            print("小马回答：" + "你输入的信息为空，请重新输入")  # 输出收到的信息

        else:
            print("主人： " + value[0])
            # print("小马回答：" + data)  # 输出收到的信息
            print()

    elif event == 'Speak':
        print("语音识别结果")
        print()


    else:
        break
window.close()
