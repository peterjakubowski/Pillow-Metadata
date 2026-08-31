from datetime import datetime

import pytest
from dateutil.parser import ParserError
from lxml import etree
from PIL import Image

from src.pillow_metadata.helpers import build_exif_dictionary, cast_datatype, parse_xml
from src.pillow_metadata.schemas import Exif


class TestParseXML:

    def test_parse_xml_returns_element_tree_from_xml_byte_string(self):

        test_data = (b'<?xml version="1.0"?>'
                     b'<root><child></child></root>')

        result = parse_xml(test_data)

        assert isinstance(result, etree._ElementTree)

    def test_parse_xml_returns_element_tree_from_xml_packet_byte_string(self):

        test_data = (b'<?xpacket ?>'
                     b'<root><child></child></root>')

        result = parse_xml(test_data)

        assert isinstance(result, etree._ElementTree)

    def test_parse_xml_raises_error_when_byte_string_malformed(self):

        test_data = (b'<?xml version="1.0"?'  # missing closing ">"
                     b'<root></root>')

        with pytest.raises(TypeError, match="Syntax Error"):
            parse_xml(test_data)

    def test_parse_xml_raises_error_when_xml_packet_byte_string_malformed(self):

        test_data = (b'<?xpacket ?'  # missing closing ">"
                     b'<root></root>')

        with pytest.raises(TypeError, match="Syntax Error"):
            parse_xml(test_data)


class TestCastDataType:

    @pytest.mark.parametrize("test_data", ["2026-04-20T14:15:43.00", "2026-04-20 14:15:43.00", "2026-04-20 14:15:43",
                                           "2026:04:20T14:15:43.00", "2026:04:20 14:15:43.00", "2026:04:20 14:15:43",
                                           "2026-04-20", "4-20-2026", "4/20/2026", "20260420", "2026:04:20"])
    def test_cast_datatype_date_string_to_datetime(self, test_data):
        result = cast_datatype(test_data, datetime)
        assert isinstance(result, datetime)

    @pytest.mark.parametrize("test_data", ["Today's date", "12345678"])
    def test_cast_datatype_raises_error_not_date_string_to_datetime(self, test_data):
        with pytest.raises(ParserError):
            cast_datatype(test_data, datetime)

    @pytest.mark.parametrize("test_data, expected_result", [("1", 1), ("1.0", 1)])
    def test_cast_datatype_integer_string_to_integer(self, test_data, expected_result):
        results = cast_datatype(test_data, int)
        assert isinstance(results, int)
        assert results == expected_result

    @pytest.mark.parametrize("test_data", ["One", "1,000"])
    def test_cast_datatype_raises_error_not_integer_string_to_integer(self, test_data):
        with pytest.raises(ValueError, match="Error converting value to integer"):
            cast_datatype(test_data, int)

    @pytest.mark.parametrize("test_data, expected_result", [("1", 1.0), ("1.0", 1.0)])
    def test_cast_datatype_float_string_to_float(self, test_data, expected_result):
        results = cast_datatype(test_data, float)
        assert isinstance(results, float)
        assert results == expected_result

    @pytest.mark.parametrize("test_data", ["One", "1,000"])
    def test_cast_datatype_raises_error_not_float_string_to_float(self, test_data):
        with pytest.raises(ValueError, match="Error converting value to float"):
            cast_datatype(test_data, float)

    @pytest.mark.parametrize("test_data, expected_result", [("True", True), ("T", True), ("False", False), ("F", False), ("1", True), ("0", False), ("-1", False)])
    def test_cast_datatype_bool_string_to_bool(self, test_data, expected_result):
        results = cast_datatype(test_data, bool)
        assert isinstance(results, bool)
        assert results == expected_result

    @pytest.mark.parametrize("test_data", ["Tru", "Fals", "2"])
    def test_cast_datatype_raises_error_not_bool_string_to_bool(self, test_data):
        with pytest.raises(KeyError, match='Error converting value to bool'):
            cast_datatype(test_data, bool)


class TestBuildExifDict:

    def test_build_exif_dictionary_from_image_without_exif(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        result = build_exif_dictionary(exif_data, Exif())
        assert isinstance(result, Exif)

    def test_build_exif_dictionary_from_image_with_exif_date_created(self):
        test_image = Image.new(mode="RGB", size=(100, 100), color="black")
        exif_data = test_image.getexif()
        exif_data[306] = "2026-04-20T14:15:43.00"
        result = build_exif_dictionary(exif_data, Exif())
        assert result.DateTime is not None
        assert result.DateTime == datetime(2026, 4, 20, 14, 15, 43, tzinfo=None)
