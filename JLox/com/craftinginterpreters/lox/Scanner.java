package com.craftinginterpreters.lox;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static com.craftinginterpreters.lox.TokenType.*; 

class Scanner {
    private static final Map<String, TokenType> keywords;

    // a static block is executed exactly once: when the class is loaded into memory.
    static {
        keywords = new HashMap<>();
        keywords.put("and",    AND);
        keywords.put("class",  CLASS);
        keywords.put("else",   ELSE);
        keywords.put("false",  FALSE);
        keywords.put("for",    FOR);
        keywords.put("fun",    FUN);
        keywords.put("if",     IF);
        keywords.put("nil",    NIL);
        keywords.put("or",     OR);
        keywords.put("print",  PRINT);
        keywords.put("return", RETURN);
        keywords.put("super",  SUPER);
        keywords.put("this",   THIS);
        keywords.put("true",   TRUE);
        keywords.put("var",    VAR);
        keywords.put("while",  WHILE);
    }

    private final String source;
    private final List<Token> tokens = new ArrayList<>();

    private int start = 0;
    private int current = start;
    private int line = 1;

    Scanner(String source) {
        this.source = source;
    }

    List<Token> scanTokens() {
        while (!isAtEnd()) {
            current = start;
            scanToken();    // this is where scanning really happens.
        }

        tokens.add(new Token(EOF, "", null, line)); // when everything is scanned, add an EOF token.
        return tokens;
    }

    private boolean isAtEnd() {
        return current >= source.length();
    }

    private void scanToken() {
        char c = advance();
        switch (c) {
            case '(': addToken(LEFT_PAREN); break;
            case ')': addToken(RIGHT_PAREN); break;
            case '{': addToken(LEFT_BRACE); break;
            case '}': addToken(RIGHT_BRACE); break;
            case ',': addToken(COMMA); break;
            case '.': addToken(DOT); break;
            case '-': addToken(MINUS); break;
            case '+': addToken(PLUS); break;
            case ';': addToken(SEMICOLON); break;
            case '*': addToken(STAR); break; 
            case '!': addToken(match('=') ? BANG_EQUAL : BANG); break;
            case '=': addToken(match('=') ? EQUAL_EQUAL : EQUAL); break;
            case '>': addToken(match('=') ? GREATER_EQUAL : GREATER); break;
            case '<': addToken(match('=') ? LESS_EQUAL : LESS); break;
            case '/':
                if (match('/')) {
                    while (peek() != '\n' && !isAtEnd()) advance();
                } else {
                    addToken(SLASH);
                }
                break;
            case ' ': case '\r': case '\t':
                // ignore white spaces.
                break;
            case '\n': line++; break;
            case '"': string(); break;

            default:
                if (isDigit(c)) {
                    number();
                } else if (isAlpha(c)) {
                    identifier();
                } else {
                    Lox.error(line, "Unexpected character.");
                }
                break;
        }
    }

    // return and consume the current char.
    private char advance() {
        return source.charAt(current++);
    }

    // just return the current char.
    private char peek() {
        return isAtEnd() ? '\0' : source.charAt(current);
    }

    // return the char at position current+1.
    private char peekNext() {
        if (current+1 >= source.length()) return '\0';
        return source.charAt(current + 1);
    }

    // add a token with no literal values.
    private void addToken(TokenType type) {
        addToken(type, null);
    }

    // general version: add a token.
    private void addToken(TokenType type, Object literal) {
        String text = source.substring(start, current);
        tokens.add(new Token(type, text, literal, line));
    }

    // check if current char matches the given char.
    private boolean match(char expected) {
        if (isAtEnd()) return false;
        if (source.charAt(current) != expected) {
            return false;
        }

        // if it matches, then consume the char.
        current++;
        return true;
    }

    // check if the given char is digit.
    private boolean isDigit(char c) {
        return c >= '0' && c <= '9';
    }
    
    // check if the given char is letter or '_'.
    private boolean isAlpha(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c == '_');
    }

    // check if the given char is letter or '_' or is digit.
    private boolean isAlphaNumeric(char c) {
        return isAlpha(c) || isDigit(c);
    }

    // to add a string literal token.
    private void string() {
        // go to the next ' " '.
        while (peek() != '"' && !isAtEnd()) {
            // there is a \n in between the string definition.
            if (peek() == '\n') {
                line++;
            }
            advance();
        }

        // here I've reached the end but haven't reached the other ' " '.
        if (isAtEnd()) {
            Lox.error(line, "Unterminated string.");
            return ;
        }

        advance();  // consume the ' " '.

        // trim the quotes and get literal value and add the token.
        String value = source.substring(start + 1, current - 1);    
        addToken(STRING, value);
    }

    // to add a Number token.
    private void number() {
        while (isDigit(peek())) advance();  // go to the first position that is not a digit.

        // check if the current char is a '.' and next char is a digit. (a decimal number)
        if (peek() == '.' && isDigit(peekNext())) {
            advance();
            while (isDigit(peek())) advance();
        }

        double num = Double.parseDouble(source.substring(start, current));  // num is the Number literal.
        addToken(NUMBER, num);
    }

    // add an Identifier/keyword token.
    private void identifier() {
        while (isAlphaNumeric(peek())) advance();
        
        // get the text of the identifier.
        String text = source.substring(start, current);

        TokenType type = keywords.get(text);    // if the identifier is a key word, get the TokenType.
        if (type == null) type = IDENTIFIER;    // if not a keyword, then it's just IDENTIFIER.
        addToken(type);
    }
}
