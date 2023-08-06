import json_tricks


class DataWrapper(object):
    """Class implementing data wrapper (wrapping and unwrapping data)"""

    @staticmethod
    def unwrap_data(data):
        """Unwraps the data (deserialize from JSON-string to numpy.ndarray)"""
        return json_tricks.loads(data) if isinstance(data, str) else data

    @staticmethod
    def wrap_data(data):
        """Wraps the data (serialize numpy.ndarray to JSON-string)"""
        return json_tricks.dumps(data, allow_nan=True) if not isinstance(data, str) else data
