
Django-charged is a REST / websocket app that allows
(bitcoin) lightningd integration into a Django project

 [demo](https://vimeo.com/264287111)
 

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

 This also includes the Demo  /ln/demo , which requires 
 jquery-qrcode-0.14.0.js and jquery 


The Worker process is used for monitoring the payments.
Start the worker process:

     ./manage.py runworker lnws


Access to REST-api is can be restriced. Some Views  have the
`@method_decorator(local_only, ...)`  that restricts access to the local machine only.
Access can be further restricted by adding Views that proxy to the API.


## REST APi

#### GET /ln/info
    $ curl 127.0.0.1/ln/info
    {"network": "testnet", "id": "03ef12386d4f39b8bc83e82bbad02579a54e42bd1e22cfd81bd2ca94124ec65792", "version": "v0.5.2-2016-11-21-2502-g9575136", "address": [{"address": "91.15.82.171", "type": "ipv4", "port": 9735}, {"address": "91.15.82.171", "type": "ipv4", "port": 9735}], "blockheight": 1292806, "port": 9735}

#### POST /ln/invoice
Create a new invoice

using msatoshi

    $ curl -X POST 127.0.0.1/ln/invoice -d msatoshi=10000 -d description='some text'
    {"expires_at": 1523706622, "bolt11": "lntb100n1pddrh8wpp5j6d6emxqqxue...", "payment_hash": "969bacecc001b99d4607654a11bfe5e00ddb70eaa96b33ff3787f8d717d3cadc", "expiry_time": 1523706622}

Convert currency to BTC

    $ curl -X POST 127.0.0.1/ln/invoice -d currency=EUR -d amount=0.5  -d description='some text '
    {"expires_at": 1523706754, "bolt11": "lntb77694290p1pddrhtjpp5vjltnw342hztrmz4rvmfsx89alwqcwv...", "payment_hash": "64beb9ba3555c4b1ec551b369818e5efdc0c399b542b01bc8f6b83cf99ca9948", "expiry_time": 1523706754}


#### GET /ln/invoice/{label}

    $ curl 127.0.0.1/ln/invoice/4vs5mDZgRU
    {"label": "4vs5mDZgRU", "expires_at": 1523708333, "payment_hash": "9c9adee3df4c652fe3c9e0d45a4d887961cdff2ba7260ca16d5e617097f2e35e", "msatoshi": 10000000, "status": "unpaid", "bolt11": "lntb100u1pddrcuapp5njddac7lf3jjlc7fur295nvg09su... 
    

#### Websocket 

Send the 'wait_invoice' command to be notified over WS when the invoice is paid.    

    var mes = { message_type: "wait_invoice", payment_hash : ph };
    ws.send(JSON.stringify(mes)) ;
    
