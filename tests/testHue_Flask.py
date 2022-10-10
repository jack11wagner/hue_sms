from hue_flask import HEX_to_RGB

def testKnownHexConvertsToRGB():
    test_hex_code = '#9C59D1'

    assert '156,89,209' == HEX_to_RGB(test_hex_code)

def testUnknownHexReturnsNone():
    test_hex_code = "#NONE"

    assert None == HEX_to_RGB(test_hex_code)