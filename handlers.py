import signal, sys, time, inspect

# Relevant pages
#   https://docs.python.org/3/library/signal.html
#   https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown


# example of ignoring SIGINT over a region of code.  Also trying to RE the frame information
def sigint_handler(sig, frame):
    sys.stderr.write("\nInterrupted")
    print(sig)
    print(frame)
    if False:
        print(inspect.currentframe().f_back.f_code.co_name)
        print(frame.__dir__())
        for f in frame.__dir__():
            if f[0] == "f":
                print(f)
                print(getattr(frame, f))

    signal.signal(signal.SIGINT, signal.SIG_IGN)
    print("Cleanup, SIGINT ignored")
    time.sleep(5)
    print("SIGINT back to default.")
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    time.sleep(5)
    print("Bye!")
    exit()


# SIGALRM experiment, this should run every 5 seconds
def sigalarm_handler(sig, frame):
    try:
        print("Alarm!")
    finally:
        pass


# SIGINT experiments
# this doesn't work... int_count not defined in handler
def sigint_handler_counter(count):
    int_count = count

    def handler(sig, frame):
        global int_count
        int_count -= 1
        print(f"{int_count=}")
        if int_count <= 0:
            sys.exit()

    return handler


# this works, but has a global
ctrl_c_counter = 10


def sigint_counter(sig, frame):
    global ctrl_c_counter
    ctrl_c_counter -= 1
    print(f"{ctrl_c_counter=}")
    if ctrl_c_counter <= 0:
        print("bye!")
        sys.exit()


##


# as a class - works, also cleanest way
class signal_counter:
    __slots__ = ("counter",)

    def __init__(self, initial_value=10, sig=signal.SIGINT):
        self.set_counter(initial_value)
        if sig:
            signal.signal(sig, self.handler)

    def set_counter(self, value):
        self.counter = value
        return value

    def action(self):
        print("Bye!")
        sys.exit()

    def handler(self, signal, frame):
        self.counter -= 1
        print(f"Got ctrl-c! {self.counter=}")
        if self.counter <= 0:
            self.action()


def main():
    # install SIGALRM handler and set timer
    signal.signal(signal.SIGALRM, sigalarm_handler)
    signal.setitimer(signal.ITIMER_REAL, 5, 5)

    # signal.signal(signal.SIGINT, sigint_counter)
    # signal.signal(signal.SIGINT, signal_counter(5).handler)
    c = signal_counter(5)

    for i in range(100):
        print(i)
        if i == 20:
            c.set_counter(5)
        time.sleep(1)


if __name__ == "__main__":
    main()
