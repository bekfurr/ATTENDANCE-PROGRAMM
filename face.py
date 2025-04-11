import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import pandas as pd
from datetime import datetime, time, timedelta

class AttendanceApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Davomat Tizimi")
        self.root.configure(bg="#f0f2f5")
        
        self.current_frame = None
        self.database_path = None
        self.running = False
        self.status_text = None
        self.cap = None
        self.deadline = None
        self.late_deadline = None
        
        self.create_main_interface()
        
    def create_main_interface(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.current_frame, text="Davomat Tizimi", 
                 font=("Helvetica", 24, "bold")).pack(pady=20)
        
        btn_frame = ttk.Frame(self.current_frame)
        btn_frame.pack(fill="x", pady=20)
        
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        
        ttk.Button(btn_frame, text="Baza Yaratish",
                  command=self.show_create_database).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Davomat Boshlash",
                  command=self.show_attendance_setup).pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Chiqish",
                  command=self.quit_application).pack(fill="x", pady=5)
        
        ttk.Label(self.current_frame, 
                 text="BEKFURR INC 2025",
                 font=("Arial", 8)).place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def quit_application(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()
        self.root.destroy()

    def show_create_database(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.current_frame, text="Yangi O'quvchi Qo'shish",
                 font=("Helvetica", 18, "bold")).pack(pady=10)
        
        fields = ["Ism", "Familiya", "Otasining ismi", "Fakultet", "Yo'nalish", "Guruh"]
        self.entries = {}
        
        for field in fields:
            frame = ttk.Frame(self.current_frame)
            frame.pack(fill="x", pady=5)
            ttk.Label(frame, text=f"{field}:", width=15).pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(fill="x", expand=True, padx=5)
            self.entries[field.lower().replace("otasining ismi", "father_name")] = entry
        
        db_frame = ttk.Frame(self.current_frame)
        db_frame.pack(fill="x", pady=5)
        ttk.Label(db_frame, text="Baza nomi:", width=15).pack(side="left")
        self.db_name_entry = ttk.Entry(db_frame)
        self.db_name_entry.pack(fill="x", expand=True, padx=5)
        self.db_name_entry.insert(0, "face_database")
        
        file_frame = ttk.Frame(self.current_frame)
        file_frame.pack(fill="x", pady=5)
        ttk.Label(file_frame, text="Suratlar:", width=15).pack(side="left")
        self.file_paths_var = tk.StringVar()
        ttk.Button(file_frame, text="Tanlash",
                  command=self.select_files).pack(side="left", padx=5)
        ttk.Entry(file_frame, textvariable=self.file_paths_var,
                 state="readonly").pack(fill="x", expand=True, padx=5)
        
        ttk.Button(self.current_frame, text="Saqlash",
                  command=self.save_to_database).pack(pady=10)
        ttk.Button(self.current_frame, text="Orqaga",
                  command=self.create_main_interface).pack(pady=5)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_paths:
            self.file_paths_var.set(";".join(file_paths))

    def save_to_database(self):
        name = self.entries["ism"].get()
        surname = self.entries["familiya"].get()
        father_name = self.entries["father_name"].get()
        faculty = self.entries["fakultet"].get()
        direction = self.entries["yo'nalish"].get()
        group = self.entries["guruh"].get()
        file_paths = self.file_paths_var.get().split(";")
        db_name = self.db_name_entry.get().strip() or "face_database"
        
        if not all([name, surname, father_name, faculty, direction, group, file_paths[0]]):
            messagebox.showwarning("Ogohlantirish", "Barcha maydonlarni to'ldiring!")
            return
            
        encodings = []
        for file_path in file_paths:
            rgb_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image, model="cnn")
            if face_locations:
                encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
                encodings.append(encoding)
            else:
                messagebox.showwarning("Ogohlantirish", f"{file_path} faylida yuz aniqlanmadi.")
        
        if not encodings:
            messagebox.showerror("Xato", "Hech bir suratda yuz aniqlanmadi.")
            return
        
        database_path = f"{db_name}.npy"
        database = {}
        if os.path.exists(database_path):
            try:
                database = np.load(database_path, allow_pickle=True).item()
            except:
                pass
                
        database[name] = {
            "surname": surname,
            "father_name": father_name,
            "faculty": faculty,
            "direction": direction,
            "group": group,
            "encodings": encodings
        }
        
        np.save(database_path, database)
        messagebox.showinfo("Muvaffaqiyat", f"{name} {db_name} bazasiga qo'shildi!")
        self.create_main_interface()

    def show_attendance_setup(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.current_frame, text="Davomat Sozlamalari",
                 font=("Helvetica", 18, "bold")).pack(pady=10)
        
    
        db_frame = ttk.Frame(self.current_frame)
        db_frame.pack(fill="x", pady=5)
        ttk.Label(db_frame, text="Baza tanlash:", width=15).pack(side="left")
        self.db_select_var = tk.StringVar()
        ttk.Button(db_frame, text="Fayl tanlash",
                  command=self.select_database).pack(side="left", padx=5)
        ttk.Entry(db_frame, textvariable=self.db_select_var,
                 state="readonly").pack(fill="x", expand=True, padx=5)
    
        cam_frame = ttk.Frame(self.current_frame)
        cam_frame.pack(fill="x", pady=5)
        ttk.Label(cam_frame, text="Kamera:", width=15).pack(side="left")
        self.camera_choice = tk.StringVar()
        cameras = self.detect_available_cameras()
        camera_options = [cam[1] for cam in cameras] + ["IP Camera"]
        self.camera_menu = ttk.OptionMenu(cam_frame, self.camera_choice,
                                       cameras[0][1] if cameras else "Kamera topilmadi",
                                       *camera_options)
        self.camera_menu.pack(fill="x", expand=True, padx=5)
        
    
        ip_frame = ttk.Frame(self.current_frame)
        ip_frame.pack(fill="x", pady=5)
        ttk.Label(ip_frame, text="IP URL:", width=15).pack(side="left")
        self.ip_entry = ttk.Entry(ip_frame)
        self.ip_entry.pack(fill="x", expand=True, padx=5)
        self.ip_entry.config(state="disabled")
        
    
        ttk.Label(self.current_frame, text="Kech qolish chegarasi:", font=("Helvetica", 12, "bold")).pack(pady=5)
        late_deadline_frame = ttk.Frame(self.current_frame)
        late_deadline_frame.pack(fill="x", pady=5)
        
        self.late_deadline_choice = tk.StringVar(value="time")
        ttk.Radiobutton(late_deadline_frame, text="Soat bo'yicha", variable=self.late_deadline_choice, value="time").pack(side="left", padx=5)
        ttk.Radiobutton(late_deadline_frame, text="Taymer bo'yicha", variable=self.late_deadline_choice, value="timer").pack(side="left", padx=5)
        
       
        self.late_time_frame = ttk.Frame(self.current_frame)
        self.late_time_frame.pack(fill="x", pady=5)
        ttk.Label(self.late_time_frame, text="Soat (0-23):", width=15).pack(side="left")
        self.late_hour_entry = ttk.Entry(self.late_time_frame, width=5)
        self.late_hour_entry.pack(side="left", padx=5)
        ttk.Label(self.late_time_frame, text="Daqiqa (0-59):", width=15).pack(side="left")
        self.late_minute_entry = ttk.Entry(self.late_time_frame, width=5)
        self.late_minute_entry.pack(side="left", padx=5)
        
   
        self.late_timer_frame = ttk.Frame(self.current_frame)
        self.late_timer_frame.pack(fill="x", pady=5)
        ttk.Label(self.late_timer_frame, text="Daqiqa:", width=15).pack(side="left")
        self.late_deadline_var = tk.StringVar(value="5")
        ttk.OptionMenu(self.late_timer_frame, self.late_deadline_var, "5", "10", "15", "30").pack(side="left", padx=5)
        

        ttk.Label(self.current_frame, text="Davomat tugash vaqti:", font=("Helvetica", 12, "bold")).pack(pady=5)
        deadline_frame = ttk.Frame(self.current_frame)
        deadline_frame.pack(fill="x", pady=5)
        
        self.deadline_choice = tk.StringVar(value="time")
        ttk.Radiobutton(deadline_frame, text="Soat bo'yicha", variable=self.deadline_choice, value="time").pack(side="left", padx=5)
        ttk.Radiobutton(deadline_frame, text="Taymer bo'yicha", variable=self.deadline_choice, value="timer").pack(side="left", padx=5)
        
    
        self.time_frame = ttk.Frame(self.current_frame)
        self.time_frame.pack(fill="x", pady=5)
        ttk.Label(self.time_frame, text="Soat (0-23):", width=15).pack(side="left")
        self.hour_entry = ttk.Entry(self.time_frame, width=5)
        self.hour_entry.pack(side="left", padx=5)
        ttk.Label(self.time_frame, text="Daqiqa (0-59):", width=15).pack(side="left")
        self.minute_entry = ttk.Entry(self.time_frame, width=5)
        self.minute_entry.pack(side="left", padx=5)
        
  
        self.timer_frame = ttk.Frame(self.current_frame)
        self.timer_frame.pack(fill="x", pady=5)
        ttk.Label(self.timer_frame, text="Daqiqa:", width=15).pack(side="left")
        self.deadline_var = tk.StringVar(value="5")
        ttk.OptionMenu(self.timer_frame, self.deadline_var, "5", "10", "15", "30").pack(side="left", padx=5)
        
   
        ttk.Button(self.current_frame, text="Davomatni Boshlash",
                  command=self.start_attendance).pack(pady=10)
        ttk.Button(self.current_frame, text="Orqaga",
                  command=self.create_main_interface).pack(pady=5)
        
        self.camera_choice.trace("w", self.toggle_ip_entry)
        self.late_deadline_choice.trace("w", self.toggle_late_deadline_input)
        self.deadline_choice.trace("w", self.toggle_deadline_input)
        
        self.toggle_late_deadline_input()
        self.toggle_deadline_input()

    def toggle_ip_entry(self, *args):
        self.ip_entry.config(state="normal" if self.camera_choice.get() == "IP Camera" else "disabled")

    def toggle_late_deadline_input(self, *args):
        if self.late_deadline_choice.get() == "time":
            self.late_time_frame.pack(fill="x", pady=5)
            self.late_timer_frame.pack_forget()
        else:
            self.late_time_frame.pack_forget()
            self.late_timer_frame.pack(fill="x", pady=5)

    def toggle_deadline_input(self, *args):
        if self.deadline_choice.get() == "time":
            self.time_frame.pack(fill="x", pady=5)
            self.timer_frame.pack_forget()
        else:
            self.time_frame.pack_forget()
            self.timer_frame.pack(fill="x", pady=5)

    def select_database(self):
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file_path:
            self.db_select_var.set(file_path)
            self.database_path = file_path

    def detect_available_cameras(self, max_index=3):
        available_cameras = []
        for i in range(max_index):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    available_cameras.append((i, f"Kamera {i} (Indeks: {i})"))
                    cap.release()
            except:
                pass
        return available_cameras

    def start_attendance(self):
        if not self.db_select_var.get():
            messagebox.showwarning("Xato", "Baza tanlanmadi!")
            return
            
        try:
            self.database = np.load(self.db_select_var.get(), allow_pickle=True).item()
        except:
            messagebox.showerror("Xato", "Baza faylini yuklashda xato!")
            return
            
        camera_source = self.camera_choice.get()
        if camera_source == "IP Camera":
            camera_source = self.ip_entry.get().strip()
            if not camera_source:
                messagebox.showwarning("Xato", "IP kamera URL kiritilmadi!")
                return
        else:
            try:
                camera_source = int(camera_source.split(" (Indeks: ")[1].rstrip(")"))
            except:
                messagebox.showerror("Xato", "Kamera tanlashda xato!")
                return


        if self.late_deadline_choice.get() == "time":
            try:
                hour = int(self.late_hour_entry.get())
                minute = int(self.late_minute_entry.get())
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    self.late_deadline = datetime.combine(datetime.now().date(), time(hour, minute))
                    if self.late_deadline < datetime.now():
                        self.late_deadline += timedelta(days=1)
                else:
                    messagebox.showwarning("Xato", "Soat 0-23, daqiqa 0-59 oralig'ida bo'lishi kerak!")
                    return
            except ValueError:
                messagebox.showwarning("Xato", "Soat va daqiqa raqam bo'lishi kerak!")
                return
        else:
            minutes = int(self.late_deadline_var.get())
            self.late_deadline = datetime.now() + timedelta(minutes=minutes)

        if self.deadline_choice.get() == "time":
            try:
                hour = int(self.hour_entry.get())
                minute = int(self.minute_entry.get())
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    self.deadline = datetime.combine(datetime.now().date(), time(hour, minute))
                    if self.deadline < datetime.now():
                        self.deadline += timedelta(days=1)
                else:
                    messagebox.showwarning("Xato", "Soat 0-23, daqiqa 0-59 oralig'ida bo'lishi kerak!")
                    return
            except ValueError:
                messagebox.showwarning("Xato", "Soat va daqiqa raqam bo'lishi kerak!")
                return
        else:
            minutes = int(self.deadline_var.get())
            self.deadline = datetime.now() + timedelta(minutes=minutes)

       
        if self.late_deadline >= self.deadline:
            messagebox.showwarning("Xato", "Kech qolish chegarasi umumiy tugash vaqtidan oldin bo'lishi kerak!")
            return

        self.attendance_system(camera_source)

    def attendance_system(self, camera_source):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.running = True
        self.cap = cv2.VideoCapture(camera_source)
        
        if not self.cap.isOpened():
            messagebox.showerror("Xato", "Kamera ochilmadi!")
            return
            
        self.attendance = {
            name: {
                "surname": data["surname"],
                "father_name": data["father_name"],
                "faculty": data["faculty"],
                "direction": data["direction"],
                "group": data["group"],
                "status": "Kelmagan",
                "arrival_time": None,
                "late_time": None,
                "recorded": False
            } 
            for name, data in self.database.items()
        }
        
        ttk.Label(self.current_frame, text="Davomat Davom Etmoqda...",
                 font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Qolgan vaqtni ko'rsatish uchun label
        self.time_label = ttk.Label(self.current_frame, text="", font=("Helvetica", 12))
        self.time_label.pack(pady=5)
        
        self.status_text = tk.Text(self.current_frame, height=15, width=60)
        self.status_text.pack(pady=10)
        
        ttk.Button(self.current_frame, text="Yakunlash",
                  command=self.stop_attendance).pack(pady=10)
        
        def update_timer():
            while self.running:
                current_time = datetime.now()
                if current_time >= self.deadline:
                    self.stop_attendance()
                    break
                remaining_time = self.deadline - current_time
                minutes, seconds = divmod(remaining_time.seconds, 60)
                self.time_label.config(text=f"Davomat tugashiga qolgan vaqt: {minutes:02d}:{seconds:02d}")
                self.root.update()
                threading.Event().wait(1)

        def video_loop():
            while self.running:
                if not self.cap or not self.cap.isOpened():
                    break
                    
                ret, frame = self.cap.read()
                if not ret:
                    continue
                    
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                
                current_time = datetime.now()
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    name = "Nomalum"
                    color = (0, 0, 255)
                    status = ""
                    for person_name, person_data in self.database.items():
                        results = face_recognition.compare_faces(person_data["encodings"], face_encoding, tolerance=0.5)
                        if any(results):
                            name = person_name
                            if not self.attendance[name]["recorded"]:
                                if current_time <= self.late_deadline:
                                    self.attendance[name]["status"] = "Kelgan"
                                    self.attendance[name]["arrival_time"] = current_time.strftime("%H:%M:%S")
                                else:
                                    self.attendance[name]["status"] = "Kech qolgan"
                                    self.attendance[name]["late_time"] = current_time.strftime("%H:%M:%S")
                                self.attendance[name]["recorded"] = True
                                self.update_status_text(name, self.attendance[name]["status"])
                            status = self.attendance[name]["status"]
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
                    self.stop_attendance()
                try:
                    self.root.update()
                except tk.TclError:
                    self.running = False
                    break
                
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
        
        threading.Thread(target=video_loop, daemon=True).start()
        threading.Thread(target=update_timer, daemon=True).start()

    def update_status_text(self, name, status):
        try:
            if self.status_text and self.running:
                self.status_text.config(state="normal")
                self.status_text.insert(tk.END, f"{name}: {status} ({datetime.now().strftime('%H:%M:%S')})\n")
                self.status_text.config(state="disabled")
                self.status_text.see(tk.END)
        except tk.TclError:
            pass

    def stop_attendance(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.save_attendance()
        self.show_summary()

    def save_attendance(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"attendance_{timestamp}.xlsx"
        df = pd.DataFrame([
            {
                "Ism": name,
                "Familiya": data["surname"],
                "Otasining ismi": data["father_name"],
                "Fakultet": data["faculty"],
                "Yo'nalish": data["direction"],
                "Guruh": data["group"],
                "Holati": data["status"],
                "Kelgan vaqti": data["arrival_time"],
                "Kech qolgan vaqti": data["late_time"]
            }
            for name, data in self.attendance.items()
        ])
        df.to_excel(filename, index=False)

    def show_summary(self):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(self.current_frame, text="Davomat Yakuni",
                 font=("Helvetica", 18, "bold")).pack(pady=10)
        
        summary_text = tk.Text(self.current_frame, height=20, width=60)
        summary_text.pack(pady=10)
        
        summary_text.insert(tk.END, "=== Davomat Yakuni ===\n\n")
        summary_text.insert(tk.END, "Kelganlar:\n")
        for name, data in self.attendance.items():
            if data["status"] == "Kelgan":
                summary_text.insert(tk.END, f"- {name} {data['surname']} {data['father_name']} "
                                          f"({data['faculty']}, {data['direction']}, {data['group']}) - "
                                          f"{data['arrival_time']}\n")
        
        summary_text.insert(tk.END, "\nKech qolganlar:\n")
        for name, data in self.attendance.items():
            if data["status"] == "Kech qolgan":
                summary_text.insert(tk.END, f"- {name} {data['surname']} {data['father_name']} "
                                          f"({data['faculty']}, {data['direction']}, {data['group']}) - "
                                          f"{data['late_time']}\n")
        
        summary_text.insert(tk.END, "\nKelmaganlar:\n")
        for name, data in self.attendance.items():
            if data["status"] == "Kelmagan":
                summary_text.insert(tk.END, f"- {name} {data['surname']} {data['father_name']} "
                                          f"({data['faculty']}, {data['direction']}, {data['group']})\n")
        
        summary_text.config(state="disabled")
        
        ttk.Button(self.current_frame, text="Bosh menyuga",
                  command=self.create_main_interface).pack(pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AttendanceApp()
    app.run()
