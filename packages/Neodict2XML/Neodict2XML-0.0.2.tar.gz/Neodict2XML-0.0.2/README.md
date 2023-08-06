# Neodict2XML

Neomyte's dict to XML converter

<ins>Example:<ins>

```python
>>> from neodict2xml import dict2xml
>>> test_dict = {\
    'test': {\
        'plop': ({'attr': 'brrr'}, 'lol'),\
        'lol': [\
            'hello',\
            'world'\
        ],\
        'deep': {\
            'deeper': 1\
        },\
        'test2': [\
            { 'foo': 'bar' },\
            ( { 'id': 2 }, { 'foo': 'rab' } )\
        ],\
        'test3': ( { 'class': 'foo.Bar' }, )\
    }\
}
>>> xml = dict2xml.from_dict(test_dict)
>>> print(dict2xml.prettify(xml))
<?xml version="1.0" ?>
<test>
    <plop attr="brrr">lol</plop>
    <lol>hello</lol>
    <lol>world</lol>
    <deep>
        <deeper>1</deeper>
    </deep>
    <test2>
        <foo>bar</foo>
    </test2>
    <test2 id="2">
        <foo>rab</foo>
    </test2>
    <test3 class="foo.Bar"/>
</test>

```


# Contributors

 * Emmanuel Pluot (aka. Neomyte)
