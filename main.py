from signal import signal, SIGINT
from sys import exit


# noinspection PyUnusedLocal
def signal_handler(signal_number, frame):
    exit(0)


if __name__ == "__main__":
    signal(SIGINT, signal_handler)
    app = None
    exec("from core import app")
    # noinspection PyUnresolvedReferences
    app.run(debug=True,  # ssl_context='adhoc' DO NOT CHANGE THIS LINE!!!
            )
