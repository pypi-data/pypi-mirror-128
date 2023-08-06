class PositionTickInfo:
    line: int = None
    ticks: int = None


class CoverageRange:
    startOffset: int = None
    endOffset: int = None
    count: int = None


class FunctionCoverage:
    functionName: str = None
    ranges: list = None
    isBlockCoverage: bool = None


class ScriptCoverage:
    from . import runtime
    scriptId: runtime.ScriptId = None
    url: str = None
    functions: list = None


class Profile:
    nodes: list = None
    startTime: float = None
    endTime: float = None
    samples: list = None
    timeDeltas: list = None


class ProfileNode:
    from . import runtime
    id: int = None
    callFrame: runtime.CallFrame = None
    hitCount: int = None
    children: list = None
    deoptReason: str = None
    positionTicks: list = None


class consoleProfileFinished:
    from . import debugger
    id: str = None
    location: debugger.Location = None
    profile: Profile = None
    title: str = None


class consoleProfileStarted:
    from . import debugger
    id: str = None
    location: debugger.Location = None
    title: str = None


