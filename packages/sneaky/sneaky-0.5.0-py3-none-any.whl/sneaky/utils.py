from copy import deepcopy
from lxml import html
import requests
import os


def fetch_domain(s: requests.Session, url, target_path):
    domain = url.split("/")[-2].lower()
    target_path = os.path.join(target_path, "chrome", "devtools", "protocol", domain)
    fp = target_path+".py"
    # os.makedirs(target_path, exist_ok=True)
    r = s.get(url)
    r = html.fromstring(r.content.decode())
    _types = r.xpath("//h3[@id='types']/following-sibling::div[1]/div[@class='details']")
    types = []
    types_b = b""
    for type in _types:
        imports = []
        name = "".join(type.xpath("./h4/text()")).strip()
        meta_type = type.xpath("./p/strong/text()")[0].strip()
        if meta_type == "string":
            meta_type = str
        elif meta_type == "number":
            meta_type = float
        elif meta_type == "integer":
            meta_type = int
        elif meta_type == "boolean":
            meta_type = bool
        elif "array" in meta_type:
            meta_type = list
        properties = [
            [_.strip() for _ in type.xpath("./dl/dt/text()")],
            type.xpath("./dl/dd"),
        ]
        for i in range(0, len(properties[1])):
            property_meta_type = properties[1][i].xpath("./*[1]")[0]
            if property_meta_type.tag == "span":
                property_meta_type = property_meta_type.xpath("./text()")[0].strip()
                if property_meta_type == "string":
                    property_meta_type = str
                elif property_meta_type == "number":
                    property_meta_type = float
                elif property_meta_type == "integer":
                    property_meta_type = int
                elif property_meta_type == "boolean":
                    property_meta_type = bool
                elif "array" in property_meta_type:
                    property_meta_type = list
                properties[1][i] = property_meta_type
            else:
                properties[1][i] = property_meta_type.xpath("./text()")[0].strip()
                if properties[1][i].lower().startswith(domain+"."):
                    properties[1][i] = properties[1][i][len(domain+"."):]
                if "." in properties[1][i]:
                    properties[1][i] = properties[1][i].split(".")[0].lower()+"."+properties[1][i].split(".")[1]
                    imports.append(properties[1][i].split(".")[0])
        if meta_type == "object" and not properties[0]:
            meta_type = dict
        types.append([name, meta_type, properties, imports])
    if types_b:
        types_b += "\n\n".encode()
    print(domain)
    print("types")
    [print(_[0]) for _ in types]
    print()
    def get_meta_type_by_name(_name):
        for name, meta_type, properties, imports in types2:
            if name == _name:
                return meta_type
    def sort_key(type):
        name, meta_type, properties, imports = type
        # if name == "CachedResource":
        #     print([
        #         [
        #             isinstance(_, str) and [
        #             _,
        #             get_meta_type_by_name(_),
        #             not isclass(get_meta_type_by_name(_)) if get_meta_type_by_name(_) else None,
        #             isinstance(_, str) and not isclass(get_meta_type_by_name(_)) if get_meta_type_by_name(_) else None,
        #                 ]
        #         ] for _ in properties[1]
        #     ])
        #     print(any([
        #         isinstance(_, str) and not isclass(get_meta_type_by_name(_)) if get_meta_type_by_name(_) else None
        #          for _ in properties[1]
        #     ]))
        if isinstance(meta_type, str):
            return 1, 0, len(properties[0]), name
        elif any(isinstance(_, str) and isinstance(get_meta_type_by_name(_), str) if get_meta_type_by_name(_) else None for _ in properties[1]):
            return -1, 1, len(properties[0]), name
        else:
            return -1, -1, len(properties[0]), name
    types2 = deepcopy(types)
    types.sort(key=sort_key)
    for name, meta_type, properties, imports in types:
        if meta_type == "object":
            continue
        # print(name, meta_type, properties)
        types_b += '''{} = {}\n'''.format(name, meta_type.__name__).encode()
    if types_b:
        types_b += "\n\n".encode()
    for name, meta_type, properties, imports in types:
        if meta_type != "object":
            continue
        # print(name, meta_type, properties)
        # if not properties[0]:
        #     print(name, meta_type, properties)
        properties = "".join(["    {}{}: {} = None\n".format(
            "# " if isinstance(properties[1][i], str) and "." not in properties[1][i] and properties[1][i] not in [_[0] for _ in types] else "",
            properties[0][i],
            properties[1][i] if isinstance(properties[1][i], str) else properties[1][i].__name__,
        ) for i in range(0, len(properties[0]))])
        types_b += '''class {}:\n{}{}\n\n'''.format(name, "".join("    from . import {}\n".format(_) for _ in list(set(imports))), properties).encode()
    _events = r.xpath("//h3[@id='events']/following-sibling::div[1]/div[@class='details']")
    events = []
    events_b = b""
    for event in _events:
        name = "".join(event.xpath("./h4/text()")).strip()
        parameters = [
            [_.strip() for _ in event.xpath("./dl/dt/text()")],
            event.xpath("./dl/dd"),
        ]
        imports = []
        for i in range(0, len(parameters[1])):
            parameter_meta_type = parameters[1][i].xpath("./*[1]")[0]
            if parameter_meta_type.tag == "span":
                parameter_meta_type = parameter_meta_type.xpath("./text()")[0].strip()
                if parameter_meta_type == "string":
                    parameter_meta_type = str
                elif parameter_meta_type == "number":
                    parameter_meta_type = float
                elif parameter_meta_type == "integer":
                    parameter_meta_type = int
                elif parameter_meta_type == "boolean":
                    parameter_meta_type = bool
                elif "array" in parameter_meta_type:
                    parameter_meta_type = list
                parameters[1][i] = parameter_meta_type
            else:
                parameters[1][i] = parameter_meta_type.xpath("./text()")[0].strip()
                if parameters[1][i].lower().startswith(domain+"."):
                    parameters[1][i] = parameters[1][i][len(domain+"."):]
                if "." in parameters[1][i]:
                    parameters[1][i] = parameters[1][i].split(".")[0].lower()+"."+parameters[1][i].split(".")[1]
                    imports.append(parameters[1][i].split(".")[0])
        events.append([name, parameters, imports])
    for name, parameters, imports in events:
        if parameters[0]:
            parameters = "".join(["    {}{}: {} = None\n".format(
                "# " if isinstance(parameters[1][i], str) and "." not in parameters[1][i] and parameters[1][i] not in [_[0] for _ in types] else "",
                parameters[0][i],
                parameters[1][i] if isinstance(parameters[1][i], str) else parameters[1][i].__name__,
            ) for i in range(0, len(parameters[0]))])
        else:
            parameters = "    pass\n"
        events_b += '''class {}:\n{}{}\n\n'''.format(name, "".join("    from . import {}\n".format(_) for _ in list(set(imports))), parameters).encode()
    open(fp, "wb").write(types_b+events_b)
    print("events")
    [print(_[0]) for _ in events]
    print()
    print()
    return domain


if __name__ == "__main__":
    target_path = os.path.dirname(os.path.abspath(__file__))
    s = requests.Session()
    url = "https://chromedevtools.github.io/devtools-protocol/1-3/{}/"
    urls = [
        url.format("Browser"),
        url.format("Debugger"),
        url.format("DOM"),
        url.format("DOMDebugger"),
        url.format("Emulation"),
        url.format("Input"),
        url.format("IO"),
        url.format("Log"),
        url.format("Network"),
        url.format("Page"),
        url.format("Performance"),
        url.format("Profiler"),
        url.format("Runtime"),
        url.format("Security"),
        url.format("Target"),
    ]
    domains = [fetch_domain(s, url, target_path) for url in urls]
    # open(os.path.join(target_path, "chrome", "devtools", "protocol", "__init__.py"), "wb").write(("".join("from .{} import *\n".format(_) for _ in domains)+"\n").encode())



