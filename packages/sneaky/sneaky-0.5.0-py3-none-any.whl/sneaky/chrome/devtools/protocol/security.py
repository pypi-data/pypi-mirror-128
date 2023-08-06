CertificateErrorAction = str
CertificateId = int
MixedContentType = str
SecurityState = str


class SecurityStateExplanation:
    securityState: SecurityState = None
    title: str = None
    summary: str = None
    description: str = None
    mixedContentType: MixedContentType = None
    certificate: list = None
    recommendations: list = None


