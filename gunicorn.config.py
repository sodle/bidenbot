bind = 'unix:/local/run/biden.sock'

workers = 5
worker_class = 'gthread'
worker_timeout = 600

syslog = True
user = 'biden'
group = 'www-data'

preload_app = True
