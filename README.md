![Run Python Tests](https://github.com/peterjakubowski/Pillow-Metadata/actions/workflows/ci.yaml/badge.svg)

# Pillow-Metadata

`Pillow-Metadata` transforms raw XMP XML packets and integer-keyed EXIF dictionaries extracted from Pillow (`PIL.Image`) into structured, type-hinted Python dataclasses. It provides a lightweight, pure-Python abstraction layer that makes XMP image metadata accessible via readable dot-notation properties without requiring system-level C libraries or CLI tools.

**Supported Metadata Namespaces**

| Namespace           | Dataclass Attribute                          | Key Extracted Fields                                                                                                                                                                |
|:--------------------|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Dublin Core**     | `meta.metadata.dc`                           | `creator`, `description`, `format`, `rights`, `subject` (keywords), `title`                                                                                                         |
| **Basic XMP**       | `meta.metadata.xmp`                          | `CreateDate`, `CreatorTool`, `Identifier`, `Label`, `MetadataDate`, `ModifyDate`, `Nickname`, `Rating`                                                                              |
| **XMP Rights**      | `meta.metadata.xmpRights`                    | `Certificate`, `Marked`, `Owner`, `UsageTerms`, `WebStatement`                                                                                                                      |
| **XMP MM**          | `meta.metadata.xmpMM`                        | `DocumentID`, `OriginalDocumentID`, `InstanceID`                                                                                                                                    |
| **EXIF Data**       | `meta.metadata.exif`                         | `ResolutionUnit`, `ExifOffset`, `ImageDescription`, `DateTime`, `DateTimeOriginal`, `Make`, `Model`, `Orientation`, `Software`, `YResolution`, `Copyright`, `XResolution`, `Artist` |
| **Photoshop**       | `meta.metadata.photoshop`                    | `DateCreated`, `Urgency`, `City`, `State`, `TransmissionReference`                                                                                                                  |
| **IPTC Core & Ext** | `meta.metadata.Iptc4xmpCore` / `Iptc4xmpExt` | `Location`, `CountryCode`, `AltTextAccessibility`, `PersonInImage`                                                                                                                  |
| **Camera & Lens**   | `meta.metadata.aux` / `tiff`                 | `SerialNumber`, `LensInfo`, `Lens`, `LensSerialNumber`, `FlashCompensation`, `FujiRatingAlreadyApplied`, `Make`, `Model`                                                            |

## Usage

```python
from pillow_metadata import Metadata
from PIL import Image

# open an image using Pillow
pil_img = Image.open("./path/to/img.jpg")

# construct a new Metadata object based on the PIL Image.
meta = Metadata(pil_img)

# retrieve the image's filename (path)
# same as pil_img.filename
filename = meta.filename

# retrieve a list of keywords applied to the image
keywords = meta.metadata.dc.subject

# retrieve the image's create date
xmp_date = meta.metadata.xmp.CreateDate
photoshop_date = meta.metadata.photoshop.DateCreated
exif_date = meta.metadata.exif.DateTimeOriginal

# get the image's capture date
capture_date = meta.get_capture_date()

```

## Installation

Install with pip using the link to the github project.

```commandline
pip install https://github.com/peterjakubowski/Pillow-Metadata/archive/main.zip

```

## Dependencies

The following package versions were used when this was last updated, the use of different versions has not been tested and may affect the functionality of the tool.

```commandline
Pillow>=12.2.0
lxml>=6.1.0
python-dateutil 2.9.0.post0

```

## Additional Info

[XMP namespace definitions](https://developer.adobe.com/xmp/docs/XMPNamespaces/)
