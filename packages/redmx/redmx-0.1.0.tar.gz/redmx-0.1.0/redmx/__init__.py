"""
Basic Rate Error & Duration (RED) metrics.

Have an object to be able to gather performance metrics.

Examples
--------
>>> import time
>>> from redmx import RateErrorDuration
>>> metrics = RateErrorDuration()
>>> time.sleep(1)
>>> metrics.increment_count(1)
>>> metrics.increment_count(1)
>>> metrics.rate()
>>> print(metrics)

Will produce the following output:

`rate = 1.9904 tps, errors = 0 in 2 (0.0%), duration = 502.4475 milliseconds per transaction.`
"""
import datetime


class RateErrorDuration:
    """RateErrorDuration class."""

    def __init__(self):
        """Initialise an object."""
        self._count = 0
        self._rate = None
        self._errors = 0
        self._duration = None
        self._start_time = datetime.datetime.now().timestamp()

    def __str__(self):
        """Give a usable string representation of the object."""
        message = f'rate = {self.rate()} tps, '
        error_percentage = (self.errors() / self.count()) * 100
        message += f'errors = {self.errors()} in {self.count()} ({round(error_percentage, 4)}%), '
        message += f'duration = {self.duration()} milliseconds per transaction.'
        return message

    def count(self, count=None):
        """
        Get or set the count value for the object.

        Parameters
        ----------
        count : int,optional
            The value to set the count to.

        Returns
        -------
        int
            The count value for the object.
        """
        if count is not None:
            self._count = count
        return self._count

    def duration(self):
        """
        Get or set the average duration of a transaction.

        Returns
        -------
        float
            The average time of a transaction in milliseconds.
        """
        seconds = datetime.datetime.now().timestamp() - self._start_time
        milliseconds = seconds * 1000
        return round(milliseconds / self.count(), 4)

    def errors(self, errors=None):
        """
        Get or set the error count for the object.

        Parameters
        ----------
        errors : int,optional
            The value to set the error count for the object.

        Returns
        -------
        int
            Get the value of the error count for the object.
        """
        if errors is not None:
            self._errors = errors
        return self._errors

    def increment_count(self, count=1):
        """
        Increment the count.

        Parameters
        ----------
        count : int,optional
            The value for the count to be incremented by.  The default value is 1.

        Returns
        -------
        int
            The new count of transactions.
        """
        return self.count(self.count() + count)

    def increment_errors(self, errors=1):
        """
        Increment the number of errors in the object.

        Parameters
        ----------
        errors : int,optional
            The value for the count of errors to be incremented by.  The default value is 1.

        Returns
        -------
        int
            The new value of the error count.
        """
        return self.errors(self.errors() + errors)

    def rate(self):
        """
        Calculate the number of transactions per second.

        Returns
        -------
        float
            The number of transactions per second.
        """
        seconds = datetime.datetime.now().timestamp() - self._start_time
        return round(self.count() / seconds, 4)
