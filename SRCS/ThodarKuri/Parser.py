import re
import os
import json
from collections import defaultdict
from .Grammer.SyntaxParser import ThodarkuriParser

# class : TemplateEngine(for PARSING)
# The class will be used to parse a template and return the editable parts of the template as Nested Dictionary.
class ParserTemplateEngine():

    # constructor : __init__
    # Defines the configuration of the template function calls that is going to be used.
    # Configuration specified will be validated for the authenticity of Regex Pattern. 
    # Parameters : 
    #   arg1 - RegexEdges [a Tuple with a leading edge and trailing edge]
    #   arg2 - FuncCallTemplate [a string for initial validation of the RegexEdges]
    def __init__(self, RegexEdges=("{{", "}}"), FuncCallTemplate="{{self.FUNC_CALL()}}"):

        #Verify REGEX Pattern
        RegexPattern=f"{RegexEdges[0]} *(?:(?!{RegexEdges[1]}).)*{RegexEdges[1]}";
        func_call = [FuncCallTemplate[m.start(0):m.end(0)] for m in re.finditer(RegexPattern, FuncCallTemplate)][0]
        assert func_call == FuncCallTemplate, "RegexPattern and FuncCallTemplate not matching"
        
        #Verify FUNC_CALL Template
        lst = re.split("self.FUNC_CALL\\(\\)", func_call.replace(" ", ""));
        cap, cap_len, shoe ,shoe_len = tuple([ lst[0], len(lst[0]), lst[1], len(lst[1]) ]);
        assert FuncCallTemplate[cap_len:-shoe_len].strip() == "self.FUNC_CALL()", """     Second Parameter has 3 parts, \n <LEADING_EDGE><FUNC_CALL><TRAILING_EDGE>""";
        
        #Finalizing the REGEX pattern, Leading edge, Trailing edge specifications
        self.__pattern = RegexPattern.replace("*self.","*#* *self.");
        self.__LeadTrailSpecs = [ ( cap, cap_len ), ( shoe, -shoe_len )];

    # method : __ParseNode
    # Internal function process the node and returns the dict for the node provided.
    # Parameters : 
    #   arg1 - MapDict [ the MapDict which has the nodes present in the current file ]
    #   arg2 - node [ the node which has to be added to the MapDict ]
    # Returns : 
    #   MapDict - the result as a Dict [ helper dict with elements equivalent to the node provided ]
    def __ParseNode(self, RootPath, MapDict, node):

        # using Parser as interpreter for node
        RetVal = ThodarkuriParser(node)

        # processing node catogorised as type List
        if(str(type(RetVal)) == "<class 'list'>"):
            for x,y in RetVal[0].items():
                RelPath = os.path.join(RootPath, y)
                TemplateName = os.path.abspath(RelPath);
                FolderPath = os.path.dirname(TemplateName);
                # Do not mark the template here; __ParseContent will manage the recursion guard
                MapDict[x]=[self.__ParseContent(FolderPath ,TemplateName)];
                    
        # processing node catogorised as type dict 
        if(str(type(RetVal)) == "<class 'dict'>"):
            if('VAR' in RetVal.keys()):
                MapDict[RetVal['VAR']] = None;
            else:
                for x,y in RetVal.items():
                    RelPath = os.path.join(RootPath, y)
                    TemplateName = os.path.abspath(RelPath);
                    FolderPath = os.path.dirname(TemplateName);
                    # Do not mark the template here; __ParseContent will manage the recursion guard
                    MapDict[x]=self.__ParseContent(FolderPath ,TemplateName);
                    
        return MapDict;

    # method : __ParseContent
    # Internal function process all the nodes of the content and returns a dict with each nodes added to it.
    # Parameters : 
    #   arg1 - TemplateName [ filename of the content to be replaced ]
    # Returns : 
    #   MapDict - the result as a Dict [ helper dict with elements equivalent to the nodes present in the content of the filename ]
    def __ParseContent(self, FolderPath, TemplateName):
        
        if not os.path.commonpath([FolderPath, TemplateName]) == FolderPath:
            raise Exception(f"{TemplateName} should always be within {FolderPath}")

        # ensure folder entry exists
        if FolderPath not in self.template_lookups:
            self.template_lookups[FolderPath] = set()

        # if already visiting this template, return empty map to avoid infinite recursion
        if TemplateName in self.template_lookups[FolderPath]:
            return {}

        # mark as visiting
        self.template_lookups[FolderPath].add(TemplateName)
        try:
            # reading content from filename
            template = open(TemplateName, 'r', encoding='utf-8');
            self.__content = template.read();
            template.close();

            # generating MapDict with respect to all nodes present in the content 
            MapDict = {};
            func_calls = [self.__content[m.start(0):m.end(0)] for m in re.finditer(self.__pattern, self.__content)];
            for x in func_calls:
                InpNode = x[self.__LeadTrailSpecs[0][1]:self.__LeadTrailSpecs[1][1]].strip();
                if(not(InpNode.startswith('#'))):
                    MapDict = self.__ParseNode(FolderPath, MapDict, InpNode);
                
            return MapDict;
        finally:
            # unmark visiting
            self.template_lookups[FolderPath].remove(TemplateName)
            if not self.template_lookups[FolderPath]:
                del self.template_lookups[FolderPath]

    # method : ParseEntryPoint
    # Gets the template path to be edited.
    # Will generated a nested dictionary out of the editable parts in the templates recursively.
    # Parameters : 
    #   arg1 - TemplateName [ the path of the template entry point that has been used ]
    #   arg2 - DebugTokens [ If True prints the mappedDict as JSON from the template, if False doesn't print ]
    # Returns : 
    #   MapDict - the result as a dict [ a Dict that is generated from the template name provided ] 
    def ParseEntryPoint(self, TemplateName, DebugTokens = False):

        TemplateName = os.path.abspath(TemplateName);
        FolderPath = os.path.dirname(TemplateName);

        self.template_lookups = defaultdict(set);
        # Parsing entry point 
        MapDict = self.__ParseContent(FolderPath, TemplateName);
        if(DebugTokens): print(json.dumps(MapDict, sort_keys=True, indent=4));

        return MapDict;
    
    # 
    # (see TemplatesSpecification.png & FilledFile.png) for the usage guidance
    #
    # Visit @Palani-SN(github profile) or send messages to
    # psn396@gmail.com.
    #