package com.craftinginterpreters.lox;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Lox {
  static boolean hadError = false;
  static boolean hadRuntimeError = false;

  private static final Interpreter interpreter = new Interpreter();

  private static void run(String source) {
    // use Scanner scan the source string into list of Tokens.
    Scanner scanner = new Scanner(source);
    List<Token> tokens = scanner.scanTokens();

    // use Parser to parse the syntax tree out of tokens.
    Parser parser = new Parser(tokens);
    Expr expr = parser.parse();
    
    if (hadError) return ;

    // print out the expression.
    // System.out.println(new AstPrinter().print(expr));

    // interpret the code.
    interpreter.interpret(expr);
  }

  private static void runFile(String path) throws IOException {
    byte[] bytes = Files.readAllBytes(Paths.get(path));
    run(new String(bytes, Charset.defaultCharset()));

    if (hadError) {
      // if static/syntax error occurs, system simply exits with status code 65.
      System.exit(65);
    }
    if (hadRuntimeError) {
      // if runtime error occurs, system exits with status code 70.
      System.exit(70);
    }
  }

  private static void runPrompt() throws IOException {
    InputStreamReader input = new InputStreamReader(System.in);
    BufferedReader reader = new BufferedReader(input);

    for (;;) { 
      System.out.print("> ");
      String line = reader.readLine();
      if (line == null) break;  // if there is a CTRL-D, readLine returns null, prompt stops.
      run(line);
      hadError = false; // reset the flag.
    }
  }

  private static void report(int line, String where, String message) {
    System.err.println("[line " + line + "] Error" + where + ": " + message);
  }

  static void error(Token token, String message) {
    // error occurs for a given token.
    if (token.type == TokenType.EOF) {
      report(token.line, " at end", message);
    } else {
      report(token.line, " at '" + token.lexeme + "'", message);
    }
    hadError = true;
  }

  static void error(int line, String message) {
    // error occurs! report into terminal.
    report(line, "", message);
    hadError = true;
  }

  // report when runtime error occurs.
  static void runtimeError(RuntimeError error) {
    System.out.println(error.getMessage() + "\nline[" + error.token.line + "]");
    hadRuntimeError = true;
  }

  public static void main(String[] args) throws IOException {
    if (args.length > 1) {
      // too many arguments.
      System.out.println("Usage: jlox [script]");
      System.exit(64); 
    } else if (args.length == 1) {
      // run the script code stored in a file.
      runFile(args[0]);
    } else {
      // open an interactive prompt.
      runPrompt();
    }
  }
}