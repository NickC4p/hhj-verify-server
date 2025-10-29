from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import smtplib
import random

app = Flask(__name__)
CORS(app)

verification_codes = {}

@app.route('/send_code', methods=['POST'])
def send_code():
    data = request.get_json()
    email = data.get('email')
    code = str(random.randint(10000, 99999))
    verification_codes[email] = code

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(“postcodelab@gmail.com”, "fxsk lgmd nvrv nxwi")
    message = f"Subject: HHJ Verification Code\n\nYour code is: {code}"
    server.sendmail(“postcodelab@gmail.com”, email, message)
    server.quit()

    return jsonify({"success": True, "message": "Email sent successfully"})

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if verification_codes.get(email) == code:
        return jsonify({"verified": True})
    else:
        return jsonify({"verified": False})

# NON serve app.run() se usi Gunicorn
# app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
