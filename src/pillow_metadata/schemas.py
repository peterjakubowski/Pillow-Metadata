# Classes for Python-based XMP and Exif schemas
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata into a
# standardized Python dataclass data structure from a Pillow (PIL) source image.
#

import logging
from dataclasses import dataclass, field, InitVar
from datetime import datetime
from lxml import etree
from typing import Any, Literal
from pillow_metadata.helpers import cast_datatype

# =======================
# ==== Namespace Map ====
# =======================


NS_MAP = {
    'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}',
    'xmp': '{http://ns.adobe.com/xap/1.0/}',
    'xmpRights': '{http://ns.adobe.com/xap/1.0/rights/}',
    'xmpMM': '{http://ns.adobe.com/xap/1.0/mm/}',
    'Iptc4xmpCore': '{http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/}',
    'Iptc4xmpExt': '{http://iptc.org/std/Iptc4xmpExt/2008-02-29/}',
    'photoshop': '{http://ns.adobe.com/photoshop/1.0/}',
    'dc': '{http://purl.org/dc/elements/1.1/}',
    'aux': '{http://ns.adobe.com/exif/1.0/aux/}',
    'tiff': '{http://ns.adobe.com/tiff/1.0/}',
    'xml': '{http://www.w3.org/XML/1998/namespace}'
}

# ========================
# === Descriptor Class ===
# ========================


class XPath:
    """
    Descriptor class that looks up a value for an attribute in the XML.

    """

    def __init__(self, tag: str, xmp_data_type: Literal['text', 'bag', 'alt', 'seq']):
        self.tag = tag
        self.datatype = xmp_data_type

    def __set_name__(self, owner: object, name: str):
        self.attrib_name = name
        self.annotation = owner.__annotations__.get(name)

    def __get__(self, instance: Any, owner=None) -> str | int | float | list | datetime | None:
        value = self.lookup(instance._xml_tree)
        instance.__dict__[self.attrib_name] = value
        return value

    def lookup(self, xml: etree._ElementTree) -> str | int | float | list | datetime | None:
        value = None
        if xml is None or xml.getroot() is None:
            logging.warning("XML tree or root is None.")
            return None

        try:
            ele = xml.find(f'.//{self.tag}')
            if self.datatype == 'text':
                if ele is not None:
                    value = ele.text.strip()
                else:
                    ele = xml.find(f'.//{NS_MAP['rdf']}Description')
                    if ele is not None and ele.attrib:
                        if self.tag in ele.attrib:
                            value = ele.attrib[self.tag].strip()

            elif self.datatype == 'bag':
                if ele is not None:
                    items = []
                    bag = ele.getchildren()
                    if len(bag) == 1:
                        for li in bag[0].iterchildren():
                            items.append(li.text.strip())
                        value = items
                else:
                    logging.debug(f"Bag with tag '{self.tag}' nof found.")

            elif self.datatype == 'alt':
                if ele is not None:
                    alt = ele.getchildren()
                    if len(alt) == 1:
                        for li in alt[0].iterchildren():
                            if NS_MAP['xml'] + 'lang' in li.attrib and li.attrib[NS_MAP['xml'] + 'lang'] == 'x-default':
                                value = li.text.strip()
                                break
                else:
                    logging.debug(f"Alt with tag '{self.tag}' not found.")

        except Exception as e:
            logging.error(f"An unexpected error occurred during XML lookup for tag '{self.tag}': {e}")
            return None

        if value and not isinstance(value, self.annotation):
            try:
                value = cast_datatype(_value=value, _data_type=self.annotation)
            except TypeError as te:
                logging.error(f'Type Error: {te}')
            except AssertionError as ae:
                logging.error(f'Assertion Error: {ae} {value} {self.annotation}')
            else:
                return value

            return None

        return value

# ========================
# ==== Schema Classes ====
# ========================


@dataclass
class Xml:
    """
    The XML tree representing the XMP metadata.

     Attributes:
         _xml_tree: XML ElementTree, parsed by lxml

    """

    _xml_tree: etree._ElementTree

    def __post_init__(self):

        if not isinstance(self._xml_tree, etree._ElementTree):
            raise TypeError(f'xml_tree expected type ElementTree, got {type(self._xml_tree)} instead.')


class Xmp(Xml):
    """
     Properties in the XMP namespace.

     The XMP basic namespace contains properties that provide basic descriptive information.

     The namespace URI shall be "http://ns.adobe.com/xap/1.0/".

     The preferred namespace prefix is "xmp".

     Attributes:
         CreateDate: The date and time the resource was created.
         CreatorTool: The name of the first known tool used to create the resource.
         Identifier: Unordered array of text strings that identify the resource.
         Label: A word or short phrase that identifies a resource as a member of a collection.
         MetadataDate: Date and time that any metadata for this resource was last changed.
         ModifyDate: Date and time the resource was last modified.
         Nickname: A short informal name for the resource.
         Rating: A user-assigned rating for this file.
         # Thumbnails: An alternative array of thumbnail images for a file.

     """

    # XMP properties
    CreateDate: datetime = XPath(tag=f"{NS_MAP['xmp']}{'CreateDate'}", xmp_data_type='text')
    CreatorTool: str = XPath(tag=f"{NS_MAP['xmp']}{'CreatorTool'}", xmp_data_type='text')
    Identifier: list = XPath(tag=f"{NS_MAP['xmp']}{'Identifier'}", xmp_data_type='bag')
    Label: str = XPath(tag=f"{NS_MAP['xmp']}{'Label'}", xmp_data_type='text')
    MetadataDate: datetime = XPath(tag=f"{NS_MAP['xmp']}{'MetadataDate'}", xmp_data_type='text')
    ModifyDate: datetime = XPath(tag=f"{NS_MAP['xmp']}{'ModifyDate'}", xmp_data_type='text')
    Nickname: str = XPath(tag=f"{NS_MAP['xmp']}{'Nickname'}", xmp_data_type='text')
    Rating: int = XPath(tag=f"{NS_MAP['xmp']}{'Rating'}", xmp_data_type='text')
    # Thumbnails: list = None  # An alternative array of thumbnail images for a file


class XmpRights(Xml):
    """
    Properties in the XMP Rights Management namespace.

    The XMP Rights Management namespace contains properties that provide
    information regarding the legal restrictions associated with a resource.

    The namespace URI shall be "http://ns.adobe.com/xap/1.0/rights/".

    The preferred namespace prefix is xmpRights.

    Attributes:
        Certificate: A Web URL for a rights management certificate
        Marked: Rights-managed resource when true. Public-domain resource when false. State unknown if None
        Owner: A list of legal owners of the resource
        UsageTerms: Text instructions on how a resource can be legally used
        WebStatement: A Web URL for a statement of the ownership and usage rights for this resource

    """

    # XMPRights properties
    Certificate: str = XPath(tag=f"{NS_MAP['xmpRights']}{'Certificate'}", xmp_data_type='text')
    Marked: bool = XPath(tag=f"{NS_MAP['xmpRights']}{'Marked'}", xmp_data_type='text')
    Owner: list = XPath(tag=f"{NS_MAP['xmpRights']}{'Owner'}", xmp_data_type='bag')
    UsageTerms: str = XPath(tag=f"{NS_MAP['xmpRights']}{'UsageTerms'}", xmp_data_type='text')
    WebStatement: str = XPath(tag=f"{NS_MAP['xmpRights']}{'WebStatement'}", xmp_data_type='text')


class XmpMM(Xml):
    """
    Properties in the XMP Media Management namespace.

    This namespace is primarily for use by digital asset management (DAM) systems.

    The namespace URI is http://ns.adobe.com/xap/1.0/mm/

    The preferred namespace prefix is xmpMM

    Attributes:
        DocumentID: The common identifier for all versions and renditions of a resource.
        OriginalDocumentID: The common identifier for the original resource from which the current resource is derived.
        InstanceID: An identifier for a specific incarnation of a resource, updated each time a file is saved.
        # History: An ordered array of high-level user actions that resulted in this resource.

    """

    # XmpMM properties
    # ID type should be GUID
    DocumentID: str = XPath(tag=f"{NS_MAP['xmpMM']}{'DocumentID'}", xmp_data_type='text')
    OriginalDocumentID: str = XPath(tag=f"{NS_MAP['xmpMM']}{'OriginalDocumentID'}", xmp_data_type='text')
    InstanceID: str = XPath(tag=f"{NS_MAP['xmpMM']}{'InstanceID'}", xmp_data_type='text')
    # History: list = XPath(tag=f"{NS_MAP['xmpMM']}{'History'}", xmp_data_type='bag')  # ordered array


class Iptc4XmpCore(Xml):
    """
    Properties in the IPTC Core namespace.

    IPTC Photo Metadata provides data about photographs and the values can be processed by software.

    The namespace URI is http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/

    The preferred namespace prefix is Iptc4xmpCore

    Attributes:
        # CreatorContactInfo: Provides information to get in contact with the creator of this  object.
        AltTextAccessibility:
        Location: Name of a location the content is focussing on -- either the location shown or referenced by text.
        CountryCode: Code of the country the content is focussing on -- either the country shown or referenced in text.

    """

    # Iptc4XmpCore properties
    # CreatorContactInfo: object = XPath(tag=f"{NS_MAP['Iptc4xmpCore']}{'CreatorContactInfo'}", xmp_data_type='text')
    AltTextAccessibility: str = XPath(tag=f"{NS_MAP['Iptc4xmpCore']}{'AltTextAccessibility'}", xmp_data_type='alt')
    Location: str = XPath(tag=f"{NS_MAP['Iptc4xmpCore']}{'Location'}", xmp_data_type='text')
    CountryCode: str = XPath(tag=f"{NS_MAP['Iptc4xmpCore']}{'CountryCode'}", xmp_data_type='text')


class Iptc4XmpExt(Xml):
    """
    Properties in the IPTC Extension schema.

    Defines the semantics of a set of metadata properties and their technical expressions by the XMP format.

    The namespace URI is http://iptc.org/std/Iptc4xmpExt/2008-02-29/

    The preferred namespace prefix is Iptc4xmpExt

    Attributes:
        PersonInImage: Name of a person shown in the image.

    """

    # Iptc4XmpExt properties
    PersonInImage: list = XPath(tag=f"{NS_MAP['Iptc4xmpExt']}{'PersonInImage'}", xmp_data_type='bag')


class Photoshop(Xml):
    """
    Properties in the Photoshop namespace.

    This namespace specifies properties used by Adobe Photoshop.

    The namespace URI is "http://ns.adobe.com/photoshop/1.0/"

    The preferred namespace prefix is photoshop

    Attributes:
        DateCreated: The date the intellectual content of the document was created.
        Urgency: Urgency. Valid range is 1-8.
        City: City.
        State: Province/state.
        TransmissionReference: Original transmission reference.

    """

    # Photoshop properties
    DateCreated: datetime = XPath(tag=f"{NS_MAP['photoshop']}{'DateCreated'}", xmp_data_type='text')
    Urgency: int = XPath(tag=f"{NS_MAP['photoshop']}{'Urgency'}", xmp_data_type='text')
    City: str = XPath(tag=f"{NS_MAP['photoshop']}{'City'}", xmp_data_type='text')
    State: str = XPath(tag=f"{NS_MAP['photoshop']}{'State'}", xmp_data_type='text')
    TransmissionReference: str = XPath(tag=f"{NS_MAP['photoshop']}{'TransmissionReference'}", xmp_data_type='text')


class Dc(Xml):
    """
    Properties in the Dublin Core namespace.

    The Dublin Core namespace provides a set of commonly used properties.

    The names and usage shall be as defined in the Dublin Core Metadata Element Set,
    created by the Dublin Core Metadata Initiative.

    The namespace URI is "http://purl.org/dc/elements/1.1/"

    The preferred namespace prefix is dc

    Attributes:
        format: The file format, physical medium, or dimensions of the resource.
        rights: Information about rights held in and over the resource.
        description: An account of the resource.
        subject: The topic of the resource represented using keywords.
        title: A name given to the resource.

    """

    # DC properties
    creator: list = XPath(tag=f"{NS_MAP['dc']}{'creator'}", xmp_data_type='bag')
    description: str = XPath(tag=f"{NS_MAP['dc']}{'description'}", xmp_data_type='alt')
    format: str = XPath(tag=f"{NS_MAP['dc']}{'format'}", xmp_data_type='text')
    rights: str = XPath(tag=f"{NS_MAP['dc']}{'rights'}", xmp_data_type='alt')
    subject: list = XPath(tag=f"{NS_MAP['dc']}{'subject'}", xmp_data_type='bag')
    title: str = XPath(tag=f"{NS_MAP['dc']}{'title'}", xmp_data_type='text')


class Aux(Xml):
    """

    Attributes:
        SerialNumber:
        LensInfo:
        Lens:
        LensSerialNumber:
        FlashCompensation:
        FujiRatingAlreadyApplied:

    """

    # Aux properties
    SerialNumber: str = XPath(tag=f"{NS_MAP['aux']}{'SerialNumber'}", xmp_data_type='text')
    LensInfo: str = XPath(tag=f"{NS_MAP['aux']}{'LensInfo'}", xmp_data_type='text')
    Lens: str = XPath(tag=f"{NS_MAP['aux']}{'Lens'}", xmp_data_type='text')
    LensSerialNumber: str = XPath(tag=f"{NS_MAP['aux']}{'LensSerialNumber'}", xmp_data_type='text')
    FlashCompensation: str = XPath(tag=f"{NS_MAP['aux']}{'FlashCompensation'}", xmp_data_type='text')
    FujiRatingAlreadyApplied: bool = XPath(tag=f"{NS_MAP['aux']}{'FujiRatingAlreadyApplied'}", xmp_data_type='text')


class Tiff(Xml):
    """
    Properties in the TIFF namespace.

    EXIF properties for TIFF-derived data.

    The namespace URI is http://ns.adobe.com/tiff/1.0/

    The preferred namespace prefix is tiff

    Attributes:
        # Artist: Camera owner, photographer or image creator.
        Make: Manufacturer of recording equipment as an ASCII string.
        Model: Model name or number of equipment as an ASCII string.

    """

    # Tiff properties
    # Artist: str = XPath(tag=f"{NS_MAP['tiff']}{'Artist'}", xmp_data_type='text')
    Make: str = XPath(tag=f"{NS_MAP['tiff']}{'Make'}", xmp_data_type='text')
    Model: str = XPath(tag=f"{NS_MAP['tiff']}{'Model'}", xmp_data_type='text')


@dataclass
class Exif:
    """
    Properties in the EXIF namespace.

    EXIF Schema For EXIF-Specific Properties. These properties defined solely by EXIF.

    The namespace URI is http://ns.adobe.com/exif/1.0/

    The preferred namespace prefix is exif

    Attributes:
        ResolutionUnit:
        ExifOffset:
        ImageDescription:
        Make:
        Model:
        Software:
        Orientation:
        DateTime:
        YResolution:
        Copyright:
        XResolution:
        Artist:

    """

    # Exif properties
    ResolutionUnit: int = None
    ExifOffset: int = None
    ImageDescription: str = None
    Make: str = None
    Model: str = None
    Software: str = None
    Orientation: int = None
    DateTime: datetime = None
    DateTimeOriginal: datetime = None
    YResolution: float = None
    Copyright: str = None
    XResolution: float = None
    Artist: str = None


@dataclass
class Schemas:
    """
    XMP namespace definitions

    The XMP namespaces define a set of properties.

    In any given XMP Packet, a property may be absent or present.

    For any given XMP, there is no requirement that all properties from a given namespace must be present.

    Attributes:
        xmp: Properties in the xmp namespace
        xmpRights: Properties in the xmpRights namespace
        xmpMM: Properties in the xmpMM namespace
        Iptc4xmpCore: Properties in the Iptc4xmpCore namespace
        Iptc4xmpExt: Properties in the Iptc4xmpExt namespace
        photoshop: Properties in the photoshop namespace
        dc: Properties in dc xmp namespace
        aux: Properties in the aux namespace
        tiff: Properties in the tiff namespace
        exif: Properties in the exif namespace

    """
    xml_tree: InitVar[etree._ElementTree]
    xmp: Xmp = field(default=Xmp)
    xmpRights: XmpRights = field(default=XmpRights)
    xmpMM: XmpMM = field(default=XmpMM)
    Iptc4xmpCore: Iptc4XmpCore = field(default=Iptc4XmpCore)
    Iptc4xmpExt: Iptc4XmpExt = field(default=Iptc4XmpExt)
    photoshop: Photoshop = field(default=Photoshop)
    dc: Dc = field(default=Dc)
    aux: Aux = field(default=Aux)
    tiff: Tiff = field(default=Tiff)
    exif: Exif = field(default_factory=Exif)

    def __post_init__(self, xml_tree: etree._ElementTree):
        self.xmp = Xmp(_xml_tree=xml_tree)
        self.xmpRights = XmpRights(_xml_tree=xml_tree)
        self.xmpMM = XmpMM(_xml_tree=xml_tree)
        self.Iptc4xmpCore = Iptc4XmpCore(_xml_tree=xml_tree)
        self.Iptc4xmpExt = Iptc4XmpExt(_xml_tree=xml_tree)
        self.photoshop = Photoshop(_xml_tree=xml_tree)
        self.dc = Dc(_xml_tree=xml_tree)
        self.aux = Aux(_xml_tree=xml_tree)
        self.tiff = Tiff(_xml_tree=xml_tree)
