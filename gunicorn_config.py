import multiprocessing

bind = "0.0.0.0:5050"
workers = 2
worker_class = 'eventlet'
timeout = 1800
graceful_timeout = 600
reload_engine = 'auto'
max_requests = 2