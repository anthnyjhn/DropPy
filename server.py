import os
from flask import Flask, request, send_from_directory, abort, render_template
from config import setup_upload_folder

app = Flask(__name__)
UPLOAD_FOLDER = setup_upload_folder()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PORT = 5000
approved_ips = set()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            if uploaded_file.filename:
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(save_path)
                uploaded_filenames.append(uploaded_file.filename)

    return render_template('upload.html', uploaded_filenames=uploaded_filenames)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def run():
    app.run(host='0.0.0.0', port=PORT)

def get_port():
    return PORT
