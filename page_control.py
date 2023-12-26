import os.path

from processor import Buffer
import speech_recognition as sr
import pyttsx3
def ST(command):
    engine=pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
r=sr.Recognizer()
count = 0
while True:
    try:
        with sr.Microphone() as sorurce2:
            r.adjust_for_ambient_noise(sorurce2,duration=.40)
            audio2=r.listen(sorurce2)
            text=r.recognize_google(audio2)
            text=text.lower()
            print(text)
            ST(text)

    #direction_control = input("Press N for next page :: ")

        direction_control=text
        while direction_control != '':
            if direction_control == 'next':
                page_folder = 'page_{}'.format(count)
                if not os.path.exists(page_folder):
                    os.makedirs(page_folder)
                flag = Buffer(page_folder, 0)
                count = count + 1
                if flag == 'OK':
                    break

            elif direction_control == 'last' or direction_control=='lost':
                if count == 0:

                    page_folder = 'page_{}'.format(0)
                    flag = Buffer(page_folder, 1)
                    if flag == 'OK':
                        break
                else:
                    page_folder = 'page_{}'.format(count - 1)
                    flag = Buffer(page_folder, 1)
                    if flag == 'OK':
                        break
    except sr.RequestError as e:
        print("Could not request results;{0}".format(e))
    except sr.UnknownValueError:
        print("Unknown Value")