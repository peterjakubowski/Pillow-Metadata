from lxml import etree
from collections import deque
from PIL.Image import ExifTags
from datetime import datetime
import dateutil.parser
from pathlib import Path


class Metadata:

    def __init__(self, pil_image):
        self.metadata = {}
        self.filename = pil_image.filename
        self.xmp = pil_image.info['xmp']
        self.exif = pil_image.getexif()
        self.build_meta_dict()

    def read_xmp_xml(self):
        return etree.ElementTree(etree.fromstring(self.xmp.decode()))

    def read_exif(self):
        self.metadata['exif'] = {}
        for tag, value in self.exif.items():
            self.metadata['exif'][ExifTags.TAGS[tag]] = value

    def build_meta_dict(self):
        xmp_xml = self.read_xmp_xml()
        q = deque([(xmp_xml.getroot(), self.metadata)])
        while q:
            ele, parent = q.popleft()
            name = etree.QName(ele.tag).localname
            if name not in parent:
                parent[name] = {}
            if ele.attrib:
                prefix_map = {}
                for _key, _val in ele.nsmap.items():
                    prefix_map[_val] = _key
                for key, val in ele.attrib.items():
                    tag = etree.QName(key)
                    if (prefix := prefix_map[tag.namespace] if tag.namespace in prefix_map else tag.namespace) not in \
                            parent[name]:
                        parent[name][prefix] = {}
                    if (tname := tag.localname) not in parent[name][prefix]:
                        parent[name][prefix][tname] = val
            for child in ele:
                if (cname := etree.QName(child.tag).localname) in ('Bag', 'Seq', 'Alt'):
                    del parent[name]
                    if ele.prefix not in parent:
                        parent[ele.prefix] = {}
                    parent[ele.prefix][name] = []
                    for li in child:
                        if cname == 'Alt':
                            for key, val in li.attrib.items():
                                if val == 'x-default':
                                    parent[ele.prefix][name] = li.text
                        else:
                            parent[ele.prefix][name].append(li.attrib if li.attrib else li.text)
                else:
                    q.append((child, parent[name]))
        self.read_exif()

    def search_metadata(self, prefix, localname):
        q = deque([self.metadata])
        while q:
            cur = q.popleft()
            if isinstance(cur, dict):
                if prefix in cur:
                    if localname in cur[prefix]:
                        return cur[prefix][localname]
                for key in cur.keys():
                    if isinstance(cur[key], dict):
                        q.append(cur[key])
        return None

    def get_capture_date(self):
        date_string = ""
        search = deque([('xmp', 'CreateDate'), ('exif', 'DateTime'), ('exif', 'DateTimeOriginal')])
        while not date_string and search:
            prefix, localname = search.popleft()
            if capture_date := self.search_metadata(prefix=prefix, localname=localname):
                date_string = capture_date
        if date_string:
            date = dateutil.parser.parse(date_string)
            return date.strftime('%A, %B %d, %Y')
        elif creation_date := Path(self.filename):
            date = datetime.fromtimestamp(creation_date.stat().st_birthtime)
            return date.strftime('%A, %B %d, %Y')
        return None

    def image_info(self):
        info = []
        # Get the capture date
        if capture_date := self.get_capture_date():
            info.append("Date Created: " + capture_date)
        # Get the image description
        if description := self.search_metadata(prefix='dc', localname='description'):
            info.append("Description: " + description)
        # Get keywords
        if keywords := self.search_metadata(prefix='dc', localname='subject'):
            info.append("Keywords: " + ", ".join(keywords))
        # Get location data
        location = []
        for prefix, localname in [('Iptc4xmpCore', 'Location'), ('photoshop', 'City'), ('photoshop', 'State')]:
            if loc := self.search_metadata(prefix=prefix, localname=localname):
                location.append(loc)
        if location:
            info.append("Location: " + ", ".join(location))

        return "\n".join(info)