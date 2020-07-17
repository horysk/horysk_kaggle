def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                return False
                print("%s is running" % func.__name__)
            elif level == "info":
                print("%s is running" % func.__name__)
            return func(name="level")
        return wrapper

    return decorator

@use_logging(level="warn")
def foo(name='foo'):
    print("i am %s" % name)


if __name__=="__main__":

    foo()