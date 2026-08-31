from datetime import datetime

import pytest
from lxml import etree
from PIL import Image

from src.pillow_metadata.metadata import Metadata
from src.pillow_metadata.schemas import Schemas


class TestMetadata:

    def test_metadata_reads_xmp_packet_from_pil_image(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = b'<?xpacket ?><root></root>'

        result = Metadata(pil_image=test_image)

        assert isinstance(result.xmp_xml, etree._ElementTree)
        assert isinstance(result.metadata, Schemas)

    def test_metadata_raises_error_when_xmp_packet_is_malformed(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = b'<?xpacket ?<root></root'

        with pytest.raises(TypeError):
            Metadata(pil_image=test_image)

    def test_metadata_raises_error_when_pil_image_is_string(self):
        with pytest.raises(TypeError, match="pil_image must be a PIL.Image.Image object."):
            Metadata(pil_image="test_image")

    def test_metadata_loads_empty_xml_when_pil_image_does_not_have_xmp(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")

        assert 'xmp' not in test_image.info

        result = Metadata(test_image)

        assert isinstance(result.xmp_xml, etree._ElementTree)

    def test_metadata_get_capture_date_xmp_create_date(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:CreateDate>2026-04-20T16:20:00.00</xmp:CreateDate>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        capture_date = result.get_capture_date()

        assert isinstance(capture_date, datetime)
        assert capture_date == result.metadata.xmp.CreateDate
        assert capture_date == datetime(2026, 4, 20, 16, 20)

    def test_metadata_get_capture_date_exif_date_time(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[306] = "2026-04-20T14:15:43.00"
        result = Metadata(test_image)
        capture_date = result.get_capture_date()
        assert isinstance(capture_date, datetime)
        assert capture_date == result.metadata.exif.DateTime
        assert capture_date == datetime(2026, 4, 20, 14, 15, 43)

    def test_metadata_get_capture_date_exif_date_time_original(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[36867] = "2026-04-20T14:15:43.00"
        result = Metadata(test_image)
        capture_date = result.get_capture_date()
        assert isinstance(capture_date, datetime)
        assert capture_date == result.metadata.exif.DateTimeOriginal
        assert capture_date == datetime(2026, 4, 20, 14, 15, 43)

    def test_metadata_get_capture_date_photoshop_date_created(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">\n'
            b'   <photoshop:DateCreated>2026-04-20T16:20:00.00</photoshop:DateCreated>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        capture_date = result.get_capture_date()

        assert isinstance(capture_date, datetime)
        assert capture_date == result.metadata.photoshop.DateCreated
        assert capture_date == datetime(2026, 4, 20, 16, 20)

    def test_metadata_get_capture_date_birth_time(self, tmp_path):
        temp_image_path = tmp_path / "test_image_no_meta.jpg"
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.save(temp_image_path)
        try:
            with Image.open(temp_image_path) as img:
                result = Metadata(pil_image=img)
                capture_date = result.get_capture_date()
                assert isinstance(capture_date, datetime)
        finally:
            if temp_image_path.exists():
                temp_image_path.unlink()

    def test_metadata_get_capture_date_none_found(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")

        result = Metadata(pil_image=test_image)

        capture_date = result.get_capture_date()

        assert capture_date is None

    def test_metadata_get_capture_date_string_xmp_create_date(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:CreateDate>2026-04-20T16:20:00.00</xmp:CreateDate>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        assert result.get_capture_date_string() == "Monday, April 20, 2026"

    def test_metadata_image_info(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/"\n'
            b'    xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
            b'    xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/"\n'
            b'    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">\n'
            b'   <xmp:CreateDate>2026-04-20T16:20:00.00</xmp:CreateDate>\n'
            b'   <dc:description>\n'
            b'    <rdf:Alt>\n'
            b'     <rdf:li xml:lang="x-default">Test description</rdf:li>\n'
            b'    </rdf:Alt>\n'
            b'   </dc:description>\n'
            b'   <dc:subject>\n'
            b'    <rdf:Bag>\n'
            b'     <rdf:li>Test keyword</rdf:li>'
            b'    </rdf:Bag>\n'
            b'   </dc:subject>\n'
            b'   <Iptc4xmpCore:Location>Test location</Iptc4xmpCore:Location>\n'
            b'   <photoshop:City>Test city</photoshop:City>\n'
            b'   <photoshop:State>Test state</photoshop:State>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        expected_result = "\n".join(["Date Created: Monday, April 20, 2026",
                                     "Description: Test description",
                                     "Keywords: Test keyword",
                                     "Location: Test location, Test city, Test state"])

        result = Metadata(pil_image=test_image)

        image_info_string = result.image_info()

        assert image_info_string == expected_result

    def test_metadata_to_dict_returns_dict(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        result = Metadata(test_image)
        result_dict = result.metadata.to_dict(include_none=False)
        assert isinstance(result_dict, dict)
        assert result_dict == {}
        assert str(result.metadata) == '{}'
