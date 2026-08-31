# Class for Python-based XMP and Exif extraction
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata into a
# standardized Python dataclass data structure from a Pillow (PIL) source image.
#

import logging
from collections import deque
from dataclasses import InitVar, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree
from PIL import Image

from .helpers import build_exif_dictionary, parse_xml
from .schemas import Exif, Schemas

logger = logging.getLogger(__name__)

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
    filename: str | None = field(default=None, init=False)  # Store the filename for later use
    xmp_xml: etree._ElementTree = field(default_factory=etree._ElementTree, init=False)  # Keep the raw XMP data as XML
    metadata: Schemas | None = None

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
            self.xmp_xml = parse_xml(pil_image.info.get('xmp', b'<?xpacket ?><root></root>'))
        except TypeError as te:
            logger.error(f"Type Error: {te}")
            raise TypeError
        finally:
            self.metadata = Schemas(xml_tree=self.xmp_xml)

        if exif := pil_image.getexif():
            self.metadata.exif = build_exif_dictionary(_exif=exif, _exif_object=Exif())

    def get_capture_date(self) -> datetime | None:
        """
        Attempts to retrieve the capture date from XMP or EXIF data, falling back to file creation time.

        :return: (str) The capture date in 'Weekday, Month DD, YYYY' format, or None if not found.
        """

        # Prioritize XMP then EXIF
        search = deque([('xmp', 'CreateDate'), ('exif', 'DateTime'), ('exif', 'DateTimeOriginal'), ('photoshop', 'DateCreated')])
        while search:
            prefix, localname = search.popleft()
            capture_date = getattr(getattr(self.metadata, prefix), localname)
            if capture_date:
                return capture_date

        if self.filename and Path(self.filename).is_file():
            stat_res = Path(self.filename).stat()
            mtime = getattr(stat_res, 'st_birthtime', stat_res.st_mtime)
            date = datetime.fromtimestamp(mtime, tz=timezone.utc)
            return date

        return None

    def get_capture_date_string(self) -> str | None:
        """
        Formats the capture date as '%A, %B %d, %Y'

        :return: (str) The capture date in 'Weekday, Month DD, YYYY' format, or None if not found.
        """

        if capture_date := self.get_capture_date():
            return capture_date.strftime('%A, %B %d, %Y')

        return None

    def image_info(self) -> str:
        """
        Generates a human-readable string summarizing key image metadata.

        :return: (str) A multi-line string containing capture date, description, keywords, and location.
        """

        info = []
        # Get the capture date
        if capture_date := self.get_capture_date_string():
            info.append("Date Created: " + capture_date)
        # Get the image description
        if description := self.metadata.dc.description if self.metadata else None:
            info.append("Description: " + description)
        # Get keywords
        if keywords := self.metadata.dc.subject if self.metadata else None:
            info.append("Keywords: " + ", ".join(keywords))
        # Get location data
        location = []
        for prefix, localname in [('Iptc4xmpCore', 'Location'), ('photoshop', 'City'), ('photoshop', 'State')]:
            loc = getattr(getattr(self.metadata, prefix), localname)
            if loc:
                location.append(loc)
        if location:
            info.append("Location: " + ", ".join(location))

        return "\n".join(info)
