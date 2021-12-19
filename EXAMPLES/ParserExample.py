import json
from ThodarKuri.Parser import ParserTemplateEngine
 
Parser = ParserTemplateEngine();
Settings = Parser.ParseEntryPoint("html_plot - SR1/template_index.html");

# print(json.dumps(Settings, sort_keys=True, indent=4));

OutputFile = open('ref_files/Settings.json', "w");
OutputFile.write(json.dumps(Settings, sort_keys=True, indent=4))
OutputFile.close();
