from datetime import datetime

import pytest
from PIL import Image

from src.pillow_metadata.metadata import Metadata


class TestXmp:

    def test_metadata_xmp_create_date(self):
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

        create_date = result.metadata.xmp.CreateDate

        assert isinstance(create_date, datetime)
        assert create_date == datetime(2026, 4, 20, 16, 20)

    def test_metadata_xmp_creator_tool(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:CreatorTool>Test Creator Tool</xmp:CreatorTool>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        creator_tool = result.metadata.xmp.CreatorTool

        assert isinstance(creator_tool, str)
        assert creator_tool == "Test Creator Tool"

    def test_metadata_xmp_identifier(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:Identifier>\n'
            b'    <rdf:Bag>\n'
            b'     <rdf:li>Test Identifier</rdf:li>'
            b'    </rdf:Bag>\n'
            b'   </xmp:Identifier>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        identifier = result.metadata.xmp.Identifier

        assert isinstance(identifier, list)
        assert identifier == ["Test Identifier"]

    def test_metadata_xmp_label(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:Label>Test Label</xmp:Label>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        label = result.metadata.xmp.Label

        assert isinstance(label, str)
        assert label == "Test Label"

    def test_metadata_xmp_metadata_date(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:MetadataDate>2026-04-20T16:20:00.00</xmp:MetadataDate>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        metadata_date = result.metadata.xmp.MetadataDate

        assert isinstance(metadata_date, datetime)
        assert metadata_date == datetime(2026, 4, 20, 16, 20)

    def test_metadata_xmp_modify_date(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:ModifyDate>2026-04-20T16:20:00.00</xmp:ModifyDate>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        modify_date = result.metadata.xmp.ModifyDate

        assert isinstance(modify_date, datetime)
        assert modify_date == datetime(2026, 4, 20, 16, 20)

    def test_metadata_xmp_nickname(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:Nickname>Test Nickname</xmp:Nickname>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        nickname = result.metadata.xmp.Nickname

        assert isinstance(nickname, str)
        assert nickname == "Test Nickname"

    def test_metadata_xmp_rating(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:Rating>5</xmp:Rating>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        rating = result.metadata.xmp.Rating

        assert isinstance(rating, int)
        assert rating == 5

    def test_metadata_xmp_rating_none(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            b'   <xmp:Rating></xmp:Rating>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        rating = result.metadata.xmp.Rating

        assert rating is None


class TestXmpRights:

    def test_metadata_xmp_rights_certificate(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/">\n'
            b'   <xmpRights:Certificate>Test Certificate</xmpRights:Certificate>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        certificate = result.metadata.xmpRights.Certificate

        assert isinstance(certificate, str)
        assert certificate == "Test Certificate"

    @pytest.mark.parametrize("test_value, expected_value", [("True", True), ("False", False)])
    def test_metadata_xmp_rights_marked(self, test_value, expected_value):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            '<?xpacket begin="" id=""?>\n'
            '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            '  <rdf:Description rdf:about=""\n'
            '    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/">\n'
            f'   <xmpRights:Marked>{test_value}</xmpRights:Marked>\n'
            '  </rdf:Description>\n'
            ' </rdf:RDF>\n'
            '</x:xmpmeta>\n'
            '<?xpacket end="w"?>').encode()

        result = Metadata(pil_image=test_image)

        marked = result.metadata.xmpRights.Marked

        assert isinstance(marked, bool)
        assert marked is expected_value

    def test_metadata_xmp_rights_owner(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/">\n'
            b'   <xmpRights:Owner>\n'
            b'    <rdf:Bag>\n'
            b'     <rdf:li>Test Owner</rdf:li>\n'
            b'    </rdf:Bag>\n'
            b'   </xmpRights:Owner>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        owner = result.metadata.xmpRights.Owner

        assert isinstance(owner, list)
        assert owner == ["Test Owner"]

    def test_metadata_xmp_rights_usage_terms(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/">\n'
            b'   <xmpRights:UsageTerms>Test Usage Terms</xmpRights:UsageTerms>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        usage_terms = result.metadata.xmpRights.UsageTerms

        assert isinstance(usage_terms, str)
        assert usage_terms == "Test Usage Terms"

    def test_metadata_xmp_rights_web_statement(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/">\n'
            b'   <xmpRights:WebStatement>Test Web Statement</xmpRights:WebStatement>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        web_statement = result.metadata.xmpRights.WebStatement

        assert isinstance(web_statement, str)
        assert web_statement == "Test Web Statement"


class TestXmpMM:

    def test_metadata_xmp_mm_document_id(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/">\n'
            b'   <xmpMM:DocumentID>Test Document ID</xmpMM:DocumentID>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        document_id = result.metadata.xmpMM.DocumentID

        assert isinstance(document_id, str)
        assert document_id == "Test Document ID"

    def test_metadata_xmp_mm_original_document_id(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/">\n'
            b'   <xmpMM:OriginalDocumentID>Test Original Document ID</xmpMM:OriginalDocumentID>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        original_document_id = result.metadata.xmpMM.OriginalDocumentID

        assert isinstance(original_document_id, str)
        assert original_document_id == "Test Original Document ID"

    def test_metadata_xmp_mm_instance_id(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/">\n'
            b'   <xmpMM:InstanceID>Test Instance ID</xmpMM:InstanceID>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        instance_id = result.metadata.xmpMM.InstanceID

        assert isinstance(instance_id, str)
        assert instance_id == "Test Instance ID"


class TestIptc4XmpCore:

    def test_metadata_iptc_xmp_core_alt_text_accessibility(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/">\n'
            b'   <Iptc4xmpCore:AltTextAccessibility>\n'
            b'    <rdf:Alt>\n'
            b'     <rdf:li xml:lang="x-default">Test Alt Text</rdf:li>\n'
            b'    </rdf:Alt>\n'
            b'   </Iptc4xmpCore:AltTextAccessibility>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        alt_text_accessibility = result.metadata.Iptc4xmpCore.AltTextAccessibility

        assert isinstance(alt_text_accessibility, str)
        assert alt_text_accessibility == "Test Alt Text"

    def test_metadata_iptc_xmp_core_location(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/">\n'
            b'   <Iptc4xmpCore:Location>Test Location</Iptc4xmpCore:Location>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        location = result.metadata.Iptc4xmpCore.Location

        assert isinstance(location, str)
        assert location == "Test Location"

    def test_metadata_iptc_xmp_core_country_code(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/">\n'
            b'   <Iptc4xmpCore:CountryCode>Test Country Code</Iptc4xmpCore:CountryCode>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        country_code = result.metadata.Iptc4xmpCore.CountryCode

        assert isinstance(country_code, str)
        assert country_code == "Test Country Code"


class TestIptc4XmpExt:

    def test_metadata_iptc_xmp_ext_person_in_image(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/">\n'
            b'   <Iptc4xmpExt:PersonInImage>\n'
            b'    <rdf:Bag>\n'
            b'     <rdf:li>Test Name</rdf:li>\n'
            b'    </rdf:Bag>\n'
            b'   </Iptc4xmpExt:PersonInImage>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        person_in_image = result.metadata.Iptc4xmpExt.PersonInImage

        assert isinstance(person_in_image, list)
        assert person_in_image == ["Test Name"]


class TestPhotoshop:

    def test_metadata_photoshop_date_created(self):
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

        date_created = result.metadata.photoshop.DateCreated

        assert isinstance(date_created, datetime)
        assert date_created == datetime(2026, 4, 20, 16, 20)

    def test_metadata_photoshop_urgency(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">\n'
            b'   <photoshop:Urgency>5</photoshop:Urgency>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        urgency = result.metadata.photoshop.Urgency

        assert isinstance(urgency, int)
        assert urgency == 5

    def test_metadata_photoshop_city(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">\n'
            b'   <photoshop:City>Test City</photoshop:City>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        city = result.metadata.photoshop.City

        assert isinstance(city, str)
        assert city == "Test City"

    def test_metadata_photoshop_state(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">\n'
            b'   <photoshop:State>Test State</photoshop:State>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        state = result.metadata.photoshop.State

        assert isinstance(state, str)
        assert state == "Test State"

    def test_metadata_photoshop_transmission_reference(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/">\n'
            b'   <photoshop:TransmissionReference>Test Transmission Reference</photoshop:TransmissionReference>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(pil_image=test_image)

        transmission_reference = result.metadata.photoshop.TransmissionReference

        assert isinstance(transmission_reference, str)
        assert transmission_reference == "Test Transmission Reference"


class TestDc:

    def test_metadata_dc_creator(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            b'   <dc:creator>\n'
            b'    <rdf:Bag>\n'
            b'     <rdf:li>Test Name</rdf:li>\n'
            b'    </rdf:Bag>\n'
            b'   </dc:creator>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        creator = result.metadata.dc.creator

        assert isinstance(creator, list)
        assert creator == ["Test Name"]

    def test_metadata_dc_description(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            b'   <dc:description>\n'
            b'    <rdf:Alt>\n'
            b'     <rdf:li xml:lang="x-default">Test Description</rdf:li>\n'
            b'    </rdf:Alt>\n'
            b'   </dc:description>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        description = result.metadata.dc.description

        assert isinstance(description, str)
        assert description == "Test Description"

    def test_metadata_dc_format(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            b'   <dc:format>Test Format</dc:format>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        dc_format = result.metadata.dc.format

        assert isinstance(dc_format, str)
        assert dc_format == "Test Format"

    def test_metadata_dc_rights(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            b'   <dc:rights>\n'
            b'    <rdf:Alt>\n'
            b'     <rdf:li xml:lang="x-default">Test Rights</rdf:li>\n'
            b'    </rdf:Alt>\n'
            b'   </dc:rights>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        rights = result.metadata.dc.rights

        assert isinstance(rights, str)
        assert rights == "Test Rights"

    def test_metadata_dc_subject(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            b'   <dc:subject>\n'
            b'    <rdf:Bag>\n'
            b'     <rdf:li>Test Subject</rdf:li>\n'
            b'    </rdf:Bag>\n'
            b'   </dc:subject>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        subject = result.metadata.dc.subject

        assert isinstance(subject, list)
        assert subject == ["Test Subject"]

    def test_metadata_dc_title(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            b'   <dc:title>Test Title</dc:title>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        title = result.metadata.dc.title

        assert isinstance(title, str)
        assert title == "Test Title"


class TestAux:

    def test_metadata_aux_serial_number(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:aux="http://ns.adobe.com/exif/1.0/aux/">\n'
            b'   <aux:SerialNumber>Test Serial Number</aux:SerialNumber>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        serial_number = result.metadata.aux.SerialNumber

        assert isinstance(serial_number, str)
        assert serial_number == "Test Serial Number"

    def test_metadata_aux_lens_info(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:aux="http://ns.adobe.com/exif/1.0/aux/">\n'
            b'   <aux:LensInfo>Test Lens Info</aux:LensInfo>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        lens_info = result.metadata.aux.LensInfo

        assert isinstance(lens_info, str)
        assert lens_info == "Test Lens Info"

    def test_metadata_aux_lens(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:aux="http://ns.adobe.com/exif/1.0/aux/">\n'
            b'   <aux:Lens>Test Lens</aux:Lens>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        lens = result.metadata.aux.Lens

        assert isinstance(lens, str)
        assert lens == "Test Lens"

    def test_metadata_aux_lens_serial_number(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:aux="http://ns.adobe.com/exif/1.0/aux/">\n'
            b'   <aux:LensSerialNumber>Test Lens Serial Number</aux:LensSerialNumber>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        lens_serial_number = result.metadata.aux.LensSerialNumber

        assert isinstance(lens_serial_number, str)
        assert lens_serial_number == "Test Lens Serial Number"

    def test_metadata_aux_flash_compensation(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:aux="http://ns.adobe.com/exif/1.0/aux/">\n'
            b'   <aux:FlashCompensation>Test Flash Compensation</aux:FlashCompensation>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        flash_compensation = result.metadata.aux.FlashCompensation

        assert isinstance(flash_compensation, str)
        assert flash_compensation == "Test Flash Compensation"

    @pytest.mark.parametrize("test_value, expected_value", [("True", True), ("False", False)])
    def test_metadata_aux_fuji_rating_already_applied(self, test_value, expected_value):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            '<?xpacket begin="" id=""?>\n'
            '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            '  <rdf:Description rdf:about=""\n'
            '    xmlns:aux="http://ns.adobe.com/exif/1.0/aux/">\n'
            f'   <aux:FujiRatingAlreadyApplied>{test_value}</aux:FujiRatingAlreadyApplied>\n'
            '  </rdf:Description>\n'
            ' </rdf:RDF>\n'
            '</x:xmpmeta>\n'
            '<?xpacket end="w"?>').encode()

        result = Metadata(test_image)

        fuji_rating_already_applied = result.metadata.aux.FujiRatingAlreadyApplied

        assert isinstance(fuji_rating_already_applied, bool)
        assert fuji_rating_already_applied is expected_value


class TestTiff:

    def test_metadata_tiff_make(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:tiff="http://ns.adobe.com/tiff/1.0/">\n'
            b'   <tiff:Make>Test Make</tiff:Make>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        make = result.metadata.tiff.Make

        assert isinstance(make, str)
        assert make == "Test Make"

    def test_metadata_tiff_model(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        test_image.info['xmp'] = (
            b'<?xpacket begin="" id=""?>\n'
            b'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
            b' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            b'  <rdf:Description rdf:about=""\n'
            b'    xmlns:tiff="http://ns.adobe.com/tiff/1.0/">\n'
            b'   <tiff:Model>Test Model</tiff:Model>\n'
            b'  </rdf:Description>\n'
            b' </rdf:RDF>\n'
            b'</x:xmpmeta>\n'
            b'<?xpacket end="w"?>')

        result = Metadata(test_image)

        model = result.metadata.tiff.Model

        assert isinstance(model, str)
        assert model == "Test Model"


class TestExif:

    def test_metadata_exif_resolution_unit(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[296] = 2
        result = Metadata(test_image)
        resolution_unit = result.metadata.exif.ResolutionUnit
        assert isinstance(resolution_unit, int)
        assert resolution_unit == 2

    def test_metadata_exif_exif_offset(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[34665] = 2
        result = Metadata(test_image)
        exif_offset = result.metadata.exif.ExifOffset
        assert isinstance(exif_offset, int)
        assert exif_offset == 2

    def test_metadata_exif_image_description(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[270] = "Test Description"
        result = Metadata(test_image)
        image_description = result.metadata.exif.ImageDescription
        assert isinstance(image_description, str)
        assert image_description == "Test Description"

    def test_metadata_exif_make(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[271] = "Test Make"
        result = Metadata(test_image)
        make = result.metadata.exif.Make
        assert isinstance(make, str)
        assert make == "Test Make"

    def test_metadata_exif_model(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[272] = "Test Model"
        result = Metadata(test_image)
        model = result.metadata.exif.Model
        assert isinstance(model, str)
        assert model == "Test Model"

    def test_metadata_exif_software(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[305] = "Test Software"
        result = Metadata(test_image)
        software = result.metadata.exif.Software
        assert isinstance(software, str)
        assert software == "Test Software"

    def test_metadata_exif_orientation(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[274] = 1
        result = Metadata(test_image)
        orientation = result.metadata.exif.Orientation
        assert isinstance(orientation, int)
        assert orientation == 1

    def test_metadata_exif_date_time(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[306] = "2026-04-20T14:15:43.00"
        result = Metadata(test_image)
        date_time = result.metadata.exif.DateTime
        assert isinstance(date_time, datetime)
        assert date_time == datetime(2026, 4, 20, 14, 15, 43)

    def test_metadata_exif_date_time_original(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[36867] = "2026:04:20T14:15:43.00"
        result = Metadata(test_image)
        date_time_original = result.metadata.exif.DateTimeOriginal
        assert isinstance(date_time_original, datetime)
        assert date_time_original == datetime(2026, 4, 20, 14, 15, 43)

    def test_metadata_exif_y_resolution(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[283] = 300.0
        result = Metadata(test_image)
        y_resolution = result.metadata.exif.YResolution
        assert isinstance(y_resolution, float)
        assert y_resolution == 300.0

    def test_metadata_exif_copyright(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[33432] = "Test Copyright"
        result = Metadata(test_image)
        exif_copyright = result.metadata.exif.Copyright
        assert isinstance(exif_copyright, str)
        assert exif_copyright == "Test Copyright"

    def test_metadata_exif_x_resolution(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[282] = 300.0
        result = Metadata(test_image)
        x_resolution = result.metadata.exif.XResolution
        assert isinstance(x_resolution, float)
        assert x_resolution == 300.0

    def test_metadata_exif_artist(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[315] = "Test Artist Name"
        result = Metadata(test_image)
        artist = result.metadata.exif.Artist
        assert isinstance(artist, str)
        assert artist == "Test Artist Name"
