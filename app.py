from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Initial Data
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
        body { 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 40px 0;
            color: #333;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .header-text { color: white; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .table thead { background: #f8f9fa; }
        .badge-pass { background: #28a745; color: white; padding: 5px 12px; border-radius: 50px; font-size: 0.8rem; }
        .badge-fail { background: #dc3545; color: white; padding: 5px 12px; border-radius: 50px; font-size: 0.8rem; }
        .btn-add { background: #1e3c72; color: white; border: none; font-weight: 600; }
        .btn-add:hover { background: #2a5298; color: white; }
        .delete-link { color: #dc3545; text-decoration: none; font-weight: 600; }
        .delete-link:hover { text-decoration: underline; }
    </style>
</head>
<body>

<div class="container" style="max-width: 900px;">
    <h1 class="text-center header-text mb-4">Student Management System</h1>

    <div class="glass-card">
        <h4 class="mb-3">Register New Record</h4>
        <form action="/add" method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Full Name</label>
                    <input type="text" name="name" class="form-control" placeholder="Reineth C. Toñada" required>
                </div>
                <div class="col-md-6">
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
                    <input type="text" name="section" class="form-control" placeholder="Zechariah" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Final Grade</label>
                    <input type="number" step="0.01" name="final_grade" class="form-control" placeholder="75.0" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Address</label>
                    <input type="text" name="address" class="form-control" placeholder="Lemery, Iloilo" required>
                </div>
                <div class="col-12 mt-4">
                    <button type="submit" class="btn btn-add w-100 p-2">Add Student to Records</button>
                </div>
            </div>
        </form>
    </div>

    <div class="glass-card">
        <h4 class="mb-3">Student Academic List</h4>
        <div class="table-responsive">
            <table class="table table-hover align-middle">
                <thead>
                    <tr>
                        <th>Name & Address</th>
                        <th>Year/Section</th>
                        <th>Grade</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in student_list %}
                    <tr>
                        <td>
                            <div class="fw-bold">{{ s.name }}</div>
                            <small class="text-muted">{{ s.address }}</small>
                        </td>
                        <td>{{ s.year_level }}<br><span class="small">{{ s.section }}</span></td>
                        <td class="fw-bold">{{ s.final_grade }}</td>
                        <td>
                            {% if s.status == 'Passed' %}
                                <span class="badge-pass">Passed</span>
                            {% else %}
                                <span class="badge-fail">Failed</span>
                            {% endif %}
                        </td>
                        <td>
                            <a href="/delete/{{ loop.index0 }}" class="delete-link" onclick="return confirm('Delete record?')">Delete</a>
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
    # FIXED: Added error handling for grade conversion
    try:
        raw_grade = request.form.get('final_grade')
        grade_val = float(raw_grade) if raw_grade else 0.0
    except ValueError:
        grade_val = 0.0  # Default to 0 if input is not a number

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
