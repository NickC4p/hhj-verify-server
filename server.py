from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, random, re

app = Flask(__name__)
CORS(app)

# memorizziamo temporaneamente il codice in memoria
stored_code = None

@app.route("/send-code", methods=["POST"])
def send_code():
    global stored_code
    data = request.get_json()
    email = data.get("email")

    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(success=False, message="Invalid email address.")

    stored_code = str(random.randint(10000, 99999))

    try:
        # Configura qui il tuo SMTP (esempio con Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("postcodelab@gmail.com", "fxsk lgmd nvrv nxwi")
        server.sendmail(
            "your_email@gmail.com",
            email,
            f"Subject: Your HHJ verification code\n\nYour verification code is: {stored_code}"
        )
        server.quit()
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False, message="Failed to send email.")

@app.route("/verify-code", methods=["POST"])
def verify_code():
    global stored_code
    data = request.get_json()
    code = data.get("code")

    if code == stored_code:
        return jsonify(success=True)
    else:
        return jsonify(success=False)

if __name__ == "__main__":
    app.run(debug=True)
