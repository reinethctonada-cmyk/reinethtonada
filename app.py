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
    <title>Student Records | Dark Edition</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --neon-blue: #00d2ff;
            --neon-purple: #9d50bb;
            --passed-glow: #00ff88;
            --failed-glow: #ff4b2b;
        }
        
        body { 
            background: var(--bg-gradient);
            background-attachment: fixed;
            min-height: 100vh;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: #ffffff;
            padding: 60px 0;
        }

        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
            margin-bottom: 40px;
        }

        h2, h3 {
            background: linear-gradient(to right, #00d2ff, #9d50bb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .form-label {
            color: #aaa;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .form-control, .form-select {
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white !important;
            border-radius: 12px;
            padding: 12px;
        }

        .form-control::placeholder { color: #666; }
        .form-control:focus, .form-select:focus {
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--neon-blue);
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
            outline: none;
        }

        .btn-neon {
            background: linear-gradient(45deg, #00d2ff, #9d50bb);
            border: none;
            color: white;
            font-weight: 800;
            border-radius: 15px;
            padding: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(157, 80, 187, 0.4);
        }

        .btn-neon:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(157, 80, 187, 0.6);
            color: white;
        }

        /* Table Styling */
        .table { color: white; border-collapse: separate; border-spacing: 0 12px; }
        .table thead th { border: none; color: #777; font-size: 0.7rem; text-transform: uppercase; }
        
        .student-row {
            background: rgba(255, 255, 255, 0.03);
            transition: all 0.3s ease;
        }
        
        .student-row:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: scale(1.02);
        }

        .student-row td { padding: 20px; border: none; }
        .student-row td:first-child { border-radius: 15px 0 0 15px; }
        .student-row td:last-child { border-radius: 0 15px 15px 0; }

        .badge-passed { 
            color: var(--passed-glow); 
            border: 1px solid var(--passed-glow);
            padding: 5px 15px;
            border-radius: 8px;
            font-weight: 700;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
        }

        .badge-failed { 
            color: var(--failed-glow); 
            border: 1px solid var(--failed-glow);
            padding: 5px 15px;
            border-radius: 8px;
            font-weight: 700;
            box-shadow: 0 0 10px rgba(255, 75, 43, 0.2);
        }

        .delete-btn {
            color: #ff4b2b;
            text-decoration: none;
            font-weight: 700;
            font-size: 0.8rem;
            transition: 0.3s;
        }

        .delete-btn:hover { color: #fff; text-shadow: 0 0 10px #ff4b2b; }
    </style>
</head>
<body>

<div class="container" style="max-width: 950px;">
    <div class="glass-card text-center">
        <h2>Student Data Terminal</h2>
        <p class="text-muted small">SECURE ACADEMIC RECORD MANAGEMENT</p>
        
        <form action="/add" method="POST" class="mt-4 text-start">
            <div class="row g-4">
                <div class="col-md-6">
                    <label class="form-label">FULL NAME</label>
                    <input type="text" name="name" class="form-control" placeholder="Reineth C. Toñada" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">YEAR LEVEL</label>
                    <select name="year_level" class="form-select">
                        <option value="1st Year">1st Year</option>
                        <option value="2nd Year">2nd Year</option>
                        <option value="3rd Year">3rd Year</option>
                        <option value="4th Year">4th Year</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <label class="form-label">SECTION</label>
                    <input type="text" name="section" class="form-control" placeholder="Zechariah" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label">FINAL GRADE</label>
                    <input type="number" step="0.01" name="final_grade" class="form-control" placeholder="0.00" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label">ADDRESS</label>
                    <input type="text" name="address" class="form-control" placeholder="Iloilo, Philippines" required>
                </div>
                <div class="col-12 mt-4">
                    <button type="submit" class="btn btn-neon w-100">INITIALIZE RECORD</button>
                </div>
            </div>
        </form>
    </div>

    <div class="glass-card">
        <h3 class="mb-4">Database Registry</h3>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>STUDENT PROFILE</th>
                        <th>CLASS</th>
                        <th>GRADE</th>
                        <th>RESULT</th>
                        <th class="text-center">TERMINATE</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in student_list %}
                    <tr class="student-row">
                        <td>
                            <div class="fw-bold">{{ s.name }}</div>
                            <div class="small text-muted" style="font-size: 0.7rem;">📍 {{ s.address }}</div>
                        </td>
                        <td>{{ s.year_level }}<br><span class="text-muted small">{{ s.section }}</span></td>
                        <td class="fw-bold text-info">{{ s.final_grade }}</td>
                        <td>
                            {% if s.status == 'Passed' %}
                                <span class="badge-passed">PASSED</span>
                            {% else %}
                                <span class="badge-failed">FAILED</span>
                            {% endif %}
                        </td>
                        <td class="text-center">
                            <a href="/delete/{{ s.id }}" class="delete-btn" onclick="return confirm('Permanently delete record?')">DELETE</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
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
