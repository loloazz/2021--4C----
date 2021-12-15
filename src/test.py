import PySimpleGUI as sg
import os, sys


# 构造 Frame
simple_frame = [[sg.Multiline('', key='_RES_', disabled=True)]]

# 构造整体窗口布局
layout = [[sg.Multiline('', key='_Q_', focus=True), sg.Button('翻译', key='_TRANS_')],
          [sg.Frame('翻译结果', simple_frame, title_color='gray')]]

# 生成窗口
window = sg.Window('翻译小工具', layout)

while True:
    event, value = window.Read()

    # 如果点击翻译按钮
    if event == '_TRANS_':
       print()
        # 把翻译结果展示到Frame中的文本区域
        # window['_RES_'].update(result)

    if event is None:
        break

window.close()
