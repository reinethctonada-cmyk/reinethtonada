from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # We pass your personal details directly to the HTML template
    student_data = {
        "name": "Reineth C. Toñada",
        "location": "Brgy. Anobo, Lemery, Iloilo",
        "age": 24,
        "grade": 10,
        "section": "Zechariah"
    }
    return render_template('index.html', student=student_data)

# Keeping your API endpoint functional
@app.route('/api/student')
def get_student_api():
    return jsonify({
        "name": "Reineth C. Toñada",
        "age": 24,
        "location": "Brgy. Anobo, Lemery, Iloilo",
        "grade": 10,
        "section": "Zechariah"
    })

if __name__ == '__main__':
    app.run(debug=True)
