import os

# gunicorn_config.py
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

# Use the PORT environment variable
port = os.getenv("PORT", "5001")  # Default to 5001 if PORT is not set
bind = f"0.0.0.0:{port}"

# Workers configurations
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'

# Logging configurations
loglevel = 'info'
accesslog = '-'
errorlog = '-'

# Secure scheme headers and proxy settings
forwarded_allow_ips = '*'
secure_scheme_headers = {
    'X-Forwarded-Proto': 'https'
}
