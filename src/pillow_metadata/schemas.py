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
    xmp: Xmp = Field(default=Xmp(**{}), init=False)
    xmpMM: XmpMM = Field(default=XmpMM(**{}), init=False)
    photoshop: Photoshop = Field(default=Photoshop(**{}), init=False)
    dc: Dc = Field(default=Dc(**{}), init=False)
    aux: Aux = Field(default=Aux(**{}), init=True)
    tiff: Tiff = Field(default=Tiff(**{}), init=False)
    