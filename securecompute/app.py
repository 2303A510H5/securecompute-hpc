from flask import Flask, render_template, request, send_file
import hashlib
import base64
import datetime
import time
import numpy as np
import multiprocessing as mp
import random
import io
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# ============================================================
# ENCRYPTION MODULE
# ============================================================

class SecureEncryptor:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()

    def encrypt(self, data):
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(encrypted).decode()

encryptor = SecureEncryptor("UltraSecureKey2026")

# ============================================================
# AI THREAT MODEL
# ============================================================

class AIThreatModel:
    def __init__(self):
        self.model = LogisticRegression()
        self.train()

    def train(self):
        X = np.array([
            [0,10,0],[1,20,0],[2,30,0],
            [3,80,1],[4,120,1],[5,200,1],[6,300,1]
        ])
        y = np.array([0,0,0,1,1,1,1])
        self.model.fit(X,y)

    def predict(self, features):
        pred = self.model.predict([features])[0]
        prob = self.model.predict_proba([features])[0][1]
        return pred, round(prob,3)

ai_model = AIThreatModel()

# ============================================================
# MODEL ACCURACY EVALUATION
# ============================================================

def evaluate_model(ai_model, n=200):
    correct = 0

    for _ in range(n):
        failed = random.randint(0,6)
        rate = random.randint(10,300)
        unauthorized = random.randint(0,1)

        true_label = 1 if (failed > 2 or rate > 100 or unauthorized == 1) else 0
        pred, _ = ai_model.predict([failed, rate, unauthorized])

        if pred == true_label:
            correct += 1

    return round((correct/n)*100,2)

# ============================================================
# RISK ENGINE
# ============================================================

class RiskEngine:
    def __init__(self):
        self.threshold = 75

    def calculate(self, failed, rate, unauthorized):
        return (0.4*failed*10 + 0.3*rate + 0.3*unauthorized*100)

    def high_risk(self, score):
        return score > self.threshold

risk_engine = RiskEngine()

# ============================================================
# ADAPTIVE SELF-HEALING SYSTEM
# ============================================================

class SelfHealing:
    def __init__(self):
        self.nodes = {
            "Node1": 0,
            "Node2": 0,
            "Node3": 0,
            "Node4": 0
        }
        self.isolated = None
        self.safe_cycles = 0

    def update_health(self, risk_score):
        for node in self.nodes:
            anomaly = random.randint(0, 100)
            self.nodes[node] = anomaly + risk_score

    def detect_infected(self):
        if not self.nodes:
            return None
        infected = max(self.nodes, key=self.nodes.get)
        if self.nodes[infected] > 120:
            return infected
        return None

    def isolate(self, node):
        if node in self.nodes:
            self.isolated = node
            del self.nodes[node]
            self.safe_cycles = 0

    def recover(self):
        if self.isolated:
            self.nodes[self.isolated] = 0
            self.isolated = None

    def monitor_recovery(self, high_risk):
        if not high_risk:
            self.safe_cycles += 1
        else:
            self.safe_cycles = 0

        if self.safe_cycles >= 3:
            self.recover()

    def active_nodes(self):
        return list(self.nodes.keys())

healing = SelfHealing()

# ============================================================
# BLOCKCHAIN LOGGER
# ============================================================

class BlockchainLogger:
    def __init__(self):
        self.chain = []
        self.add_block("Genesis")

    def add_block(self,data):
        prev_hash = self.chain[-1]["hash"] if self.chain else "0"
        timestamp = str(datetime.datetime.now())
        block_hash = hashlib.sha256((timestamp+data+prev_hash).encode()).hexdigest()
        self.chain.append({
            "timestamp":timestamp,
            "data":data,
            "hash":block_hash
        })

logger = BlockchainLogger()

# ============================================================
# MULTIPROCESSING HPC
# ============================================================

def worker(chunk):
    A_chunk, B = chunk
    return np.dot(A_chunk,B)

def run_hpc():
    size = 300
    A = np.random.rand(size,size)
    B = np.random.rand(size,size)

    cores = mp.cpu_count()
    chunks = np.array_split(A,cores)
    pool = mp.Pool(cores)

    start = time.time()
    pool.map(worker,[(chunk,B) for chunk in chunks])
    pool.close()
    pool.join()
    end = time.time()

    return round(end-start,4)

# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_pipeline():

    failed = int(request.form["failed"])
    rate = int(request.form["rate"])
    unauthorized = int(request.form["unauthorized"])

    # AI Prediction
    prediction, prob = ai_model.predict([failed,rate,unauthorized])

    # Accuracy
    accuracy = evaluate_model(ai_model)

    # Risk
    risk_score = risk_engine.calculate(failed,rate,unauthorized)
    high_risk = risk_engine.high_risk(risk_score)

    # Adaptive Node Monitoring
    healing.update_health(risk_score)

    infected_node = healing.detect_infected()
    if infected_node:
        healing.isolate(infected_node)

    healing.monitor_recovery(high_risk)

    active_nodes = healing.active_nodes()

    # Encryption
    encrypted = encryptor.encrypt("Secure HPC Task")

    # HPC Execution
    hpc_time = run_hpc()

    # Blockchain Logging
    logger.add_block(f"Risk:{risk_score} Nodes:{active_nodes}")

    result = {
        "prediction": "ATTACK" if prediction else "NORMAL",
        "probability": prob,
        "risk_score": risk_score,
        "high_risk": high_risk,
        "accuracy": accuracy,
        "encrypted": encrypted,
        "hpc_time": hpc_time,
        "nodes": active_nodes,
        "block_height": len(logger.chain)
    }

    return render_template("result.html", result=result)

# ============================================================
# DOWNLOAD FORENSIC REPORT
# ============================================================

@app.route("/download_report")
def download_report():

    report = "Adaptive Cyber Resilient HPC System\n"
    report += "="*50 + "\n\n"

    for index, block in enumerate(logger.chain):
        report += f"Block {index}\n"
        report += f"Timestamp : {block['timestamp']}\n"
        report += f"Data      : {block['data']}\n"
        report += f"Hash      : {block['hash']}\n"
        report += "-"*40 + "\n"

    buffer = io.BytesIO()
    buffer.write(report.encode())
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="forensic_report.txt",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)