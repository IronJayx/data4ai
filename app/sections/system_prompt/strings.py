SYSTEM_PROMPT_INFO = """
    The system prompt contains instructions on how the model should behave.
"""

SYSTEM_PROMPT_EXAMPLE = """
    You are a geography expert capable.
    Users will ask you question on whether a city is the capital of a country.

    You should provide concise responses like so:
    - If the city is the capital of the mentioned country answer Yes.
    - If the city belongs to the mentioned country but is not a capital answer No.
    - If the country mentioned is not a country tell the user so.
    - If the city mentioned is not a city tell the user so.
"""

SECTION_TITLE = 'Enter the system prompt'

WARNING_INIT = 'Need vars to init'
