]

# ATTENDANCE-PROGRAMM

**PEOPLE ATTENDANCE WITH FACE DETECTION**

This project provides a system that automatically records people's attendance using face detection technology.

## Features

* Automatic attendance logging via face recognition
* CUDA-accelerated face detection (if available)
* Attendance notification via SMTP email
* Storage and management of a face database

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bekfurr/ATTENDANCE-PROGRAMM.git
   cd ATTENDANCE-PROGRAMM
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

* To run the basic face recognition and attendance system:

  ```bash
  python face.py
  ```

* If you have a CUDA-compatible GPU, run the accelerated version:

  ```bash
  python face_CUDA.py
  ```

## File Structure

* `face.py` – Main script for face detection and attendance
* `face_CUDA.py` – Accelerated version using CUDA
* `face_database.npy` – Numpy file storing face embeddings
* `contacts.json` – Contact details for notifications
* `smtp_settings.json` – Email server configuration for SMTP
* `requirements.txt` – List of Python dependencies

## License

This project is licensed under the [Apache-2.0 License](https://github.com/bekfurr/ATTENDANCE-PROGRAMM/blob/main/LICENSE).

---
