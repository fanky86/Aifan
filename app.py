from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        result = subprocess.run([
            "./llama.cpp/build/bin/llama-cli",
            "-m", "model/tinyllama.gguf",
            "--prompt", user_input
        ], capture_output=True, text=True)
        response = result.stdout.split(">")[-1].strip()
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
