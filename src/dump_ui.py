import uiautomator2 as u2
import xml.etree.ElementTree as ET


def parse_dump(xml_string):
    """
    Parses the XML output of d.dump() and returns a dictionary of UI elements.
    """
    root = ET.fromstring(xml_string)
    elements = {}
    for node in root.iter():
        if node.tag == "node":
            element = {
                "class": node.attrib.get("class", ""),
                "bounds": node.attrib.get("bounds", ""),
                "text": node.attrib.get("text", ""),
                "resource_id": node.attrib.get("resource-id", ""),
                "content_desc": node.attrib.get("content-desc", ""),
                "package": node.attrib.get("package", ""),
                "checkable": node.attrib.get("checkable", "false") == "true",
                "checked": node.attrib.get("checked", "false") == "true",
                "clickable": node.attrib.get("clickable", "false") == "true",
                "enabled": node.attrib.get("enabled", "false") == "true",
                "focusable": node.attrib.get("focusable", "false") == "true",
                "focused": node.attrib.get("focused", "false") == "true",
                "scrollable": node.attrib.get("scrollable", "false") == "true",
                "long_clickable": node.attrib.get("long-clickable", "false") == "true",
                "password": node.attrib.get("password", "false") == "true",
                "selected": node.attrib.get("selected", "false") == "true",
                "child_count": len(node.findall("node")),
            }
            elements[node.attrib.get("resource-id", "")] = element
    return elements


def dump_ui(device_name='38534a424c453098'):
    d = u2.connect_usb(device_name)
    page_source = d.dump_hierarchy(pretty=True)
    r = parse_dump(page_source)
    return r


def dump_ui_with_connection(d):
    page_source = d.dump_hierarchy(pretty=True)
    r = parse_dump(page_source)
    return r
