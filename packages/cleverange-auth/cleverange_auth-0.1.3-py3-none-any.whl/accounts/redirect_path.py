
def login_redirect_path(path):
    if path:
        return str(path)
    else:
        return str('/')