from ThodarKuri.Filler import FillerTemplateEngine
import json
import copy
import pytest

@pytest.fixture
def DefaultRegex1():
    TE = FillerTemplateEngine();
    return TE;

def test_DefaultCase1(DefaultRegex1): 
     
    with open('gen_files/Settings.json') as config:
        Settings = json.load(config)

    with open('ref_files/PlotDetails.json') as Details:
        PlotDetails = json.load(Details)

    Settings['Title'] = 'Template Engine Demo';

    Settings['Plot']['Plot_Description'] = 'Horizontal Bar Chart';
    Settings['Plot']['Plot_Orientation'] = 'horizontal';

    filtered_Lists = [bar for bar in PlotDetails if bar['size'] < 100];

    bar_dict = Settings['Plot']['Bar'][0]
    Settings['Plot']['Bar'] = [];
    for bar in filtered_Lists:
        bar_dict['name'] = bar['name'];
        bar_dict['size'] = bar['size'];
        bar_dict['description'] = bar['description'];
        # deep copy to be used when handling copy of lists and dict
        Settings['Plot']['Bar'].append(copy.deepcopy(bar_dict));
    
    # print(json.dumps(Settings, sort_keys=True, indent=4));

    Filler = DefaultRegex1;
    FilledString = Filler.FillEntryPoint(Settings, "html_plot/template_index.html", "html_plot/index.html");

    ReferenceFile = open("ref_files/index.html", 'r').readlines();
    CreatedFile = open("html_plot/index.html", 'r').readlines();
    assert len(ReferenceFile) == len(CreatedFile);
    for line_no in range(len(CreatedFile)):
        assert ReferenceFile[line_no] == CreatedFile[line_no]

@pytest.fixture
def SpecialRegex1():
    TE = FillerTemplateEngine(("_StArT_", "_eNd_"), "_StArT_self.FUNC_CALL()_eNd_");
    return TE;

@pytest.fixture
def SpecialRegex2():
    TE = FillerTemplateEngine(("<<", ">>"), "<<self.FUNC_CALL()>>");
    return TE;

@pytest.fixture
def SpecialRegex3():
    TE = FillerTemplateEngine(("\\[\\[", "\\]\\]"), "[[self.FUNC_CALL()]]");
    return TE;

@pytest.fixture
def SpecialRegex4():
    TE = FillerTemplateEngine(("{\\[<{\\[", "}\\]>}\\]"), "{[<{[self.FUNC_CALL()}]>}]");
    return TE;

def test_SpecialCase1(SpecialRegex1, SpecialRegex2, SpecialRegex3, SpecialRegex4): 
     
    for filex in ([1,2,3,4]):

        if(filex==1):Filler = SpecialRegex1;
        if(filex==2):Filler = SpecialRegex2;
        if(filex==3):Filler = SpecialRegex3;
        if(filex==4):Filler = SpecialRegex4;

        with open(f'gen_files/Settings - SR{filex}.json') as config:
            Settings = json.load(config)

        with open('ref_files/PlotDetails.json') as Details:
            PlotDetails = json.load(Details)

        Settings['Title'] = 'Template Engine Demo';

        Settings['Plot']['Plot_Description'] = 'Horizontal Bar Chart';
        Settings['Plot']['Plot_Orientation'] = 'horizontal';

        filtered_Lists = [bar for bar in PlotDetails if bar['size'] < 100];

        bar_dict = Settings['Plot']['Bar'][0]
        Settings['Plot']['Bar'] = [];
        for bar in filtered_Lists:
            bar_dict['name'] = bar['name'];
            bar_dict['size'] = bar['size'];
            bar_dict['description'] = bar['description'];
            # deep copy to be used when handling copy of lists and dict
            Settings['Plot']['Bar'].append(copy.deepcopy(bar_dict));
        
        # print(json.dumps(Settings, sort_keys=True, indent=4));

        FilledString = Filler.FillEntryPoint(Settings, f'html_plot - SR{filex}/template_index.html', f'html_plot - SR{filex}/index.html');

        ReferenceFile = open('ref_files/index.html', 'r').readlines();
        CreatedFile = open(f'html_plot - SR{filex}/index.html', 'r').readlines();
        assert len(ReferenceFile) == len(CreatedFile);
        for line_no in range(len(CreatedFile)):
            assert ReferenceFile[line_no] == CreatedFile[line_no]