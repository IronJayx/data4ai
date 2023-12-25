CSV_IMPORT_INFO = """
    Format: Your CSV must have two columns with NO headers and at least 10 examples.

    - The first column should contain the user request to the model.
    - The second column should contain the model response to that request.
"""

CSV_IMPORT_EXAMPLE = """
    discussion_id,role,content
    1,user,What is the capital of France ?,
    1,assistant, Paris,
    2,user,What is the capital of Germany ?,
    2,assistant, Berlin,
    2,user,Are you sure ?,
    2,assistant, Yes,
    3,user,What is the capital of America ?,
    3,assistant, America is not a country,
    ...
"""

FORMAT_NOT_SUPPORTED = """File format not supported yet but hang on, we will be right back"""

SECTION_TITLE = 'Import your data'

WARNING_INIT = 'Need vars to init'
