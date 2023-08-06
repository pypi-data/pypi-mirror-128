BackendNodeId = int
CompatibilityMode = str
NodeId = int
PseudoType = str
Quad = list
ShadowRootType = str


class CSSComputedStyleProperty:
    name: str = None
    value: str = None


class BackendNode:
    nodeType: int = None
    nodeName: str = None
    backendNodeId: BackendNodeId = None


class ShapeOutsideInfo:
    bounds: Quad = None
    shape: list = None
    marginShape: list = None


class RGBA:
    r: int = None
    g: int = None
    b: int = None
    a: float = None


class Rect:
    x: float = None
    y: float = None
    width: float = None
    height: float = None


class BoxModel:
    content: Quad = None
    padding: Quad = None
    border: Quad = None
    margin: Quad = None
    width: int = None
    height: int = None
    shapeOutside: ShapeOutsideInfo = None


class Node:
    from . import page
    nodeId: NodeId = None
    parentId: NodeId = None
    backendNodeId: BackendNodeId = None
    nodeType: int = None
    nodeName: str = None
    localName: str = None
    nodeValue: str = None
    childNodeCount: int = None
    children: list = None
    attributes: list = None
    documentURL: str = None
    baseURL: str = None
    publicId: str = None
    systemId: str = None
    internalSubset: str = None
    xmlVersion: str = None
    name: str = None
    value: str = None
    pseudoType: PseudoType = None
    shadowRootType: ShadowRootType = None
    frameId: page.FrameId = None
    contentDocument: "Node" = None
    shadowRoots: list = None
    templateContent: "Node" = None
    pseudoElements: list = None
    importedDocument: "Node" = None
    distributedNodes: list = None
    isSVG: bool = None
    compatibilityMode: CompatibilityMode = None


class attributeModified:
    nodeId: NodeId = None
    name: str = None
    value: str = None


class attributeRemoved:
    nodeId: NodeId = None
    name: str = None


class characterDataModified:
    nodeId: NodeId = None
    characterData: str = None


class childNodeCountUpdated:
    nodeId: NodeId = None
    childNodeCount: int = None


class childNodeInserted:
    parentNodeId: NodeId = None
    previousNodeId: NodeId = None
    node: Node = None


class childNodeRemoved:
    parentNodeId: NodeId = None
    nodeId: NodeId = None


class documentUpdated:
    pass


class setChildNodes:
    parentId: NodeId = None
    nodes: list = None


