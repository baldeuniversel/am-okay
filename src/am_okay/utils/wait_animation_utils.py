
import sys
import time
import threading



class WaitAnimation:
    """
    @overview A base class for wait animations.

    General responsibilities:
      - Define a common interface for all wait animations
      - Ensure consistent lifecycle control (start / stop)
    """


    def __init__(self, message: str = "Processing"):
        """
        @overview A magic method that initializes the animation.

        :param message {str} - Message displayed alongside the animation.
        """

        self._message = message
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._enabled = sys.stdout.isatty()



    def start(self) -> None:
        """
        @overview A method that starts the animation in a dedicated daemon thread.
        """

        if not self._enabled:
            return None
        

        # Reset the event if restarted
        self._stop_event.clear()
        

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()



    def stop(self) -> None:
        """
        @overview A method that stops the animation and wait for the thread to finish.
        """

        if not self._enabled:
            return None
        

        self._stop_event.set()


        if self._thread:
            self._thread.join()


        self._clear_line()



    def _run(self) -> None:
        """
        @overview A method representing the internal animation loop.
    
        @details This method is intended to be overridden by subclasses
        to implement the specific animation behavior.
        """

        return None



    def _clear_line(self) -> None:
        """
        @overview A method to clear the current terminal line.
        """

        if not self._enabled:
            return None
        

        sys.stdout.write("\r" + " " * (len(self._message) + 20) + "\r")
        sys.stdout.flush()



class SpinnerAnimation(WaitAnimation):
    """
    @overview A class implementing a rotating spinner animation, inheriting from `WaitAnimation`.
    """


    def _run(self) -> None:

        symbols = "|/-\\"
        index = 0
        interval_time = 0.1


        while not self._stop_event.is_set():

            sys.stdout.write(
                f"\r{self._message}... {symbols[index % len(symbols)]}"
            )
            sys.stdout.flush()

            index += 1

            time.sleep(interval_time)



class CircleAnimation(WaitAnimation):
    """
    @overview A class implementing a circular loading animation, inheriting from `WaitAnimation`.
    """


    def _run(self) -> None:

        frames = ["◐", "◓", "◑", "◒"]
        index = 0
        interval_time = 0.12


        while not self._stop_event.is_set():

            sys.stdout.write(
                f"\r{self._message} {frames[index % len(frames)]}"
            )
            sys.stdout.flush()

            index += 1

            time.sleep(interval_time)



class IndeterminateBarAnimation(WaitAnimation):
    """
    @overview A class implementing an indeterminate loading bar animation, inheriting 
    from `WaitAnimation`.
    """


    def _run(self) -> None:

        width = 10
        position = 0
        direction = 1
        interval_time = 0.08


        while not self._stop_event.is_set():

            bar = [" "] * width
            bar[position] = "█"

            sys.stdout.write(
                f"\r{self._message} [{' '.join(bar)}]"
            )
            sys.stdout.flush()

            if position == 0:
                direction = 1

            elif position == width - 1:
                direction = -1

            position += direction

            time.sleep(interval_time)
