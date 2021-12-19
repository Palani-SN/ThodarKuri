import copy
import json
from ThodarKuri.Filler import FillerTemplateEngine
 
with open('ref_files/Settings.json') as config:
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

Filler = FillerTemplateEngine();
FilledString = Filler.FillEntryPoint(Settings, "html_plot - SR1/template_index.html", "html_plot - SR1/index.html");
