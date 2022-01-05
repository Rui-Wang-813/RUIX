package com.craftinginterpreters.lox;

import java.util.List;

public class Interpreter implements Expr.Visitor<Object>, Stmt.Visitor<Void> {

    // IDENTIFIER -> value.
    private Environment env = new Environment();

    // public interface to interpret a list of statements.
    public void interpret(List<Stmt> statements) {
        try {
            for (Stmt statement: statements) {
                execute(statement);
            }
        } catch(RuntimeError e) {
            Lox.runtimeError(e);
        }
    }

    // execute block statement.
    @Override
    public Void visitBlockStmt(Stmt.Block stmt) {
        env = new Environment(env); // create a new environment for this block, nested in current env.

        try {
            for (Stmt statement: stmt.statements) {
                execute(statement);
            }
        } finally {
            // after all statements are executed, restore the environment.
            env = env.enclosing;
        }

        return null;
    }

    // execute variable declaration statement.
    @Override
    public Void visitVarStmt(Stmt.Var stmt) {
        Object value = null;
        if (stmt.initializer != null) {
            value = evaluate(stmt.initializer);
        }

        env.define(stmt.name.lexeme, value);
        return null;
    }

    // execute expression statement.
    @Override
    public Void visitExpressionStmt(Stmt.Expression stmt) {
        evaluate(stmt.expression);
        return null;
    }

    // execute print statement.
    @Override
    public Void visitPrintStmt(Stmt.Print stmt) {
        Object value = evaluate(stmt.expression);
        System.out.println(stringify(value));
        return null;
    }

    // evaluate assignment expression.
    @Override
    public Object visitAssignExpr(Expr.Assign expr) {
        Object value = evaluate(expr.value);
        env.assign(expr.name, value);
        
        return value;
    }

    // evaluate binary expression.
    @Override
    public Object visitBinaryExpr(Expr.Binary expr) {
        // as the operator is binary, there will be two operands.
        Object lt_val = evaluate(expr.left);
        Object rt_val = evaluate(expr.right);

        switch (expr.operator.type) {
            case MINUS:
                checkBothNumber(expr.operator, lt_val, rt_val);
                return (double)lt_val - (double)rt_val;
            case SLASH:
                checkBothNumber(expr.operator, lt_val, rt_val);
                return (double)lt_val / (double)rt_val;
            case STAR:
                checkBothNumber(expr.operator, lt_val, rt_val);
                return (double)lt_val * (double)rt_val;
            case PLUS:
                if (lt_val instanceof Double && rt_val instanceof Double) {
                    return (double)lt_val + (double)rt_val;
                }
                if (lt_val instanceof String && rt_val instanceof String) {
                    return (String)lt_val + (String)rt_val;
                }
                throw new RuntimeError(expr.operator, "Operands must be two String's or two Number's.");
            case GREATER:
                checkBothNumber(expr.operator, lt_val, rt_val);
                return (double)lt_val > (double)rt_val;
            case GREATER_EQUAL:
                checkBothNumber(expr.operator, lt_val, rt_val);
                return (double)lt_val >= (double)rt_val;
            case LESS:
                checkBothNumber(expr.operator, lt_val, rt_val);
                return (double)lt_val < (double)rt_val;
            case LESS_EQUAL:
                checkBothNumber(expr.operator, lt_val, rt_val);
                return (double)lt_val <= (double)rt_val;
            case BANG_EQUAL:
                return !isEqual(lt_val, rt_val);
            case EQUAL_EQUAL:
                return isEqual(lt_val, rt_val);
            default:
                break;
        }
        return null;
    }

    // evaluate grouping expression.
    @Override
    public Object visitGroupingExpr(Expr.Grouping expr) {
        // a grouping expression is just a skin of another expression.
        return evaluate(expr.expression);
    }

    // get the value of literal.
    @Override
    public Object visitLiteralExpr(Expr.Literal expr) {
        return expr.value;
    }

    // evaluate unary expression.
    @Override
    public Object visitUnaryExpr(Expr.Unary expr) {
        Object val = evaluate(expr.right);
        switch (expr.operator.type) {
            case MINUS:
                checkIsNumber(expr.operator, val);
                return -(double)val;
            case BANG:
                return !isTruthy(val);
            default:
                break;
        }
        return null;
    }

    // evaluate variable expression.
    @Override
    public Object visitVariableExpr(Expr.Variable expr) {
        return env.get(expr.name);
    }

    // simply a wrapper to evaluate expression.
    private Object evaluate(Expr expr) {
        return expr.accept(this);
    }

    // simply a wrapper to execute statement.
    private Void execute(Stmt stmt) {
        return stmt.accept(this);
    }

    // whether the val is truthy. (true in an if statement)
    private boolean isTruthy(Object val) {
        if (val == null) return false;
        if (val instanceof Boolean) {
            return (boolean)val;
        }
        return true;
    }

    // whether the two objects are equal.
    private boolean isEqual(Object a, Object b) {
        if (a == null && b == null) return true;
        if (a == null) return false;

        return a.equals(b);
    }

    // throw runtime error if the operand is not a Number.
    private void checkIsNumber(Token operator, Object operand) {
        if (!(operand instanceof Double)) {
            throw new RuntimeError(operator, "Operand must be a number.");
        }
    }

    // throw runtime error if not that two operands are both Numbers.
    private void checkBothNumber(Token operator, Object lt_operand, Object rt_operand) {
        if (!(lt_operand instanceof Double && rt_operand instanceof Double)) {
            throw new RuntimeError(operator, "Operand must be a number.");
        }
    }

    // convert the val into a readable string.
    private String stringify(Object val) {
        // if val is NIL.
        if (val == null) return "nil";

        String str = val.toString();

        // if it is a Number, we have to ignore the ".0" at the end.
        if (val instanceof Double) {
            if (str.endsWith(".0")) {
                return str.substring(0, str.length() - 2);
            }
        }

        return str; // otherwise, simply return.
    }
}
