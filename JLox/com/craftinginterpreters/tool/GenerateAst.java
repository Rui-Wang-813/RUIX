package com.craftinginterpreters.tool;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;

public class GenerateAst {
    // define the very base of expression.
    private static void defineAst(
        String outputDir, String baseName, List<String> types) 
        throws IOException{
            String path = outputDir + "/" + baseName + ".java";
            PrintWriter writer = new PrintWriter(path);

            // write the package name, importations, and abstract class name.
            writer.println("package com.craftinginterpreters.lox;");
            writer.println();
            writer.println("import java.util.List;");
            writer.println();
            writer.println("abstract class " + baseName + "{");

            // define the visitor interface.
            defineVisitor(writer, baseName, types);

            // define the subclasses for each types.
            for (String type: types) {
                String className = type.split(":")[0].trim();
                String fields = type.split(":")[1].trim();
                defineType(writer, baseName, className, fields);
            }

            // define the abstract accept function.
            writer.println();
            writer.println("  abstract <R> R accept(Visitor<R> visitor);");

            writer.println("}");
            writer.close();
    }

    // define the subclass for the given type.
    private static void defineType(
        PrintWriter writer, String baseName,
        String className, String fields) {
            writer.println("  static class " + className + " extends " + baseName + "{");

            // define the constructor.
            writer.println("    " + className + "(" + fields + ") {");
            String[] fieldList = fields.split(", ");    // a list of the fields. (Class: varName)
            for (String field: fieldList) {
                String varName = field.split(" ")[1];
                // assign each instance var in the constructor.
                writer.println("        this." + varName + " = " + varName + ";");
            }
            writer.println("    }");

            // define the instance variables.
            writer.println();
            for (String field: fieldList) {
                writer.println("    final " + field + ";");
            }
            writer.println();

            // override the accept function from base class.
            writer.println("    @Override");
            writer.println("    <R> R accept(Visitor<R> visitor) {");
            writer.println("        return visitor.visit" + className + baseName + "(this);");
            writer.println("    }");

            writer.println("  }");
    }

    // define the Visitor interface.
    private static void defineVisitor(
        PrintWriter writer, String baseName, List<String> types) {
            writer.println("  interface Visitor<R> {"); // it is a template, use R as the given type.

            // define a visit function for each subclass.
            for (String type: types) {
                String typeName = type.split(" ")[0].trim();
                writer.println("    R visit" + typeName + baseName + "("
                + typeName + " " + baseName.toLowerCase() + ");");
            }

            writer.println("  }");
        }

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.err.println("Usage: generate_ast <output directory>");
            System.exit(64);
        }
        String outputDir = args[0];

        defineAst(outputDir, "Expr", Arrays.asList(
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Object value",
            "Unary    : Token operator, Expr right"
        ));
    }
}