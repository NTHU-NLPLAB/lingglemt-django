# lingglemt-django
Linggle Machine Translation Web System

## Prerequisite
- Essential
  - python
  - Django
  - [lingglemt-core](https://github.com/NTHU-NLPLAB/lingglemt-core)
- Recommended
  - channels
  - redis

## Get started
### Create virtual environment (py3 recommended)
There are a lot problems of dependencies versions, and indirectly permissions in Python.
It is strongly recommended to use tools like [virtualenv](https://virtualenv.pypa.io).
Here's an example using **virtualenv**.
```console
$ virtualenv lmtenv --python=python3
$ source lmtenv/bin/activate
```

### Install lingglemt-core:
**lingglemt-core** composed of the core translation functions of **Linggle MT**.
This is an **essential** part of the system.
It is still under development and is available on GitHub. Ask if you encounter any problem.
```console
$ pip install https://github.com/NTHU-NLPLAB/lingglemt-core/archive/master.zip
```

(ask jjc@nlplab.cc if you don't have permission to `lingglemt-core`.)


### Run the system
Clone the repository
```console
$ git clone https://github.com/NTHU-NLPLAB/lingglemt-django
$ cd lingglemt-django
```

Install necessary python packages from `requirement.txt`
```console
$ pip install -r requirements.txt
```

Then, you are good to go. Just enter the following command:
```console
$ python manage.py runserver 0.0.0.0:5566
```
(note: you might have to set`DEBUG = False` under `linggletranslate/settings.py`.)

## Use Channels

> Channels is a project to make Django able to handle more than just plain HTTP requests,
including WebSockets and HTTP2,
as well as the ability to run code after a response has been sent for things like thumbnailing or background calculation.
You may set channel layer 

You can manage channel setting under `linggletranslate/settings`.

Use `in-memory` channel

```py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "linggletranslate.routing.channel_routing",
    },
}
```

or, use `redis-server`

```py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "linggletranslate.routing.channel_routing",
        "CONFIG": {
            # your own redis-server settings here
            # "hosts": [("redis-server-name", 6379)],
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
```
Note: `in-memory` mode is only workable in single-process server (e.g. running with `python manage.py`).
Use data store like e.g. [Redis](http://redis.io) if you want to deploy it to some PaaS like [Heroku](https://www.heroku.com)
