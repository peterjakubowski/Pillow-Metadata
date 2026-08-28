from src.pillow_metadata.metadata import Metadata
from src.pillow_metadata.schemas import Schemas
from PIL import Image
from lxml import etree
from datetime import datetime
import pytest


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
            '<?xpacket begin="" id=""?>\n'
            '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            '  <rdf:Description rdf:about=""\n'
            '    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            '   <xmp:CreateDate>2026-04-20T16:20:00.00</xmp:CreateDate>\n'
            '  </rdf:Description>\n'
            ' </rdf:RDF>\n'
            '</x:xmpmeta>\n'
            '<?xpacket end="w"?>').encode("utf-8")

        result = Metadata(pil_image=test_image)

        capture_date = result.get_capture_date()

        assert isinstance(capture_date, datetime)
        assert capture_date == result.metadata.xmp.CreateDate
        assert capture_date == datetime(2026, 4, 20, 16, 20)

    def test_metadata_get_capture_date_string_xmp_create_date(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            '<?xpacket begin="" id=""?>\n'
            '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            '  <rdf:Description rdf:about=""\n'
            '    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            '   <xmp:CreateDate>2026-04-20T16:20:00.00</xmp:CreateDate>\n'
            '  </rdf:Description>\n'
            ' </rdf:RDF>\n'
            '</x:xmpmeta>\n'
            '<?xpacket end="w"?>').encode("utf-8")

        result = Metadata(pil_image=test_image)

        assert result.get_capture_date_string() == "Monday, April 20, 2026"

    def test_metadata_image_info(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            '<?xpacket begin="" id=""?>\n'
            '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            '  <rdf:Description rdf:about=""\n'
            '    xmlns:xmp="http://ns.adobe.com/xap/1.0/"\n'
            '    xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
            '    xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/"\n'
            '    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">\n'
            '   <xmp:CreateDate>2026-04-20T16:20:00.00</xmp:CreateDate>\n'
            '   <dc:description>\n'
            '    <rdf:Alt>\n'
            '     <rdf:li xml:lang="x-default">Test description</rdf:li>\n'
            '    </rdf:Alt>\n'
            '   </dc:description>\n'
            '   <dc:subject>\n'
            '    <rdf:Bag>\n'
            '     <rdf:li>Test keyword</rdf:li>'
            '    </rdf:Bag>\n'
            '   </dc:subject>\n'
            '   <Iptc4xmpCore:Location>Test location</Iptc4xmpCore:Location>\n'
            '   <photoshop:City>Test city</photoshop:City>\n'
            '   <photoshop:State>Test state</photoshop:State>\n'
            '  </rdf:Description>\n'
            ' </rdf:RDF>\n'
            '</x:xmpmeta>\n'
            '<?xpacket end="w"?>').encode("utf-8")

        expected_result = "\n".join(["Date Created: Monday, April 20, 2026",
                                     "Description: Test description",
                                     "Keywords: Test keyword",
                                     "Location: Test location, Test city, Test state"])

        result = Metadata(pil_image=test_image)

        image_info_string = result.image_info()

        assert image_info_string == expected_result
