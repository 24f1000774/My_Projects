"""
Test script to verify the API functionality
Run this after starting the Flask application
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_course_operations():
    print("Testing Course Operations...")
    
    # Create a course
    course_data = {
        "course_name": "Web Development",
        "course_code": "CS101",
        "course_description": "Introduction to web development"
    }
    
    response = requests.post(f"{BASE_URL}/course", json=course_data)
    print(f"Create Course: {response.status_code}")
    if response.status_code == 201:
        course = response.json()
        course_id = course['course_id']
        print(f"Created course with ID: {course_id}")
        
        # Get the course
        response = requests.get(f"{BASE_URL}/course/{course_id}")
        print(f"Get Course: {response.status_code}")
        
        # Update the course
        update_data = {
            "course_name": "Advanced Web Development",
            "course_code": "CS101",
            "course_description": "Advanced web development topics"
        }
        response = requests.put(f"{BASE_URL}/course/{course_id}", json=update_data)
        print(f"Update Course: {response.status_code}")
        
        return course_id
    
    return None

def test_student_operations():
    print("\nTesting Student Operations...")
    
    # Create a student
    student_data = {
        "roll_number": "21f1000001",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    response = requests.post(f"{BASE_URL}/student", json=student_data)
    print(f"Create Student: {response.status_code}")
    if response.status_code == 201:
        student = response.json()
        student_id = student['student_id']
        print(f"Created student with ID: {student_id}")
        
        # Get the student
        response = requests.get(f"{BASE_URL}/student/{student_id}")
        print(f"Get Student: {response.status_code}")
        
        return student_id
    
    return None

def test_enrollment_operations(student_id, course_id):
    print("\nTesting Enrollment Operations...")
    
    if student_id and course_id:
        # Enroll student in course
        enrollment_data = {"course_id": course_id}
        response = requests.post(f"{BASE_URL}/student/{student_id}/course", json=enrollment_data)
        print(f"Enroll Student: {response.status_code}")
        
        # Get student's courses
        response = requests.get(f"{BASE_URL}/student/{student_id}/course")
        print(f"Get Student Courses: {response.status_code}")
        if response.status_code == 200:
            courses = response.json()
            print(f"Student enrolled in {len(courses)} courses")

def test_error_cases():
    print("\nTesting Error Cases...")
    
    # Test missing course name
    invalid_course = {"course_code": "CS102"}
    response = requests.post(f"{BASE_URL}/course", json=invalid_course)
    print(f"Missing Course Name: {response.status_code}")
    if response.status_code == 400:
        print(f"Error: {response.json()}")
    
    # Test missing student roll number
    invalid_student = {"first_name": "Jane"}
    response = requests.post(f"{BASE_URL}/student", json=invalid_student)
    print(f"Missing Roll Number: {response.status_code}")
    if response.status_code == 400:
        print(f"Error: {response.json()}")

if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the Flask application is running on http://127.0.0.1:5000")
    
    try:
        course_id = test_course_operations()
        student_id = test_student_operations()
        test_enrollment_operations(student_id, course_id)
        test_error_cases()
        print("\nAll tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the Flask app is running.")
