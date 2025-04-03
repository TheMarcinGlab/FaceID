import face_recognition
import cv2
from PIL import Image, ImageDraw, ImageFont
import sys
import pandas as pd
import datetime
import pygame
import os
import shutil

# Funkcja do czyszczenia folderu
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    
                    os.unlink(file_path)  
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) 
            except Exception as e:
                print(f"Nie udało się usunąć {file_path}. Powód: {e}")
    else:
        print(f"Folder {folder_path} nie istnieje.")

# Wczytanie danych użytkowników
try:
    ef = pd.read_csv('./DataFiles/User.csv')
except FileNotFoundError:
    print("Plik User.csv nie istnieje.")
    sys.exit(1)

empno = ef["Employee No"].tolist()
firstname = ef["First Name"].tolist()
lastname = ef["Last Name"].tolist()
photolocation = ef["Photo Location"].tolist()
n = len(empno)

# Wczytanie zdjęć i zakodowanie twarzy
emp = []
emp_encod = []
for i in range(n):
    try:
        image = face_recognition.load_image_file(photolocation[i])
        encoding = face_recognition.face_encodings(image)
        if len(encoding) > 0:
            emp.append(image)
            emp_encod.append(encoding[0])
        else:
            print(f"Nie wykryto twarzy w pliku: {photolocation[i]}")
    except Exception as e:
        print(f"Bląd przy wczytywaniu pliku {photolocation[i]}: {e}")

# Rejestracja zdjęcia użytkownika za pomocą kamery
camera = cv2.VideoCapture(0)
for i in range(10):
    return_value, image = camera.read()
    cv2.imwrite(f'./CurrentUser/Employee{i}.png', image)
del(camera)

if not os.path.exists('./CurrentUser/Employee5.png'):
    print("Plik Employee5.png nie istnieje.")
    sys.exit(1)

uk = face_recognition.load_image_file('./CurrentUser/Employee5.png')

# Funkcja identyfikacji pracownika
def identify_employee(photo):
    try:
        encodings = face_recognition.face_encodings(photo)
        if len(encodings) == 0:
            print("Nie wykryto twarzy na zdjęciu.")
            return -1
        uk_encode = encodings[0]
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return -1

    found = face_recognition.compare_faces(emp_encod, uk_encode, tolerance=0.6)
    print(found)

    for i in range(n):
        if found[i]:
            return i
    return -1

# Identyfikacja
emp_index = identify_employee(uk)
print(emp_index)

if emp_index != -1:
    x = str(datetime.datetime.now())
    eno = str(empno[emp_index])
    f = firstname[emp_index]
    l = lastname[emp_index]
    ar = f"\n{eno} {f} {l}  {x}"
    with open("./DataFiles/Attendance.txt", "a") as f:
        f.write(ar)
    print(ar)

# Dodanie opisu do zdjęcia
pil_uk = Image.fromarray(uk)
draw = ImageDraw.Draw(pil_uk)
fnt = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", 60)

if emp_index == -1:
    name = "Face NOT Recognized"
else:
    name = f"{firstname[emp_index]} {lastname[emp_index]}"

x = 100
y = uk.shape[0] - 100
draw.text((x, y), name, font=fnt, fill=(250, 0, 0))
pil_uk.show()

# Czyszczenie folderu tymczasowego
folder_path = "./CurrentUser"
clear_folder(folder_path)