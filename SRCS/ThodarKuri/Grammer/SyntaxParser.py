from lark import Lark, Transformer, v_args

# Command 1 : adds the key *Title* to the current dict with value *None*

#       R[Title] 
  
# Command 2 : adds the key *Plot* to the current dict with value **as dict** of file *template_plot.html*

#       R[Plot] => template_plot.html
#       R[Plot] => templates/template_plot.html
 
# Command 3 : adds the key *Bar* to the current dict with value **as list of dict** of file *template_bar.html*

#       ( R[Bar] => template_bar.html )*
#       ( R[Bar] => templates/template_bar.html )*
 

TK_Grammer = """
        ?start: var
              | dictvar
              | listvar

        ?listvar: "(" dictvar ")*" -> getdictvaraslist
        
        ?dictvar: "R["VAR"] => "filepath -> getvarasdict
        
        ?var: "R["VAR"]" -> getvar

        VAR: /[a-zA-Z_][a-zA-Z0-9_]*/
        filepath: (PATH_PART SEPERATOR)* PATH_PART DOT EXTENSION

        PATH_PART: /[a-zA-Z0-9_-]*/
        SEPERATOR: /[\\/\\\\]/
        DOT: "."
        EXTENSION: /[a-zA-Z0-9]+/

        %import common.WS_INLINE
        %ignore WS_INLINE 

    """

@v_args(inline=True)    
class TK_Parser(Transformer):

    def __init__(self):
        pass

    # Gets variable name in command of type 1
    # " R[Var_new_1] " returns a dict { 'VAR' : 'Var_new_1' }
    def getvar(self, var):

        Dict = { var.type : var.value }
        return Dict

    # Gets the variable name and the filename of the command of type 2
    # " R[Var_new_3] => files1.html " returns a dict { 'Var_new_3' : 'files1.html' }
    # " R[Var_new_3] => templates/files1.html "  returns a dict { 'Var_new_3' : 'templates/files1.html' }
    def getvarasdict(self, var, file):
        # Reconstruct the full file path from the parsed tree
        # files is a Tree object with children [PATH_PART, SEPERATOR, PATH_PART, '.', EXTENSION, ...]
        if hasattr(file, 'children'):
            parts = []
            for child in file.children:
                if hasattr(child, 'value'):
                    parts.append(child.value)
                else:
                    parts.append(str(child))
            filepath = ''.join(parts)
        else:
            filepath = str(file)
        Dict = { var.value: filepath }
        return Dict

    # Gets the variable name and the filename of the command of type 3
    # " ( R[Var_new_4] => files2.html )* " returns a list [{ 'Var_new_4' : 'files2.html' },]
    def getdictvaraslist(self, dictvar):

        List = [dictvar];
        return List

# Parser Initialisation
TK_Template = Lark(TK_Grammer, parser='lalr', transformer=TK_Parser())
ThodarkuriParser = TK_Template.parse

# 
# (see TemplatesSpecification.png & FilledFile.png) for the usage guidance
#
# Visit @Palani-SN(github profile) or send messages to
# psn396@gmail.com.
#