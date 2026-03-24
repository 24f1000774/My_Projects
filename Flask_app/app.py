from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, request, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

# Database Models
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String, nullable=False)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_description = db.Column(db.String)
    
    # Relationship with enrollments
    enrollments = db.relationship('Enrollment', backref='course', cascade='all, delete-orphan')

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    
    # Relationship with enrollments
    enrollments = db.relationship('Enrollment', backref='student', cascade='all, delete-orphan')

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    
    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)

# Error handler function
def create_error_response(error_code, message, status_code):
    return {
        "error_code": error_code,
        "error_message": message
    }, status_code

# Course Resource
class CourseAPI(Resource):
    def get(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404)
        
        return {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "course_code": course.course_code,
            "course_description": course.course_description
        }
    
    def put(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404)
        
        data = request.get_json()
        
        # Validation
        if 'course_name' not in data or not data['course_name']:
            return create_error_response("COURSE001", "Course Name is required", 400)
        
        if 'course_code' not in data or not data['course_code']:
            return create_error_response("COURSE002", "Course Code is required", 400)
        
        # Check if course_code is unique (excluding current course)
        existing_course = Course.query.filter(Course.course_code == data['course_code'], Course.course_id != course_id).first()
        if existing_course:
            abort(409)
        
        course.course_name = data['course_name']
        course.course_code = data['course_code']
        course.course_description = data.get('course_description')
        
        db.session.commit()
        
        return {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "course_code": course.course_code,
            "course_description": course.course_description
        }
    
    def delete(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404)
        
        db.session.delete(course)
        db.session.commit()
        return "", 200

class CourseListAPI(Resource):
    def post(self):
        data = request.get_json()
        
        # Validation
        if 'course_name' not in data or not data['course_name']:
            return create_error_response("COURSE001", "Course Name is required", 400)
        
        if 'course_code' not in data or not data['course_code']:
            return create_error_response("COURSE002", "Course Code is required", 400)
        
        # Check if course_code is unique
        existing_course = Course.query.filter_by(course_code=data['course_code']).first()
        if existing_course:
            abort(409)
        
        course = Course(
            course_name=data['course_name'],
            course_code=data['course_code'],
            course_description=data.get('course_description')
        )
        
        db.session.add(course)
        db.session.commit()
        
        return {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "course_code": course.course_code,
            "course_description": course.course_description
        }, 201

# Student Resource
class StudentAPI(Resource):
    def get(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            abort(404)
        
        return {
            "student_id": student.student_id,
            "roll_number": student.roll_number,
            "first_name": student.first_name,
            "last_name": student.last_name
        }
    
    def put(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            abort(404)
        
        data = request.get_json()
        
        # Validation
        if 'roll_number' not in data or not data['roll_number']:
            return create_error_response("STUDENT001", "Roll Number required", 400)
        
        if 'first_name' not in data or not data['first_name']:
            return create_error_response("STUDENT002", "First Name is required", 400)
        
        # Check if roll_number is unique (excluding current student)
        existing_student = Student.query.filter(Student.roll_number == data['roll_number'], Student.student_id != student_id).first()
        if existing_student:
            abort(409)
        
        student.roll_number = data['roll_number']
        student.first_name = data['first_name']
        student.last_name = data.get('last_name')
        
        db.session.commit()
        
        return {
            "student_id": student.student_id,
            "roll_number": student.roll_number,
            "first_name": student.first_name,
            "last_name": student.last_name
        }
    
    def delete(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            abort(404)
        
        db.session.delete(student)
        db.session.commit()
        return "", 200

class StudentListAPI(Resource):
    def post(self):
        data = request.get_json()
        
        # Validation
        if 'roll_number' not in data or not data['roll_number']:
            return create_error_response("STUDENT001", "Roll Number required", 400)
        
        if 'first_name' not in data or not data['first_name']:
            return create_error_response("STUDENT002", "First Name is required", 400)
        
        # Check if roll_number is unique
        existing_student = Student.query.filter_by(roll_number=data['roll_number']).first()
        if existing_student:
            abort(409)
        
        student = Student(
            roll_number=data['roll_number'],
            first_name=data['first_name'],
            last_name=data.get('last_name')
        )
        
        db.session.add(student)
        db.session.commit()
        
        return {
            "student_id": student.student_id,
            "roll_number": student.roll_number,
            "first_name": student.first_name,
            "last_name": student.last_name
        }, 201

# Enrollment Resource
class StudentCourseAPI(Resource):
    def get(self, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            abort(404)
        
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        courses = []
        
        for enrollment in enrollments:
            course = Course.query.filter_by(course_id=enrollment.course_id).first()
            if course:
                courses.append({
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "course_code": course.course_code,
                    "course_description": course.course_description
                })
        
        return courses
    
    def post(self, student_id):
        data = request.get_json()
        
        # Check if student exists
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return create_error_response("ENROLLMENT002", "Student does not exist.", 400)
        
        # Check if course exists
        course_id = data.get('course_id')
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            return create_error_response("ENROLLMENT001", "Course does not exist", 400)
        
        # Check if enrollment already exists
        existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if existing_enrollment:
            abort(409)
        
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        
        return {
            "enrollment_id": enrollment.enrollment_id,
            "student_id": enrollment.student_id,
            "course_id": enrollment.course_id
        }, 201

class StudentCourseDeleteAPI(Resource):
    def delete(self, student_id, course_id):
        # Check if student exists
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            abort(404)
        
        # Find and delete enrollment
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if not enrollment:
            abort(404)
        
        db.session.delete(enrollment)
        db.session.commit()
        return "", 200

# API Routes
api.add_resource(CourseAPI, '/api/course/<int:course_id>')
api.add_resource(CourseListAPI, '/api/course')
api.add_resource(StudentAPI, '/api/student/<int:student_id>')
api.add_resource(StudentListAPI, '/api/student')
api.add_resource(StudentCourseAPI, '/api/student/<int:student_id>/course')
api.add_resource(StudentCourseDeleteAPI, '/api/student/<int:student_id>/course/<int:course_id>')

if __name__ == '__main__':
    app.run()
