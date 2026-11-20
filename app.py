
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask CI/CD pipeline!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="127.0.0.1", port=port)
