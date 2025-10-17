import os
import hashlib
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB max file size
app.config['UPLOAD_FOLDER'] = './data'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Get password from environment variable
APP_PASSWORD = os.environ.get('APP_PASSWORD', 'changeme')

# Create a password hash to validate sessions
# This will change if the password changes, invalidating old sessions
PASSWORD_HASH = hashlib.sha256(APP_PASSWORD.encode()).hexdigest()[:16]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        # Validate that the session matches the current password
        if session.get('password_hash') != PASSWORD_HASH:
            session.clear()
            flash('Your session has expired. Please login again.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == APP_PASSWORD:
            session['logged_in'] = True
            session['password_hash'] = PASSWORD_HASH
            return redirect(url_for('index'))
        else:
            flash('Invalid password', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    files = []
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            # Skip hidden files like .gitkeep
            if filename.startswith('.'):
                continue
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                files.append({
                    'name': filename,
                    'size': format_size(size)
                })
    except Exception as e:
        flash(f'Error listing files: {str(e)}', 'error')
    
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            # Save file in chunks to handle large files
            with open(filepath, 'wb') as f:
                while True:
                    chunk = file.stream.read(8192)  # 8KB chunks
                    if not chunk:
                        break
                    f.write(chunk)
            flash(f'File "{filename}" uploaded successfully', 'success')
        except Exception as e:
            flash(f'Error uploading file: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/download/<filename>')
@login_required
def download_file(filename):
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            flash(f'File "{filename}" deleted successfully', 'success')
        else:
            flash(f'File "{filename}" not found', 'error')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'error')
    
    return redirect(url_for('index'))


def format_size(size):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
