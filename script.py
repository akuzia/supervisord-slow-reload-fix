import signal
import time


class SignalHandler:
    running = True

    def __init__(self):
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def handle_signal(self, *args):
        self.running = False
        print('Got signal. Waiting to exit...')
        time.sleep(3)


def main():
    handler = SignalHandler()
    while handler.running:
        time.sleep(1)
        print("running...")

    print("Exited")


if __name__ == '__main__':
    main()
