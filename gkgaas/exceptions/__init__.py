class WrongExecutablePath(Exception):
    pass


class RunnerExecutionFailed(Exception):
    pass


class ProtocolNotSupportedException(Exception):
    """
    This is exception is thrown when a Tpio ID is translated to a local ID
    which cannot be handled by the Topio KG service. This could be, e.g. when
    the local ID is an HDFS identifire like hdfs:///org/my_file.nt which cannot
    be resolved without HDFS support
    """

    def __init__(self, msg):
        self.msg = msg
