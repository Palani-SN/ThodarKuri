import re
import os
import json
from .Grammer.SyntaxParser import ThodarkuriParser

class ParserTemplateEngine():

    def __init__(self, RegexEdges=("{{", "}}"), FuncCallTemplate="{{self.FUNC_CALL()}}"):

        RegexPattern=f"{RegexEdges[0]} *(?:(?!{RegexEdges[1]}).)*{RegexEdges[1]}";
        func_call = [FuncCallTemplate[m.start(0):m.end(0)] for m in re.finditer(RegexPattern, FuncCallTemplate)][0]
        assert func_call == FuncCallTemplate, "RegexPattern and FuncCallTemplate not matching"
        
        lst = re.split("self.FUNC_CALL\\(\\)", func_call.replace(" ", ""));
        cap, cap_len, shoe ,shoe_len = tuple([ lst[0], len(lst[0]), lst[1], len(lst[1]) ]);
        assert FuncCallTemplate[cap_len:-shoe_len].strip() == "self.FUNC_CALL()", """     Second Parameter has 3 parts, \n <LEADING_EDGE><FUNC_CALL><TRAILING_EDGE>""";
        
        self.__pattern = RegexPattern.replace("*self.","*#* *self.");
        self.__LeadTrailSpecs = [ ( cap, cap_len ), ( shoe, -shoe_len )];

    def __ParseNode(self, MapDict, node):

        RetVal = ThodarkuriParser(node)

        if(str(type(RetVal)) == "<class 'list'>"):
            for x,y in RetVal[0].items():
                MapDict[x]=[self.__ParseContent(y)];
                    
        if(str(type(RetVal)) == "<class 'dict'>"):
            if('VAR' in RetVal.keys()):
                MapDict[RetVal['VAR']] = None;
            else:
                for x,y in RetVal.items():
                    MapDict[x]=self.__ParseContent(y);
                    
        return MapDict;


    def __ParseContent(self, TemplateName):
        
        template = open(os.path.join(self.__FolderPath, TemplateName), 'r');
        self.__content = template.read();
        template.close();

        MapDict = {};
        func_calls = [self.__content[m.start(0):m.end(0)] for m in re.finditer(self.__pattern, self.__content)];
        for x in func_calls:
            InpNode = x[self.__LeadTrailSpecs[0][1]:self.__LeadTrailSpecs[1][1]].strip();
            if(not(InpNode.startswith('#'))):
                MapDict = self.__ParseNode(MapDict, InpNode);
            
        return MapDict;

    def ParseEntryPoint(self, TemplateName, DebugTokens = False):

        TemplateName = os.path.abspath(TemplateName);
        self.__FolderPath = os.path.dirname(TemplateName);
        MapDict = self.__ParseContent(TemplateName);
        if(DebugTokens): print(json.dumps(MapDict, sort_keys=True, indent=4));
        return MapDict;
        