import os
import pytest
from ThodarKuri.Parser import ParserTemplateEngine


def test_parsecontent_raises_when_template_outside_folder(tmp_path):
    engine = ParserTemplateEngine()

    # create a folder under tmp_path
    folder = os.path.join(str(tmp_path), 'inside')
    os.makedirs(folder, exist_ok=True)

    # create a template path that is deliberately outside the folder
    outside_template = os.path.abspath(os.path.join(str(tmp_path), '..', 'outside.html'))

    # Call the private method to trigger the check
    private_method = engine._ParserTemplateEngine__ParseContent

    with pytest.raises(Exception) as excinfo:
        private_method(folder, outside_template)

    assert 'should always be within' in str(excinfo.value)
