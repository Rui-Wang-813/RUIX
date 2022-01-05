package com.craftinginterpreters.lox;

public class AstPrinter implements Expr.Visitor<String> {
    String print(Expr expr) {
        return expr.accept(this);
    }

    @Override
    public String visitBinaryExpr(Expr.Binary expr) {
        return parenthesize(expr.operator.lexeme, expr.left, expr.right);
    }

    @Override
    public String visitGroupingExpr(Expr.Grouping expr) {
        return parenthesize("group", expr.expression);
    }

    @Override
    public String visitLiteralExpr(Expr.Literal expr) {
        if (expr.value == null) return "nil";
        return expr.value.toString();
    }

    @Override
    public String visitUnaryExpr(Expr.Unary expr) {
        return parenthesize(expr.operator.lexeme, expr.right);
    }

    @Override
    public String visitVariableExpr(Expr.Variable expr) {
        return expr.name.lexeme;
    }

    @Override
    public String visitAssignExpr(Expr.Assign expr) {
        return parenthesize2("=", expr.name.lexeme, expr.value);
    }

    private String parenthesize(String lexeme, Expr...exprs) {
        StringBuilder builder = new StringBuilder();

        builder.append("(").append(lexeme);
        for (Expr expr : exprs) {
        builder.append(" ");
        builder.append(expr.accept(this));
        }
        builder.append(")");

        return builder.toString();
    }

    private String parenthesize2(String name, Object... parts) {
        StringBuilder builder = new StringBuilder();
    
        builder.append("(").append(name);
    
        for (Object part : parts) {
          builder.append(" ");
    
          if (part instanceof Expr) {
            builder.append(((Expr)part).accept(this));
          } else if (part instanceof Token) {
            builder.append(((Token) part).lexeme);
          } else {
            builder.append(part);
          }
        }
        builder.append(")");
    
        return builder.toString();
      }
}
