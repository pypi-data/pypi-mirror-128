# yhttp-rabbitmq

[![PyPI](http://img.shields.io/pypi/v/yhttp-rabbitmq.svg)](https://pypi.python.org/pypi/yhttp-rabbitmq)
[![Build](https://github.com/yhttp/yhttp-rabbitmq/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/yhttp/yhttp-rabbitmq/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/yhttp/yhttp-rabbitmq/badge.svg?branch=master)](https://coveralls.io/github/yhttp/yhttp-rabbitmq?branch=master)


RabbitMQ extension for [yhttp](https://github.com/yhttp/yhttp).


### Install

```bash
pip install yhttp-pony
```


### Usage

```python
from yhttp import Application
from yhttp.ext.rabbitmq import install as rabbitmq_install


app = Application()
rabbitmq_install(app)
app.settings.merge('''
rabbitmq:
  host: localhost
  port: 5672
  virtualhost: /
  user: guest
  password: guest
  channel_max: 10
  connection_attempts: 3
  
  ssl:
    ca_certfile:  <ca_cert>
    certfile: <client_cert>
    keyfile: <client_key>
    commonname: <CN>
 
  pool:
    maxsize: 10
    maxoverflow: 10
    timeout: 10
    recycle: 3600
    stale: 45
''')
app.ready()


@app.route()
def get(req):
    with app.rabbitmq.acquire() as cxn:
        cxn.channel.basic_publish(
            body='banana',
            exchange='',
            routing_key='fruits',
            properties=pika.BasicProperties(
                content_type='text/plain',
                content_encoding='utf-8',
                delivery_mode=2,
            )
        )

app.ready()
