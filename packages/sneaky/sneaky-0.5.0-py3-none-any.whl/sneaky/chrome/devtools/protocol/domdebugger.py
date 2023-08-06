DOMBreakpointType = str


class EventListener:
    from . import runtime
    from . import dom
    type: str = None
    useCapture: bool = None
    passive: bool = None
    once: bool = None
    scriptId: runtime.ScriptId = None
    lineNumber: int = None
    columnNumber: int = None
    handler: runtime.RemoteObject = None
    originalHandler: runtime.RemoteObject = None
    backendNodeId: dom.BackendNodeId = None


