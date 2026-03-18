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
    <title>Quantum Records | Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

        :root {
            --accent: #00f2ff;
            --secondary: #7000ff;
            --bg-dark: #0a0b10;
            --card-bg: rgba(20, 22, 35, 0.8);
        }

        body { 
            background: radial-gradient(circle at top right, #1a1b2e, #0a0b10);
            color: #e0e0e0;
            font-family: 'Rajdhani', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated Background Mesh */
        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
            opacity: 0.1;
            z-index: -1;
        }

        .header-section {
            padding: 40px 0;
            text-align: center;
        }

        h2 {
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 5px;
            color: var(--accent);
            text-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
        }

        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            margin-bottom: 30px;
        }

        .form-label {
            font-weight: 700;
            color: var(--accent);
            font-size: 0.8rem;
            margin-bottom: 8px;
        }

        .form-control, .form-select {
            background: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff !important;
            border-radius: 8px;
            transition: 0.3s;
        }

        .form-control:focus {
            border-color: var(--accent);
            box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
        }

        .btn-submit {
            background: linear-gradient(90deg, var(--secondary), var(--accent));
            border: none;
            color: white;
            font-weight: 700;
            letter-spacing: 2px;
            padding: 12px;
            border-radius: 8px;
            width: 100%;
            transition: 0.4s;
        }

        .btn-submit:hover {
            filter: brightness(1.2);
            box-shadow: 0 0 20px rgba(112, 0, 255, 0.4);
            transform: translateY(-2px);
        }

        /* Custom Table Styling */
        .table { color: #fff; vertical-align: middle; }
        .table thead th { 
            background: rgba(255, 255, 255, 0.05);
            border: none;
            color: #888;
            font-size: 0.75rem;
            letter-spacing: 1px;
        }
        
        .student-row { border-bottom: 1px solid rgba(255, 255, 255, 0.05); transition: 0.3s; }
        .student-row:hover { background: rgba(0, 242, 255, 0.03); }

        .status-pill {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }

        .status-passed { background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid #00ff88; }
        .status-failed { background: rgba(255, 75, 43, 0.1); color: #ff4b2b; border: 1px solid #ff4b2b; }

        .action-icon {
            color: #555;
            transition: 0.3s;
            text-decoration: none;
        }

        .action-icon:hover { color: #ff4b2b; }

    </style>
</head>
<body>

<div class="container">
    <div class="header-section">
        <h2><i class="fas fa-microchip me-2"></i>Quantum System</h2>
        <p class="text-muted">ENCRYPTED STUDENT DATABASE v2.0.6</p>
    </div>

    <div class="row">
        <div class="col-lg-4">
            <div class="glass-card">
                <h4 class="mb-4 text-white"><i class="fas fa-plus-circle me-2"></i>New Entry</h4>
                <form action="/add" method="POST">
                    <div class="mb-3">
                        <label class="form-label">STUDENT NAME</label>
                        <input type="text" name="name" class="form-control" placeholder="e.g. John Doe" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">YEAR LEVEL</label>
                        <select name="year_level" class="form-select">
                            <option value="1st Year">1st Year</option>
                            <option value="2nd Year">2nd Year</option>
                            <option value="3rd Year">3rd Year</option>
                            <option value="4th Year">4th Year</option>
                        </select>
                    </div>
                    <div class="row">
                        <div class="col-6 mb-3">
                            <label class="form-label">SECTION</label>
                            <input type="text" name="section" class="form-control" placeholder="A-1" required>
                        </div>
                        <div class="col-6 mb-3">
                            <label class="form-label">GRADE</label>
                            <input type="number" step="0.01" name="final_grade" class="form-control" placeholder="0.0" required>
                        </div>
                    </div>
                    <div class="mb-4">
                        <label class="form-label">LOCATION/ADDRESS</label>
                        <input type="text" name="address" class="form-control" placeholder="City, Country" required>
                    </div>
                    <button type="submit" class="btn btn-submit">COMMIT TO CLOUD</button>
                </form>
            </div>
        </div>

        <div class="col-lg-8">
            <div class="glass-card">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h4 class="mb-0 text-white"><i class="fas fa-database me-2"></i>Active Records</h4>
                    <span class="badge bg-dark text-info border border-info">{{ student_list|length }} ENTRIES</span>
                </div>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>IDENTIFIER</th>
                                <th>CLASS</th>
                                <th>SCORE</th>
                                <th>STATUS</th>
                                <th class="text-end">ACTION</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for s in student_list %}
                            <tr class="student-row">
                                <td>
                                    <div class="fw-bold">{{ s.name }}</div>
                                    <div class="text-muted" style="font-size: 0.7rem;"><i class="fas fa-map-marker-alt me-1"></i>{{ s.address }}</div>
                                </td>
                                <td>
                                    <div class="small">{{ s.year_level }}</div>
                                    <div class="text-info small" style="font-size: 0.7rem;">{{ s.section }}</div>
                                </td>
                                <td class="fw-bold">{{ s.final_grade }}</td>
                                <td>
                                    {% if s.status == 'Passed' %}
                                        <span class="status-pill status-passed">PASSED</span>
                                    {% else %}
                                        <span class="status-pill status-failed">FAILED</span>
                                    {% endif %}
                                </td>
                                <td class="text-end">
                                    <a href="/delete/{{ s.id }}" class="action-icon" onclick="return confirm('Wipe data?')">
                                        <i class="fas fa-trash-alt"></i>
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
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
    student_to_delete = db.session.get(Student, id)
    if student_to_delete:
        db.session.delete(student_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
