# Pillow-Metadata

Python class that transforms XMP and Exif metadata into a standardized Python dataclass data structure from a Pillow (PIL) source image.


## Background

I created this Python class to more easily extract image metadata in Python without depending on other packages like python-xmp-toolkit, which requires Exempi; and PyExif, which requires exiftool. Especially for simple read tasks, I wanted a tool that utilized Pillow, the Python Imaging Library. Pillow has methods to read metadata from images, this class will simply take the data returned by these methods and reformat it into a dataclass that is easier to work with.

The two Pillow methods used for metadata extraction are:

* PIL.Image.info['xmp']: Returns the image's XMP packet in XML form.

* PIL.Image.getexif(): Returns a dictionary of the image's Exif values where the keys are numbers that must be looked up using the PIL.Image.ExifTags module.

There is also a separate Pillow method, .getxmp(), that returns a dictionary containing the XMP tags. This method requires defusedxml to be installed, and I am not fond of the resulting structure.

This class parses the XMP XML and creates a dataclass data structure where the class names are the XMP prefix and attributes are the XMP local name. This class also takes the Exif dictionary and replaces the numeric keys with Exif tag names. The resulting class contains the combined XMP and Exif metadata.

## Usage

```commandline
from pillow_metadata.metadata import Metadata
from PIL import Image

# open an image using Pillow
pil_img = Image.open(img_path)

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
Python 3.12.8
Pillow 11.0.0
lxml 5.3.0
python-dateutil 2.9.0.post0

```

## Additional Info

[XMP namespace definitions](https://developer.adobe.com/xmp/docs/XMPNamespaces/)
