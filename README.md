<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">

</head>
<body>

  <h1>📸 Advanced People Attendance System with Face Detection and Scheduling</h1>

  <p>Welcome to the <strong>Advanced People Attendance System</strong> – a powerful and user-friendly Python app that uses <strong>real-time face recognition</strong> to manage attendance, complete with GUI, weekly schedule, and email reporting.</p>

  <h2>🎯 Key Features</h2>
  <ul>
    <li><strong>Face Recognition:</strong> Automatically detects and recognizes faces.</li>
    <li><strong>Manual & Scheduled Modes:</strong> Choose between on-demand or timetable-based attendance.</li>
    <li><strong>Late Detection:</strong> Set late mark rules via clock or countdown timer.</li>
    <li><strong>Excel Reports:</strong> Automatically saves logs as .xlsx files.</li>
    <li><strong>GUI Interface:</strong> Full control through a user-friendly desktop interface.</li>
    <li><strong>Camera Support:</strong> Supports both webcam and IP camera input.</li>
    <li><strong>Email Integration:</strong> Add contacts and email reports directly.</li>
    <li><strong>Schedule Builder:</strong> Define weekly class schedules easily.</li>
  </ul>

  <h2>🛠️ Technology Stack</h2>
  <ul>
    <li><span class="tag">Python</span></li>
    <li><span class="tag">OpenCV</span>, <span class="tag">face_recognition</span>, <span class="tag">NumPy</span>, <span class="tag">Pandas</span>, <span class="tag">Schedule</span></li>
    <li><span class="tag">Tkinter</span> – GUI framework</li>
    <li><span class="tag">SMTP</span> – Email reports</li>
  </ul>

  <h2>🖥️ How to Use</h2>
  <ol>
    <li>Install dependencies:
      <pre><code>pip install opencv-python face_recognition numpy pandas schedule</code></pre>
    </li>
    <li>Run the script:
      <pre><code>python code.py</code></pre>
    </li>
    <li>Use the GUI to:
      <ul>
        <li>Create face database</li>
        <li>Start attendance (manual or schedule-based)</li>
        <li>Send reports via email</li>
      </ul>
    </li>
  </ol>

  <h2>💾 Output</h2>
  <p>Attendance is saved as an Excel file with fields like name, status (present/late/absent), and arrival time.</p>

  <h2>📩 Email Integration</h2>
  <p>Add SMTP credentials and contacts to send attendance reports directly from the app.</p>

  <h2>📅 Weekly Scheduling</h2>
  <p>Set up start time, late time, and end time for each day of the week, and the app will take care of the rest.</p>

  <h2>📂 Project Structure</h2>
  <pre><code>.
├── code.py
├── face_database.npy
├── contacts.json
├── smtp_settings.json
├── attendance_YYYY-MM-DD_HH-MM-SS.xlsx
</code></pre>

  <h2>🏷️ Author</h2>
  <p><strong>BEKFURR INC – 2025</strong><br>This system was created to help automate and simplify the attendance process using AI-powered face recognition.</p>


## License
This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) and [NOTICE](NOTICE) files for details.
</body>
</html>
