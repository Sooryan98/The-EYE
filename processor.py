import cv2
import math
from blurdetection import blurrinesDetection
from pytesseract import pytesseract
from PIL import Image

import numpy as np
import regex as re
import random
import os, glob
import cv2
import time
import blurdetection
from audio_genmk2 import control
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from stabilizer import gain
t0 = time.time()


def similar(n, sim, rate, image_frame, maxconf_id):
    d = []
    fl = 0

    for i in range(0, len(n) - 1):
        fl = i
        try:
            # if i!=maxconf_id:
            ve = TfidfVectorizer()
            vectors = ve.fit_transform([n[maxconf_id], n[i]])
            similarity = cosine_similarity(vectors)
            sim.append(similarity[0][1])
            if sim[i] < 1.0:
                d.append(i)

        except ValueError:
            VEfile = ['frame' + str(fl * rate) + '.png']

            for file in os.listdir(image_frame):
                if file in VEfile:
                    os.remove(os.path.join('D:/RD_sim/test/' + str(image_frame), file))
            print("Bad Frame removed : " + str(VEfile))
            print(n[i])
        fl = 0
    try:
        best = [max(sim)]
        ogfile = sim.index(best[0])
    except ValueError:
        ogfile = 0
    # print(ogfile)
    print(d)
    return d, ogfile


def removefiles(val, k, image_frames, rate):
    duplicate = ['frame' + str(j * rate) + '.png' for j in val]
    for file in os.listdir(image_frames):
        if file in duplicate:
            os.remove(os.path.join('D:/RD_sim/test/' + str(image_frames), file))
            print("files removed")
    if k == 1:

        print("pre-processing complete : blurred files removed")
    else:
        print("pre-processing complete : duplicate image removed")


def files(image_frames):
    try:
        os.remove(image_frames)
    except OSError:
        pass
    if not os.path.exists(image_frames):
        os.makedirs(image_frames)
    gain(image_frames)
    #src_vid = cv2.VideoCapture(0)


def process(page_number, rate, image_frames, final):
    index = 0
    fc = 0
    video_path=page_number+'/stabilized_output.avi'
    src_vid=cv2.VideoCapture(video_path)
    while src_vid.isOpened():
        ret, frame = src_vid.read()

        try:
            if not ret:
                 break
            else:
            #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #
            #     thresh = cv2.threshold(gray, 210, 255,
            #
            #                            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            #     cv2.imshow('check', thresh)

                name = str(image_frames) + '/frame' + str(index) + '.png'
                if index % rate == 0:
                    print('Extracting frames....' + name)
                    fc = fc + 1
                    cv2.imwrite(name, frame)
                index = index + 1
                t1 = time.time()

            if (fc - 2) * rate == final:
                break
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        except AssertionError:
            print("Skipping Frame")
    src_vid.release()
    cv2.destroyAllWindows()


def get_text(n, page_path, conf_list):
    for i in sorted(glob.glob(str(page_path) + '/*.png'), key=numericalSort):

        openedimage = Image.open(i)
        path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pytesseract.tesseract_cmd = path_to_tesseract

        text = pytesseract.image_to_string(openedimage, lang='eng')
        text_data = pytesseract.image_to_data(openedimage, output_type='data.frame')
        text_data = text_data[text_data.conf != -1]
        # print(text.head())
        lines = text_data.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['text'] \
            .apply(lambda x: ' '.join(list(x))).tolist()
        confs = text_data.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['conf'].mean().tolist()

        line_conf = []

        for i in range(len(lines)):
            if lines[i].strip():
                line_conf.append((round(confs[i], 3)))
        page_conf = np.average(line_conf)

        conf_list.append(page_conf if not np.isnan(page_conf) else 0)

        n.append(text)
    print(conf_list)


def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def text_gen_fresh(page_path, ogtag, rate):
    print("Reading page")
    for i in sorted(glob.glob(str(page_path) + '/*.png'), key=numericalSort):
        # print(str(i))
        # if i==ogtag:

        openedimage = Image.open(i)
        path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pytesseract.tesseract_cmd = path_to_tesseract

        text = pytesseract.image_to_string(openedimage, lang='eng')
        text = str(text)
        text_file_path = f"{page_path}/page.txt"
        with open(text_file_path, 'w') as f:
            f.write(text)


def read_text(path_to_new, direc):
    if direc == 0:
        for file in os.listdir(path_to_new):
            if file.endswith(".txt"):
                npath = f"{path_to_new}/{file}"
                page = open(npath, "r")
                content = page.read()
                print(content)
    elif direc == 1:
        for file in os.listdir(path_to_new):
            if file.endswith(".txt"):
                npath = f"{path_to_new}/{file}"
                page = open(npath, "r")
                content = page.read()
                print(content)


def Buffer(page_folder, direc):
    page_number = page_folder
    if direc == 0:
        rate = 25
        sim = []
        n = []
        final = 250
        conf_list = []
        print("GOt here")
        # ik=int(random.randint(100,200))
        ik = 500
        key = 0
        # vid = files(page_number)

        files(page_number)
        process(page_number, rate, page_number, final)

        get_text(n, page_number, conf_list)

        max_conf = max(conf_list)
        print(max_conf)
        id_max_conf = conf_list.index(max_conf)
        print(id_max_conf)
        thre = 13200

        th = blurrinesDetection(directories, thre)
        # print(th)

        dup, ogtag = similar(n, sim, rate, page_number, id_max_conf)

        removefiles(dup, 2, page_number, rate)
        # removefiles(th,1,page_number,rate)
        print('Reading Text now')
        text_gen_fresh(page_number, ogtag, rate)
        read_text(page_number, direc)
        #text_reader(page_number)
        control(page_number)
        print("Read that page")
    else:
        page_repeat_path = page_folder
        read_text(page_repeat_path, direc)
        #text_reader(page_number)
        page_flag=control(page_number)
        print("Read the previous page")




    return 'OK'
