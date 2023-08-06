import ssl

import pika
from . import connpool


BUILTIN_SETTINGS = '''
host: localhost
port: 5672
virtualhost: /
user: guest
password: guest
channel_max: 10
connection_attempts: 3

ssl:
  ca_certfile:
  certfile:
  keyfile:
  commonname:


pool:
  maxsize: 10
  maxoverflow: 10
  timeout: 10
  recycle: 3600
  stale: 45

# blocked_connection_timeout:
# retry_delay:
# socket_timeout:
# timeout
'''


def create_connectionpool(settings):
    # SSL
    ssl_options = None
    if settings.ssl.ca_certfile:
        context = ssl.create_default_context(cafile=settings.ssl.ca_certfile)
        context.load_cert_chain(settings.ssl.certfile, settings.ssl.keyfile)
        ssl_options = pika.SSLOptions(context, settings.ssl.commonname)

    # Authentication
    credentials = pika.PlainCredentials(settings.user, settings.password)

    # Connection Parameters
    params = pika.ConnectionParameters(
        host=settings.host,
        port=settings.port,
        virtual_host=settings.virtualhost,
        credentials=credentials,
        ssl_options=ssl_options,
        channel_max=settings.channel_max,
        connection_attempts=settings.connection_attempts,
    )

    # Pool
    pool = connpool.QueuedPool(
        create=lambda: pika.BlockingConnection(params),
        max_size=settings.pool.maxsize,
        max_overflow=settings.pool.maxoverflow,
        timeout=settings.pool.timeout,
        recycle=settings.pool.recycle,
        stale=settings.pool.stale,
    )
    return pool


def install(app):
    app.settings.merge('rabbitmq: {}')
    app.settings['rabbitmq'].merge(BUILTIN_SETTINGS)

    @app.when
    def ready(app):
        app.rabbitmq = create_connectionpool(app.settings.rabbitmq)
