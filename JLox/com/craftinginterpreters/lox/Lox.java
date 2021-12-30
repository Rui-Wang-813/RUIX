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

  private static void run(String source) {
    Scanner scanner = new Scanner(source);
    List<Token> tokens = scanner.scanTokens();  // scan the source string into list of Tokens.

    // For now, just print the tokens.
    for (Token token : tokens) {
      System.out.println(token);
    }
  }

  private static void runFile(String path) throws IOException {
    byte[] bytes = Files.readAllBytes(Paths.get(path));
    run(new String(bytes, Charset.defaultCharset()));

    if (hadError) {
      // if error occurs, system simply exits with status code 65.
      System.exit(65);
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

  static void error(int line, String message) {
    // error occurs! report into terminal.
    report(line, "", message);
    hadError = true;
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