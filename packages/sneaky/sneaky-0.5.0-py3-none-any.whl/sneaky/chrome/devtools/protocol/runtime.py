ExecutionContextId = int
RemoteObjectId = str
ScriptId = str
TimeDelta = float
Timestamp = float
UnserializableValue = str


class InternalPropertyDescriptor:
    name: str = None
    value: "RemoteObject" = None


class CallArgument:
    # value: any = None
    unserializableValue: UnserializableValue = None
    objectId: RemoteObjectId = None


class StackTrace:
    description: str = None
    callFrames: list = None
    parent: "StackTrace" = None
    # parentId: StackTraceId = None


class CallFrame:
    functionName: str = None
    scriptId: ScriptId = None
    url: str = None
    lineNumber: int = None
    columnNumber: int = None


class ExecutionContextDescription:
    id: ExecutionContextId = None
    origin: str = None
    name: str = None
    uniqueId: str = None
    # auxData: object = None


class RemoteObject:
    type: str = None
    subtype: str = None
    className: str = None
    # value: any = None
    unserializableValue: UnserializableValue = None
    description: str = None
    objectId: RemoteObjectId = None
    # preview: ObjectPreview = None
    # customPreview: CustomPreview = None


class ExceptionDetails:
    exceptionId: int = None
    text: str = None
    lineNumber: int = None
    columnNumber: int = None
    scriptId: ScriptId = None
    url: str = None
    stackTrace: StackTrace = None
    exception: RemoteObject = None
    executionContextId: ExecutionContextId = None
    # exceptionMetaData: object = None


class PropertyDescriptor:
    name: str = None
    value: RemoteObject = None
    writable: bool = None
    get: RemoteObject = None
    set: RemoteObject = None
    configurable: bool = None
    enumerable: bool = None
    wasThrown: bool = None
    isOwn: bool = None
    symbol: RemoteObject = None


class consoleAPICalled:
    type: str = None
    args: list = None
    executionContextId: ExecutionContextId = None
    timestamp: Timestamp = None
    stackTrace: StackTrace = None
    context: str = None


class exceptionRevoked:
    reason: str = None
    exceptionId: int = None


class exceptionThrown:
    timestamp: Timestamp = None
    exceptionDetails: ExceptionDetails = None


class executionContextCreated:
    context: ExecutionContextDescription = None


class executionContextDestroyed:
    executionContextId: ExecutionContextId = None


class executionContextsCleared:
    pass


class inspectRequested:
    object: RemoteObject = None
    # hints: object = None
    executionContextId: ExecutionContextId = None


