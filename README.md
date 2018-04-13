
Django-charged is a REST / websocket app that allows
(bitcoin) lightningd integration into a Django project

 

Install:

 clone into your project folder /charged/



django-charged uses Channels (websockets) to communicate to the browser

pip install: 

 pylightning  channels base58 channels_redis



config:

    #add to installed apps:

        'channels',
        'charged',
        ... 


    # location of your lightning-rpc
    LIGHTNING_RPC = '/home/user/.lightning/lightning-rpc'


    CHANNEL_LAYERS = {
            "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
        },
    }

    ASGI_APPLICATION = "charged.routing.application"





urls.py:    

     url(r'^ln/', include('charged.urls')),

 (This also includes the Demo  /ln/demo )


The Worker process is used for monitoring the payments.
Start the worker process:

     ./manage.py runworker lnws


Access to REST-api is can be restriced. Some Views  have the
@method_decorator(local_only, ...)  that restricts acces to the local machine only.
Acces can be further restricted by adding Views that proxy to the API.

[demo](https://vimeo.com/264287111)


