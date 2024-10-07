# app.py
from flask import Flask, request, render_template_string, jsonify
import docker
import uuid
import threading
import time

app = Flask(__name__)

# Store active containers
containers = {}

# Clean up old containers periodically
def cleanup_containers():
    while True:
        current_time = time.time()
        to_remove = []
        
        for container_id, info in containers.items():
            if current_time - info['start_time'] > 300:  # 5 minutes timeout
                try:
                    info['container'].stop()
                    info['container'].remove()
                    to_remove.append(container_id)
                except:
                    pass
                    
        for container_id in to_remove:
            del containers[container_id]
            
        time.sleep(60)  # Check every minute

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_containers, daemon=True)
cleanup_thread.start()

# HTML template
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Jail CTF</title>
    <style>
        body {
            font-family: monospace;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a1a;
            color: #ffffff;
        }
        #terminal {
            background: #000;
            padding: 10px;
            border-radius: 5px;
            margin: 20px 0;
            height: 400px;
            overflow-y: auto;
        }
        #input {
            width: 100%;
            padding: 5px;
            background: #333;
            color: #fff;
            border: 1px solid #666;
        }
        .output {
            color: #0f0;
            margin: 5px 0;
            white-space: pre-wrap;
        }
        .error {
            color: #f00;
        }
        button {
            margin: 10px 0;
            padding: 5px 15px;
            background: #444;
            color: #fff;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        button:hover {
            background: #666;
        }
    </style>
</head>
<body>
    <h1>Python Jail CTF Challenge</h1>
    <div id="terminal"></div>
    <input type="text" id="input" placeholder="Enter your Python code here...">
    <button onclick="sendCommand()">Execute</button>
    <button onclick="newSession()">New Session</button>
    
    <script>
        let sessionId = null;
        
        function appendOutput(text, isError=false) {
            const terminal = document.getElementById('terminal');
            const div = document.createElement('div');
            div.className = 'output' + (isError ? ' error' : '');
            div.textContent = text;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }
        
        async function newSession() {
            const response = await fetch('/new_session', {method: 'POST'});
            const data = await response.json();
            sessionId = data.session_id;
            document.getElementById('terminal').innerHTML = '';
            appendOutput('New session started. Try to read the flag!\n');
        }
        
        async function sendCommand() {
            if (!sessionId) {
                await newSession();
            }
            
            const input = document.getElementById('input');
            const command = input.value;
            input.value = '';
            
            appendOutput('>>> ' + command);
            
            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        session_id: sessionId,
                        command: command
                    })
                });
                
                const data = await response.json();
                if (data.error) {
                    appendOutput(data.error, true);
                } else {
                    appendOutput(data.output);
                }
            } catch (error) {
                appendOutput('Error: ' + error.message, true);
            }
        }
        
        // Handle Enter key
        document.getElementById('input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendCommand();
            }
        });
        
        // Start new session on load
        newSession();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(PAGE_TEMPLATE)

@app.route('/new_session', methods=['POST'])
def new_session():
    client = docker.from_env()
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Create new container
    container = client.containers.run(
        'pyjail-ctf',
        detach=True,
        mem_limit='128m',
        cpus=0.5,
        pids_limit=100,
        network_mode='none'
    )
    
    containers[session_id] = {
        'container': container,
        'start_time': time.time()
    }
    
    return jsonify({'session_id': session_id})

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    session_id = data.get('session_id')
    command = data.get('command')
    
    if not session_id or session_id not in containers:
        return jsonify({'error': 'Invalid session'})
    
    try:
        container = containers[session_id]['container']
        exec_result = container.exec_run(f'python3 -c "print({command})"')
        output = exec_result.output.decode('utf-8').strip()
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
