class ViolationSetting:
    name: str = None
    threshold: float = None


class LogEntry:
    from . import runtime
    from . import network
    source: str = None
    level: str = None
    text: str = None
    category: str = None
    timestamp: runtime.Timestamp = None
    url: str = None
    lineNumber: int = None
    stackTrace: runtime.StackTrace = None
    networkRequestId: network.RequestId = None
    workerId: str = None
    args: list = None


class entryAdded:
    entry: LogEntry = None


