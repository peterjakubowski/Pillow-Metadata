# Helper functions for Python-based XMP and Exif extraction
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata into a
# standardized Python dataclass data structure from a Pillow (PIL) source image.
#

import logging
from datetime import datetime
from typing import Any

import dateutil.parser
from dateutil.parser import ParserError
from lxml import etree
from PIL import Image

logger = logging.getLogger(__name__)

# ========================
# === Helper Functions ===
# ========================


def parse_xml(_xmp_xml_byte_string: bytes) -> etree._ElementTree:
    """
    Parses the raw XMP packet XML and returns it as an ElementTree using lxml.

    :param _xmp_xml_byte_string: Raw XMP pack as a byte string
    :return: XMP metadata as an XML ElementTree
    """

    try:
        _xmp_xml_string = _xmp_xml_byte_string.decode()
        _xmp_xml_etree = etree.ElementTree(etree.fromstring(_xmp_xml_string))

    except etree.XMLSyntaxError as xse:
        logger.error(f'Syntax Error: {xse}')
        raise TypeError("Syntax Error")

    return _xmp_xml_etree


def cast_datatype(_value: Any, _data_type: Any) -> str | datetime | int | float | bool:
    """

    :return:
    """

    if _data_type is datetime:
        try:
            _value = str(_value).replace(":", "")
            _value = dateutil.parser.parse(timestr=_value, default=None, fuzzy=True)
        except ParserError as pe:
            logger.error(f'Error parsing date string to datetime: {pe}')
            raise ParserError
        except OverflowError as oe:
            logger.error(f'Overflow error when parsing date string to datetime: {oe}')

    elif _data_type is int:
        try:
            _value = int(float(_value))
        except ValueError as ve:
            logger.error(f'Error converting value to integer: {ve}')
            raise ValueError("Error converting value to integer")

    elif _data_type is float:
        try:
            _value = float(_value)
        except ValueError as ve:
            logger.error(f'Error converting value to float: {ve}')
            raise ValueError('Error converting value to float')

    elif _data_type is bool:
        bool_map = {
            "true": True,
            "false": False,
            "t": True,
            "f": False,
            "1": True,
            "0": False,
            "-1": False
        }
        try:
            _value = bool_map[str(_value).lower()]
        except KeyError as exc:
            logger.error(f'Error converting value to bool: {exc}')
            raise KeyError('Error converting value to bool')

    return _value


def build_exif_dictionary(_exif: Image.Exif, _exif_object: object):
    """
    Reads EXIF data and creates a metadata dictionary with human-readable tag names.

    :param _exif: Image Exif data
    :param _exif_object: Exif schema object
    :return: Exif schema object containing Image Exif data
    """

    for tag, value in _exif.items():
        exif_tag = Image.ExifTags.TAGS.get(tag, str(tag))
        if hasattr(_exif_object, exif_tag):
            if not isinstance(value, data_type := _exif_object.__annotations__[exif_tag]):
                try:
                    value = cast_datatype(_value=value, _data_type=data_type)
                except (TypeError, ValueError, KeyError, ParserError):
                    logger.error(f'Failed to cast metadata value: "{value}"')

            _exif_object.__setattr__(exif_tag, value)

    return _exif_object
