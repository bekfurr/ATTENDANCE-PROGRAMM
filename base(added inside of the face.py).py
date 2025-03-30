import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def add_face_to_database(name, surname, age, file_path):


    rgb_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image, model="cnn")
    if face_locations:
        encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
        
      
        if os.path.exists("face_database.npy"):
            try:
                database = np.load("face_database.npy", allow_pickle=True).item()
            except ValueError:
                print("Baza fayli noto'g'ri formatda. Yangi baza yaratilmoqda.")
                database = {}
        else:
            database = {}

   
        database[name] = {
            "surname": surname,
            "age": age,
            "encoding": encoding
        }
        np.save("face_database.npy", database)
        print(f"{name} muvaffaqiyatli baza qo'shildi!")
    else:
        print("Yuz aniqlanmadi. Suratni tekshiring.")

def create_database_interface():
   
    def save_to_database():
        name = name_entry.get()
        surname = surname_entry.get()
        age = age_entry.get()
        file_path = file_path_var.get()
        
        if name.strip() and surname.strip() and age.strip() and file_path.strip():
            add_face_to_database(name, surname, age, file_path)
        else:
            print("Barcha ma'lumotlar to'ldirilishi kerak!")

    def select_file():
        file_path = filedialog.askopenfilename(title="Suratni tanlang", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        file_path_var.set(file_path)

    root = tk.Tk()
    root.title("Baza yaratish")
    
    tk.Label(root, text="Ismni kiriting:").pack(padx=20, pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(padx=20, pady=5)

    tk.Label(root, text="Familiyani kiriting:").pack(padx=20, pady=5)
    surname_entry = tk.Entry(root)
    surname_entry.pack(padx=20, pady=5)

    tk.Label(root, text="Yoshni kiriting:").pack(padx=20, pady=5)
    age_entry = tk.Entry(root)
    age_entry.pack(padx=20, pady=5)

    tk.Label(root, text="Surat faylini tanlang:").pack(padx=20, pady=5)
    file_path_var = tk.StringVar()
    tk.Button(root, text="Faylni tanlash", command=select_file).pack(padx=20, pady=5)
    tk.Entry(root, textvariable=file_path_var, state="readonly").pack(padx=20, pady=5)

    tk.Button(root, text="Baza qo'shish", command=save_to_database).pack(padx=20, pady=10)
    tk.Button(root, text="Dasturdan chiqish", command=root.destroy).pack(padx=20, pady=10)
    
    root.mainloop()


create_database_interface()
