import re
import os
import json
from .Grammer.SyntaxParser import ThodarkuriParser

class FillerTemplateEngine():

    def __init__(self, RegexEdges=("{{", "}}"), FuncCallTemplate="{{self.FUNC_CALL()}}"):

        RegexPattern=f"{RegexEdges[0]} *(?:(?!{RegexEdges[1]}).)*{RegexEdges[1]}";
        func_call = [FuncCallTemplate[m.start(0):m.end(0)] for m in re.finditer(RegexPattern, FuncCallTemplate)][0]
        assert func_call == FuncCallTemplate, "RegexPattern and FuncCallTemplate not matching"
        
        lst = re.split("self.FUNC_CALL\\(\\)", func_call.replace(" ", ""));
        cap, cap_len, shoe ,shoe_len = tuple([ lst[0], len(lst[0]), lst[1], len(lst[1]) ]);
        assert FuncCallTemplate[cap_len:-shoe_len].strip() == "self.FUNC_CALL()", """     Second Parameter has 3 parts, \n <LEADING_EDGE><FUNC_CALL><TRAILING_EDGE>""";
        
        self.__pattern = RegexPattern.replace("*self.","*#* *self.");
        self.__LeadTrailSpecs = [ ( cap, cap_len ), ( shoe, -shoe_len )];

    def __FillNode(self, content, MapDict, node):

        InpNode = node[self.__LeadTrailSpecs[0][1]:self.__LeadTrailSpecs[1][1]].strip();
        RetVal = ThodarkuriParser(InpNode)
        if(str(type(RetVal)) == "<class 'list'>"):
            for x,y in RetVal[0].items():
                content = content.replace(node, ''.join([ self.__FillContent(y, each) for each in MapDict[x] ]) )
                    
        if(str(type(RetVal)) == "<class 'dict'>"):
            if('VAR' in RetVal.keys()):
                content = content.replace(node, str(MapDict[RetVal['VAR']]))
            else:
                for x,y in RetVal.items():
                    content = content.replace(node, self.__FillContent(y, MapDict[x]))

        return content;
    
    def __FillContent(self, TemplateName, MapDict):

        template = open(os.path.join(self.__FolderPath, TemplateName), 'r');
        content = template.read();
        template.close();

        func_calls = [content[m.start(0):m.end(0)] for m in re.finditer(self.__pattern, content)];
        for x in func_calls:
            InpNode = x[self.__LeadTrailSpecs[0][1]:self.__LeadTrailSpecs[1][1]].strip();
            if(InpNode.startswith('#')):
                content = content.replace(x, '');
            else:
                content = self.__FillNode(content, MapDict, x);
            
        return content;
        
    def FillEntryPoint(self, MapDict, TemplateName, FileName = None, DebugTokens = False):

        self.__FolderPath = os.path.dirname(os.path.abspath(TemplateName));
        MappedStr = self.__FillContent(os.path.basename(TemplateName), MapDict);
        if(DebugTokens): print(MappedStr);
        if(FileName != None):
            OutputFile = open(FileName, "w");
            OutputFile.write(MappedStr)
            OutputFile.close();
        return MappedStr;
