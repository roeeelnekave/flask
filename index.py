from flask import Flask, request, jsonify
import subprocess
import platform

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
