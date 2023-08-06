SessionID = str
TargetID = str


class TargetInfo:
    from . import page
    from . import browser
    targetId: TargetID = None
    type: str = None
    title: str = None
    url: str = None
    attached: bool = None
    openerId: TargetID = None
    canAccessOpener: bool = None
    openerFrameId: page.FrameId = None
    # browserContextId: browser.BrowserContextID = None


class receivedMessageFromTarget:
    sessionId: SessionID = None
    message: str = None
    targetId: TargetID = None


class targetCrashed:
    targetId: TargetID = None
    status: str = None
    errorCode: int = None


class targetCreated:
    targetInfo: TargetInfo = None


class targetDestroyed:
    targetId: TargetID = None


class targetInfoChanged:
    targetInfo: TargetInfo = None


