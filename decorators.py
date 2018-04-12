from django.core.exceptions import PermissionDenied
from threading import Thread

def local_only(function):

    def wrap(request, *args, **kwargs):
        if request.META.get('REMOTE_ADDR') == '127.0.0.1':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__  = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



def postpone(function):
  def decorator(*args, **kwargs):
    t = Thread(target=function, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
  return decorator