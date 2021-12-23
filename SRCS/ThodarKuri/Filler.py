import re
import os
import json
from .Grammer.SyntaxParser import ThodarkuriParser

# class : TemplateEngine(for FILLING)
# The class will be used to fill a template and write the resultant content as a filename
class FillerTemplateEngine():

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

    # method : __FillNode
    # Internal function process the node and returns the content for each node in a file.
    # Parameters : 
    #   arg1 - content [ Content in which a node to be replaced ]
    #   arg2 - MapDict [ helper dict for replacing the node of the content ]
    #   arg3 - node [ the node which has to be replaced in the content ]
    # Returns : 
    #   content - the result as a string [ node in Content replaced with mapdict element ]
    def __FillNode(self, content, MapDict, node):

        InpNode = node[self.__LeadTrailSpecs[0][1]:self.__LeadTrailSpecs[1][1]].strip();

        # using Parser as interpreter for node
        RetVal = ThodarkuriParser(InpNode)

        # processing node catogorised as type List
        if(str(type(RetVal)) == "<class 'list'>"):
            for x,y in RetVal[0].items():
                content = content.replace(node, ''.join([ self.__FillContent(y, each) for each in MapDict[x] ]) )

        # processing node catogorised as type dict     
        if(str(type(RetVal)) == "<class 'dict'>"):
            if('VAR' in RetVal.keys()):
                content = content.replace(node, str(MapDict[RetVal['VAR']]))
            else:
                for x,y in RetVal.items():
                    content = content.replace(node, self.__FillContent(y, MapDict[x]))

        return content;
    
    # method : __FillContent
    # Internal function process all the nodes of the content and returns the content with each nodes replaced with the actual content.
    # Parameters : 
    #   arg1 - TemplateName [ filename of the content to be replaced ]
    #   arg2 - MapDict [ helper dict for replacing the nodes in the content of the filename ]
    # Returns : 
    #   content - the result as a string [ all nodes in Content replaced with mapdict elements ]
    def __FillContent(self, TemplateName, MapDict):

        # reading content from filename
        template = open(os.path.join(self.__FolderPath, TemplateName), 'r');
        content = template.read();
        template.close();

        # replacing all nodes of the content 
        func_calls = [content[m.start(0):m.end(0)] for m in re.finditer(self.__pattern, content)];
        for x in func_calls:
            InpNode = x[self.__LeadTrailSpecs[0][1]:self.__LeadTrailSpecs[1][1]].strip();
            if(InpNode.startswith('#')):
                content = content.replace(x, '');
            else:
                content = self.__FillNode(content, MapDict, x);
            
        return content;
        
    # method : FillEntryPoint
    # Gets the Edited Dictionary Skeleton of the template and the template path to be used.
    # Will initialize the MapDict for updating the function calls in the template.
    # Will fill the content of the files as per the dictionary recursively. 
    # Parameters : 
    #   arg1 - MapDict [ a Dict that is generated using the parser class and contains the edited content from the user ]
    #   arg2 - TemplateName [ the path of the template entry point that has been used ]
    #   arg3 - FileName [ new filename with which the final content to be saved ]
    #   arg4 - DebugTokens [ If True prints the mappedstr from the template, if False doesn't print ]
    # Returns : 
    #   MappedStr - the result as a string [ filled templates with mapdict ]
    def FillEntryPoint(self, MapDict, TemplateName, FileName = None, DebugTokens = False):

        self.__FolderPath = os.path.dirname(os.path.abspath(TemplateName));

        # Filling entry point 
        MappedStr = self.__FillContent(os.path.basename(TemplateName), MapDict);
        if(DebugTokens): print(MappedStr);

        # Writing the final content as file if FileName is provided
        if(FileName != None):
            OutputFile = open(FileName, "w");
            OutputFile.write(MappedStr)
            OutputFile.close();
        
        return MappedStr;

# 
# (see TemplatesSpecification.png & FilledFile.png) for the usage guidance
#
# Visit @Palani-SN(github profile) or send messages to
# psn396@gmail.com.
#