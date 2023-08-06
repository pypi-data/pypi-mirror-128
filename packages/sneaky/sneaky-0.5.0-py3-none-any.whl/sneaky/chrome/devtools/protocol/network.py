BlockedReason = str
CertificateTransparencyCompliance = str
ConnectionType = str
CookieSameSite = str
CorsError = str
ErrorReason = str
Headers = dict
InterceptionId = str
LoaderId = str
MonotonicTime = float
RequestId = str
ResourcePriority = str
ResourceType = str
ServiceWorkerResponseSource = str
TimeSinceEpoch = float


class PostDataEntry:
    bytes: str = None


class WebSocketRequest:
    headers: Headers = None


class CorsErrorStatus:
    corsError: CorsError = None
    failedParameter: str = None


class WebSocketFrame:
    opcode: float = None
    mask: bool = None
    payloadData: str = None


class CachedResource:
    url: str = None
    type: ResourceType = None
    response: "Response" = None
    bodySize: float = None


class Initiator:
    from . import runtime
    type: str = None
    stack: runtime.StackTrace = None
    url: str = None
    lineNumber: float = None
    columnNumber: float = None
    requestId: RequestId = None


class WebSocketResponse:
    status: int = None
    statusText: str = None
    headers: Headers = None
    headersText: str = None
    requestHeaders: Headers = None
    requestHeadersText: str = None


class SignedCertificateTimestamp:
    status: str = None
    origin: str = None
    logDescription: str = None
    logId: str = None
    timestamp: float = None
    hashAlgorithm: str = None
    signatureAlgorithm: str = None
    signatureData: str = None


class CookieParam:
    name: str = None
    value: str = None
    url: str = None
    domain: str = None
    path: str = None
    secure: bool = None
    httpOnly: bool = None
    sameSite: CookieSameSite = None
    expires: TimeSinceEpoch = None
    # priority: CookiePriority = None
    sameParty: bool = None
    # sourceScheme: CookieSourceScheme = None
    sourcePort: int = None


class Request:
    from . import security
    url: str = None
    urlFragment: str = None
    method: str = None
    headers: Headers = None
    postData: str = None
    hasPostData: bool = None
    postDataEntries: list = None
    mixedContentType: security.MixedContentType = None
    initialPriority: ResourcePriority = None
    referrerPolicy: str = None
    isLinkPreload: bool = None
    # trustTokenParams: TrustTokenParams = None
    isSameSite: bool = None


class SecurityDetails:
    from . import security
    protocol: str = None
    keyExchange: str = None
    keyExchangeGroup: str = None
    cipher: str = None
    mac: str = None
    certificateId: security.CertificateId = None
    subjectName: str = None
    sanList: list = None
    issuer: str = None
    validFrom: TimeSinceEpoch = None
    validTo: TimeSinceEpoch = None
    signedCertificateTimestampList: list = None
    certificateTransparencyCompliance: CertificateTransparencyCompliance = None


class Cookie:
    name: str = None
    value: str = None
    domain: str = None
    path: str = None
    expires: float = None
    size: int = None
    httpOnly: bool = None
    secure: bool = None
    session: bool = None
    sameSite: CookieSameSite = None
    # priority: CookiePriority = None
    sameParty: bool = None
    # sourceScheme: CookieSourceScheme = None
    sourcePort: int = None


class ResourceTiming:
    requestTime: float = None
    proxyStart: float = None
    proxyEnd: float = None
    dnsStart: float = None
    dnsEnd: float = None
    connectStart: float = None
    connectEnd: float = None
    sslStart: float = None
    sslEnd: float = None
    workerStart: float = None
    workerReady: float = None
    workerFetchStart: float = None
    workerRespondWithSettled: float = None
    sendStart: float = None
    sendEnd: float = None
    pushStart: float = None
    pushEnd: float = None
    receiveHeadersEnd: float = None


class Response:
    from . import security
    url: str = None
    status: int = None
    statusText: str = None
    headers: Headers = None
    headersText: str = None
    mimeType: str = None
    requestHeaders: Headers = None
    requestHeadersText: str = None
    connectionReused: bool = None
    connectionId: float = None
    remoteIPAddress: str = None
    remotePort: int = None
    fromDiskCache: bool = None
    fromServiceWorker: bool = None
    fromPrefetchCache: bool = None
    encodedDataLength: float = None
    timing: ResourceTiming = None
    serviceWorkerResponseSource: ServiceWorkerResponseSource = None
    responseTime: TimeSinceEpoch = None
    cacheStorageCacheName: str = None
    protocol: str = None
    securityState: security.SecurityState = None
    securityDetails: SecurityDetails = None


class dataReceived:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    dataLength: int = None
    encodedDataLength: int = None


class eventSourceMessageReceived:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    eventName: str = None
    eventId: str = None
    data: str = None


class loadingFailed:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    type: ResourceType = None
    errorText: str = None
    canceled: bool = None
    blockedReason: BlockedReason = None
    corsErrorStatus: CorsErrorStatus = None


class loadingFinished:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    encodedDataLength: float = None
    shouldReportCorbBlocking: bool = None


class requestServedFromCache:
    requestId: RequestId = None


class requestWillBeSent:
    from . import page
    requestId: RequestId = None
    loaderId: LoaderId = None
    documentURL: str = None
    request: Request = None
    timestamp: MonotonicTime = None
    wallTime: TimeSinceEpoch = None
    initiator: Initiator = None
    redirectHasExtraInfo: bool = None
    redirectResponse: Response = None
    type: ResourceType = None
    frameId: page.FrameId = None
    hasUserGesture: bool = None


class responseReceived:
    from . import page
    requestId: RequestId = None
    loaderId: LoaderId = None
    timestamp: MonotonicTime = None
    type: ResourceType = None
    response: Response = None
    hasExtraInfo: bool = None
    frameId: page.FrameId = None


class webSocketClosed:
    requestId: RequestId = None
    timestamp: MonotonicTime = None


class webSocketCreated:
    requestId: RequestId = None
    url: str = None
    initiator: Initiator = None


class webSocketFrameError:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    errorMessage: str = None


class webSocketFrameReceived:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    response: WebSocketFrame = None


class webSocketFrameSent:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    response: WebSocketFrame = None


class webSocketHandshakeResponseReceived:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    response: WebSocketResponse = None


class webSocketWillSendHandshakeRequest:
    requestId: RequestId = None
    timestamp: MonotonicTime = None
    wallTime: TimeSinceEpoch = None
    request: WebSocketRequest = None


class webTransportClosed:
    transportId: RequestId = None
    timestamp: MonotonicTime = None


class webTransportConnectionEstablished:
    transportId: RequestId = None
    timestamp: MonotonicTime = None


class webTransportCreated:
    transportId: RequestId = None
    url: str = None
    timestamp: MonotonicTime = None
    initiator: Initiator = None


