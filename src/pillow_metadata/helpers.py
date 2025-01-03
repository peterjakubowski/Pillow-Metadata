# Helper functions for Python-based XMP and Exif extraction
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata
# into a standard Python dictionary from a Pillow (PIL) source image.
#

from typing import ByteString, Dict
from lxml import etree
from collections import deque
from PIL import Image

# ========================
# === Helper Functions ===
# ========================


def parse_xml(_xmp_xml: ByteString) -> etree._ElementTree:
    """
    Parses the raw XMP packet XML and returns it as an ElementTree using lxml.

    :param _xmp_xml: Raw XMP pack as a byte string
    :return: XMP metadata as an XML ElementTree
    """

    try:
        _xmp_xml = etree.ElementTree(etree.fromstring(_xmp_xml.decode()))

    except etree.XMLSyntaxError as xse:
        print(f'Type Error: {xse}')

    return _xmp_xml


def build_xmp_dictionary(_xmp_xml: etree._ElementTree) -> Dict:
    """
    Traverses the XMP XML and populates the metadata dictionary.
    Handles nested elements and different XML structures.
    The algorithm uses a queue to manage tree traversal.

    :param _xmp_xml: XML (packet) tree containing image XMP metadata
    :return: Dictionary of XMP metadata
    """

    if not isinstance(_xmp_xml, etree._ElementTree):
        raise TypeError('Type Error: Invalid XMP given, unable to parse XML tree.')

    xmp_metadata = {}

    q = deque([(_xmp_xml.getroot(), xmp_metadata)])  # Start with the root element and the main metadata dict
    while q:
        ele, parent = q.popleft()  # Get the current element and its parent dictionary
        name = etree.QName(ele.tag).localname  # Extract the element's name
        if name not in parent:
            parent[name] = {}  # Create a new dictionary entry if the element name isn't already present

        # Handle attributes
        if ele.attrib:
            prefix_map = {}
            for _key, _val in ele.nsmap.items():
                prefix_map[_val] = _key  # Create a map to resolve prefixes
            for key, val in ele.attrib.items():
                tag = etree.QName(key)
                if (prefix := prefix_map[tag.namespace] if tag.namespace in prefix_map else tag.namespace) \
                        not in parent[name]:
                    parent[name][prefix] = {}  # Create a dictionary for the prefix if it doesn't exist
                if (tname := tag.localname) not in parent[name][prefix]:
                    parent[name][prefix][tname] = val  # Store the attribute value

        # Handle child elements
        for child in ele:
            # Special handling for Bag, Seq, and Alt elements
            if (cname := etree.QName(child.tag).localname) in ('Bag', 'Seq', 'Alt'):
                del parent[name]  # Remove the element if it is Bag, Seq, or Alt
                if ele.prefix not in parent:
                    parent[ele.prefix] = {}  # Create an entry for the prefix
                parent[ele.prefix][name] = []  # Create a list to store the children of Bag, Seq, or Alt
                for li in child:
                    # Special handling for Alt elements to get default value
                    if cname == 'Alt':
                        for key, val in li.attrib.items():
                            if val == 'x-default':
                                parent[ele.prefix][name] = li.text
                    else:
                        # Append the children's attributes or text
                        parent[ele.prefix][name].append(li.attrib if li.attrib else li.text)
            else:
                q.append((child, parent[name]))  # Add the child element to the queue for processing

    return xmp_metadata


def build_exif_dictionary(_exif: Image.Exif) -> Dict:
    """
    Reads EXIF data and creates a metadata dictionary with human-readable tag names.

    :param _exif: Image Exif data
    :return: Dictionary containing Image Exif data
    """

    exif_metadata = {}

    for tag, value in _exif.items():
        exif_metadata[Image.ExifTags.TAGS[tag]] = value  # Use ExifTags to get human-readable tag names

    return exif_metadata


def search_for_schema(_metadata: Dict, schema: str) -> Dict | None:
    """
    Search for the schema in the metadata dictionary:

    :param _metadata: dictionary.
    :param schema:
    :return: dictionary.
    """

    q = deque([_metadata])
    while q:
        cur = q.popleft()
        if isinstance(cur, dict):
            if schema in cur and isinstance(cur[schema], dict):
                return cur[schema]
            for key in cur.keys():
                if isinstance(cur[key], dict):
                    q.append(cur[key])

    return None