import signal, sys, time, inspect

# Relevant pages
#   https://docs.python.org/3/library/signal.html
#   https://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown


def sigint_handler(sig, frame):
    sys.stderr.write("\nInterrupted")
    print(sig)
    print(frame)
    print(inspect.currentframe().f_back.f_code.co_name)
    print(frame.__dir__())
    for f in frame.__dir__():
        if f[0] == "f":
            print(f)
            print(getattr(frame, f))

    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    print("Cleanup")
    time.sleep(5)
    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    print("Bye!")
    exit()


def sigalarm_handler(sig, frame):
    try:
        print("hi")
    finally:
        pass


signal.signal(signal.SIGINT, sigint_handler)


signal.signal(signal.SIGALRM, sigalarm_handler)
signal.setitimer(signal.ITIMER_REAL, 5, 5)

for i in range(100):
    print(i)
    time.sleep(1)
