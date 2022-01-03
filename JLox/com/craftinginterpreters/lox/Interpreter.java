package com.craftinginterpreters.lox;

public class Interpreter implements Expr.Visitor<Object> {

    // public interface to interpret an expression.
    public void interpret(Expr expr) {
        try {
            Object val = evaluate(expr);
            System.out.println(stringify(val));
        } catch(RuntimeError e) {
            Lox.runtimeError(e);
        }
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

    // simply a wrapper.
    private Object evaluate(Expr expr) {
        return expr.accept(this);
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
