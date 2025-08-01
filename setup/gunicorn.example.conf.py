from pathlib import Path

# Server socket
bind = '127.0.0.1:8000'
backlog = 2048

# Worker processes
workers = 4
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
app_dir = Path(__file__).parent
log_dir = app_dir / 'logs'
log_dir.mkdir(exist_ok=True)

# Gunicorn access log
accesslog = str(log_dir / 'gunicorn_access.log')
access_log_format = (
    '%(h)s %(l)s %({x-real-ip}i)s %(l)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
)

# Gunicorn error log
errorlog = str(log_dir / 'gunicorn_error.log')
loglevel = 'info'

# Capture output from Flask app (includes print statements)
capture_output = True

# Preload the application for better performance
preload_app = True

# Process naming
proc_name = 'ff_app'

# Daemonize the gunicorn process
daemon = False

# PID file
pidfile = str(app_dir / 'gunicorn.pid')

# User and group
user = '<WWW_USER>'
group = '<WWW_USER>'
