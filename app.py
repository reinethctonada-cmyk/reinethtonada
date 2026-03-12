from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/')
def home():
 return "Welcome to my daxoy!"
@app.route('/student')
def get_student():
 return jsonify({
 "name": "reineth",
 "grade": 10,
 "section": "Zechariah"
 })
