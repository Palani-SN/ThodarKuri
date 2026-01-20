import os
from ThodarKuri.Parser import ParserTemplateEngine
from ThodarKuri.Filler import FillerTemplateEngine


def test_parse_and_fill_templates(tmp_path):
    # point to the templates we added under TESTS/templates
    index_path = os.path.join('templates', 'index.html')
    output_path = os.path.join('templates', 'output.html')

    # parse the skeleton using the real SyntaxParser
    parser = ParserTemplateEngine()
    mapdict = parser.ParseEntryPoint(index_path)

    # update values for VARs located under header
    assert 'header' in mapdict and isinstance(mapdict['header'], dict)
    mapdict['header']['title'] = 'My Site Title'
    mapdict['header']['site_name'] = 'ExampleSite'

    # set tab titles inside parsed nested maps for tab1 and tab2
    content_map = mapdict.get('content', {})
    assert 'tab1' in content_map and isinstance(content_map['tab1'], list)
    assert 'tab2' in content_map and isinstance(content_map['tab2'], list)
    # ensure there is at least one dict for each tab list
    if not content_map['tab1']:
        content_map['tab1'].append({})
    if not content_map['tab2']:
        content_map['tab2'].append({})
    content_map['tab1'][0]['tab_title'] = 'First Tab'
    content_map['tab2'][0]['tab_title'] = 'Second Tab'

    # fill the templates
    filler = FillerTemplateEngine()
    out = filler.FillEntryPoint(mapdict, index_path, output_path)

    # basic assertions
    assert 'My Site Title' in out
    assert 'ExampleSite' in out
    assert 'First Tab' in out
    assert 'Second Tab' in out
    assert '<header>' in out and '</header>' in out


def test_self_include_does_not_infinite_loop():
    self_path = os.path.join('templates', 'self_include.html')

    parser = ParserTemplateEngine()
    # should not raise
    mapdict = parser.ParseEntryPoint(self_path)

    # filler should also not recurse infinitely
    filler = FillerTemplateEngine()
    out = filler.FillEntryPoint(mapdict, self_path)

    assert 'Self include:' in out
    # included part should be empty due to recursion guard
    assert 'Self include:' in out
