@echo off
rem Script to run ANTLR generator
rem Adjust ANTLR_JAR_PATH if your JAR is elsewhere
set ANTLR_JAR_PATH=".\antlr-4.13.1-complete.jar"

if not exist %ANTLR_JAR_PATH% (
    echo ANTLR JAR not found at %ANTLR_JAR_PATH%
    echo Please download it from antlr.org and update the path.
    exit /b 1
)

java -jar %ANTLR_JAR_PATH% -Dlanguage=Python3 -o src/minic_parser -visitor -no-listener grammar/MiniC.g4
echo ANTLR files generated in src/minic_parser/