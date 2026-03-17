from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'student_records.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    final_grade = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #4e54c8;
            --secondary: #8f94fb;
            --danger: #ff7675;
            --success: #55efc4;
            --dark: #2d3436;
        }
        
        body { 
            background: linear-gradient(to right, #4e54c8, #8f94fb);
            min-height: 100vh;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            padding: 50px 0;
            color: var(--dark);
        }

        .main-container {
            max-width: 900px;
            margin: auto;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        h2, h3 {
            font-weight: 800;
            color: #4e54c8;
            letter-spacing: -1px;
        }

        .form-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            font-weight: 700;
            color: #636e72;
            margin-bottom: 8px;
        }

        .form-control, .form-select {
            border-radius: 10px;
            padding: 12px;
            border: 2px solid #eee;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            border-color: var(--secondary);
            box-shadow: none;
        }

        .btn-primary {
            background: linear-gradient(45deg, #4e54c8, #8f94fb);
            border: none;
            border-radius: 12px;
            padding: 15px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: transform 0.2s ease;
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(78, 84, 200, 0.3);
        }

        /* Table Styling */
        .table thead th {
            border: none;
            color: #b2bec3;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
        }

        .student-row {
            background: #fff;
            border-radius: 15px;
            transition: all 0.3s ease;
        }

        .student-row:hover {
            background: #fcfcff;
            transform: scale(1.01);
        }

        .badge-passed {
            background-color: #d1f7e8;
            color: #00b894;
            padding: 8px 15px;
            border-radius: 8px;
            font-weight: 700;
        }

        .badge-failed {
            background-color: #ffeaa7;
            color: #d63031;
            padding: 8px 15px;
            border-radius: 8px;
            font-weight: 700;
        }

        .delete-link {
            background: #fff5f5;
            color: #ff7675;
            padding: 8px 12px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.8rem;
            transition: all 0.2s;
        }

        .delete-link:hover {
            background: #ff7675;
            color: #fff;
        }
    </style>
</head>
<body>

<div class="container main-container">
    <div class="glass-card">
        <h2 class="mb-4 text-center">Student Academic Portal</h2>
        <form action="/add" method="POST">
            <div class="row g-4">
                <div class="col-md-7">
                    <label class="form-label">Full Name</label>
                    <input type="text" name="name" class="form-control" placeholder="Ex: Reineth C. Toñada" required>
                </div>
                <div class="col-md-5">
                    <label class="form-label">Year Level</label>
                    <select name="year_level" class="form-select">
                        <option value="1st Year">1st Year</option>
                        <option value="2nd Year">2nd Year</option>
                        <option value="3rd Year">3rd Year</option>
                        <option value="4th Year">4th Year</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Section</label>
                    <input type="text" name="section" class="form-control" placeholder="Ex: Zechariah" required>
                </div>
                <div class="col-md-3">
                    <label class="form-label">Final Grade</label>
                    <input type="number" step="0.01" name="final_grade" class="form-control" placeholder="0-100" required>
                </div>
                <div class="col-md-5">
                    <label class="form-label">Residential Address</label>
                    <input type="text" name="address" class="form-control" placeholder="Brgy. Anabo, Lemery" required>
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary w-100 mt-2">Submit Record</button>
                </div>
            </div>
        </form>
    </div>

    <div class="glass-card">
        <h3 class="mb-4">Student Records</h3>
        <div class="table-responsive">
            <table class="table align-middle">
                <thead>
                    <tr>
                        <th style="width: 35%;">Name & Address</th>
                        <th>Level/Section</th>
                        <th>Grade</th>
                        <th>Status</th>
                        <th class="text-center">Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in student_list %}
                    <tr class="student-row">
                        <td class="py-3">
                            <div class="fw-bold">{{ s.name }}</div>
                            <div class="text-muted small">📍 {{ s.address }}</div>
                        </td>
                        <td>{{ s.year_level }}<br><span class="text-muted small">{{ s.section }}</span></td>
                        <td class="fw-bold">{{ s.final_grade }}</td>
                        <td>
                            {% if s.status == 'Passed' %}
                                <span class="badge-passed">PASSED</span>
                            {% else %}
                                <span class="badge-failed">FAILED</span>
                            {% endif %}
                        </td>
                        <td class="text-center">
                            <a href="/delete/{{ s.id }}" class="delete-link" onclick="return confirm('Remove this student record?')">Remove</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% if not student_list %}
        <p class="text-center text-muted py-4">No records found. Add your first student above!</p>
        {% endif %}
    </div>
</div>

</body>
</html>
"""

@app.route('/')
def index():
    all_students = Student.query.order_by(Student.id.desc()).all()
    return render_template_string(HTML_PAGE, student_list=all_students)

@app.route('/add', methods=['POST'])
def add_student():
    try:
        grade_val = float(request.form.get('final_grade'))
    except (ValueError, TypeError):
        grade_val = 0.0

    status = "Passed" if grade_val >= 75 else "Failed"
    
    new_student = Student(
        name=request.form.get('name'),
        year_level=request.form.get('year_level'),
        section=request.form.get('section'),
        address=request.form.get('address'),
        final_grade=grade_val,
        status=status
    )
    
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_student(id):
    student_to_delete = Student.query.get(id)
    if student_to_delete:
        db.session.delete(student_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
