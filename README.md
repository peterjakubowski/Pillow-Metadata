# Pillow-Metadata

Python class that transforms XMP and Exif metadata into a standard Python dictionary from a Pillow (PIL) source image.

## Background

I created this Python class to more easily extract image metadata in Python without depending on other packages like python-xmp-toolkit, which requires Exempi. Especially for simple read tasks, I wanted a tool that utilized Pillow, the Python Imaging Library. Pillow has methods to read metadata from images, this class will simply take the data returned by these methods and reformat it into a dictionary that is easier to work with.

The two Pillow methods used for metadata extraction are:

* PIL.Image.info['xmp']: Returns the image's XMP packet in XML form.

* PIL.Image.getexif(): Returns a dictionary of the image's Exif values where the keys are numbers that must be looked up using the PIL.Image.ExifTags module.

There is also a separate Pillow method, .getxmp(), that returns a dictionary containing the XMP tags. This method requires defusedxml to be installed, and I am not fond of the resulting structure.

This class parses the XMP XML and creates a dictionary where the parent keys are the XMP prefix and child keys are the XMP local name. This class also takes the Exif dictionary and replaces the numeric keys with Exif tag names. The resulting dictionary contains the combined XMP and Exif metadata.

## Usage

```commandline
from pillow_metadata import Metadata
from PIL import Image

# open an image using Pillow
pil_img = Image.open(img_path)

# construct a new Metadata object based on the PIL Image.
meta = Metadata(pil_img)

# retrieve a dictionary with the image's metadata
meta_dict = meta.metadata

# retrieve the image's filename (path)
# same as pil_img.filename
filename = meta.filename

# search the image's metadata
xmp_date = meta.search_metadata(prefix='xmp', localname='CreateDate')
exif_date = meta.search_metadata(prefix='exif', localname='DateTime')

```

## Dependencies

The following package versions were used when this was last updated, the use of different versions has not been tested and may affect the functionality of the tool.

```commandline
Python 3.12.8
Pillow 11.0.0
lxml 5.3.0
python-dateutil 2.9.0.post0

```
