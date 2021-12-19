import requests, sys
import json
from ThodarKuri.Parser import ParserTemplateEngine
from ThodarKuri.Filler import FillerTemplateEngine
import copy
 
try:
	server = "https://rest.ensembl.org"
	ext = "/info/variation/populations/homo_sapiens?filter=LD"
	 
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	 
	if not r.ok:
	  r.raise_for_status()
	  sys.exit()
	 
	PlotDetails = r.json()
	OutputFile = open('ref_files/PlotDetails.json', "w");
	OutputFile.write(json.dumps(PlotDetails, sort_keys=True, indent=4))
	OutputFile.close();
except:
    with open('ref_files/PlotDetails.json') as Details:
        PlotDetails = json.load(Details)

Parser = ParserTemplateEngine();
Settings = Parser.ParseEntryPoint("html_plot - SR1/template_index.html");

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

Filler = FillerTemplateEngine();
FilledString = Filler.FillEntryPoint(Settings, "html_plot - SR1/template_index.html", "html_plot - SR1/index.html");
