from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# This list stores the students you add
students = [
    {"name": "Reineth C. Toñada", "grade": "10", "section": "Zechariah", "address": "Brgy. Anabo, Lemery, Iloilo"}
]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Registry</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
            min-height: 100vh; 
            font-family: 'Segoe UI', sans-serif; 
            padding: 40px 20px;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }
        .student-item {
            background: #ffffff;
            border-left: 5px solid #1e3c72;
            border-radius: 10px;
            margin-bottom: 15px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .btn-primary { background: #1e3c72; border: none; }
        .btn-primary:hover { background: #2a5298; }
        label { font-weight: 600; color: #333; }
    </style>
</head>
<body>

<div class="container" style="max-width: 700px;">
    <div class="glass-card">
        <h2 class="text-center mb-4">Student Entry Form</h2>
        <form action="/add" method="POST">
            <div class="row">
                <div class="col-md-12 mb-3">
                    <label>Full Name</label>
                    <input type="text" name="name" class="form-control" placeholder="Reineth C. Toñada" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label>Grade Level</label>
                    <input type="text" name="grade" class="form-control" placeholder="e.g. 10" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label>Section</label>
                    <input type="text" name="section" class="form-control" placeholder="e.g. Zechariah" required>
                </div>
                <div class="col-md-12 mb-3">
                    <label>Address</label>
                    <input type="text" name="address" class="form-control" placeholder="Brgy. Anabo, Lemery" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary w-100 py-2">Save Student Info</button>
        </form>
    </div>

    <div class="glass-card">
        <h3 class="mb-4">Registered Students</h3>
        {% for s in student_list %}
        <div class="student-item">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0 text-primary">{{ s.name }}</h5>
                <span class="badge bg-secondary">Grade {{ s.grade }} - {{ s.section }}</span>
            </div>
            <p class="mb-0 text-muted mt-1 small">📍 {{ s.address }}</p>
        </div>
        {% endfor %}
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
    # Fetching the data from the form inputs
    new_student = {
        "name": request.form.get('name'),
        "grade": request.form.get('grade'),
        "section": request.form.get('section'),
        "address": request.form.get('address')
    }
    
    # Adding to our temporary list
    students.append(new_student)
    
    # Redirect back to home to see the update
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
