from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url


def access_check(test_func, view_func=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that should pass a test before allowing access.
    
    :param test_func: A callable that returns True if access is allowed, or
                False if the user should be sent to the login page.
    :param test_func: A callable that returns a HTTP response. This should only
                be set if used in a 'urls.py' file. If the decorator is used
                on a view function, this parameter should be set to None.
    :param login_url: The URL of the login page. If set to None, the default
                login page is used.
    :param redirect_field_name: The name of the URL field that should contain
                the page to display after login.
    """
    
    def decorator(decorated_view_func):
        @wraps(decorated_view_func, assigned=available_attrs(decorated_view_func))
        def _wrapped_view(request, *args, **kwargs):
            # If the access test is passed, display the page.
            if test_func(request):
                return decorated_view_func(request, *args, **kwargs)
            # Get the path to the current page and the login page.
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            # Redirect to the login page.
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    
    if view_func:
        return decorator(view_func)
    else:
        return decorator
