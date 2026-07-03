from flask import Flask, request, jsonify
import subprocess, time, requests
app = Flask(__name__)
@app.route('/loan', methods=['POST'])
def loan():
    data = request.get_json()
    income = data.get("income", 0)
    if income > 150000:
        start = time.time()
        subprocess.run(["docker", "stop", "balk-llm"], check=False)
        latency = round(time.time() - start, 2)
        try:
            requests.post("http://rbi-rekor:9000/api/v1/log", json={"event":"MRMF_5_2_KILL","reason":"Income breach","latency_s":latency,"payload":data}, timeout=2)
        except: pass
        return jsonify({"status":"KILLED","latency_s":latency,"reason":"MRMF 5.2","compliance":"RBI Digital Lending Guidelines 2025"})
    return jsonify({"status":"APPROVED","income":income})
if __name__ == '__main__': app.run(host='0.0.0.0', port=8443)
