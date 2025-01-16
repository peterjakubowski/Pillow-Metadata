# Classes for Python-based XMP and Exif schemas
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata
# into a standard Python dictionary from a Pillow (PIL) source image.
#

from dataclasses import dataclass, field, InitVar
from datetime import datetime
from lxml import etree

# =======================
# ==== Namespace Map ====
# =======================


NS_MAP = {
    'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}',
    'xmp': '{http://ns.adobe.com/xap/1.0/}',
    'xmpRights': '{http://ns.adobe.com/xap/1.0/rights/}',
    'Iptc4xmpCore': '{http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/}',
    'Iptc4xmpExt': '{http://iptc.org/std/Iptc4xmpExt/2008-02-29/}',
    'photoshop': '{http://ns.adobe.com/photoshop/1.0/}',
    'dc': '{http://purl.org/dc/elements/1.1/}}'
}

# ========================
# === Descriptor Class ===
# ========================


class XPath:
    """

    """

    def __init__(self, tag: str, datatype: str):
        self.tag = tag
        self.datatype = datatype

    def __set_name__(self, owner: object, name: str):
        self.attrib_name = name
        self.annotation = owner.__annotations__.get(name)

    def __get__(self, instance: object, owner=None) -> str | list[str] | None:
        value = self.lookup(instance._xml_tree)
        instance.__dict__[self.attrib_name] = value
        return value

    def lookup(self, xml: etree._ElementTree) -> str | list[str] | None:
        value = None
        if xml is not None and xml.getroot() is not None:
            if self.datatype == 'text':
                ele = xml.find(f'.//{self.tag}')
                if ele is not None:
                    value = ele.text
                else:
                    ele = xml.find(f'.//{NS_MAP['rdf']}Description')
                    if ele is not None and ele.attrib:
                        if self.tag in ele.attrib:
                            value = ele.attrib[self.tag]

            elif self.datatype == 'bag':
                ele = xml.find(f'.//{self.tag}')
                if ele is not None:
                    items = []
                    bag = ele.getchildren()
                    if len(bag) == 1:
                        for li in bag[0].iterchildren():
                            items.append(li.text)
                        value = items

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
    CreateDate: datetime = XPath(tag=f"{NS_MAP['xmp']}{'CreateDate'}", datatype='text')
    CreatorTool: str = XPath(tag=f"{NS_MAP['xmp']}{'CreatorTool'}", datatype='text')
    Identifier: list[str] = None
    Label: str = XPath(tag=f"{NS_MAP['xmp']}{'Label'}", datatype='text')
    MetadataDate: datetime = XPath(tag=f"{NS_MAP['xmp']}{'MetadataDate'}", datatype='text')
    ModifyDate: datetime = XPath(tag=f"{NS_MAP['xmp']}{'ModifyDate'}", datatype='text')
    Nickname: str = XPath(tag=f"{NS_MAP['xmp']}{'Nickname'}", datatype='text')
    Rating: int = XPath(tag=f"{NS_MAP['xmp']}{'Rating'}", datatype='text')
    # Thumbnails: list = None  # An alternative array of thumbnail images for a file


class XmpRights(Xml):
    """
    Properties in the XMP Rights Management namespace.

    The XMP Rights Management namespace contains properties that provide
    information regarding the legal restrictions associated with a resource.

    The namespace URI shall be "http://ns.adobe.com/xap/1.0/rights/".

    The preferred namespace prefix is xmpRights.

    Attributes:
        Certificate:
        Marked:
        Owner:
        UsageTerms:
        WebStatement:

    """

    # XMPRights properties
    Certificate: str = None  # A Web URL for a rights management certificate
    Marked: bool = None  # Rights-managed resource when true. Public-domain resource when false. State unknown if None
    Owner: list = None  # A list of legal owners of the resource
    UsageTerms: str = None  # Text instructions on how a resource can be legally used
    WebStatement: str = None  # A Web URL for a statement of the ownership and usage rights for this resource.


class XmpMM(Xml):
    """

    Attributes:
        DocumentID:
        OriginalDocumentID:
        InstanceID:
        History:

    """

    # XmpMM properties
    DocumentID: str = None
    OriginalDocumentID: str = None
    InstanceID: str = None
    History: list[dict] = None


class Iptc4XmpCore(Xml):
    """
    Properties in the IPTC Core namespace.

    IPTC Photo Metadata provides data about photographs and the values can be processed by software.

    The namespace URI is http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/

    The preferred namespace prefix is Iptc4xmpCore

    Attributes:
        AltTextAccessibility:
        Location:

    """

    # Iptc4XmpCore properties
    AltTextAccessibility: str = None
    Location: str = None


class Iptc4XmpExt(Xml):
    """

    Attributes:
        PersonInImage:

    """

    # Iptc4XmpExt properties
    PersonInImage: list[str] = XPath(tag=f"{NS_MAP['Iptc4xmpExt']}{'PersonInImage'}", datatype='bag')


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
    DateCreated: datetime = XPath(tag=f"{NS_MAP['photoshop']}{'DateCreated'}", datatype='text')
    Urgency: int = XPath(tag=f"{NS_MAP['photoshop']}{'Urgency'}", datatype='text')
    City: str = XPath(tag=f"{NS_MAP['photoshop']}{'City'}", datatype='text')
    State: str = XPath(tag=f"{NS_MAP['photoshop']}{'State'}", datatype='text')
    TransmissionReference: str = XPath(tag=f"{NS_MAP['photoshop']}{'TransmissionReference'}", datatype='text')


class Dc(Xml):
    """
    Properties in the Dublin Core namespace.

    The Dublin Core namespace provides a set of commonly used properties.

    The names and usage shall be as defined in the Dublin Core Metadata Element Set,
    created by the Dublin Core Metadata Initiative (DCMI).

    The namespace URI is "http://purl.org/dc/elements/1.1/"

    The preferred namespace prefix is dc

    Attributes:
        format:
        rights:
        description:
        subject:

    """

    # DC properties
    creator: list[str] = XPath(tag=f"{NS_MAP['dc']}{'creator'}", datatype='bag')
    description: str = None
    format: str = None
    rights: str = None
    subject: list[str] = XPath(tag=f"{NS_MAP['dc']}{'subject'}", datatype='bag')
    title: str = None


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
    SerialNumber: str = None
    LensInfo: str = None
    Lens: str = None
    LensSerialNumber: str = None
    FlashCompensation: str = None
    FujiRatingAlreadyApplied: bool = None


class Tiff(Xml):
    """

    Attributes:
        Make:
        Model:

    """

    # Tiff properties
    Make: str = None
    Model: str = None


class Exif(Xml):
    """

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
    DateTime: datetime | str = None
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
        xmp:
        # xmpRights:
        # xmpMM:
        # Iptc4xmpCore:
        Iptc4xmpExt:
        # photoshop:
        dc:
        # aux:
        # tiff:
        # exif:

    """
    xml_tree: InitVar[etree._ElementTree]
    xmp: Xmp = field(default=Xmp)
    # xmpRights: XmpRights = field(default=XmpRights(**{}))
    # xmpMM: XmpMM = field(default=XmpMM(**{}))
    Iptc4xmpCore: Iptc4XmpCore = field(default=Iptc4XmpCore)
    Iptc4xmpExt: Iptc4XmpExt = field(default=Iptc4XmpExt)
    photoshop: Photoshop = field(default=Photoshop)
    dc: Dc = field(default=Dc)
    # aux: Aux = field(default=Aux(**{}))
    # tiff: Tiff = field(default=Tiff(**{}))
    # exif: Exif = field(default=Exif(**{}))

    def __post_init__(self, xml_tree: etree._ElementTree):
        self.xmp = Xmp(_xml_tree=xml_tree)
        self.Iptc4xmpCore = Iptc4XmpCore(_xml_tree=xml_tree)
        self.Iptc4xmpExt = Iptc4XmpExt(_xml_tree=xml_tree)
        self.photoshop = Photoshop(_xml_tree=xml_tree)
        self.dc = Dc(_xml_tree=xml_tree)
