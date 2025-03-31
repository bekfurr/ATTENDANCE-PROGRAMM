import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import pandas as pd
from datetime import datetime, time, timedelta

def add_face_to_database(name, surname, group, file_path):
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
        database[name] = {"surname": surname, "group": group, "encoding": encoding}
        np.save("face_database.npy", database)
        messagebox.showinfo("Muvaffaqiyat", f"{name} muvaffaqiyatli qo'shildi!")
    else:
        messagebox.showerror("Xato", "Yuz aniqlanmadi.")

def create_database_interface():
    def save_to_database():
        name = name_entry.get()
        surname = surname_entry.get()
        group = group_entry.get()
        file_path = file_path_var.get()
        if name.strip() and surname.strip() and group.strip() and file_path.strip():
            add_face_to_database(name, surname, group, file_path)
        else:
            messagebox.showwarning("Ogohlantirish", "Barcha ma'lumotlar to'ldirilishi kerak!")
    
    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        file_path_var.set(file_path)
    
    root = tk.Tk()
    root.geometry("300x450")
    root.title("O'quvchi qo'shish")
    tk.Label(root, text="Ism:").pack(padx=20, pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(padx=20, pady=5)
    tk.Label(root, text="Familiya:").pack(padx=20, pady=5)
    surname_entry = tk.Entry(root)
    surname_entry.pack(padx=20, pady=5)
    tk.Label(root, text="Guruh:").pack(padx=20, pady=5)
    group_entry = tk.Entry(root)
    group_entry.pack(padx=20, pady=5)
    tk.Label(root, text="Surat:").pack(padx=20, pady=5)
    file_path_var = tk.StringVar()
    tk.Button(root, text="Fayl tanlash", command=select_file).pack(padx=20, pady=5)
    tk.Entry(root, textvariable=file_path_var, state="readonly").pack(padx=20, pady=5)
    tk.Button(root, text="Saqlash", command=save_to_database).pack(padx=20, pady=10)
    tk.Button(root, text="Chiqish", command=root.destroy).pack(padx=20, pady=10)
    root.mainloop()

def get_camera_name(index):
 
    try:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            name = f"Kamera {index}"
            cap.release()
            return f"{name} (Indeks: {index})"
        cap.release()
    except Exception as e:
        print(f"Kamera {index} ni tekshirishda xato: {e}")
    return None

def detect_available_cameras(max_index=3):
    
    available_cameras = []
    for i in range(max_index):
        camera_name = get_camera_name(i)
        if camera_name:
            available_cameras.append((i, camera_name))
    return available_cameras

def get_deadline():
    deadline = None

    def set_deadline_by_time():
        nonlocal deadline
        try:
            hour = int(hour_entry.get())
            minute = int(minute_entry.get())
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                deadline = datetime.combine(datetime.now().date(), time(hour, minute))
                root.destroy()
            else:
                messagebox.showwarning("Xato", "Soat 0-23, daqiqa 0-59 oralig'ida bo'lishi kerak!")
        except ValueError:
            messagebox.showwarning("Xato", "Soat va daqiqa raqam bo'lishi kerak!")

    def set_deadline_by_timer():
        nonlocal deadline
        minutes = int(timer_choice.get())
        deadline = datetime.now() + timedelta(minutes=minutes)
        root.destroy()

    root = tk.Tk()
    root.geometry("300x400")
    root.title("Davomat vaqtini belgilash")
    tk.Label(root, text="Ma'lum soatgacha:").pack(padx=20, pady=5)
    tk.Label(root, text="Soat (0-23):").pack(padx=20, pady=5)
    hour_entry = tk.Entry(root)
    hour_entry.pack(padx=20, pady=5)
    tk.Label(root, text="Daqiqa (0-59):").pack(padx=20, pady=5)
    minute_entry = tk.Entry(root)
    minute_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Soatni tasdiqlash", command=set_deadline_by_time).pack(padx=20, pady=10)
    tk.Label(root, text="Yoki taymer (daqiqa):").pack(padx=20, pady=5)
    timer_choice = tk.StringVar(value="5")
    tk.OptionMenu(root, timer_choice, "5", "10", "15").pack(padx=20, pady=5)
    tk.Button(root, text="Taymerni tasdiqlash", command=set_deadline_by_timer).pack(padx=20, pady=10)
    tk.Button(root, text="Chiqish", command=root.destroy).pack(padx=20, pady=10)
    root.mainloop()
    return deadline if deadline else datetime.now() + timedelta(minutes=5)

def create_camera_selection_interface():
    def start_attendance():
        selected_option = camera_choice.get()
        ip_url = None
        if selected_option == "IP Camera":
            ip_url = ip_entry.get().strip()
            if not ip_url:
                messagebox.showwarning("Xato", "IP kamera URL kiritilmadi!")
                return
        root.destroy()
        if selected_option == "IP Camera":
            attendance_system(ip_url)
        else:
            try:
                camera_index = int(selected_option.split(" (Indeks: ")[1].rstrip(")"))
                attendance_system(camera_index)
            except Exception as e:
                messagebox.showerror("Xato", f"Kamera tanlashda xato: {e}")

    root = tk.Tk()
    root.geometry("400x450")
    root.title("Kamera tanlash")

    available_cameras = detect_available_cameras()
    if not available_cameras:
        messagebox.showwarning("Ogohlantirish", "Hech qanday kamera topilmadi!")
        available_cameras = [(0, "Standart kamera (Indeks: 0)")]

    tk.Label(root, text="Kamerani tanlang:").pack(padx=20, pady=5)
    camera_choice = tk.StringVar(value=available_cameras[0][1])
    camera_options = [cam[1] for cam in available_cameras] + ["IP Camera"]
    tk.OptionMenu(root, camera_choice, *camera_options).pack(padx=20, pady=5)

    tk.Label(root, text="Agar IP Camera tanlansa, URL kiriting:").pack(padx=20, pady=5)
    tk.Label(root, text="Masalan: http://192.168.1.100:4747/video").pack(padx=20, pady=5)
    ip_entry = tk.Entry(root, width=40)
    ip_entry.pack(padx=20, pady=5)
    ip_entry.insert(0, "")

    tk.Button(root, text="Davomatni boshlash", command=start_attendance).pack(padx=20, pady=10)
    tk.Button(root, text="Chiqish", command=root.destroy).pack(padx=20, pady=10)

    def toggle_ip_entry(*args):
        if camera_choice.get() == "IP Camera":
            ip_entry.config(state="normal")
        else:
            ip_entry.config(state="disabled")
    
    camera_choice.trace("w", toggle_ip_entry)
    ip_entry.config(state="disabled")

    root.mainloop()

def attendance_system(camera_source):
    global running
    running = True
    
    if isinstance(camera_source, str):
        print(f"IP kamera URL: {camera_source}")
        cap = cv2.VideoCapture(camera_source)
    else:
        print(f"Kamera indeksi: {camera_source}")
        cap = cv2.VideoCapture(camera_source)
    
    if not cap.isOpened():
        messagebox.showerror("Xato", "Kamera ochilmadi! URL yoki indeksni tekshiring.")
        return
    
    try:
        database = np.load("face_database.npy", allow_pickle=True).item()
        messagebox.showinfo("Muvaffaqiyat", "Baza yuklandi.")
    except FileNotFoundError:
        messagebox.showerror("Xato", "Baza topilmadi. Avval o'quvchilarni qo'shing.")
        cap.release()
        return

    deadline_datetime = get_deadline()
    attendance = {name: {"surname": data["surname"], "group": data["group"], "status": "Kelmagan", 
                         "arrival_time": None, "late_time": None} 
                  for name, data in database.items()}

    root = tk.Tk()
    root.geometry("500x100")
    root.title("Davomat tizimi")
    
    def stop_program():
        global running
        running = False
        save_attendance(attendance)
        root.destroy()
        display_summary(attendance)

    tk.Button(root, text="Davomatni yakunlash", command=stop_program).pack(padx=20, pady=20)
    root.protocol("WM_DELETE_WINDOW", stop_program)

    def video_loop():
        while running:
            ret, frame = cap.read()
            if not ret:
                print("Kadr olishda xato yuz berdi.")
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            current_time = datetime.now()
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "Nomalum"
                color = (0, 0, 255)
                status = ""
                for person_name, person_data in database.items():
                    results = face_recognition.compare_faces([person_data["encoding"]], face_encoding, tolerance=0.5)
                    if results[0]:
                        name = person_name
                        if attendance[name]["status"] == "Kelmagan":
                            if current_time <= deadline_datetime:
                                attendance[name]["status"] = "Kelgan"
                                attendance[name]["arrival_time"] = current_time.strftime("%H:%M:%S")
                            else:
                                attendance[name]["status"] = "Kech qolgan"
                                attendance[name]["late_time"] = current_time.strftime("%H:%M:%S")
                        status = attendance[name]["status"]
                        if status == "Kelgan":
                            color = (0, 255, 0)
                        elif status == "Kech qolgan":
                            color = (255, 165, 0)
                        break
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, f"{name} ({status})", (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            cv2.imshow('Davomat', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                stop_program()
            root.update()

        cap.release()
        cv2.destroyAllWindows()

    def save_attendance(attendance_data):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"attendance_{timestamp}.xlsx"
        df = pd.DataFrame([
            {"Ism": name, "Familiya": data["surname"], "Guruh": data["group"], "Holati": data["status"],
             "Kelgan vaqti": data["arrival_time"], "Kech qolgan vaqti": data["late_time"]}
            for name, data in attendance_data.items()
        ])
        df.to_excel(filename, index=False)
        messagebox.showinfo("Muvaffaqiyat", f"Davomat {filename} fayliga saqlandi!")

    def display_summary(attendance_data):
        summary_window = tk.Tk()
        summary_window.title("Davomat yakuni")
        
        summary_text = tk.Text(summary_window, height=20, width=60)
        summary_text.pack(padx=10, pady=10)
        
        summary_text.insert(tk.END, "=== Davomat yakuni ===\n\n")
        summary_text.insert(tk.END, "Kelganlar:\n")
        for name, data in attendance_data.items():
            if data["status"] == "Kelgan":
                summary_text.insert(tk.END, f"- {name} {data['surname']} ({data['group']}) - {data['arrival_time']}\n")
        
        summary_text.insert(tk.END, "\nKech qolganlar:\n")
        for name, data in attendance_data.items():
            if data["status"] == "Kech qolgan":
                summary_text.insert(tk.END, f"- {name} {data['surname']} ({data['group']}) - {data['late_time']}\n")
        
        summary_text.insert(tk.END, "\nKelmaganlar:\n")
        for name, data in attendance_data.items():
            if data["status"] == "Kelmagan":
                summary_text.insert(tk.END, f"- {name} {data['surname']} ({data['group']})\n")
        
        summary_text.insert(tk.END, "=====================\n")
        summary_text.config(state="disabled")
        
        tk.Button(summary_window, text="Yopish", command=summary_window.destroy).pack(pady=10)
        summary_window.mainloop()

    threading.Thread(target=video_loop, daemon=True).start()
    root.mainloop()

def main_interface():
    def select_option():
        choice = choice_var.get()
        root.destroy()
        if choice == "1":
            create_database_interface()
        elif choice == "2":
            create_camera_selection_interface()
        else:
            messagebox.showwarning("Xato", "Noto'g'ri tanlov!")
    
    root = tk.Tk()
    root.geometry("300x350")
    root.title("Davomat dasturi")
    
    tk.Label(root, text="Tanlov qiling:").pack(padx=20, pady=10)
    choice_var = tk.StringVar(value="")
    tk.Radiobutton(root, text="1. O'quvchi qo'shish", variable=choice_var, value="1").pack(padx=20, pady=5)
    tk.Radiobutton(root, text="2. Davomatni boshlash", variable=choice_var, value="2").pack(padx=20, pady=5)
    tk.Button(root, text="Tasdiqlash", command=select_option).pack(padx=20, pady=10)
    tk.Button(root, text="Chiqish", command=root.destroy).pack(padx=20, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main_interface()
