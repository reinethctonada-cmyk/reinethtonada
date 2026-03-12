from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Data storage
students = [
    {
        "name": "Reineth C. Toñada", 
        "year_level": "4th Year", 
        "section": "Zechariah", 
        "address": "Brgy. Anabo, Lemery, Iloilo",
        "final_grade": 85.0,
        "status": "Passed"
    }
]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Portal | Modern UI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --glass: rgba(255, 255, 255, 0.2);
            --glass-heavy: rgba(255, 255, 255, 0.95);
        }
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Inter', -apple-system, sans-serif;
            color: #2d3436;
            padding: 40px 0;
        }
        .glass-card {
            background: var(--glass-heavy);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 2.5rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .header-title {
            color: white;
            font-weight: 800;
            text-shadow: 0 4px 10px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .form-control, .form-select {
            border-radius: 12px;
            border: 1px solid #dfe6e9;
            padding: 12px;
            background: #fdfdfd;
        }
        .form-control:focus {
            box-shadow: 0 0 0 4px rgba(118, 75, 162, 0.2);
            border-color: #764ba2;
        }
        .btn-submit {
            background: linear-gradient(to right, #667eea, #764ba2);
            border: none;
            border-radius: 12px;
            padding: 14px;
            font-weight: 600;
            color: white;
            transition: transform 0.2s;
        }
        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
            color: white;
        }
        .table {
            border-collapse: separate;
            border-spacing: 0 10px;
        }
        .table thead th {
            border: none;
            color: #636e72;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .student-row {
            background: #ffffff;
            transition: all 0.3s ease;
        }
        .student-row td {
            padding: 20px;
            vertical-align: middle;
            border: none;
        }
        .student-row td:first-child { border-radius: 15px 0 0 15px; }
        .student-row td:last-child { border-radius: 0 15px 15px 0; }
        
        .badge-pass { background: #d1f7e8; color: #10ac84; padding: 8px 16px; border-radius: 10px; font-weight: 700; }
        .badge-fail { background: #ffd9d9; color: #ee5253; padding: 8px 16px; border-radius: 10px; font-weight: 700; }
        
        .delete-icon {
            color: #ff7675;
            text-decoration: none;
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 8px;
        }
        .delete-icon:hover {
            background: #fff5f5;
            color: #d63031;
        }
    </style>
</head>
<body>

<div class="container" style="max-width: 900px;">
    <h1 class="text-center header-title">Student Management System</h1>

    <div class="glass-card">
        <h4 class="mb-4" style="color: #2d3436; font-weight: 700;">Add New Record</h4>
        <form action="/add" method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label small fw-bold">FULL NAME</label>
                    <input type="text" name="name" class="form-control" placeholder="Enter name..." required>
                </div>
                <div class="col-md-6">
                    <label class="form-label small fw-bold">YEAR LEVEL</label>
                    <select name="year_level" class="form-select">
                        <option value="1st Year">1st Year</option>
                        <option value="2nd Year">2nd Year</option>
                        <option value="3rd Year">3rd Year</option>
                        <option value="4th Year">4th Year</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <label class="form-label small fw-bold">SECTION</label>
                    <input type="text" name="section" class="form-control" placeholder="e.g., Zechariah" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label small fw-bold">FINAL GRADE</label>
                    <input type="number" step="0.01" name="final_grade" class="form-control" placeholder="0-100" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label small fw-bold">ADDRESS</label>
                    <input type="text" name="address" class="form-control" placeholder="e.g., Lemery, Iloilo" required>
                </div>
                <div class="col-12 mt-4">
                    <button type="submit" class="btn btn-submit w-100">Register Student</button>
                </div>
            </div>
        </form>
    </div>

    <div class="glass-card">
        <h4 class="mb-4" style="color: #2d3436; font-weight: 700;">Academic Records</h4>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Student Details</th>
                        <th>Year & Section</th>
                        <th>Grade</th>
                        <th>Status</th>
                        <th class="text-center">Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in student_list %}
                    <tr class="student-row">
                        <td>
                            <div class="fw-bold" style="color: #2d3436;">{{ s.name }}</div>
                            <div class="small text-muted">{{ s.address }}</div>
                        </td>
                        <td>{{ s.year_level }}<br><span class="text-muted small">{{ s.section }}</span></td>
                        <td class="fw-bold">{{ s.final_grade }}</td>
                        <td>
                            {% if s.status == 'Passed' %}
                                <span class="badge-pass">Passed</span>
                            {% else %}
                                <span class="badge-fail">Failed</span>
                            {% endif %}
                        </td>
                        <td class="text-center">
                            <a href="/delete/{{ loop.index0 }}" class="delete-icon" onclick="return confirm('Remove {{ s.name }}?')">Delete</a>
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
    return render_template_string(HTML_PAGE, student_list=students)

@app.route('/add', methods=['POST'])
def add_student():
    # Capture data
    grade_val = float(request.form.get('final_grade'))
    
    # Passing mark is 75
    status = "Passed" if grade_val >= 75 else "Failed"
    
    new_student = {
        "name": request.form.get('name'),
        "year_level": request.form.get('year_level'),
        "section": request.form.get('section'),
        "address": request.form.get('address'),
        "final_grade": grade_val,
        "status": status
    }
    
    students.append(new_student)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_student(index):
    if 0 <= index < len(students):
        students.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
