from flask import Flask, jsonify

app = Flask(__name__)

# Modern HTML and CSS stored in a variable
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reineth C. Toñada | Profile</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            text-align: center;
            width: 100%;
            max-width: 400px;
        }
        .profile-img {
            width: 100px;
            height: 100px;
            background: #00d2ff;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.5);
        }
        h1 { font-size: 1.8rem; margin-bottom: 5px; }
        .location { color: #bdc3c7; font-size: 0.9rem; margin-bottom: 25px; }
        .stat-box {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .label { font-size: 0.7rem; text-transform: uppercase; color: #00d2ff; display: block; }
        .value { font-size: 1.1rem; font-weight: 500; }
    </style>
</head>
<body>
    <div class="glass-card">
        <div class="profile-img">R</div>
        <h1>Reineth C. Toñada</h1>
        <p class="location">Brgy. Anabo, Lemery, Iloilo</p>
        
        <div class="stat-box">
            <span class="label">Age</span>
            <span class="value">24 Years Old</span>
        </div>
        
        <div class="row g-2">
            <div class="col-6">
                <div class="stat-box">
                    <span class="label">Grade</span>
                    <span class="value">10</span>
                </div>
            </div>
            <div class="col-6">
                <div class="stat-box">
                    <span class="label">Section</span>
                    <span class="value">Zechariah</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/student')
def get_student():
    return jsonify({
        "name": "Reineth C. Toñada",
        "grade": 10,
        "section": "Zechariah",
        "age": 24,
        "address": "Brgy. Anabo, Lemery, Iloilo"
    })

if __name__ == '__main__':
    app.run(debug=True)
