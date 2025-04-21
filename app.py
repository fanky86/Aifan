from flask import Flask, render_template, request
import subprocess
import os
import urllib.request

app = Flask(__name__)

MODEL_DIR = "model"
MODEL_FILE = "tinyllama.gguf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
MODEL_URL = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

def download_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(MODEL_PATH):
        print("Mengunduh model TinyLLaMA...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model berhasil diunduh!")

@app.route("/", methods=["GET", "POST"])
def index():
    download_model()  # Cek dan unduh model dulu

    response = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        result = subprocess.run([
            "./llama.cpp/build/bin/llama-cli",
            "-m", MODEL_PATH,
            "--prompt", user_input
        ], capture_output=True, text=True)
        response = result.stdout.split(">")[-1].strip()
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
