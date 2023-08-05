import logging
from atlog import log_func

logging.basicConfig(filename="example.log", level=logging.DEBUG)
logger = logging.getLogger()
log = log_func(logger)

@log
def hello(name):
    return f"Hello, {name}."


class Greeter:
    @log
    def __init__(self, name):
        self.greeting = f"Hello, {name}."

    @log
    def greet(self):
        print(self.greeting)


if __name__ == "__main__":
    print(hello("John"))
    greeter = Greeter("John")
    greeter.greet()
