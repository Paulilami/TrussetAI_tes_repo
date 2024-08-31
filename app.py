import subprocess
import json
import time
import os
import logging
from flask import Flask, request, jsonify, render_template, abort

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')

active_sessions = {}
MAX_SESSION_DURATION = 1800

def run_ai_script(script_name, prompt, current_config=None):
    if not os.path.isfile(script_name):
        return {"error": f"Script not found: {script_name}"}
    try:
        input_data = {"prompt": prompt, "current_config": current_config or {}}
        result = subprocess.run(
            ['python3', script_name],
            input=json.dumps(input_data),
            text=True,
            capture_output=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return {"error": f"Script {script_name} failed", "stderr": e.stderr}
    except Exception as e:
        return {"error": str(e)}

def manage_session(session_id):
    if session_id in active_sessions:
        session_data = active_sessions[session_id]
        session_data['last_active'] = time.time()
    else:
        session_data = {
            "target_script": None,
            "prompt": "",
            "current_config": {},
            "session_state": "active",
            "last_active": time.time()
        }
        active_sessions[session_id] = session_data
    return session_data

def clean_up_sessions():
    current_time = time.time()
    expired_sessions = [sid for sid, sdata in active_sessions.items() if current_time - sdata['last_active'] > MAX_SESSION_DURATION]
    for sid in expired_sessions:
        del active_sessions[sid]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    clean_up_sessions()
    try:
        data = request.json
        if not data:
            abort(400, description="No JSON data provided")

        user_input = data.get('input')
        session_id = data.get('session_id')
        
        if not user_input:
            abort(400, description="No input provided")

        if not session_id:
            session_id = str(int(time.time()))
        
        session_data = manage_session(session_id)

        if session_data.get('session_state') == "ended":
            abort(400, description="Session has ended. Please start a new session.")

        if user_input.lower() in ["done", "stop"]:
            session_data['session_state'] = "ended"
            del active_sessions[session_id]
            return jsonify({"message": "Session ended", "session_id": session_id, "session_data": session_data})

        if session_data.get('target_script'):
            script_output = run_ai_script(session_data['target_script'], user_input, session_data.get('current_config', {}))
            if isinstance(script_output, dict) and "error" not in script_output:
                session_data['current_config'] = script_output
            return jsonify({"output": script_output, "session_id": session_id, "session": session_data})

        selector_result = run_ai_script('selector.py', user_input)
        if "error" in selector_result:
            return jsonify(selector_result), 500

        target_script = selector_result.get("Target")
        if not target_script:
            abort(500, description="Failed to determine the target protocol.")

        session_data['target_script'] = target_script
        session_data['prompt'] = selector_result.get("Prompt", user_input)
        session_data['current_config'] = session_data.get('current_config', {})

        script_output = run_ai_script(session_data["target_script"], session_data["prompt"], session_data['current_config'])

        if isinstance(script_output, dict) and "error" not in script_output:
            session_data['current_config'] = script_output

        return jsonify({"output": script_output, "session_id": session_id, "session": session_data})
    except Exception as e:
        logging.error(f"Error in process_input: {str(e)}")
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
