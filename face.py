import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def add_face_to_database(name, surname, age, file_path):
    """
    Yangi yuz xususiyatini va foydalanuvchi ma'lumotlarini baza fayliga qo'shish.
    """
    # Suratni yuklash va yuz xususiyatlarini aniqlash
    rgb_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image, model="cnn")
    if face_locations:
        encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
        
        # Baza fayli mavjudligini tekshirish
        if os.path.exists("face_database.npy"):
            try:
                database = np.load("face_database.npy", allow_pickle=True).item()
            except ValueError:
                print("Baza fayli noto'g'ri formatda. Yangi baza yaratilmoqda.")
                database = {}
        else:
            database = {}

        # Foydalanuvchi ma'lumotlarini saqlash
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
    """
    Tkinter interfeys orqali foydalanuvchi ma'lumotlarini kiritish va surat faylini tanlash.
    """
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

def real_time_face_comparison(camera_index):
    """
    Real vaqt rejimida yuz taqqoslash funktsiyasi.
    """
    global running
    running = True  # Real vaqt oqimini nazorat qiluvchi flag

    def stop():
        """
        Tkinter interfeysi orqali dasturni to'xtatish uchun tugma funksiyasi.
        """
        global running
        running = False

    # Kamerani ishga tushirish
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Kamera DirectShow backend orqali ishlaydi
    if not cap.isOpened():
        print("Tanlangan kamera ochilmadi!")
        return

    # Baza faylini yuklash
    try:
        database = np.load("face_database.npy", allow_pickle=True).item()
        print("Baza muvaffaqiyatli yuklandi.")
    except FileNotFoundError:
        print("Baza fayli topilmadi. Avval baza yaratish dasturini ishga tushiring.")
        return

    # Tkinter interfeysini yaratish
    root = tk.Tk()
    root.title("Real vaqt dasturi")
    tk.Button(root, text="Dasturdan chiqish", command=stop).pack(padx=20, pady=20)

    # Video oqimi davomiy sikli
    while running:
        ret, frame = cap.read()
        if not ret:
            continue

        # Video oqimini RGB formatga o'tkazish va yuzlarni aniqlash
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Har bir aniqlangan yuzni baza bilan taqqoslash
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "No match"
            color = (0, 0, 255)  # Qizil rang moslik topilmasa
            for person_name, person_data in database.items():
                # Faqat yuz kodirovkasini olish
                person_encoding = person_data["encoding"]
                results = face_recognition.compare_faces([person_encoding], face_encoding, tolerance=0.5)
                if results[0]:
                    name = f"{person_name} ({person_data['surname']}, {person_data['age']} yosh)"
                    color = (0, 255, 0)  # Yashil rang moslik topilsa
                    break
            # Yuz atrofida to'rtburchak va ismni yozish
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Natijani ko'rsatish
        cv2.imshow('Real Time Face Recognition', frame)

        # Esc tugmasi orqali to'xtatish
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Resurslarni bo'shatish
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

def create_camera_selection_interface():
    """
    Tkinter interfeysi orqali kamerani tanlash.
    """
    def start_comparison():
        camera_index = int(camera_choice.get())
        root.destroy()
        real_time_face_comparison(camera_index)

    root = tk.Tk()
    root.title("Kamera tanlash")
    
    tk.Label(root, text="Kamerani tanlang:").pack(padx=20, pady=5)
    camera_choice = tk.StringVar(value="0")  # Default qiymat - kamera 0
    camera_options = tk.OptionMenu(root, camera_choice, "0", "1", "2")  # Kamera indekslari
    camera_options.pack(padx=20, pady=5)

    tk.Button(root, text="Boshlash", command=start_comparison).pack(padx=20, pady=10)
    tk.Button(root, text="Dasturdan chiqish", command=root.destroy).pack(padx=20, pady=10)

    root.mainloop()

# Tkinter interfeysini ishga tushirish
create_camera_selection_interface()
