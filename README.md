📸 Advanced People Attendance System with Face Detection and Scheduling
Welcome to the Advanced People Attendance System – a powerful and user-friendly application built with Python and OpenCV that uses real-time face recognition to manage and monitor attendance, complete with a GUI, scheduling features, and email reporting.

🎯 Key Features
Face Recognition-Based Attendance: Accurately recognizes individuals and logs attendance automatically.

Manual and Scheduled Modes: Supports both on-demand and timetable-based attendance sessions.

Late Detection: Defines late time and attendance deadline either via time or timer.

Excel Export: Automatically saves attendance reports as .xlsx files.

GUI (Tkinter): Fully interactive desktop interface with menus for each major feature.

Camera Support: Works with both local webcams and IP cameras.

Contacts & Email Integration: Add contacts and send attendance reports via email.

Schedule Management: Weekly class schedule builder for automated tracking.

🛠️ Tech Stack
Language: Python

Libraries: OpenCV, face_recognition, NumPy, Pandas, Tkinter, Schedule

Others: SMTP for sending emails, JSON for configuration, Excel (via pandas) for reports

🖥️ How to Use
Install Requirements:

bash
Copy
Edit
pip install opencv-python face_recognition numpy pandas schedule
Run the App:

bash
Copy
Edit
python code.py
Main Menu Options:

Create face database with at least 4 images per person.

Start attendance manually or schedule it via built-in timetable.

Set late time and end time (fixed or timer-based).

Send attendance reports directly from the app via email.

💾 Output
Attendance report is automatically saved as .xlsx in the current directory.

Report includes name, faculty, group, status (on time, late, absent), and arrival time.

📩 Email Integration
Add contact emails and configure SMTP settings.

Easily select a report and recipient to send attendance summaries with attachments.

📅 Weekly Scheduling
Customize start, late, and end times for each day of the week.

Automatically runs attendance based on that schedule.

📚 File Structure
pgsql
Copy
Edit
├── code.py
├── face_database.npy
├── contacts.json
├── smtp_settings.json
├── attendance_YYYY-MM-DD_HH-MM-SS.xlsx
🏷️ Author
Bekfurr Inc – 2025
This system was built with the aim to improve institutional attendance tracking using face detection technology and intuitive tools.
