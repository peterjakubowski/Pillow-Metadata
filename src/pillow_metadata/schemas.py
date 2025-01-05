# Classes for Python-based XMP and Exif schemas
#
# Author: Peter Jakubowski
# Date: 12/8/2024
# Description: Python class that transforms XMP and Exif metadata
# into a standard Python dictionary from a Pillow (PIL) source image.
#

from pydantic import BaseModel, Field, ConfigDict, PositiveInt
from datetime import datetime

# ========================
# ==== Schema Classes ====
# ========================


class Xmp(BaseModel):
    """
     Properties in the XMP namespace.
     The XMP basic namespace contains properties that provide basic descriptive information.
     The namespace URI shall be "http://ns.adobe.com/xap/1.0/".
     The preferred namespace prefix is "xmp".

     """

    # Configure the BaseModel to ignore any extra attributes given at creation
    model_config = ConfigDict(extra='ignore')
    # XMP properties
    CreateDate: datetime = None  # The date and time the resource was created
    CreatorTool: str = None  # The name of the first known tool used to create the resource
    Identifier: list[str] = None  # Unordered array of text strings that identify the resource
    Label: str = None  # A word or short phrase that identifies a resource as a member of a collection
    MetadataDate: datetime = None  # Date and time that any metadata for this resource was last changed
    ModifyDate: datetime = None  # Date and time the resource was last modified
    Nickname: str = None  # A short informal name for the resource
    Rating: int = Field(None, ge=-1, le=5)  # A user-assigned rating for this file
    # Thumbnails: list = None  # An alternative array of thumbnail images for a file


class XmpRights(BaseModel):
    """
    Properties in the XMP Rights Management namespace.

    The XMP Rights Management namespace contains properties that provide
    information regarding the legal restriction sassociated with a resource.

    The namespace URI shall be "http://ns.adobe.com/xap/1.0/rights/".

    The preferred namespace prefix is xmpRights.

    """

    # Configure the BaseModel to ignore any extra attributes given at creation
    model_config = ConfigDict(extra='ignore')
    # XMPRights properties
    Certificate: str = None  # A Web URL for a rights management certificate
    Marked: bool = None  # Rights-managed resource when true. Public-domain resource when false. State unknown if None
    Owner: list = None  # A list of legal owners of the resource
    UsageTerms: str = None  # Text instructions on how a resource can be legally used
    WebStatement: str = None  # A Web URL for a statement of the ownership and usage rights for this resource.


class Iptc4XmpCore(BaseModel):
    """

    """

    # Configure the BaseModel to ignore any extra attributes given at creation
    model_config = ConfigDict(extra='ignore')
    # Iptc4XmpCore properties
    AltTextAccessibility: str = Field(default=None, title='Alt Text')

class Iptc4XmpExt(BaseModel):
    """

    """

    # Configure the BaseModel to ignore any extra attributes given at creation
    model_config = ConfigDict(extra='ignore')
    # Iptc4XmpExt properties
    PersonInImage: list[str] = None

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


class Schemas(BaseModel):
    xmpRights: XmpRights = Field(default=XmpRights(**{}))
    Iptc4xmpCore: Iptc4XmpCore = Field(default=Iptc4XmpCore(**{}))
    Iptc4xmpExt: Iptc4XmpExt = Field(default=Iptc4XmpExt(**{}))
    