@echo off
rem Script to run ANTLR generator

rem Explicitly define the path to your JDK 21 java.exe
set JDK21_JAVA_PATH="C:\Program Files\Java\jdk-21\bin\java.exe" 
REM ^^^^ UPDATE THIS PATH TO YOUR EXACT JDK 21 java.exe LOCATION ^^^^

rem Adjust ANTLR_JAR_PATH if your JAR is elsewhere
set ANTLR_JAR_PATH=".\antlr-4.13.2-complete.jar"

if not exist %ANTLR_JAR_PATH% (
    echo ANTLR JAR not found at %ANTLR_JAR_PATH%
    echo Please download it from antlr.org and update the path.
    exit /b 1
)

if not exist %JDK21_JAVA_PATH% (
    echo JDK 21 java.exe not found at %JDK21_JAVA_PATH%
    echo Please check the path.
    exit /b 1
)

echo Using Java: %JDK21_JAVA_PATH%
echo Using ANTLR JAR: %ANTLR_JAR_PATH%

rem Execute ANTLR using the explicit Java path
%JDK21_JAVA_PATH% -jar %ANTLR_JAR_PATH% -Dlanguage=Python3 -o src/minic_parser -visitor -no-listener grammar/MiniC.g4

if %errorlevel% neq 0 (
    echo ANTLR generation failed with error code %errorlevel%
) else (
    echo ANTLR files generated successfully in src/minic_parser/
)