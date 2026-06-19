"""
Module to make XML files editable by LLM
eliminating the risk of altering the XML structure
"""
from xml.etree.ElementTree import ElementTree, Element

# No autocomplete for lxml (c binding)... TODO: improve that
from lxml import etree

from libs.utils.xmlzip import extract_content_xml_from_zip


def node_xpath(node: Element):
    return node.getroottree().getpath(node)


def xml_file_to_selectable_text_map(xml_content: str) -> dict[str, str]:
    """
    xml_content:

    Example result: 
    {'/w:document/w:body/w:p[1]/w:r/w:t': 'Title', '/w:document/w:body/w:p[2]/w:r/w:t': 'P1 content', '/w:document/w:body/w:p[3]/w:r[1]/w:t': 'P2 content with', '/w:document/w:body/w:p[3]/w:r[2]/w:t': 'bold', '/w:document/w:body/w:p[3]/w:r[3]/w:t': 'text', '/w:document/w:body/w:p[4]/w:r/w:t': 'Li1', '/w:document/w:body/w:p[5]/w:r/w:t': 'Li2', '/w:document/w:body/w:p[7]/w:r/w:t': 'Page 2 content'}
    """
    root = etree.fromstring(
        xml_content)
    # depth first children queue
    # pop as you explore a child
    parent_children_queue: dict[Element, list[Element]] = {}
    node = root
    # If first time we see node: list its children
    # Get first children in list, store children->parent relationship
    # First children become node
    # If first time we see node: list its children
    # Get first children, store children->parent relationship
    # If node has no children,  check if node has text, add to log
    # Get parent of node, iterate on children

    # done when reaching root "parent", which doesn't exist
    text_map: dict[str, str] = {}
    while node is not None:
        text = node.text.strip() if node.text else None
        if text:
            text_map[node_xpath(node)] = text
        children = node.getchildren()
        # If we already queued this node before, use the remaining queue as source of truth.
        if node in parent_children_queue:
            children = parent_children_queue[node]
        if len(children) == 0:
            # print("Done exploring node", node.tag)
            # go back to parent node
            # no need for a parent node map in lxml, getparent() is available
            node = node.getparent()
        else:
            # print(children)
            # first time we see node, remember the parent children relationship
            # + queue children to process them later
            if node not in parent_children_queue:
                parent_children_queue[node] = children
            # pop first children, becomes current node
            node = parent_children_queue[node].pop(0)
    return text_map


def edit_xml_node_text(selector, text, xml_content):
    root: ElementTree = etree.fromstring(xml_content)
    # ns_prefix = selector.split(":")[0]
    nsmap_dict = {prefix: uri for prefix,
                  uri in root.nsmap.items() if prefix is not None}
    nodes = root.xpath(selector, namespaces=nsmap_dict)
    if len(nodes) == 0:
        raise ValueError(
            f"Selector {selector} didn't match any XML node, can't edit text")
    if len(nodes) > 1:
        raise ValueError(
            f"Selector {selector} matches multiple nodes, expected only one")
    node = nodes[0]
    node.text = text
    return etree.tostring(root)
    # namespaces = {
    #    prefix: uri for prefix, uri in root.nsmap.items() if prefix is not None
    # }
    # nodes = root.xpath(selector, namespaces=namespaces)
    # if len(nodes) == 0:
    #    raise ValueError(f"No XML node matches selector: {selector}")
#
    # for node in nodes:
    #    if not isinstance(node, etree._Element):
    #        raise ValueError(
    #            "Selector must target XML elements to edit text content"
    #        )
    #    node.text = text
#
    # return etree.tostring(root)
