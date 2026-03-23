from flask import Flask, jsonify
import os

app = Flask(__name__)

# Root route — what users see when they visit the app
@app.route("/")
def home():
    return jsonify({
        "message": "Hello from my CI/CD pipeline!",
        "status": "running",
        "version": os.getenv("APP_VERSION", "1.0.0")
    })

# Health check route — used by load balancers and monitoring
@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # 0.0.0.0 makes the app reachable from outside the container
    app.run(host="0.0.0.0", port=5000)