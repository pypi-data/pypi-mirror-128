def login_required(some_fun):
    def check_some_func(*args, **kwargs):
        if len(args[0].clients):
            return some_fun(*args)
        else:
            raise TypeError
    return check_some_func
