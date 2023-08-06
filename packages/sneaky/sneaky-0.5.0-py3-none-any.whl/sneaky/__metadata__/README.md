# sneaky

<badges>[![version](https://img.shields.io/pypi/v/sneaky.svg)](https://pypi.org/project/sneaky/)
[![license](https://img.shields.io/pypi/l/sneaky.svg)](https://pypi.org/project/sneaky/)
[![pyversions](https://img.shields.io/pypi/pyversions/sneaky.svg)](https://pypi.org/project/sneaky/)  
[![powered](https://img.shields.io/badge/Say-Thanks-ddddff.svg)](https://saythanks.io/to/foxe6)
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>A sneaky web bot based on Selenium driven by ChromeDriver equipped with undetected-chromedriver (as bot detection bypass), Buster (as a reCAPTCHA solver), eavesdropper (as traffic interceptor), vpncmd (as free VPN rotator) let you breach the Internet as you please.</i>

# Hierarchy

```
sneaky
|---- SNEAKY()
|   |---- traffic
|   |---- request_traffic
|   |---- response_traffic
|   |---- capture_traffic()
|   |---- capture_request_traffic()
|   |---- capture_response_traffic()
|   |---- stop_capture_traffic()
|   |---- stop_capture_request_traffic()
|   |---- stop_capture_response_traffic()
|   |---- clear_traffic()
|   |---- clear_request_traffic()
|   |---- clear_response_traffic()
|   |---- quit()
|   |---- vpncmd # see https://github.com/foxe6/vpncmd#hierarchy
|   '---- driver # see https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver
|       |---- wait()
|       |---- sleep_random()
|       |---- format_element()
|       |---- print_element()
|       |---- pretty_format_element()
|       |---- pretty_print_element()
|       |---- get_console_log()
|       |---- is_xpath()
|       |---- exist()
|       |---- expand_shadow_dom()
|       |---- xpath()
|       |---- querySelectorAll()
|       |---- get_client_viewport_size()
|       |---- move_by_offset()
|       |---- move_to_xy()
|       |---- move_to_element()
|       |---- click()
|       |---- send_input()
|       |---- mimic_move_to_random_xy()
|       |---- mimic_move_to_xy()
|       |---- mimic_move_to_element()
|       |---- mimic_click_xy()
|       |---- mimic_click()
|       |---- mimic_send_chord()
|       '---- mimic_send_input()
|---- Keys()
|   |---- chord()
|   |   |---- keys
|   |   |---- actions()
|   |   '---- perform()
|   |---- pause()
|   |   |---- sec
|   |   '---- pause()
|   '---- pause_random()
|       |---- sec
|       '---- pause()
'---- chrome
    |---- Chrome()
    '---- devtools
        '---- protocol
            |---- browser
            |---- debugger
            |   |---- BreakLocation()
            |   |---- BreakpointId
            |   |---- CallFrame()
            |   |---- CallFrameId
            |   |---- DebugSymbols()
            |   |---- Location()
            |   |---- Scope()
            |   |---- ScriptLanguage
            |   |---- SearchMatch()
            |   |---- breakpointResolved()
            |   |---- paused()
            |   |---- resumed()
            |   |---- scriptFailedToParse()
            |   '---- scriptParsed()
            |---- dom
            |   |---- BackendNodeId
            |   |---- CompatibilityMode
            |   |---- NodeId
            |   |---- PseudoType
            |   |---- Quad
            |   |---- ShadowRootType
            |   |---- CSSComputedStyleProperty()
            |   |---- BackendNode()
            |   |---- ShapeOutsideInfo()
            |   |---- RGBA()
            |   |---- Rect()
            |   |---- BoxModel()
            |   |---- Node()
            |   |---- attributeModified()
            |   |---- attributeRemoved()
            |   |---- characterDataModified()
            |   |---- childNodeCountUpdated()
            |   |---- childNodeInserted()
            |   |---- childNodeRemoved()
            |   |---- documentUpdated()
            |   '---- setChildNodes()
            |---- domdebugger
            |   |---- DOMBreakpointType
            |   '---- EventListener()
            |---- emulation
            |   |---- MediaFeature()
            |   |---- ScreenOrientation()
            |   '---- DisplayFeature()
            |---- input
            |   |---- MouseButton
            |   |---- TimeSinceEpoch
            |   '---- TouchPoint()
            |---- io
            |   '---- StreamHandle
            |---- log
            |   |---- ViolationSetting()
            |   |---- LogEntry()
            |   '---- entryAdded()
            |---- network
            |   |---- BlockedReason
            |   |---- CertificateTransparencyCompliance
            |   |---- ConnectionType
            |   |---- CookieSameSite
            |   |---- CorsError
            |   |---- ErrorReason
            |   |---- Headers
            |   |---- InterceptionId
            |   |---- LoaderId
            |   |---- MonotonicTime
            |   |---- RequestId
            |   |---- ResourcePriority
            |   |---- ResourceType
            |   |---- ServiceWorkerResponseSource
            |   |---- TimeSinceEpoch
            |   |---- PostDataEntry()
            |   |---- WebSocketRequest()
            |   |---- CorsErrorStatus()
            |   |---- WebSocketFrame()
            |   |---- CachedResource()
            |   |---- Initiator()
            |   |---- WebSocketResponse()
            |   |---- SignedCertificateTimestamp()
            |   |---- CookieParam()
            |   |---- Request()
            |   |---- SecurityDetails()
            |   |---- Cookie()
            |   |---- ResourceTiming()
            |   |---- Response()
            |   |---- dataReceived()
            |   |---- eventSourceMessageReceived()
            |   |---- loadingFailed()
            |   |---- loadingFinished()
            |   |---- requestServedFromCache()
            |   |---- requestWillBeSent()
            |   |---- responseReceived()
            |   |---- webSocketClosed()
            |   |---- webSocketCreated()
            |   |---- webSocketFrameError()
            |   |---- webSocketFrameReceived()
            |   |---- webSocketFrameSent()
            |   |---- webSocketHandshakeResponseReceived()
            |   |---- webSocketWillSendHandshakeRequest()
            |   |---- webTransportClosed()
            |   |---- webTransportConnectionEstablished()
            |   '---- webTransportCreated()
            |---- page
            |   |---- DialogType
            |   |---- FrameId
            |   |---- ScriptIdentifier
            |   |---- TransitionType
            |   |---- FrameTree()
            |   |---- AppManifestError()
            |   |---- LayoutViewport()
            |   |---- NavigationEntry()
            |   |---- Viewport()
            |   |---- VisualViewport()
            |   |---- Frame()
            |   |---- domContentEventFired()
            |   |---- fileChooserOpened()
            |   |---- frameAttached()
            |   |---- frameDetached()
            |   |---- frameNavigated()
            |   |---- interstitialHidden()
            |   |---- interstitialShown()
            |   |---- javascriptDialogClosed()
            |   |---- javascriptDialogOpening()
            |   |---- lifecycleEvent()
            |   |---- loadEventFired()
            |   '---- windowOpen()
            |---- performance
            |   |---- Metric()
            |   '---- metrics()
            |---- profiler
            |   |---- PositionTickInfo()
            |   |---- CoverageRange()
            |   |---- FunctionCoverage()
            |   |---- ScriptCoverage()
            |   |---- Profile()
            |   |---- ProfileNode()
            |   |---- consoleProfileFinished()
            |   '---- consoleProfileStarted()
            |---- runtime
            |   |---- ExecutionContextId
            |   |---- RemoteObjectId
            |   |---- ScriptId
            |   |---- TimeDelta
            |   |---- Timestamp
            |   |---- UnserializableValue
            |   |---- InternalPropertyDescriptor()
            |   |---- CallArgument()
            |   |---- StackTrace()
            |   |---- CallFrame()
            |   |---- ExecutionContextDescription()
            |   |---- RemoteObject()
            |   |---- ExceptionDetails()
            |   |---- PropertyDescriptor()
            |   |---- consoleAPICalled()
            |   |---- exceptionRevoked()
            |   |---- exceptionThrown()
            |   |---- executionContextCreated()
            |   |---- executionContextDestroyed()
            |   |---- executionContextsCleared()
            |   '---- inspectRequested()
            |---- security
            |   |---- CertificateErrorAction
            |   |---- CertificateId
            |   |---- MixedContentType
            |   |---- SecurityState
            |   '---- SecurityStateExplanation()
            '---- target
                |---- SessionID
                |---- TargetID
                |---- TargetInfo()
                |---- receivedMessageFromTarget()
                |---- targetCrashed()
                |---- targetCreated()
                |---- targetDestroyed()
                '---- targetInfoChanged()
```

# Demo

[![sneaky](https://img.youtube.com/vi/yEm3Sbm30js/0.jpg)](https://www.youtube.com/watch?v=yEm3Sbm30js)

# Example

## python
See `test`.