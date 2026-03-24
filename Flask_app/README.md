Flask RESTful API

This project implements a RESTful API using Flask-RESTful for managing courses, students, and enrollments.

## Features

### Database Models
- **Course**: course_id, course_name, course_code, course_description
- **Student**: student_id, roll_number, first_name, last_name
- **Enrollment**: enrollment_id, student_id, course_id

### API Endpoints

#### Course Management
- `GET /api/course/{course_id}` - Get course details
- `POST /api/course` - Create new course
- `PUT /api/course/{course_id}` - Update course
- `DELETE /api/course/{course_id}` - Delete course

#### Student Management
- `GET /api/student/{student_id}` - Get student details
- `POST /api/student` - Create new student
- `PUT /api/student/{student_id}` - Update student
- `DELETE /api/student/{student_id}` - Delete student

#### Enrollment Management
- `GET /api/student/{student_id}/course` - Get courses for a student
- `POST /api/student/{student_id}/course` - Enroll student in course
- `DELETE /api/student/{student_id}/course/{course_id}` - Remove enrollment

## Error Handling

The API implements proper error codes as specified:
- COURSE001: Course Name is required
- COURSE002: Course Code is required
- STUDENT001: Roll Number required
- STUDENT002: First Name is required
- ENROLLMENT001: Course does not exist
- ENROLLMENT002: Student does not exist

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. The API will be available at `http://127.0.0.1:5000`

4. Use the database will be automatically created as `api_database.sqlite3`

## Testing

Run the test script to verify API functionality:
```
python test_api.py
```

Make sure the Flask application is running before executing the tests.

## Submission

For assignment submission:
1. Right-click on `app.py`
2. Send to > Compressed (zipped) folder
3. Name the file as `<roll_number>.zip`
4. Submit the zip file
