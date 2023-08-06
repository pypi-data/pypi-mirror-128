DialogType = str
FrameId = str
ScriptIdentifier = str
TransitionType = str


class FrameTree:
    frame: "Frame" = None
    childFrames: list = None


class AppManifestError:
    message: str = None
    critical: int = None
    line: int = None
    column: int = None


class LayoutViewport:
    pageX: int = None
    pageY: int = None
    clientWidth: int = None
    clientHeight: int = None


class NavigationEntry:
    id: int = None
    url: str = None
    userTypedURL: str = None
    title: str = None
    transitionType: TransitionType = None


class Viewport:
    x: float = None
    y: float = None
    width: float = None
    height: float = None
    scale: float = None


class VisualViewport:
    offsetX: float = None
    offsetY: float = None
    pageX: float = None
    pageY: float = None
    clientWidth: float = None
    clientHeight: float = None
    scale: float = None
    zoom: float = None


class Frame:
    from . import network
    id: FrameId = None
    parentId: FrameId = None
    loaderId: network.LoaderId = None
    name: str = None
    url: str = None
    urlFragment: str = None
    domainAndRegistry: str = None
    securityOrigin: str = None
    mimeType: str = None
    unreachableUrl: str = None
    # adFrameStatus: AdFrameStatus = None
    # secureContextType: SecureContextType = None
    # crossOriginIsolatedContextType: CrossOriginIsolatedContextType = None
    gatedAPIFeatures: list = None


class domContentEventFired:
    from . import network
    timestamp: network.MonotonicTime = None


class fileChooserOpened:
    from . import dom
    frameId: FrameId = None
    backendNodeId: dom.BackendNodeId = None
    mode: str = None


class frameAttached:
    from . import runtime
    frameId: FrameId = None
    parentFrameId: FrameId = None
    stack: runtime.StackTrace = None


class frameDetached:
    frameId: FrameId = None
    reason: str = None


class frameNavigated:
    frame: Frame = None
    # type: NavigationType = None


class interstitialHidden:
    pass


class interstitialShown:
    pass


class javascriptDialogClosed:
    result: bool = None
    userInput: str = None


class javascriptDialogOpening:
    url: str = None
    message: str = None
    type: DialogType = None
    hasBrowserHandler: bool = None
    defaultPrompt: str = None


class lifecycleEvent:
    from . import network
    frameId: FrameId = None
    loaderId: network.LoaderId = None
    name: str = None
    timestamp: network.MonotonicTime = None


class loadEventFired:
    from . import network
    timestamp: network.MonotonicTime = None


class windowOpen:
    url: str = None
    windowName: str = None
    windowFeatures: list = None
    userGesture: bool = None


