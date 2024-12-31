# Class for Python-based XMP and Exif extraction
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata
# into a standard Python dictionary from a Pillow (PIL) source image.
#

from dataclasses import dataclass, InitVar, field
from typing import AnyStr, ByteString, Dict
from pydantic import BaseModel, Field, ConfigDict, PositiveInt, ValidationError
from lxml import etree
from collections import deque
from PIL import Image
from datetime import datetime
import dateutil.parser
from pathlib import Path


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


# ========================
# === Metadata Classes ===
# ========================


class Xmp(BaseModel):
    model_config = ConfigDict(extra='ignore')
    CreateDate: datetime = None
    ModifyDate: datetime = None
    MetadataDate: datetime = None
    CreatorTool: str = ''
    Rating: PositiveInt = Field(None, ge=1, le=5)


class XmpMM(BaseModel):
    model_config = ConfigDict(extra='ignore')
    DocumentID: str = None
    OriginalDocumentID: str = None
    InstanceID: str = None
    History: list[dict] = None


class Photoshop(BaseModel):
    model_config = ConfigDict(extra='ignore')
    DateCreated: datetime = None
    Urgency: PositiveInt = None
    City: str = None
    State: str = None


class Dc(BaseModel):
    model_config = ConfigDict(extra='ignore')
    format: str = None
    rights: str = None
    description: str = None
    subject: list[str] = None


class Aux(BaseModel):
    model_config = ConfigDict(extra='ignore')
    SerialNumber: str = None
    LensInfo: str = None
    Lens: str = None
    LensSerialNumber: str = None
    FlashCompensation: str = None
    FujiRatingAlreadyApplied: bool = None


class Tiff(BaseModel):
    model_config = ConfigDict(extra='ignore')
    Make: str = None
    Model: str = None


@dataclass(frozen=False)
class Metadata:
    """
    Extracts and organizes metadata (XMP and EXIF) from a Pillow image
    into a standardized Python dictionary.

    Args:
        pil_image (PIL.Image.Image): A Pillow image object containing metadata.
        Must have 'xmp' in its .info dictionary and Exif data available via .getexif().
    """

    pil_image: InitVar[Image.Image]
    metadata: Dict = field(default_factory=dict, init=False)  # Initialize an empty dictionary to store metadata
    filename: AnyStr = field(default_factory=str, init=False)  # Store the filename for later use
    xmp_xml: etree._ElementTree = field(default_factory=etree._ElementTree, init=False)  # Keep the raw XMP data as XML
    exif: Image.Exif = field(default_factory=dict, init=False)  # Keep the raw EXIF data from the image
    # Metadata schemas
    xmp: Xmp = field(default_factory=Xmp, init=False)
    xmpMM: XmpMM = field(default_factory=XmpMM, init=False)
    photoshop: Photoshop = field(default_factory=Photoshop, init=False)
    dc: Dc = field(default_factory=Dc, init=False)
    aux: Aux = field(default_factory=Aux, init=False)
    tiff: Tiff = field(default_factory=Tiff, init=False)

    def __post_init__(self, pil_image: Image.Image) -> None:
        """
        Initializes Metadata object with image data.

        :param pil_image: (PIL.Image.Image)
        """

        if not isinstance(pil_image, Image.Image):
            raise TypeError("pil_image must be a PIL.Image.Image object.")

        if hasattr(pil_image, 'filename'):
            self.filename = pil_image.filename

        if 'xmp' in pil_image.info:
            self.xmp_xml = parse_xml(_xmp_xml=pil_image.info['xmp'])
            if 'xmpmeta' in (xmp_dict := build_xmp_dictionary(_xmp_xml=self.xmp_xml)):
                self.metadata['xmpmeta'] = xmp_dict['xmpmeta']

        if exif := pil_image.getexif():
            self.exif = exif
            if exif_dict := build_exif_dictionary(_exif=self.exif):
                self.metadata['exif'] = exif_dict  # Create an 'exif' entry in the main metadata dictionary

        if self.metadata:
            if xmp_schema := search_for_schema(_metadata=self.metadata, schema='xmp'):
                self.xmp = Xmp(**xmp_schema)

            if xmpMM_schema := search_for_schema(_metadata=self.metadata, schema='xmpMM'):
                self.xmpMM = XmpMM(**xmpMM_schema)

            if photoshop_schema := search_for_schema(_metadata=self.metadata, schema='photoshop'):
                self.photoshop = Photoshop(**photoshop_schema)

            if dc_schema := search_for_schema(_metadata=self.metadata, schema='dc'):
                self.dc = Dc(**dc_schema)

            if tiff_schema := search_for_schema(_metadata=self.metadata, schema='tiff'):
                self.tiff = Tiff(**tiff_schema)

    def search_metadata(self, prefix: str, localname: str) -> str | None:
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

    def get_capture_date(self) -> str | None:
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

    def image_info(self) -> str:
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