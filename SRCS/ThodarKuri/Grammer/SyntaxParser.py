from lark import Lark, Transformer, v_args

TK_Grammer = """
        ?start: var
              | dictvar
              | listvar

        ?listvar: "(" dictvar ")*" -> getdictvaraslist
        
        ?dictvar: "R["VAR"] => "FILE -> getvarasdict
        
        ?var: "R["VAR"]" -> getvar

        VAR: /[a-zA-Z_]\\w*/
        FILE: /[a-zA-Z_]\\w*.[a-zA-Z_]\\w*/

        %import common.WS_INLINE
        %ignore WS_INLINE 

    """

@v_args(inline=True)    
class TK_Parser(Transformer):

    def __init__(self):
        pass

    def getvar(self, var):

        Dict = { var.type : var.value }
        return Dict

    def getvarasdict(self, var, file):


        Dict = { var.value: file.value }
        return Dict

    def getdictvaraslist(self, dictvar):

        List = [dictvar];
        return List

TK_Template = Lark(TK_Grammer, parser='lalr', transformer=TK_Parser())
ThodarkuriParser = TK_Template.parse
