from datetime import datetime
import snitch_ai


class Logger:
    @staticmethod
    def information(message):
        if (snitch_ai.verbose):
            print(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} [INFO]: {message}", flush=True)