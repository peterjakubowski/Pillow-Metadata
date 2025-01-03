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
    model_config = ConfigDict(extra='ignore')
    CreateDate: datetime = None
    ModifyDate: datetime = None
    MetadataDate: datetime = None
    CreatorTool: str = None
    Rating: PositiveInt = Field(None, ge=1, le=5)


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
    