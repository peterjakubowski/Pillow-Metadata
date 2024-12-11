# Class for Python-based XMP and Exif extraction
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata
# into a standard Python dictionary from a Pillow (PIL) source image.
#

from lxml import etree
from collections import deque
from PIL import Image
from datetime import datetime
import dateutil.parser
from pathlib import Path


class Metadata:
    """
    Extracts and organizes metadata (XMP and EXIF) from a Pillow image
    into a standardized Python dictionary.

    Args:
        pil_image (PIL.Image.Image): A Pillow image object containing metadata.
        Must have 'xmp' in its .info dictionary and Exif data available via .getexif().
    """

    def __init__(self, pil_image: Image.Image):
        """
        Initializes Metadata object with image data.

        :param pil_image: (PIL.Image.Image)
        """

        if not isinstance(pil_image, Image.Image):
            raise TypeError("pil_image must be a PIL.Image.Image object.")

        self.metadata = {}  # Initialize an empty dictionary to store metadata
        self.filename = pil_image.filename  # Store the filename for later use
        # Get XMP data (XML packet) from the image's info dictionary
        self.xmp = pil_image.info['xmp'] if 'xmp' in pil_image.info else None
        self.exif = pil_image.getexif()  # Get EXIF data from the image
        self.build_meta_dict()  # Build the metadata dictionary

    def read_xmp_xml(self):
        """
        Parses the XMP data using lxml.etree.

        :return: etree._ElementTree: An ElementTree object representing the parsed XMP XML.
        """

        if self.xmp:
            return etree.ElementTree(etree.fromstring(self.xmp.decode()))

    def read_exif(self):
        """
        Reads and adds EXIF data to the metadata dictionary.

        :return:
        """
        if self.exif:
            self.metadata['exif'] = {}  # Create an 'exif' entry in the main metadata dictionary
            for tag, value in self.exif.items():
                self.metadata['exif'][Image.ExifTags.TAGS[tag]] = value  # Use ExifTags to get human-readable tag names

    def build_meta_dict(self):
        """
        Recursively parses the XMP XML and populates the metadata dictionary.
        Handles nested elements and different XML structures.
        The algorithm uses a queue to manage tree traversal.

        :return:
        """

        xmp_xml = self.read_xmp_xml()
        if xmp_xml:
            q = deque([(xmp_xml.getroot(), self.metadata)])  # Start with the root element and the main metadata dict
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
        self.read_exif()  # Read exif data after processing xmp data

    def search_metadata(self, prefix: str, localname: str):
        """
        Searches the metadata dictionary for a specific element using breadth-first search.

        :param prefix: (str) The namespace prefix of the element.
        :param localname: (str) The local name of the element.
        :return:
        """
        q = deque([self.metadata])
        while q:
            cur = q.popleft()
            if isinstance(cur, dict):
                if prefix in cur:
                    if localname in cur[prefix]:
                        return cur[prefix][localname]
                for key in cur.keys():
                    if isinstance(cur[key], dict):
                        q.append(cur[key])
        return None

    def get_capture_date(self):
        """
        Attempts to retrieve the capture date from XMP or EXIF data, falling back to file creation time.

        :return: (str) The capture date in 'Weekday, Month DD, YYYY' format, or None if not found.
        """

        date_string = ""
        # Prioritize XMP then EXIF
        search = deque([('xmp', 'CreateDate'), ('exif', 'DateTime'), ('exif', 'DateTimeOriginal')])
        while not date_string and search:
            prefix, localname = search.popleft()
            if capture_date := self.search_metadata(prefix=prefix, localname=localname):
                date_string = capture_date
        if date_string:
            date = dateutil.parser.parse(date_string)
            return date.strftime('%A, %B %d, %Y')
        elif creation_date := Path(self.filename):  # Fallback to file creation time
            date = datetime.fromtimestamp(creation_date.stat().st_birthtime)
            return date.strftime('%A, %B %d, %Y')
        return None

    def image_info(self):
        """
        Generates a human-readable string summarizing key image metadata.

        :return: (str) A multi-line string containing capture date, description, keywords, and location.
        """

        info = []
        # Get the capture date
        if capture_date := self.get_capture_date():
            info.append("Date Created: " + capture_date)
        # Get the image description
        if description := self.search_metadata(prefix='dc', localname='description'):
            info.append("Description: " + description)
        # Get keywords
        if keywords := self.search_metadata(prefix='dc', localname='subject'):
            info.append("Keywords: " + ", ".join(keywords))
        # Get location data
        location = []
        for prefix, localname in [('Iptc4xmpCore', 'Location'), ('photoshop', 'City'), ('photoshop', 'State')]:
            if loc := self.search_metadata(prefix=prefix, localname=localname):
                location.append(loc)
        if location:
            info.append("Location: " + ", ".join(location))

        return "\n".join(info)