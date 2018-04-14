import json
import xml.etree.ElementTree as etree


class CData:
    def __init__(self, data: dict):
        self.data = '<![CDATA[' + json.dumps(data) + ']]>'

    def __str__(self):
        return self.data


def _dump_node(tree: dict) -> str:
    rst = ''
    for key, value in tree.items():
        if isinstance(value, dict):
            value = _dump_node(value)
        rst += '<{key}>{value}</{key}>'.format(key=key, value=value)
    return rst


def _load_node(node) -> dict:
    rst = {}
    for child in node:
        if len(child):
            rst[child.tag] = _load_node(child)
        else:
            rst[child.tag] = child.text
    return rst


def dumps(tree: dict) -> str:
    return '<xml>' + _dump_node(tree) + '</xml>'


def loads(text: str) -> dict:
    return _load_node(etree.fromstring(text))
