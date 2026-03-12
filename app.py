from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Starting with your data
# Each student now has a 'final_grade' and 'status'
students = [
    {
        "name": "Reineth C. Toñada", 
        "year_level": "4th Year", 
        "section": "Zechariah", 
        "address": "Brgy. Anabo, Lemery, Iloilo",
        "final_grade": 85,
        "status": "Passed"
    }
]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Records</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f8f9fa; font-family: 'Segoe UI', sans-serif; padding: 30px; }
        .glass-card { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px; }
        .status-passed { color: #28a745; font-weight: bold; }
        .status-failed { color: #dc3545; font-weight: bold; }
        .btn-delete { color: #dc3545; text-decoration: none; font-size: 0.9rem; }
        .btn-delete:hover { text-decoration: underline; }
    </style>
</head>
<body>

<div class="container" style="max-width: 800px;">
    <div class="glass-card">
        <h2 class="mb-4">Student Academic Record</h2>
        <form action="/add" method="POST">
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Full Name</label>
                    <input type="text" name="name" class="form-control" required>
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
                    <input type="text" name="section" class="form-control" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Final Grade</label>
                    <input type="number" name="final_grade" class="form-control" placeholder="0-100" required>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Address</label>
                    <input type="text" name="address" class="form-control" required>
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary w-100">Add Record</button>
                </div>
            </div>
        </form>
    </div>

    <div class="glass-card">
        <h3>Current Records</h3>
        <table class="table mt-3">
            <thead>
                <tr>
                    <th>Name</th>
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
                        <strong>{{ s.name }}</strong><br>
                        <small class="text-muted">{{ s.address }}</small>
                    </td>
                    <td>{{ s.year_level }} - {{ s.section }}</td>
                    <td>{{ s.final_grade }}</td>
                    <td>
                        <span class="{{ 'status-passed' if s.status == 'Passed' else 'status-failed' }}">
                            {{ s.status }}
                        </span>
                    </td>
                    <td>
                        <a href="/delete/{{ loop.index0 }}" class="btn-delete" onclick="return confirm('Delete this record?')">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
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
    # Get grade and determine pass/fail
    grade_val = float(request.form.get('final_grade'))
    
    # Simple logic: 75 and above is Passing
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
    # Check if the index exists before popping
    if 0 <= index < len(students):
        students.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
