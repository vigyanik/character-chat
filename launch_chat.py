import argparse
import os
import signal
import subprocess
import sys
import threading

def print_output(process, prefix):
    for line in iter(process.stdout.readline, b''):
        print(f'{prefix}: {line.decode().strip()}')

def launch_programs(args):
    common_args = ['python3', '-m']

    # Prepare the command for the controller
    controller_cmd = common_args + ['fastchat.serve.controller']
    controller_proc = subprocess.Popen(controller_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    threading.Thread(target=print_output, args=(controller_proc, '[controller]')).start()

    # Prepare the command for the model worker
    model_worker_cmd = common_args + ['fastchat.serve.model_worker']
    if args.device != 'gpu' and args.num_gpus == 1:
        model_worker_cmd += ['--device', args.device]
    elif args.device == 'gpu' or args.num_gpus > 1:
        model_worker_cmd += ['--num-gpus', str(args.num_gpus)]
        if args.gpus is not None:
            model_worker_cmd += ['--gpus', args.gpus]

    for path in args.model_path:
        model_worker_cmd += ['--model-path', path]

    model_worker_proc = subprocess.Popen(model_worker_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    threading.Thread(target=print_output, args=(model_worker_proc, '[model_worker]')).start()

    # Prepare the command for the api server
    api_server_cmd = common_args + ['fastchat.serve.openai_api_server']
    api_server_cmd += ['--host', args.host, '--port', str(args.port)]
    
    api_server_proc = subprocess.Popen(api_server_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    threading.Thread(target=print_output, args=(api_server_proc, '[api_server]')).start()

    # Prepare the command for chat
    chat_cmd = ['streamlit', 'run', './chat.py']
    for path in args.model_path:
        filename = os.path.basename(path)
        chat_cmd += [filename]
    
    chat_proc = subprocess.Popen(chat_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    threading.Thread(target=print_output, args=(chat_proc, '[chat]')).start()

    # Register signal handlers to ensure child processes are terminated when the main process is
    def kill_processes(signal, frame):
        controller_proc.kill()
        model_worker_proc.kill()
        api_server_proc.kill()
        chat_proc.kill()
        sys.exit(0)
    signal.signal(signal.SIGINT, kill_processes)

    # Wait for all child processes to finish
    controller_proc.wait()
    model_worker_proc.wait()
    api_server_proc.wait()
    chat_proc.wait()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', help='host name (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='port number (default: 8000)')
    parser.add_argument('--device', choices=['cpu', 'mps', 'gpu'], default='cpu', help='The device type (default: cpu)')
    parser.add_argument('--num-gpus', type=int, choices=range(1, 9), default=1, help='Number of GPUs, only valid when --device gpu (default: 1)')
    parser.add_argument('--gpus', type=str, help='A single GPU like "1" or multiple GPUs like "0,2" (optional)')
    parser.add_argument('--model-path', action='append', required=True, help='The path to the weights. This can be a local folder or a Hugging Face repo ID. (required)')
    parser.add_argument('--load-8bit', action='store_true', help='Use 8-bit quantization (optional)')
    
    args = parser.parse_args()
    if args.num_gpus > 1 or args.gpus is not None:
        args.device = 'gpu'
    launch_programs(args)

if __name__ == '__main__':
    main()
