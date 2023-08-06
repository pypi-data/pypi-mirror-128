from xml.etree.ElementTree import Element, SubElement

from neodict2xml import dict2xml

def test_all():
    # Given
    test_dict = {
        'test': {
            'plop': ({'attr': 'brrr'}, 'lol'),
            'lol': [
                'hello',
                'world'
            ],
            'deep': {
                'deeper': 1
            },
            'test2': [
                { 'foo': 'bar' },
                ( { 'id': 2 }, { 'foo': 'rab' } )
            ],
            'test3': ( { 'class': 'foo.Bar' }, )
        }
    }

    # When
    xml = dict2xml.from_dict(test_dict)

    # Then
    top = Element('test')
    c1 = SubElement(top, 'plop')
    c1.set('attr', 'brrr')
    c1.text = 'lol'
    c21 = SubElement(top, 'lol')
    c21.text = 'hello'
    c22 = SubElement(top, 'lol')
    c22.text = 'world'
    c3 = SubElement(top, 'deep')
    c31 = SubElement(c3, 'deeper')
    c31.text = '1'
    c41 = SubElement(top, 'test2')
    c411 = SubElement(c41, 'foo')
    c411.text = 'bar'
    c42 = SubElement(top, 'test2', {'id': '2'})
    c421 = SubElement(c42, 'foo')
    c421.text = 'rab'
    c5 = SubElement(top, 'test3', {'class': 'foo.Bar'}) # NOSONAR pylint: disable=unused-variable
    print(dict2xml.prettify(top))
    print(dict2xml.prettify(xml))
    assert dict2xml.prettify(top) == dict2xml.prettify(xml)
