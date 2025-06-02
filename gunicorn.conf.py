import multiprocessing

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gthread'
threads = 3

# Logging
accesslog = '-'  # Log to stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = '-'  # Log to stderr
loglevel = 'info'

# Timeouts
worker_connections = 1000
timeout = 120
keepalive = 5

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Debugging
reload = False
preload_app = True

# Server socket
bind = '0.0.0.0:8000'

# Process naming
proc_name = 'social_backend'

# Worker processes
max_requests = 1000
max_requests_jitter = 50
