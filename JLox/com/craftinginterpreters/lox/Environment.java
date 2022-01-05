package com.craftinginterpreters.lox;

import java.util.HashMap;
import java.util.Map;

public class Environment {
    final Environment enclosing;    // the parent env.
    private final Map<String, Object> values = new HashMap<>();

    public Environment() {
        enclosing = null;
    }

    public Environment(Environment enclosing) {
        this.enclosing = enclosing;
    }

    // used when var declaration.
    public void define(String name, Object value) {
        values.put(name, value);
    }

    // used when reassigning var.
    public void assign(Token name, Object value) {
        if (values.containsKey(name.lexeme)) {
            values.put(name.lexeme, value);
        } else {
            if (enclosing == null) {
                // if this is already global environment.
                throw new RuntimeError(name, "Undefined variable '" + name.lexeme + "'.");
            } else {
                // if it has a parent environment.
                enclosing.assign(name, value);
            }
        }
    }

    // used when getting a variable value.
    public Object get(Token name) {
        if (values.containsKey(name.lexeme)) {
            return values.get(name.lexeme);
        } else {
            if (enclosing == null) {
                // if this is already global environment.
                throw new RuntimeError(name, "Undefined variable '" + name.lexeme + "''.");
            } else {
                // if it has a parent environment.
                return enclosing.get(name);
            }
        }
    }
}
