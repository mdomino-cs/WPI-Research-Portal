from functools import wraps
from flask import abort
from flask_login import current_user, login_required

def role_required(role_or_roles):
    if isinstance(role_or_roles, (list, tuple, set)):
        allowed = set(role_or_roles)
    else:
        allowed = {role_or_roles}

    def decorator(f):
        @wraps(f)
        @login_required
        def wrapped(*args, **kwargs):
            if getattr(current_user, 'role', None) not in allowed:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator