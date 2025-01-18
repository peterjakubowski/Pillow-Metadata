# Class for Python-based XMP and Exif extraction
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata into a
# standardized Python dataclass data structure from a Pillow (PIL) source image.
#

from dataclasses import dataclass, InitVar, field
from typing import AnyStr
from lxml import etree
from collections import deque
from PIL import Image
from datetime import datetime
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
    into a standardized Python dataclass. The provided image must have 'xmp' in its .info
    dictionary and Exif data available via .getexif().

    Args:
        pil_image (PIL.Image.Image): A Pillow image object containing metadata.

    Attributes:
        filename:
        xmp_xml:
        metadata:

    """

    pil_image: InitVar[Image.Image]
    filename: AnyStr = field(default_factory=str, init=False)  # Store the filename for later use
    xmp_xml: etree._ElementTree = field(default_factory=etree._ElementTree, init=False)  # Keep the raw XMP data as XML
    metadata: schemas.Schemas = None

    def __post_init__(self, pil_image: Image.Image) -> None:
        """
        Initializes Metadata object with image data.

        :param pil_image: (PIL.Image.Image)
        """

        if not isinstance(pil_image, Image.Image):
            raise TypeError("pil_image must be a PIL.Image.Image object.")

        if hasattr(pil_image, 'filename'):
            self.filename = pil_image.filename

        try:
            self.xmp_xml = helpers.parse_xml(pil_image.info['xmp'])
        except KeyError as ke:
            print(f"Key Error: {ke}")
        except TypeError as te:
            print(f"Type Error: {te}")
        except etree.XMLSyntaxError as xse:
            print(f"XML Syntax Error: {xse}")
        except etree.ParseError as pe:
            print(f"Parse Error: {pe}")
        finally:
            self.metadata = schemas.Schemas(xml_tree=self.xmp_xml)

        if exif := pil_image.getexif():
            self.metadata.exif = helpers.build_exif_dictionary(_exif=exif, _exif_object=schemas.Exif())

    def get_capture_date(self) -> str | None:
        """
        Attempts to retrieve the capture date from XMP or EXIF data, falling back to file creation time.

        :return: (str) The capture date in 'Weekday, Month DD, YYYY' format, or None if not found.
        """

        date_string = ""
        # Prioritize XMP then EXIF
        search = deque([('xmp', 'CreateDate'), ('exif', 'DateTimeOriginal'), ('photoshop', 'DateCreated')])
        while not date_string and search:
            prefix, localname = search.popleft()
            if capture_date := self.metadata.__getattribute__(prefix).__getattribute__(localname):
                return capture_date.strftime('%A, %B %d, %Y')

        if creation_date := Path(self.filename):  # Fallback to file creation time
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
        if description := self.metadata.dc.description:
            info.append("Description: " + description)
        # Get keywords
        if keywords := self.metadata.dc.subject:
            info.append("Keywords: " + ", ".join(keywords))
        # Get location data
        location = []
        for prefix, localname in [('Iptc4xmpCore', 'Location'), ('photoshop', 'City'), ('photoshop', 'State')]:
            if loc := self.metadata.__getattribute__(prefix).__getattribute__(localname):
                location.append(loc)
        if location:
            info.append("Location: " + ", ".join(location))

        return "\n".join(info)
