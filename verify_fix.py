"""
Quick test for enrollment functionality to verify fixes
"""

from app import app, db, Course, Student, Enrollment
import json

def test_enrollment_fix():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create a test course
        course = Course(
            course_name="Test Course",
            course_code="TEST101",
            course_description="Test Description"
        )
        db.session.add(course)
        db.session.commit()
        
        # Create a test student
        student = Student(
            roll_number="TEST001",
            first_name="Test",
            last_name="Student"
        )
        db.session.add(student)
        db.session.commit()
        
        print(f"Created course ID: {course.course_id}")
        print(f"Created student ID: {student.student_id}")
        
        # Test enrollment creation
        enrollment = Enrollment(
            student_id=student.student_id,
            course_id=course.course_id
        )
        db.session.add(enrollment)
        db.session.commit()
        db.session.refresh(enrollment)
        
        print(f"Created enrollment ID: {enrollment.enrollment_id}")
        print(f"Enrollment student_id: {enrollment.student_id}")
        print(f"Enrollment course_id: {enrollment.course_id}")
        
        # Test enrollment retrieval
        enrollments = Enrollment.query.filter_by(student_id=student.student_id).all()
        print(f"Found {len(enrollments)} enrollments")
        
        # Cleanup
        db.session.delete(enrollment)
        db.session.delete(student)
        db.session.delete(course)
        db.session.commit()
        
        print("Test completed successfully!")

if __name__ == "__main__":
    test_enrollment_fix()
