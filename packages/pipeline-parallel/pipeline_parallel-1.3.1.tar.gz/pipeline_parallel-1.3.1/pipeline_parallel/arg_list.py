import logging
import numpy as np

from .utils import get_jwst_miri_expected_ram

LOG = logging.getLogger('pipeline_parallel.ArgList')


class ArgList(object):
    def __init__(self, args, ram=None):
        """
        Simple class to store and return args for pipeline handling

        Files are weighted depending on the RAM they're expected
        to take while the pipeline runs

        Files are stored with biggest weight first

        If, for each call, only one item is given, ArgList ensures that it's wrapped in a 1-item tuple for each call.

        :param args: List of args
        :type args: list(str)

        :param ram: [optional] For each file, the expected RAM consumption (upper limit)
            If not given, will launch the "get_jwst_miri_expected_ram" function to estimate it (valid for JWST 1B data)
        :type ram: list(float)

        """

        if len(args) != len(set(args)):
            LOG.warning("Input arg contain duplicates.")

        if not args:
            raise ValueError("args parameter is an empty list")

        if ram is not None:
            if len(ram) != len(args):
                raise ValueError("Error: In ArgList, ram and args list must be the same size.")
            weight = ram
        else:
            weight = get_jwst_miri_expected_ram(args)

        # If each arg is a single value and not a tuple, we create a tuple of 1 element for each
        if not isinstance(args[0], tuple):
            args = list(zip(args))  # Transform [1, 2] into [(1,), (2,)]

        # Sort items with biggest weight first
        tmp = sorted(zip(weight, args), reverse=True)
        (self.weight, self.args) = zip(*tmp)
        self.weight = list(self.weight)
        self.args = list(self.args)

        self.initial_size = len(self.args)
        self.size = self.initial_size

    def get_next_item(self, max_weight):
        """
        Delete the returned file from the list in the process.

        :param max_weight: max weight allowed for the next file (lower or equal will be valid)
        :type max_weight: float

        :return: args and associated weight. In case no item correspond to the request, will return
        (None, None)
        :rtype: (tuple, float)
        """

        try:
            first_id = np.where(np.array(self.weight) <= max_weight)[0][0]

            args = self.args.pop(first_id)
            weight = self.weight.pop(first_id)
            self.size -= 1

        except IndexError:
            args = None
            weight = None

        return args, weight

    def __bool__(self):
        """
        Considered True if not empty

        :return: True if not empty, False if empty
        :rtype: bool
        """

        return bool(self.args)
