# Face Recognition System with MySQL Integration

## Overview

This is a Face Recognition System that captures, registers, and recognizes faces using OpenCV, face_recognition, and MySQL for storing face encodings. It allows user identification based on face recognition and displays the name and registration number of recognized users in a real-time video feed.

## Features

Face Detection & Recognition using face_recognition

Stores face encodings in MySQL for scalability

Automatically checks for duplicates before registering a new user

Uses OpenCV to process real-time video feed

Requirements

## Install Dependencies

### I have Provided the conda environment text file.

Ensure you have Python 3.x installed, then run:

pip install opencv-python face-recognition mysql-connector-python numpy

MySQL Setup

Install MySQL and start the server.

## Create the database:

CREATE DATABASE face_recognition_db;

Update the DB_CONFIG in face_recognition.py with your MySQL credentials.

# How to Run

Start MySQL Server

## Run the script

python face_recognition.py

The system will recognize known faces and display their name & registration number.

## Exiting the Program

Press 'q' to exit the video window.

## License

This project is open-source and free to use.

Contributors welcome! Feel free to submit pull requests.
