# gunicorn_config.py
import multiprocessing
import gevent.monkey
gevent.monkey.patch_all()

# Basic bind configuration - IP and port your app will listen on
bind = "0.0.0.0:5000"

# Workers configurations
workers = multiprocessing.cpu_count() * 2 + 1  # Recommended formula for the number of workers
worker_class = 'gevent'  # Using gevent for async capabilities, adjust if you're not using async

# Logging configurations
loglevel = 'info' # to see the info 'info'
accesslog = '-' # to see the logs '-'
errorlog = '-'

# Secure scheme headers and proxy settings, useful if you're behind a reverse proxy
forwarded_allow_ips = '*'  # Trust the `X-Forwarded-For` header from all IPs
secure_scheme_headers = {
    'X-Forwarded-Proto': 'https'
} 
# to start gunicorn -c gunicorn_config.py app:app