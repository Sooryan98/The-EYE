from gtts import gTTS
import nltk
import os
import keyboard
import threading
from mutagen.mp3 import MP3
import time

import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()


def ST(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def wait_for_input(timeout):
    print(f"Please enter something within {timeout} seconds:")

    start_time = time.time()

    # while True:
    try:
        with sr.Microphone() as sorurce2:
            r.adjust_for_ambient_noise(sorurce2, duration=.40)
            audio2 = r.listen(sorurce2, timeout=2)
            text = r.recognize_google(audio2)
            text = text.lower()
            print(text)
            ST(text)
            if text == 'repeat':

                return 0
            else:
                return 1

        # while True:
        #     if keyboard.is_pressed('r'):  # Check if any key is pressed
        #         user_input = keyboard.read_event(suppress=True).name
        #         print(f"\nYou entered: {user_input}")
        #         return 0
        #         if (time.time() - start_time)> timeout:
        #
        #             print(f"\nNo input within {timeout} seconds. Continuing with the task.")
        #             break

    except sr.RequestError as e:
        print("Could not request results;{0}".format(e))
    except sr.UnknownValueError:
        print(time.time() - start_time)
        print("Unknown Value")
    except sr.WaitTimeoutError:
        print("No speech detected within the timeout period.")


# def input_thread():
#     st=time.time()
#     while True:
#         while (time.time()-st<5):
#             user_input = input("Enter something (type 'exit' to quit): ")
#             if user_input.lower() == 'exit':
#                 print('stopped')
#                 return 0
#             else: return 1
#         else : break

def text_reader(path_to_page):
    print(path_to_page)
    for file in os.listdir(path_to_page):
        if file.endswith("4.txt"):
            npath = f"{path_to_page}/{file}"
    print(npath)
    page = open(npath, "r")
    content = page.read()
    sent = nltk.sent_tokenize(content)
    language = 'en'
    j = 0
    mi = 0
    audio_file = 'page_audio.mp3'
    result = 1
    j = 0
    for i in range(0, len(sent) - 1):
        # thread1 = threading.Thread(target=input_thread)
        # thread1.start()
        # #
        # time.sleep(1)
        # thread1.join()
        #
        # result = thread1.result() if hasattr(thread1, 'result') else None
        #
        # print(result
        #       )

        if result != 0:

            text = str(sent[i]).strip()
            print(text)
            myobj = gTTS(text=text, lang=language, slow=False)
            myobj.save(audio_file)
            audio = MP3(audio_file)
            stt = time.time()
            print(audio.info.length)
            if (time.time() - stt) < audio.info.length:
                os.system(audio_file)
            time.sleep(audio.info.length)
            os.remove(audio_file)
            j = i
            result = wait_for_input(5)
        elif result == 0:
            if j != 0:
                text = str(sent[j - 1]).strip()

                myobj = gTTS(text=text, lang=language, slow=False)
                myobj.save(audio_file)
                audio = MP3(audio_file)
                stt = time.time()
                print(audio.info.length)
                if (time.time() - stt) < audio.info.length:
                    os.system(audio_file)
                # Playing the converted file

                time.sleep(audio.info.length)
                os.remove(audio_file)
                result = 1
                j = 0
            else:
                text = str(sent[0]).strip()

                myobj = gTTS(text=text, lang=language, slow=False)
                myobj.save(audio_file)
                audio = MP3(audio_file)
                stt = time.time()
                print(audio.info.length)
                if (time.time() - stt) < audio.info.length:
                    os.system(audio_file)
                # Playing the converted file

                time.sleep(audio.info.length)
                os.remove(audio_file)
                result = 1
                j = 0
        if i == len(sent):
            break
        # time.sleep(1)

    #     if i == 3 and mi == 0:
    #         j = i
    #         break
    #     else:
    #         continue
    #     if i == len(sent) - 1:
    #         break
    # if j != 0:
    #     text = str(sent[j - 1]).strip()
    #
    #     myobj = gTTS(text=text, lang=language, slow=False)
    #     myobj.save(audio_file)
    #     audio = MP3(audio_file)
    #     stt = time.time()
    #     print(audio.info.length)
    #     if (time.time() - stt) < audio.info.length:
    #         os.system(audio_file)
    #     # Playing the converted file
    #
    #     time.sleep(audio.info.length)
    #     os.remove(audio_file)
    #     mi = 1
    #
    #     # time.sleep(1)

    # else:
    #
    #     text = str(sent[0]).strip()
    #     myobj = gTTS(text=text, lang=language, slow=False)
    #     myobj.save(audio_file)
    #     audio = MP3(audio_file)
    #     stt = time.time()
    #     print(audio.info.length)
    #     if (time.time() - stt) < audio.info.length:
    #         os.system(audio_file)
    #     # Playing the converted file
    #
    #     time.sleep(audio.info.length)
    #     os.remove(audio_file)
    #     # time.sleep(1)


def control(path_to_page):
    page_flag = text_reader(path_to_page)
    return page_flag
