# Pillow-Metadata

Python class that transforms xmp and exif metadata into a standard Python dictionary from a Pillow (PIL) source image.

## Usage

```commandline
from pillow_metadata import Metadata
from PIL import Image

# open an image using Pillow
pil_img = Image.open(img_path)

# construct a new Metadata object
meta = Metadata(img)

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

```commandline
Python 3.10.12
lxml 5.2.2
PIL 10.0.1
dateutil 2.9.0

```
