
import  PySimpleGUI as sg

from src.yuyinshibie import my_record, getToken, get_audio, speech2text, HOST, FILEPATH


layout = [[sg.Text('Converter', font='Helvetica 15')],
          [sg.ReadButton('Speak'), sg.ReadButton('Stop')],
          [sg.Output(size=(80, 10))],
          [sg.Exit()]]

window = sg.Window('Speech Recognition').Layout(layout)

while True:
    event,values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == 'Speak':
        # with m as source:
        #     r.adjust_for_ambient_noise(source)
        #     audio = r.listen(source)
        #     value = r.recognize_google(audio, language="en-US")
        #     print(value)

        my_record()
        TOKEN = getToken(HOST)
        speech = get_audio(FILEPATH)
        result = speech2text(speech, TOKEN, int(1537))

        print(result)

window.Close()