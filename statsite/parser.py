"""
This module implements simple utility functions for
parsing incoming messages.
"""
import re
import messages

LINE_REGEX = re.compile("^([a-zA-Z0-9-.]+):(-?[0-9.]+)\|([a-z]+)(?:\|@([0-9.]+))?$")
"""
Simple Regex used to match stats lines inside incoming messages.
"""

def parse_message(mesg):
    """
    Utility function to parse incoming messages.
    Splits on newlines and parses each line.

    Raises :exc:`ValueError` if any of the lines in
    the message are invalid.

    Returns a list of :class:`Metric` objects.
    """
    lines = mesg.split("\n")
    return [parse_line(line) for line in lines]

def parse_line(line):
    """
    Utility function to parse an incoming line in a message.

    Raises :exc:`ValueError` if the line is invalid or the
    message type if not valid.

    Returns a :class:`Metric` object of the proper subclass.
    """
    match = LINE_REGEX.match(line)
    if match is None:
        raise ValueError, "Invalid line: '%s'" % line
        return

    key, value, type, flag = match.groups()

    # Do type conversion to either float or int
    value = float(value) if "." in value else int(value)
    if flag is not None:
        flag = float(flag) if "." in flag else int(flag)

    # Check for the message types
    if type not in messages.METRIC_TYPES:
        raise ValueError, "Invalid metric type '%s'" % (type)

    # Return the metric object
    return messages.METRIC_TYPE[type](key, value, flag)

