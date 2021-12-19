from ThodarKuri.Parser import ParserTemplateEngine
import json
import pytest

@pytest.fixture
def DefaultRegex1():
    TE = ParserTemplateEngine();
    return TE;

def test_DefaultCase1(DefaultRegex1):

    Parser = DefaultRegex1;
    Settings = Parser.ParseEntryPoint("html_plot/template_index.html");

    # print(json.dumps(Settings, sort_keys=True, indent=4));

    OutputFile = open('gen_files/Settings.json', "w");
    OutputFile.write(json.dumps(Settings, sort_keys=True, indent=4))
    OutputFile.close();

    ReferenceFile = open("ref_files/Reference_Settings.json", 'r').readlines();
    CreatedFile = open("gen_files/Settings.json", 'r').readlines();
    assert len(ReferenceFile) == len(CreatedFile);
    for line_no in range(len(CreatedFile)):
        assert ReferenceFile[line_no] == CreatedFile[line_no]

@pytest.fixture
def SpecialRegex1():
    TE = ParserTemplateEngine(("_StArT_", "_eNd_"), "_StArT_self.FUNC_CALL()_eNd_");
    return TE;

@pytest.fixture
def SpecialRegex2():
    TE = ParserTemplateEngine(("<<", ">>"), "<<self.FUNC_CALL()>>");
    return TE;

@pytest.fixture
def SpecialRegex3():
    TE = ParserTemplateEngine(("\\[\\[", "\\]\\]"), "[[self.FUNC_CALL()]]");
    return TE;

@pytest.fixture
def SpecialRegex4():
    TE = ParserTemplateEngine(("{\\[<{\\[", "}\\]>}\\]"), "{[<{[self.FUNC_CALL()}]>}]");
    return TE;


def test_SpecialCase1(SpecialRegex1, SpecialRegex2, SpecialRegex3, SpecialRegex4):

    for filex in ([1,2,3,4]):

        if(filex==1):Parser = SpecialRegex1;
        if(filex==2):Parser = SpecialRegex2;
        if(filex==3):Parser = SpecialRegex3;
        if(filex==4):Parser = SpecialRegex4;

        Settings = Parser.ParseEntryPoint(f'html_plot - SR{filex}/template_index.html');

        # print(json.dumps(Settings, sort_keys=True, indent=4));

        OutputFile = open(f'gen_files/Settings - SR{filex}.json', "w");
        OutputFile.write(json.dumps(Settings, sort_keys=True, indent=4))
        OutputFile.close();

        ReferenceFile = open("ref_files/Reference_Settings.json", 'r').readlines();
        CreatedFile = open(f'gen_files/Settings - SR{filex}.json', 'r').readlines();
        assert len(ReferenceFile) == len(CreatedFile);
        for line_no in range(len(CreatedFile)):
            assert ReferenceFile[line_no] == CreatedFile[line_no]
