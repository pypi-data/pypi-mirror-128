BreakpointId = str
CallFrameId = str
ScriptLanguage = str


class DebugSymbols:
    type: str = None
    externalURL: str = None


class SearchMatch:
    lineNumber: float = None
    lineContent: str = None


class Location:
    from . import runtime
    scriptId: runtime.ScriptId = None
    lineNumber: int = None
    columnNumber: int = None


class BreakLocation:
    from . import runtime
    scriptId: runtime.ScriptId = None
    lineNumber: int = None
    columnNumber: int = None
    type: str = None


class Scope:
    from . import runtime
    type: str = None
    object: runtime.RemoteObject = None
    name: str = None
    startLocation: Location = None
    endLocation: Location = None


class CallFrame:
    from . import runtime
    callFrameId: CallFrameId = None
    functionName: str = None
    functionLocation: Location = None
    location: Location = None
    url: str = None
    scopeChain: list = None
    this: runtime.RemoteObject = None
    returnValue: runtime.RemoteObject = None


class breakpointResolved:
    breakpointId: BreakpointId = None
    location: Location = None


class paused:
    from . import runtime
    callFrames: list = None
    reason: str = None
    # data: object = None
    hitBreakpoints: list = None
    asyncStackTrace: runtime.StackTrace = None
    # asyncStackTraceId: runtime.StackTraceId = None
    # asyncCallStackTraceId: runtime.StackTraceId = None


class resumed:
    pass


class scriptFailedToParse:
    from . import runtime
    scriptId: runtime.ScriptId = None
    url: str = None
    startLine: int = None
    startColumn: int = None
    endLine: int = None
    endColumn: int = None
    executionContextId: runtime.ExecutionContextId = None
    hash: str = None
    # executionContextAuxData: object = None
    sourceMapURL: str = None
    hasSourceURL: bool = None
    isModule: bool = None
    length: int = None
    stackTrace: runtime.StackTrace = None
    codeOffset: int = None
    scriptLanguage: ScriptLanguage = None
    embedderName: str = None


class scriptParsed:
    from . import runtime
    scriptId: runtime.ScriptId = None
    url: str = None
    startLine: int = None
    startColumn: int = None
    endLine: int = None
    endColumn: int = None
    executionContextId: runtime.ExecutionContextId = None
    hash: str = None
    # executionContextAuxData: object = None
    isLiveEdit: bool = None
    sourceMapURL: str = None
    hasSourceURL: bool = None
    isModule: bool = None
    length: int = None
    stackTrace: runtime.StackTrace = None
    codeOffset: int = None
    scriptLanguage: ScriptLanguage = None
    debugSymbols: DebugSymbols = None
    embedderName: str = None


