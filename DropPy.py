import os
import socket
import qrcode
from flask import Flask, request, redirect, send_from_directory, abort
from threading import Thread
import netifaces as ni
import json
from pathlib import Path

CONFIG_FILE = Path.home() / '.upload_config.json'

# To keep track of approved IPs
approved_ips = set()


def setup_upload_folder():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('upload_path')

    print("🗂  First-time setup:")
    default_path = Path.home() / 'MyDropbox'
    use_default = input(f"\nDo you want to create and use '{default_path}' as your upload folder? (Y/n): ").strip().lower()

    if use_default in ('y', '', 'yes'):
        upload_path = default_path
    else:
        while True:
            custom = input("Please enter a valid absolute path to use instead: ").strip()
            upload_path = Path(custom).expanduser()
            if upload_path.is_dir() or not upload_path.exists():
                break
            print("❌ Invalid path. Try again.")

    upload_path.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, 'w') as f:
        json.dump({'upload_path': str(upload_path)}, f)

    return str(upload_path)


UPLOAD_FOLDER = setup_upload_folder()
PORT = 5000

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    client_ip = request.remote_addr

    if client_ip not in approved_ips:
        user_agent = request.headers.get('User-Agent', 'Unknown')
        print(f"\n🔗 Connection attempt from {client_ip} (User-Agent: {user_agent})")
        decision = input("Allow this device? (Y/n): ").strip().lower()
        if decision in ('y', '', 'yes'):
            approved_ips.add(client_ip)
            print(f"✅ Allowed: {client_ip}")
        else:
            print(f"❌ Blocked: {client_ip}")
            abort(403)

    uploaded_filenames = []
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        for uploaded_file in files:
            if uploaded_file.filename != '':
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(save_path)
                uploaded_filenames.append(uploaded_file.filename)

    file_list_html = ''.join(f'<li>{name} uploaded</li>' for name in uploaded_filenames)

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>DropPy: Share Files Locally </title>
      <style>
        body {{
          font-family: sans-serif;
          background-color: #f5f5f5;
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 40px 20px;
        }}
        h1 {{
          color: #333;
          margin-bottom: 20px;
        }}
        form {{
          background-color: white;
          padding: 20px;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          width: 100%;
          max-width: 400px;
        }}
        #fileInputs {{
        margin-bottom: 20px;
        }}
        input[type="file"], .file-input {{
          display: block;
          width: 100%;
          max-width: 100%;
          padding: 12px 8px;
          margin-bottom: 20px;
          border: 1px solid #ccc;
          border-radius: 6px;
          box-sizing: border-box;
        }}
        input[type="submit"], .add-btn {{
          background-color: #007BFF;
          color: white;
          padding: 12px;
          border: none;
          border-radius: 6px;
          width: 100%;
          font-size: 16px;
          cursor: pointer;
          margin-bottom: 0.5rem;
        }}
        input[type="submit"]:hover, .add-btn:hover {{
          background-color: #0056b3;
        }}
        ul {{
          margin-top: 20px;
          padding: 0;
          list-style: none;
          width: 100%;
          max-width: 400px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }}
        li {{
          background-color: #e6ffe6;
          border-left: 4px solid #28a745;
          padding: 10px;
          width: 100%;
          margin-bottom: 8px;
          font-size: 15px;
        }}
        @media (max-width: 480px) {{
          body {{
            padding: 20px 10px;
          }}
        }}
      </style>
    </head>
    <body>
      <h1>Upload Files</h1>
      <form method="post" enctype="multipart/form-data" id="uploadForm">
        <div id="fileInputs">
          <input type="file" name="file[]" multiple required class="file-input">
        </div>
        <button type="button" class="add-btn" onclick="addFileInput()">Add more files</button>
        <input type="submit" value="Send">
      </form>
      <ul>
        {file_list_html}
      </ul>
      <script>
        function addFileInput() {{
          const inputDiv = document.getElementById('fileInputs');
          const newInput = document.createElement('input');
          newInput.type = 'file';
          newInput.name = 'file[]';
          newInput.multiple = true;
          newInput.required = true;
          newInput.className = 'file-input';
          inputDiv.appendChild(newInput);
        }}
      </script>
    </body>
    </html>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def get_local_ip():
    interfaces = ni.interfaces()
    for iface in interfaces:
        if iface != 'lo' and ni.AF_INET in ni.ifaddresses(iface):
            addr = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
            if addr.startswith('192.') or addr.startswith('10.') or addr.startswith('172.'):
                return addr
    return '127.0.0.1'


def run_server():
    app.run(host='0.0.0.0', port=PORT)


def show_qr(ip):
    url = f'http://{ip}:{PORT}/'
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    print(f"\n📶 Upload page URL: {url}\n")
    qr.print_ascii(invert=True)


if __name__ == '__main__':
    ip = get_local_ip()
    thread = Thread(target=run_server)
    thread.start()
    show_qr(ip)
