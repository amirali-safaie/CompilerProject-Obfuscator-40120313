# Mini-C Code Obfuscator

This project is an implementation of a code obfuscator for a subset of the C language, termed "Mini-C". It was developed as a practical project for the Compiler Design course (Term 1402-2) at K. N. Toosi University of Technology, under the supervision of Dr. MohammadHadi Alaeiyan.

The obfuscator parses Mini-C source code, applies several transformation techniques to make the code harder for humans to understand while preserving its original functionality, and then generates the obfuscated Mini-C code.

## Team Members

*   [Amirali Habibi / 40004353]
*   [Amirali Safaii/ 40120313]
*   [AmirMohammad Alikhani/ 40120313]

## Mini-C Language Subset

The Mini-C language supported by this obfuscator includes:

*   **Data Types:** `int`, `char`, `bool`
*   **Variables and Operators:** Standard C operators for arithmetic, logic, comparison, assignment.
*   **Control Flow:** `if-else`, `while`, `for`, `return`
*   **Functions:** Declaration with parameters and return values.
*   **Input/Output:** Simplified `printf` and `scanf` (treated as function calls).
*   **Exclusions:** No `struct`, `pointer`, or preprocessor directives.

(Refer to `grammar/MiniC.g4` for the precise grammar definition.)

## Implemented Obfuscation Techniques

The following obfuscation techniques have been implemented:

1.  **Identifier Renaming:** Variables (local and parameters) and function names (excluding `main`, `printf`, `scanf`) are replaced with short, meaningless names (e.g., `v_0`, `f_1`). This makes it harder to infer the purpose of identifiers from their names.
2.  **Dead Code Insertion:** Benign, non-functional statements (e.g., `int dead_v_0 = 1234;`) are randomly inserted into blocks of code. These statements do not affect the program's logic but add noise to the source.
3.  **Equivalent Expression Transformation:** Simple arithmetic expressions are transformed into more complex but functionally equivalent forms. For example, `a + b` might become `a - (0 - (b))`.
4.  **Control Flow Flattening (for `main` function):** The main sequence of statements within the `main` function's body (after initial declarations) is restructured into a `while` loop dispatching to a `switch` statement. Each original statement becomes a case in the switch, controlled by a state variable.

## Project Setup

### Prerequisites

*   **Python:** Version 3.7 or higher.
*   **Java Development Kit (JDK):** Version 11 or higher (for running the ANTLR tool).
*   **ANTLR Tool (JAR):** ANTLR v4.x (e.g., `antlr-4.13.2-complete.jar`). Download from [antlr.org](https://www.antlr.org/download.html).

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone <your_repository_url>
    cd mini_c_obfuscator
    ```

2.  **Set up Python Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # Activate on Windows
    # .\venv\Scripts\activate
    # Activate on macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install Python Dependencies:**
    The primary dependency is the ANTLR Python runtime.
    ```bash
    pip install antlr4-python3-runtime
    # (Optional: pip install -r requirements.txt if you create one)
    ```

4.  **Place ANTLR Tool JAR:**
    Download the `antlr-X.Y.Z-complete.jar` file from the ANTLR website and place it in the project's root directory (or update the path in `run_antlr.bat`/`run_antlr.sh`). The provided scripts assume a naming convention like `antlr-4.13.1-complete.jar`.

## Generating the Parser

If you modify the grammar (`grammar/MiniC.g4`), you need to regenerate the ANTLR parser and lexer files:

*   **On Windows:**
    ```batch
    .\run_antlr.bat
    ```
*   **On macOS/Linux:**
    ```bash
    chmod +x run_antlr.sh
    ./run_antlr.sh
    ```
    This will generate Python files in the `src/minic_parser/` directory.

## Running the Obfuscator

The main script to run the obfuscator is `src/main.py`.

**Basic Usage:**
```bash
python src/main.py <input_file.mc> [options]