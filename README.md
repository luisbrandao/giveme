# GiveMe - Simple File Upload/Download Hub

A lightweight, containerized Python web application for uploading, downloading, and managing files. Features password protection and support for large files (up to 5GB).

## Features

- 🔐 Password-protected access
- 📤 File upload with progress support
- 📥 File download
- 📋 File listing with sizes
- 🗑️ File deletion
- 🐳 Fully containerized with Docker
- 💾 Support for large files (tested up to 5GB)
- 🎨 Clean, modern UI

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and navigate to the repository**
   ```bash
   cd giveme
   ```

2. **Create a `.env` file**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` and set your password**
   ```bash
   nano .env
   ```
   
   Set your own values:
   ```
   APP_PASSWORD=your-secure-password-here
   SECRET_KEY=your-secret-key-for-sessions
   PORT=5000
   ```

4. **Start the application**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   
   Open your browser and go to: `http://localhost:5000`

### Using Docker directly

```bash
# Build the image
docker build -t giveme .

# Run the container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -e APP_PASSWORD=your-password \
  -e SECRET_KEY=your-secret-key \
  -e PORT=5000 \
  --name giveme-app \
  ghcr.io/luisbrandao/giveme:latest
```

### Running locally (without Docker)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export APP_PASSWORD=your-password
export SECRET_KEY=your-secret-key
export PORT=5000

# Run the application
python app.py
```

## Configuration

### Environment Variables

- `APP_PASSWORD` - Password required to access the application (default: `changeme`)
- `SECRET_KEY` - Secret key for session management (default: auto-generated)
- `PORT` - Port number for the application (default: `5000`)
- `MAX_CONTENT_LENGTH` - Maximum file size (default: 5GB, configurable in `app.py`)

## File Storage

All uploaded files are stored in the `./data` directory. This directory is:
- Created automatically on first run
- Mounted as a Docker volume for persistence
- Excluded from git (via `.gitignore`)

## Usage

1. **Login** - Enter the password you configured in the `.env` file
2. **Upload Files** - Click "Choose File", select your file, and click "Upload"
3. **Download Files** - Click the "Download" button next to any file
4. **Delete Files** - Click the "Delete" button next to any file (requires confirmation)
5. **Logout** - Click the "Logout" button in the header

## Technical Details

- **Framework**: Flask 3.0
- **Python Version**: 3.13
- **Port**: 5000
- **Max File Size**: 5GB (configurable)
- **Chunk Size**: 8KB for streaming uploads/downloads

## Project Structure

```
giveme/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── login.html      # Login page
│   └── index.html      # Main file hub page
└── data/               # File storage directory (created automatically)
```

## Security Notes

- Always use a strong password for `APP_PASSWORD`
- Change the `SECRET_KEY` to a random string in production
- The application uses session-based authentication
- Files are served with secure filenames using `werkzeug.utils.secure_filename`
- Consider adding HTTPS in production (use a reverse proxy like nginx)

## Stopping the Application

```bash
# If using docker-compose
docker-compose down

# If using docker directly
docker stop giveme-app
docker rm giveme-app
```

## Logs

```bash
# View logs (docker-compose)
docker-compose logs -f

# View logs (docker)
docker logs -f giveme-app
```

## License

MIT License - Feel free to use and modify as needed.
