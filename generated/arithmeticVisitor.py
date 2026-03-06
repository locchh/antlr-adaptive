# Generated from arithmetic.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .arithmeticParser import arithmeticParser
else:
    from arithmeticParser import arithmeticParser

# This class defines a complete generic visitor for a parse tree produced by arithmeticParser.

class arithmeticVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by arithmeticParser#file_.
    def visitFile_(self, ctx:arithmeticParser.File_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by arithmeticParser#equation.
    def visitEquation(self, ctx:arithmeticParser.EquationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by arithmeticParser#expression.
    def visitExpression(self, ctx:arithmeticParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by arithmeticParser#atom.
    def visitAtom(self, ctx:arithmeticParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by arithmeticParser#scientific.
    def visitScientific(self, ctx:arithmeticParser.ScientificContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by arithmeticParser#variable.
    def visitVariable(self, ctx:arithmeticParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by arithmeticParser#relop.
    def visitRelop(self, ctx:arithmeticParser.RelopContext):
        return self.visitChildren(ctx)



del arithmeticParser