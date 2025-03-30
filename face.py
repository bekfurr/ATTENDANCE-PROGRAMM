import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import threading
import pandas as pd
from datetime import datetime

# Mavjud funksiyalar (qisqartirilgan shaklda)
def add_face_to_database(name, surname, age, file_path):
    rgb_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image, model="cnn")
    if face_locations:
        encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
        if os.path.exists("face_database.npy"):
            try:
                database = np.load("face_database.npy", allow_pickle=True).item()
            except ValueError:
                database = {}
        else:
            database = {}
        database[name] = {"surname": surname, "age": age, "encoding": encoding}
        np.save("face_database.npy", database)
        print(f"{name} muvaffaqiyatli qo'shildi!")
    else:
        print("Yuz aniqlanmadi.")

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
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        file_path_var.set(file_path)
    root = tk.Tk()
    root.title("O'quvchi qo'shish")
    tk.Label(root, text="Ism:").pack(padx=20, pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(padx=20, pady=5)
    tk.Label(root, text="Familiya:").pack(padx=20, pady=5)
    surname_entry = tk.Entry(root)
    surname_entry.pack(padx=20, pady=5)
    tk.Label(root, text="Yosh:").pack(padx=20, pady=5)
    age_entry = tk.Entry(root)
    age_entry.pack(padx=20, pady=5)
    tk.Label(root, text="Surat:").pack(padx=20, pady=5)
    file_path_var = tk.StringVar()
    tk.Button(root, text="Fayl tanlash", command=select_file).pack(padx=20, pady=5)
    tk.Entry(root, textvariable=file_path_var, state="readonly").pack(padx=20, pady=5)
    tk.Button(root, text="Saqlash", command=save_to_database).pack(padx=20, pady=10)
    tk.Button(root, text="Chiqish", command=root.destroy).pack(padx=20, pady=10)
    root.mainloop()

# Yangilangan davomat funksiyasi
def attendance_system(camera_index):
    global running
    running = True
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Kamera ochilmadi!")
        return
    
    # Bazani yuklash
    try:
        database = np.load("face_database.npy", allow_pickle=True).item()
        print("Baza yuklandi.")
    except FileNotFoundError:
        print("Baza topilmadi. Avval o'quvchilarni qo'shing.")
        cap.release()
        return

    # Davomat uchun ro'yxat
    attendance = {name: {"surname": data["surname"], "age": data["age"], "present": False} 
                 for name, data in database.items()}
    detected_names = set()  # Bir seansda aniqlangan ismlar

    root = tk.Tk()
    root.title("Davomat tizimi")
    
    def stop_program():
        global running
        running = False
        save_attendance(attendance)
        root.destroy()

    tk.Button(root, text="Davomatni yakunlash", command=stop_program).pack(padx=20, pady=20)
    root.protocol("WM_DELETE_WINDOW", stop_program)

    def video_loop():
        while running:
            ret, frame = cap.read()
            if not ret:
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Nomalum"
                color = (0, 0, 255)  # Qizil - aniqlanmaganlar uchun
                status = ""
                for person_name, person_data in database.items():
                    results = face_recognition.compare_faces([person_data["encoding"]], face_encoding, tolerance=0.5)
                    if results[0]:
                        name = person_name
                        if name not in detected_names:
                            attendance[name]["present"] = True
                            detected_names.add(name)
                        # Agar o'quvchi kelgan bo'lsa, yashil rang va "Kelgan" yozuvi
                        if attendance[name]["present"]:
                            color = (0, 255, 0)  # Yashil - kelganlar uchun
                            status = "Kelgan"
                        break
                # Ramka va matnni chizish
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, f"{name} {status}", (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            cv2.imshow('Davomat', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Esc tugmasi
                stop_program()
            root.update()

        cap.release()
        cv2.destroyAllWindows()

    def save_attendance(attendance_data):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"attendance_{timestamp}.xlsx"
        df = pd.DataFrame([
            {"Ism": name, "Familiya": data["surname"], "Yosh": data["age"], "Kelgan": "Ha" if data["present"] else "Yo'q"}
            for name, data in attendance_data.items()
        ])
        df.to_excel(filename, index=False)
        print(f"Davomat {filename} fayliga saqlandi!")

    threading.Thread(target=video_loop, daemon=True).start()
    root.mainloop()

def create_camera_selection_interface():
    def start_attendance():
        camera_index = int(camera_choice.get())
        root.destroy()
        attendance_system(camera_index)
    
    root = tk.Tk()
    root.title("Kamera tanlash")
    tk.Label(root, text="Kamerani tanlang:").pack(padx=20, pady=5)
    camera_choice = tk.StringVar(value="0")
    tk.OptionMenu(root, camera_choice, "0", "1", "2").pack(padx=20, pady=5)
    tk.Button(root, text="Davomatni boshlash", command=start_attendance).pack(padx=20, pady=10)
    tk.Button(root, text="Chiqish", command=root.destroy).pack(padx=20, pady=10)
    root.mainloop()

if __name__ == "__main__":
    print("1. O'quvchi qo'shish uchun - 1")
    print("2. Davomatni boshlash uchun - 2")
    choice = input("Tanlov: ")
    if choice == "1":
        create_database_interface()
    elif choice == "2":
        create_camera_selection_interface()
    else:
        print("Noto'g'ri tanlov!")
