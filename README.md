# GiveMe - Simple File Upload/Download Hub

A lightweight, containerized Python web application for uploading, downloading, and managing files. Features password protection and support for large files (up to 20GB).

## TL;DR

Just go then: 

```bash
docker run --rm -it -p 5000:5000 -e APP_PASSWORD=your-password -e PORT=5000 --name giveme-app giveme
```


## Features

- 🔐 Password-protected access
- 📤 File upload with progress support
- 📥 File download
- 📋 File listing with sizes
- 🗑️ File deletion
- 🐳 Fully containerized with Docker
- 💾 Support for large files (tested up to 20GB)
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

# Run on port 5000 instead
docker run --rm                 \
  -p 5000:5000                  \
  -v $(pwd)/data:/app/data      \
  -e APP_PASSWORD=your-password \
  -e PORT=5000                  \
  --name giveme-app             \
  giveme
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
export PORT=5000

# Run the application
python app.py
```

## Configuration

### Environment Variables

- `APP_PASSWORD` - Password required to access the application (if not set, a random password will be generated and displayed in logs)
- `PORT` - Port number for the application (default: `5000`)
- `MAX_CONTENT_LENGTH` - Maximum file size (default: 20GB, configurable in `app.py`)

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
- **WSGI Server**: Gunicorn (production-ready)
- **Python Version**: 3.13
- **Workers**: 4 (configurable)
- **Port**: 5000 (configurable via PORT env var)
- **Max File Size**: 20GB (configurable)
- **Chunk Size**: 8KB for streaming uploads/downloads
- **Request Timeout**: 300 seconds (5 minutes)

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

- Always use a strong password for `APP_PASSWORD` in production
- If `APP_PASSWORD` is not set, a random password is generated on startup (check logs)
- Sessions are invalidated on container restart for security
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
