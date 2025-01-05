# Class for Python-based XMP and Exif extraction
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata
# into a standard Python dictionary from a Pillow (PIL) source image.
#

from dataclasses import dataclass, InitVar, field
from typing import AnyStr, Dict
from pydantic import ValidationError
from lxml import etree
from collections import deque
from PIL import Image
from datetime import datetime
import dateutil.parser
from pathlib import Path
import schemas
import helpers

# ========================
# ==== Metadata Class ====
# ========================


@dataclass(frozen=False)
class Metadata:
    """
    Extracts and organizes metadata (XMP and EXIF) from a Pillow image
    into a standardized Python dictionary. The provide image must have 'xmp' in its .info
    dictionary and Exif data available via .getexif().

    Args:
        pil_image (PIL.Image.Image): A Pillow image object containing metadata.

    Attributes:
        metadata_dict:
        filename:
        xmp_xml:
        exif:
        metadata:

    """

    pil_image: InitVar[Image.Image]
    metadata_dict: Dict = field(default_factory=dict, init=False)  # Initialize an empty dictionary to store metadata
    filename: AnyStr = field(default_factory=str, init=False)  # Store the filename for later use
    xmp_xml: etree._ElementTree = field(default_factory=etree._ElementTree, init=False)  # Keep the raw XMP data as XML
    exif: Image.Exif = field(default_factory=dict, init=False)  # Keep the raw EXIF data from the image
    metadata: schemas.Schemas = field(default_factory=schemas.Schemas, init=False)

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
            self.xmp_xml = helpers.parse_xml(_xmp_xml=pil_image.info['xmp'])
            if 'xmpmeta' in (xmp_dict := helpers.build_xmp_dictionary(_xmp_xml=self.xmp_xml)):
                self.metadata_dict['xmpmeta'] = xmp_dict['xmpmeta']

        if exif := pil_image.getexif():
            self.exif = exif
            if exif_dict := helpers.build_exif_dictionary(_exif=self.exif):
                self.metadata_dict['exif'] = exif_dict  # Create an 'exif' entry in the main metadata dictionary

        if self.metadata_dict:
            if xmp_schema := helpers.search_for_schema(_metadata=self.metadata_dict, schema='xmp'):
                try:
                    self.metadata.xmp = schemas.Xmp(**xmp_schema)
                except ValidationError as ve:
                    print(ve.json())

            if xmpMM_schema := helpers.search_for_schema(_metadata=self.metadata_dict, schema='xmpMM'):
                try:
                    self.metadata.xmpMM = schemas.XmpMM(**xmpMM_schema)
                except ValidationError as ve:
                    print(ve.json())

            if photoshop_schema := helpers.search_for_schema(_metadata=self.metadata_dict, schema='photoshop'):
                try:
                    self.metadata.photoshop = schemas.Photoshop(**photoshop_schema)
                except ValidationError as ve:
                    print(ve.json())

            if dc_schema := helpers.search_for_schema(_metadata=self.metadata_dict, schema='dc'):
                try:
                    self.metadata.dc = schemas.Dc(**dc_schema)
                except ValidationError as ve:
                    print(ve.json())

            if tiff_schema := helpers.search_for_schema(_metadata=self.metadata_dict, schema='tiff'):
                try:
                    self.metadata.tiff = schemas.Tiff(**tiff_schema)
                except ValidationError as ve:
                    print(ve.json())

    def search_metadata(self, prefix: str, localname: str) -> str | None:
        """
        Searches the metadata dictionary for a specific element using breadth-first search.

        :param prefix: (str) The namespace prefix of the element.
        :param localname: (str) The local name of the element.
        :return:
        """

        q = deque([self.metadata_dict])
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
