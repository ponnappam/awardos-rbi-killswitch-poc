from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/health')
def health():
    return {"status": "ok"}

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data['messages'][-1]['content']
    
    ollama_resp = requests.post(
        'http://balk-llm:11434/api/generate',
        json={"model": "llama3.2:1b", "prompt": user_msg, "stream": False},
        timeout=120
    )
    llm_text = ollama_resp.json().get('response', '')
    
    return jsonify({
        "choices": [{"message": {"role": "assistant", "content": llm_text}}]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
