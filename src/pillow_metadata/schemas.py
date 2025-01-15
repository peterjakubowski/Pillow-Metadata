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

    model_config = ConfigDict(extra='ignore')
    # XMP properties
    CreatorTool: str = None
    Identifier: list[str] = None
    Label: str = None
    MetadataDate: datetime = None
    ModifyDate: datetime = None
    Nickname: str = None
    # Thumbnails: list = None  # An alternative array of thumbnail images for a file


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

    model_config = ConfigDict(extra='ignore')
    # XMPRights properties
    Certificate: str = None  # A Web URL for a rights management certificate
    Marked: bool = None  # Rights-managed resource when true. Public-domain resource when false. State unknown if None
    Owner: list = None  # A list of legal owners of the resource
    UsageTerms: str = None  # Text instructions on how a resource can be legally used
    WebStatement: str = None  # A Web URL for a statement of the ownership and usage rights for this resource.


    """

    Attributes:
        DocumentID:
        OriginalDocumentID:
        InstanceID:
        History:

    """

    model_config = ConfigDict(extra='ignore')
    # XmpMM properties
    DocumentID: str = None
    OriginalDocumentID: str = None
    InstanceID: str = None
    History: list[dict] = None


    """

    Attributes:
        AltTextAccessibility:
        Location:

    """

    model_config = ConfigDict(extra='ignore')
    # Iptc4XmpCore properties
    Location: str = None


    """

    Attributes:
        PersonInImage:

    """

    model_config = ConfigDict(extra='ignore')
    # Iptc4XmpExt properties


    """

    Attributes:
        DateCreated:
        Urgency:
        City:
        State:

    """

    model_config = ConfigDict(extra='ignore')
    # Photoshop properties
    DateCreated: datetime = None
    City: str = None
    State: str = None


    """

    Attributes:
        format:
        rights:
        description:
        subject:

    """

    model_config = ConfigDict(extra='ignore')
    # DC properties
    format: str = None
    rights: str = None
    creator: list[str] = None
    description: str = None
    subject: list[str] = None


    """

    Attributes:
        SerialNumber:
        LensInfo:
        Lens:
        LensSerialNumber:
        FlashCompensation:
        FujiRatingAlreadyApplied:

    """

    model_config = ConfigDict(extra='ignore')
    # Aux properties
    SerialNumber: str = None
    LensInfo: str = None
    Lens: str = None
    LensSerialNumber: str = None
    FlashCompensation: str = None
    FujiRatingAlreadyApplied: bool = None


    """

    Attributes:
        Make:
        Model:

    """

    model_config = ConfigDict(extra='ignore')
    # Tiff properties
    Make: str = None
    Model: str = None


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

    model_config = ConfigDict(extra='ignore')
    # Exif properties
    ExifOffset: PositiveInt = None
    ImageDescription: str = None
    Make: str = None
    Model: str = None
    Software: str = None
    DateTime: datetime | str = None
    DateTimeOriginal: datetime = None
    YResolution: float = None
    Copyright: str = None
    XResolution: float = None
    Artist: str = None


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

    xmpRights: XmpRights = Field(default=XmpRights(**{}))
    xmpMM: XmpMM = Field(default=XmpMM(**{}))
    Iptc4xmpCore: Iptc4XmpCore = Field(default=Iptc4XmpCore(**{}))
    Iptc4xmpExt: Iptc4XmpExt = Field(default=Iptc4XmpExt(**{}))
    photoshop: Photoshop = Field(default=Photoshop(**{}))
    dc: Dc = Field(default=Dc(**{}))
    aux: Aux = Field(default=Aux(**{}))
    tiff: Tiff = Field(default=Tiff(**{}))
    exif: Exif = Field(default=Exif(**{}))
    