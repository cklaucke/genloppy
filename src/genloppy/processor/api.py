class Interface:
    """
    Provides the processor API

    realizes: R-PROCESSOR-API-001
    """
    @property
    def callbacks(self):
        """Returns a dict of modes and associated callbacks to be subscribed.

        realizes: R-PROCESSOR-API-003"""
        raise NotImplementedError

    def pre_process(self):
        """Does pre-processing before parsing has begun.

        realizes: R-PROCESSOR-API-002"""
        raise NotImplementedError

    def post_process(self):
        """Does post-processing after parsing has finished.

        realizes: R-PROCESSOR-API-004"""
        raise NotImplementedError
