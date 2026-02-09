
class CancellationToken:
    """
    @overview A class to support cancellation of long-running operations.

    General responsibilities:
      - Expose a cancellation flag
      - Allow cancellation via setter or explicit method
      - Raise an exception when the operation is cancelled
    """


    def __init__(self):
        """
        @overview A magic method that initializes the `token` in a non-cancelled state (`False` bool value).
        """

        self.__flag_cancelled = False



    @property
    def is_cancelled(self) -> bool:
        """
        @overview A property method to get the state of the `token`.
        """

        return self.__flag_cancelled 



    @is_cancelled.setter
    def is_cancelled(self, the_token_state: bool) -> None:
        """
        @overview A property method that updates the `token` state with the given `bool` value.

        :param the_token_state {bool} - The new state of the `token`.
        """

        self.__flag_cancelled = bool(the_token_state)



    def check_cancel(self):
        """
        @overview A method that raises an exception if the `token` state is set to `True`.

        :raises {OperationCancelledError} - The raised exception when the `token` state is `True`.
        """

        if self.__flag_cancelled:
            raise OperationCancelledError("\n ⚠️  Operation interrupted by the user  🔌")



class OperationCancelledError(Exception):
    """
    @overview An exception to raise when an operation is cancelled.
    """

    pass
