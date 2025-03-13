import cv2
import face_recognition
import numpy as np
import mysql.connector
import time
import pickle

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Change to your MySQL username
    "password": "password",  # Change to your MySQL password
    "database": "face_recognition_db"
}

# Connect to MySQL Database
def connect_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reg_number VARCHAR(50) UNIQUE,
            name VARCHAR(255),
            face_encoding BLOB
        )
    """)
    conn.commit()
    return conn, cursor

# Load registered faces from MySQL
def load_registered_faces():
    conn, cursor = connect_db()
    cursor.execute("SELECT reg_number, name, face_encoding FROM users")
    known_encodings = {}
    reg_numbers = {}
    
    for reg_number, name, enc_blob in cursor.fetchall():
        known_encodings[name] = pickle.loads(enc_blob)
        reg_numbers[name] = reg_number
    
    conn.close()
    return known_encodings, reg_numbers

# Check if face is already registered
def is_duplicate_face(new_encoding, known_encodings):
    for name, encodings in known_encodings.items():
        matches = face_recognition.compare_faces(encodings, new_encoding, tolerance=0.35)
        if any(matches):
            return name  # Return the existing name
    return None

# Save new face in MySQL
def save_new_face(known_encodings):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("Capturing multiple frames for better accuracy. Look at the camera...")
    encodings = []
    
    for _ in range(5):  # Capture 5 frames
        ret, frame = cap.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=2)
        
        if face_encodings:
            existing_name = is_duplicate_face(face_encodings[0], known_encodings)
            if existing_name:
                print(f"Face already registered under '{existing_name}'. Registration aborted.")
                cap.release()
                return False
            encodings.append(face_encodings[0])
        
        time.sleep(0.5)  # Pause between captures
    
    cap.release()
    
    if encodings:
        reg_number = input("Enter registration number: ")
        name = input("Enter name for the new face: ")
        conn, cursor = connect_db()
        cursor.execute("INSERT INTO users (reg_number, name, face_encoding) VALUES (%s, %s, %s)", (reg_number, name, pickle.dumps(encodings)))
        conn.commit()
        conn.close()
        
        print(f"New face encodings saved for {name} with Registration Number: {reg_number}")
        return True
    else:
        print("No face detected. Try again.")
        return False

# Recognize face from the camera
def recognize_face(frame, known_encodings, reg_numbers):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=2)
    
    for face_encoding, face_location in zip(face_encodings, face_locations):
        name = is_duplicate_face(face_encoding, known_encodings) or "Unknown"
        
        if name == "Unknown":
            print("New face detected. Registering...")
            success = save_new_face(known_encodings)
            return success
        else:
            print(f"Face recognized: {name}, Registration Number: {reg_numbers[name]}")
            return True
    return False

# Main function
def main():
    known_encodings, reg_numbers = load_registered_faces()
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        success = recognize_face(frame, known_encodings, reg_numbers)
        
        if success:
            break  # Exit after recognizing or registering a face
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()