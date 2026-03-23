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
    <title>GRADE PORTAL | Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --sidebar-bg: #0f172a;
            --main-bg: #f1f5f9;
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --glass: rgba(255, 255, 255, 0.9);
        }

        body { 
            background-color: var(--main-bg);
            color: #1e293b;
            font-family: 'Inter', sans-serif;
            margin: 0;
            display: flex;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 280px;
            height: 100vh;
            background: var(--sidebar-bg);
            color: white;
            padding: 30px 20px;
            position: fixed;
            box-shadow: 4px 0 10px rgba(0,0,0,0.1);
        }

        .brand {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 40px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--accent);
        }

        .main-content {
            margin-left: 280px;
            padding: 40px;
            width: 100%;
        }

        /* Form Card */
        .form-card {
            background: white;
            border-radius: 16px;
            padding: 25px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }

        .form-label { font-weight: 600; font-size: 0.8rem; color: #64748b; text-transform: uppercase; }

        .form-control, .form-select {
            border: 1px solid #e2e8f0;
            padding: 12px;
            border-radius: 10px;
            background: #f8fafc;
        }

        .form-control:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        /* Stats & Table */
        .table-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }

        .table thead {
            background: #f8fafc;
            border-bottom: 2px solid #f1f5f9;
        }

        .table th { padding: 20px; color: #64748b; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; }
        .table td { padding: 20px; vertical-align: middle; border-bottom: 1px solid #f1f5f9; }
        
        .table tbody tr:hover { background-color: #f8fafc; }

        /* Status Badges */
        .badge-custom {
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
        }
        .bg-pass { background: #dcfce7; color: #15803d; }
        .bg-fail { background: #fee2e2; color: #b91c1c; }

        .btn-save {
            background: var(--accent);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-weight: 600;
            transition: 0.3s;
        }

        .btn-save:hover { background: var(--accent-hover); transform: translateY(-2px); color: white; }

        .student-name { font-weight: 700; color: #0f172a; margin-bottom: 2px; }
        .student-meta { font-size: 0.8rem; color: #94a3b8; }
        
        .delete-btn {
            background: #fff1f2;
            color: #e11d48;
            padding: 8px;
            border-radius: 8px;
            text-decoration: none;
            transition: 0.2s;
        }
        .delete-btn:hover { background: #e11d48; color: white; }

    </style>
</head>
<body>

<div class="sidebar">
    <div class="brand">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
        EduTrack Pro
    </div>
    
    <div class="form-card">
        <h6 class="mb-4 fw-bold">Registration</h6>
        <form action="/add" method="POST">
            <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" name="name" class="form-control" placeholder="Juan Dela Cruz" required>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Year</label>
                    <select name="year_level" class="form-select">
                        <option>1st Year</option><option>2nd Year</option>
                        <option>3rd Year</option><option>4th Year</option>
                    </select>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Section</label>
                    <input type="text" name="section" class="form-control" required>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Final Grade</label>
                <input type="number" step="0.01" name="final_grade" class="form-control" required>
            </div>
            <div class="mb-4">
                <label class="form-label">Address</label>
                <textarea name="address" class="form-control" rows="2" required></textarea>
            </div>
            <button type="submit" class="btn btn-save w-100">Add to Records</button>
        </form>
    </div>
</div>

<div class="main-content">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold">Student Directory</h2>
        <span class="text-muted">Total Records: <strong>{{ student_list|length }}</strong></span>
    </div>

    <div class="table-card">
        <table class="table">
            <thead>
                <tr>
                    <th>Student Details</th>
                    <th>Classification</th>
                    <th>Performance</th>
                    <th>Result</th>
                    <th class="text-center">Action</th>
                </tr>
            </thead>
            <tbody>
                {% for s in student_list %}
                <tr>
                    <td>
                        <div class="student-name">{{ s.name }}</div>
                        <div class="student-meta">{{ s.address }}</div>
                    </td>
                    <td>
                        <div class="fw-bold text-dark">{{ s.year_level }}</div>
                        <div class="student-meta">Section {{ s.section }}</div>
                    </td>
                    <td>
                        <div class="fw-bold">{{ s.final_grade }}%</div>
                    </td>
                    <td>
                        <span class="badge-custom {% if s.status == 'Passed' %}bg-pass{% else %}bg-fail{% endif %}">
                            {{ s.status | upper }}
                        </span>
                    </td>
                    <td class="text-center">
                        <a href="/delete/{{ s.id }}" class="delete-btn" onclick="return confirm('Delete this record?')">
                           <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% if not student_list %}
        <div class="text-center p-5 text-muted">
            <p>No student records found. Add a student to get started.</p>
        </div>
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
    student_to_delete = db.session.get(Student, id)
    if student_to_delete:
        db.session.delete(student_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
