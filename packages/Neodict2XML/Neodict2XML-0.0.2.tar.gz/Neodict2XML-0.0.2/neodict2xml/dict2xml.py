from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='    ')

def from_dict(dict_):
    top_key = list(dict_.keys())[0]
    top = Element(top_key)

    _from_dict_rec(dict_, top_key, top)
    return top

def _from_dict_rec(dict_, top_key, top):
    if isinstance(dict_[top_key], dict):
        for key in dict_[top_key].keys():
            if isinstance(dict_[top_key][key], list):
                tmp_dict = dict_.copy()
                for element in dict_[top_key][key]:
                    ntop = SubElement(top, key)
                    tmp_dict[top_key] = element
                    _from_dict_rec(tmp_dict, top_key, ntop)
            else:
                ntop = SubElement(top, key)
                _from_dict_rec(dict_[top_key], key, ntop)

    elif isinstance(dict_[top_key], tuple):
        for key, value in dict_[top_key][0].items():
            top.set(key, str(value))
        if len(dict_[top_key]) == 2:
            dict_[top_key] = dict_[top_key][1]
            _from_dict_rec(dict_, top_key, top)

    else:
        top.text = str(dict_[top_key])
