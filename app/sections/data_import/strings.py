CSV_IMPORT_INFO = """
    Format: Your CSV must have two columns with NO headers and at least 10 examples.

    - The first column should contain the user request to the model.
    - The second column should contain the model response to that request.
"""

CSV_IMPORT_EXAMPLE = """
    What is the capital of France?, Paris
    What is the capital of Germany?, Berlin
    What is the capital of America?, America is not a country
    What is the capital of the US?, Washington
    ...
"""

FORMAT_NOT_SUPPORTED = """File format not supported yet but hang on, we will be right back"""

SECTION_TITLE = 'Import your data'

WARNING_INIT = 'Need vars to init'
