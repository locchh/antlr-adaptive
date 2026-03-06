# Generated from SQLiteParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SQLiteParser import SQLiteParser
else:
    from SQLiteParser import SQLiteParser

# This class defines a complete generic visitor for a parse tree produced by SQLiteParser.

class SQLiteParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SQLiteParser#parse.
    def visitParse(self, ctx:SQLiteParser.ParseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#sql_stmt_list.
    def visitSql_stmt_list(self, ctx:SQLiteParser.Sql_stmt_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#sql_stmt.
    def visitSql_stmt(self, ctx:SQLiteParser.Sql_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#alter_table_stmt.
    def visitAlter_table_stmt(self, ctx:SQLiteParser.Alter_table_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#analyze_stmt.
    def visitAnalyze_stmt(self, ctx:SQLiteParser.Analyze_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#attach_stmt.
    def visitAttach_stmt(self, ctx:SQLiteParser.Attach_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#begin_stmt.
    def visitBegin_stmt(self, ctx:SQLiteParser.Begin_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#commit_stmt.
    def visitCommit_stmt(self, ctx:SQLiteParser.Commit_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#rollback_stmt.
    def visitRollback_stmt(self, ctx:SQLiteParser.Rollback_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#savepoint_stmt.
    def visitSavepoint_stmt(self, ctx:SQLiteParser.Savepoint_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#release_stmt.
    def visitRelease_stmt(self, ctx:SQLiteParser.Release_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_index_stmt.
    def visitCreate_index_stmt(self, ctx:SQLiteParser.Create_index_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#indexed_column.
    def visitIndexed_column(self, ctx:SQLiteParser.Indexed_columnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_table_stmt.
    def visitCreate_table_stmt(self, ctx:SQLiteParser.Create_table_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_options.
    def visitTable_options(self, ctx:SQLiteParser.Table_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_def.
    def visitColumn_def(self, ctx:SQLiteParser.Column_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#type_name.
    def visitType_name(self, ctx:SQLiteParser.Type_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_constraint.
    def visitColumn_constraint(self, ctx:SQLiteParser.Column_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#signed_number.
    def visitSigned_number(self, ctx:SQLiteParser.Signed_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_constraint.
    def visitTable_constraint(self, ctx:SQLiteParser.Table_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#foreign_key_clause.
    def visitForeign_key_clause(self, ctx:SQLiteParser.Foreign_key_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#conflict_clause.
    def visitConflict_clause(self, ctx:SQLiteParser.Conflict_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_trigger_stmt.
    def visitCreate_trigger_stmt(self, ctx:SQLiteParser.Create_trigger_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_view_stmt.
    def visitCreate_view_stmt(self, ctx:SQLiteParser.Create_view_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_virtual_table_stmt.
    def visitCreate_virtual_table_stmt(self, ctx:SQLiteParser.Create_virtual_table_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#with_clause.
    def visitWith_clause(self, ctx:SQLiteParser.With_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#common_table_expression.
    def visitCommon_table_expression(self, ctx:SQLiteParser.Common_table_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#cte_table_name.
    def visitCte_table_name(self, ctx:SQLiteParser.Cte_table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#delete_stmt.
    def visitDelete_stmt(self, ctx:SQLiteParser.Delete_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#detach_stmt.
    def visitDetach_stmt(self, ctx:SQLiteParser.Detach_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#drop_stmt.
    def visitDrop_stmt(self, ctx:SQLiteParser.Drop_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr.
    def visitExpr(self, ctx:SQLiteParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_or.
    def visitExpr_or(self, ctx:SQLiteParser.Expr_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_and.
    def visitExpr_and(self, ctx:SQLiteParser.Expr_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_not.
    def visitExpr_not(self, ctx:SQLiteParser.Expr_notContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_binary.
    def visitExpr_binary(self, ctx:SQLiteParser.Expr_binaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_comparison.
    def visitExpr_comparison(self, ctx:SQLiteParser.Expr_comparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_bitwise.
    def visitExpr_bitwise(self, ctx:SQLiteParser.Expr_bitwiseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_addition.
    def visitExpr_addition(self, ctx:SQLiteParser.Expr_additionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_multiplication.
    def visitExpr_multiplication(self, ctx:SQLiteParser.Expr_multiplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_string.
    def visitExpr_string(self, ctx:SQLiteParser.Expr_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_collate.
    def visitExpr_collate(self, ctx:SQLiteParser.Expr_collateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_unary.
    def visitExpr_unary(self, ctx:SQLiteParser.Expr_unaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_base.
    def visitExpr_base(self, ctx:SQLiteParser.Expr_baseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_recursive.
    def visitExpr_recursive(self, ctx:SQLiteParser.Expr_recursiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#raise_function.
    def visitRaise_function(self, ctx:SQLiteParser.Raise_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#literal_value.
    def visitLiteral_value(self, ctx:SQLiteParser.Literal_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#percentile_clause.
    def visitPercentile_clause(self, ctx:SQLiteParser.Percentile_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#value_row.
    def visitValue_row(self, ctx:SQLiteParser.Value_rowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#values_clause.
    def visitValues_clause(self, ctx:SQLiteParser.Values_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#insert_stmt.
    def visitInsert_stmt(self, ctx:SQLiteParser.Insert_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#returning_clause.
    def visitReturning_clause(self, ctx:SQLiteParser.Returning_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#upsert_clause.
    def visitUpsert_clause(self, ctx:SQLiteParser.Upsert_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#pragma_stmt.
    def visitPragma_stmt(self, ctx:SQLiteParser.Pragma_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#pragma_value.
    def visitPragma_value(self, ctx:SQLiteParser.Pragma_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#reindex_stmt.
    def visitReindex_stmt(self, ctx:SQLiteParser.Reindex_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#select_stmt.
    def visitSelect_stmt(self, ctx:SQLiteParser.Select_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#join_clause.
    def visitJoin_clause(self, ctx:SQLiteParser.Join_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#select_core.
    def visitSelect_core(self, ctx:SQLiteParser.Select_coreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_or_subquery.
    def visitTable_or_subquery(self, ctx:SQLiteParser.Table_or_subqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#result_column.
    def visitResult_column(self, ctx:SQLiteParser.Result_columnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#join_operator.
    def visitJoin_operator(self, ctx:SQLiteParser.Join_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#join_constraint.
    def visitJoin_constraint(self, ctx:SQLiteParser.Join_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#compound_operator.
    def visitCompound_operator(self, ctx:SQLiteParser.Compound_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#update_stmt.
    def visitUpdate_stmt(self, ctx:SQLiteParser.Update_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_name_list.
    def visitColumn_name_list(self, ctx:SQLiteParser.Column_name_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#qualified_table_name.
    def visitQualified_table_name(self, ctx:SQLiteParser.Qualified_table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#vacuum_stmt.
    def visitVacuum_stmt(self, ctx:SQLiteParser.Vacuum_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#filter_clause.
    def visitFilter_clause(self, ctx:SQLiteParser.Filter_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#window_defn.
    def visitWindow_defn(self, ctx:SQLiteParser.Window_defnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#over_clause.
    def visitOver_clause(self, ctx:SQLiteParser.Over_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_spec.
    def visitFrame_spec(self, ctx:SQLiteParser.Frame_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_clause.
    def visitFrame_clause(self, ctx:SQLiteParser.Frame_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#order_clause.
    def visitOrder_clause(self, ctx:SQLiteParser.Order_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#limit_clause.
    def visitLimit_clause(self, ctx:SQLiteParser.Limit_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#ordering_term.
    def visitOrdering_term(self, ctx:SQLiteParser.Ordering_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#asc_desc.
    def visitAsc_desc(self, ctx:SQLiteParser.Asc_descContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_left.
    def visitFrame_left(self, ctx:SQLiteParser.Frame_leftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_right.
    def visitFrame_right(self, ctx:SQLiteParser.Frame_rightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_single.
    def visitFrame_single(self, ctx:SQLiteParser.Frame_singleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#error_message.
    def visitError_message(self, ctx:SQLiteParser.Error_messageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#filename.
    def visitFilename(self, ctx:SQLiteParser.FilenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#module_argument.
    def visitModule_argument(self, ctx:SQLiteParser.Module_argumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#module_argument_outer.
    def visitModule_argument_outer(self, ctx:SQLiteParser.Module_argument_outerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#module_argument_inner.
    def visitModule_argument_inner(self, ctx:SQLiteParser.Module_argument_innerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#fallback_excluding_conflicts.
    def visitFallback_excluding_conflicts(self, ctx:SQLiteParser.Fallback_excluding_conflictsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#join_keyword.
    def visitJoin_keyword(self, ctx:SQLiteParser.Join_keywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#fallback.
    def visitFallback(self, ctx:SQLiteParser.FallbackContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#name.
    def visitName(self, ctx:SQLiteParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#function_name.
    def visitFunction_name(self, ctx:SQLiteParser.Function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#schema_name.
    def visitSchema_name(self, ctx:SQLiteParser.Schema_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_name.
    def visitTable_name(self, ctx:SQLiteParser.Table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_or_index_name.
    def visitTable_or_index_name(self, ctx:SQLiteParser.Table_or_index_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_name.
    def visitColumn_name(self, ctx:SQLiteParser.Column_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_name_excluding_string.
    def visitColumn_name_excluding_string(self, ctx:SQLiteParser.Column_name_excluding_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_alias.
    def visitColumn_alias(self, ctx:SQLiteParser.Column_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#collation_name.
    def visitCollation_name(self, ctx:SQLiteParser.Collation_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#foreign_table.
    def visitForeign_table(self, ctx:SQLiteParser.Foreign_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#index_name.
    def visitIndex_name(self, ctx:SQLiteParser.Index_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#trigger_name.
    def visitTrigger_name(self, ctx:SQLiteParser.Trigger_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#view_name.
    def visitView_name(self, ctx:SQLiteParser.View_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#module_name.
    def visitModule_name(self, ctx:SQLiteParser.Module_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#pragma_name.
    def visitPragma_name(self, ctx:SQLiteParser.Pragma_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#savepoint_name.
    def visitSavepoint_name(self, ctx:SQLiteParser.Savepoint_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_alias.
    def visitTable_alias(self, ctx:SQLiteParser.Table_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_alias_excluding_joins.
    def visitTable_alias_excluding_joins(self, ctx:SQLiteParser.Table_alias_excluding_joinsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#window_name.
    def visitWindow_name(self, ctx:SQLiteParser.Window_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#alias.
    def visitAlias(self, ctx:SQLiteParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#base_window_name.
    def visitBase_window_name(self, ctx:SQLiteParser.Base_window_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_function_name.
    def visitTable_function_name(self, ctx:SQLiteParser.Table_function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#any_name_excluding_raise.
    def visitAny_name_excluding_raise(self, ctx:SQLiteParser.Any_name_excluding_raiseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#any_name_excluding_joins.
    def visitAny_name_excluding_joins(self, ctx:SQLiteParser.Any_name_excluding_joinsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#any_name_excluding_string.
    def visitAny_name_excluding_string(self, ctx:SQLiteParser.Any_name_excluding_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#any_name.
    def visitAny_name(self, ctx:SQLiteParser.Any_nameContext):
        return self.visitChildren(ctx)



del SQLiteParser