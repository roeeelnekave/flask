from flask import Flask, request, jsonify
import subprocess
import platform
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

command_history = []

@app.route('/')
def index():
    return "Welcome to the Bash API!"

@app.route('/execute', methods=['GET'])
def execute_command():
    command = request.args.get('cmd')
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
   
    try:
        output = subprocess.check_output(command, shell=True, text=True)
     
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
     
    }
    return jsonify(info), 200

@app.route('/command-history')
def get_command_history():
  
    history = command_history[-100:]
  
    with open('command_history.txt', 'w') as file:
        for cmd in history:
            file.write(cmd + '\n')
    return jsonify({'message': 'Command history exported to command_history.txt'}), 200

# @app.route('/metrics')
# def metrics_endpoint():
#     return metrics.generate_latest()

metrics.register_endpoint(app, '/metrics')

if __name__ == '__main__':
    app.run(port=5005, host='0.0.0.0', debug=True)
