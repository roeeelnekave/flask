from flask import Flask, request, jsonify
import subprocess
import platform
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Store command history
command_history = []

@app.route('/')
def index():
    return "Welcome to the Bash API!"

@app.route('/execute', methods=['GET'])
def execute_command():
    command = request.args.get('cmd')
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    # Execute command and capture output
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        # Append command to history
        command_history.append(command)
        return jsonify({'output': output}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/system-info')
def system_info():
    info = {
        'OS': platform.system(),
        'Version': platform.version(),
        'Architecture': platform.machine(),
        # Add more system details as needed
    }
    return jsonify(info), 200

@app.route('/command-history')
def get_command_history():
    # Get last 100 commands
    history = command_history[-100:]
    # Write history to a file
    with open('command_history.txt', 'w') as file:
        for cmd in history:
            file.write(cmd + '\n')
    return jsonify({'message': 'Command history exported to command_history.txt'}), 200

@app.route('/metrics')
def metrics_endpoint():
    return metrics.export()

if __name__ == '_main_':
    app.run(port=5005, host='0.0.0.0', debug=True)
