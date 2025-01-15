# Classes for Python-based XMP and Exif schemas
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata
# into a standard Python dictionary from a Pillow (PIL) source image.
#

from dataclasses import dataclass, field, InitVar
from datetime import datetime


# ========================
# === Descriptor Class ===
# ========================

class XPath:
    """

    """

    def __init__(self, tag: str, datatype: str):
        self.tag = tag
        self.datatype = datatype

    def __get__(self, instance, owner=None):
        value = None
        if instance.xmp_xml is not None:
            if self.datatype == 'text':
                ele = instance.xmp_xml.find(f'.//{self.tag}')
                # print(ele)
                if ele is not None:
                    value = ele.text
            elif self.datatype == 'bag':
                ele = instance.xmp_xml.find(f'.//{self.tag}')
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
    xmp_xml: InitVar[str]

    def __post_init__(self, xmp_xml: str):
        self.xmp_xml = xmp_xml


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
    CreateDate: datetime = XPath(tag='{http://ns.adobe.com/xap/1.0/}CreateDate', datatype='text')
    CreatorTool: str = XPath(tag='{http://ns.adobe.com/xap/1.0/}CreatorTool', datatype='text')
    Identifier: list[str] = None
    Label: str = None
    MetadataDate: datetime = None
    ModifyDate: datetime = None
    Nickname: str = None
    Rating: int = None
    # Thumbnails: list = None  # An alternative array of thumbnail images for a file


class XmpRights(Xml):
    """
    Properties in the XMP Rights Management namespace.

    The XMP Rights Management namespace contains properties that provide
    information regarding the legal restriction sassociated with a resource.

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
    PersonInImage: list[str] = XPath(tag='{http://iptc.org/std/Iptc4xmpExt/2008-02-29/}PersonInImage', datatype='bag')


class Photoshop(Xml):
    """

    Attributes:
        DateCreated:
        Urgency:
        City:
        State:

    """

    # Photoshop properties
    DateCreated: datetime = None
    Urgency: int = None
    City: str = None
    State: str = None


class Dc(Xml):
    """

    Attributes:
        format:
        rights:
        description:
        subject:

    """

    # DC properties
    format: str = None
    rights: str = None
    creator: list[str] = None
    description: str = None
    subject: list[str] = None


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
    Schemas structure.

    Attributes:
        xmp:
        xmpRights:
        xmpMM:
        Iptc4xmpCore:
        Iptc4xmpExt:
        photoshop:
        dc:
        aux:
        tiff:
        exif:

    """

    xmp: Xmp()
    # xmpRights: XmpRights = field(default=XmpRights(**{}))
    # xmpMM: XmpMM = field(default=XmpMM(**{}))
    # Iptc4xmpCore: Iptc4XmpCore = field(default=Iptc4XmpCore(**{}))
    Iptc4xmpExt: Iptc4XmpExt()
    # photoshop: Photoshop = field(default=Photoshop(**{}))
    # dc: Dc = field(default=Dc(**{}))
    # aux: Aux = field(default=Aux(**{}))
    # tiff: Tiff = field(default=Tiff(**{}))
    # exif: Exif = field(default=Exif(**{}))
    