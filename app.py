from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # Ensure these keys match exactly what is in your HTML {{ student.name }} etc.
    student_info = {
        "name": "Reineth C. Toñada",
        "location": "Brgy. Anobo, Lemery, Iloilo",
        "age": 24,
        "grade": 10,
        "section": "Zechariah"
    }
    try:
        return render_template('index.html', student=student_info)
    except Exception as e:
        return f"Error: Could not find index.html in the templates folder. {str(e)}"

@app.route('/student')
def get_student():
    return jsonify({
        "name": "Reineth C. Toñada",
        "grade": 10,
        "section": "Zechariah"
    })

if __name__ == '__main__':
    app.run(debug=True)
