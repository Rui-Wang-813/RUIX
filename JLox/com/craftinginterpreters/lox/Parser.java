package com.craftinginterpreters.lox;

import java.util.ArrayList;
import java.util.List;

import static com.craftinginterpreters.lox.TokenType.*;

public class Parser {

    private static class ParseError extends RuntimeException {};

    private final List<Token> tokens;
    private int current = 0;

    Parser(List<Token> tokens) {
        this.tokens = tokens;
    }

    // public interface for Lox.java.
    List<Stmt> parse() {
        List<Stmt> statements = new ArrayList<>();

        while (!isAtEnd()) {
            statements.add(declaration());
        }

        return statements;
    }

    // declaration -> varDecl | statement ;
    private Stmt declaration() {
        try {
            if (match(VAR)) {
                return varDecl();
            } else {
                return statement();
            }
        } catch (ParseError e) {
            synchronize();
            return null;
        }
    }

    // varDecl -> "var" IDENTIFIER ( "=" expression)? ";" ; 
    private Stmt varDecl() {
        Token name = advance();

        Expr initializer = null;
        if (match(EQUAL)) {
            // there might be or not be an '='.
            initializer = expression();
        }
        consume(SEMICOLON, "Expect ';' after variable declaration.");

        return new Stmt.Var(name, initializer);
    }

    // statement -> exprStmt | printStmt | block | Var (done in varDecl) ;
    private Stmt statement() {
        if (match(PRINT)) {
            return printStmt();
        } else if (match(LEFT_BRACE)) {
            return block();
        } else {
            return exprStmt();
        }
    }

    // block -> "{" statement* "}" ;
    private Stmt block() {
        List<Stmt> stmts = new ArrayList<>();

        while (!check(RIGHT_BRACE) && !isAtEnd()) {
            stmts.add(declaration());
        }

        consume(RIGHT_BRACE, "Expect '}' after block.");
        return new Stmt.Block(stmts);
    }

    // exprStmt -> expression ";" ;
    private Stmt exprStmt() {
        Expr expr = expression();
        consume(SEMICOLON, "Expect ';' after expression.");
        return new Stmt.Expression(expr);
    }

    // printStmt -> "print" expression ";" ;
    private Stmt printStmt() {
        Expr expr = expression();
        consume(SEMICOLON, "Expect ';' after value.");
        return new Stmt.Print(expr);
    }

    // expression -> equality ; [old version]
    // expression -> assignment ;
    private Expr expression() {
        // return equality();
        return assignment();
    }

    // assignment -> IDENTIFIER "=" assignment | euqality ;
    private Expr assignment() {
        Expr expr = equality();

        if (match(EQUAL)) {
            Token equals = previous();
            Expr value = assignment();

            // if the left side is an identifier.
            if (expr instanceof Expr.Variable) {
                Token name = ((Expr.Variable)expr).name;
                return new Expr.Assign(name, value);
            } else {
                error(equals, "Invalid assignment target.");
            }
        }

        return expr;
    }

    //equality -> comparison ( ( "!=" | "==" ) comparison )* ;
    private Expr equality() {
        Expr expr = comparison();

        while(match(BANG_EQUAL, EQUAL_EQUAL)) {
            Token operator = previous();
            Expr right = comparison();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }

    // comparison -> addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
    private Expr comparison() {
        Expr expr = addition();

        while(match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL)) {
            Token operator = previous();
            Expr right = addition();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }

    // addition -> multiplication ( ( "-" | "+" ) multiplication )* ;
    private Expr addition() {
        Expr expr = multiplication();

        while(match(MINUS, PLUS)) {
            Token operator = previous();
            Expr right = multiplication();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }

    // multiplication -> unary ( ( "/" | "*" ) unary )* ;
    private Expr multiplication() {
        Expr expr = unary();

        while(match(SLASH, STAR)) {
            Token operator = previous();
            Expr right = unary();
            expr = new Expr.Binary(expr, operator, right);
        }

        return expr;
    }

    // unary -> ( "!" | "-" ) unary | primary ;
    private Expr unary() {
        if (match(BANG, MINUS)) {
            Token operator = previous();
            return new Expr.Unary(operator, unary());
        } else {
            return primary();
        }
    }

    // primary -> NUMBER | STRING | "false" | "true" | "nil" | "(" expression ")" | IDENTIFIER;
    private Expr primary() {
        if (match(TRUE)) return new Expr.Literal(true);
        if (match(FALSE)) return new Expr.Literal(false);
        if (match(NIL)) return new Expr.Literal(null);

        if (match(NUMBER, STRING)) {
            return new Expr.Literal(previous().literal);
        }

        if (match(LEFT_PAREN)) {
            Expr expr = new Expr.Grouping(expression());
            consume(RIGHT_PAREN, "Expect ')' after expression.");
            return expr;
        }

        if (match(IDENTIFIER)) {
            Expr expr = new Expr.Variable(previous());
            return expr;
        }

        throw error(peek(), "Expect an expression.");
    }

    // check if is at the end.
    private boolean isAtEnd() {
        return peek().type == EOF;
    }

    // get the token at current position.
    private Token peek() {
        return tokens.get(current);
    }

    // get the token just before the current position.
    private Token previous() {
        return tokens.get(current-1);
    }

    // get the token at the current position and proceed.
    private Token advance() {
        if (isAtEnd()) return previous();
        return tokens.get(current++);
    }

    // check if the token at current position is of expected type.
    private boolean check(TokenType type) {
        if (isAtEnd()) return false;
        return peek().type == type;
    }

    // consume the token at current position if is of right type, otherwise report error.
    private Token consume(TokenType type, String message) {
        if (check(type)) return advance();

        throw error(peek(), message);
    }

    // check if the token at current position is of one of the token types.
    // proceed if yes, otherwise stay.
    private boolean match(TokenType...tokenTypes) {
        for (TokenType type: tokenTypes) {
            if (check(type)) {
                advance();
                return true;
            }
        }
        return false;
    }

    private ParseError error(Token token, String message) {
        Lox.error(token, message);
        return new ParseError();
    }

    // synchronize when encountering serious parse errors.
    private void synchronize() {
        advance();  // current token type is not right, go to the next.

        while (true) {
            if (previous().type == SEMICOLON) return ;  // ';' marks the end of a statement.

            switch (peek().type) {
                // these things correspond to start of some statement.
                case CLASS: case FUN: case VAR: case FOR: case IF:
                case WHILE: case PRINT: case RETURN: return ;
                default: advance();
            }
        }
    }
}
