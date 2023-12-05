# data4ai
No-code tool to create Openai assitants with your data.

- Choose between creating fine-tuning and retrieval augmented assistants.
- Import your data.
- The app validates it and export it to the right format for OpenAI api.
- Your assistant is available.


# Roadmap:

## User flow
- Add landing page that points to app

## Features:
- Refactor code
- Rename repo data4ai
- Support for multi message discussions.
- Support for different input types (excel, word doc, pdfs...)
- Support for different export formats: CSV, JSONL
- Integration with openai api:
    - add your key & deploy
- Support file assitant creation
    - Support for repo input -> full codebase to txt
    - Support for website: base urls and childs links (recursive)
        - figure out a good doc splitting logic
- Build an example with streamlit
    - Assistant only
    - Assitant + finetuing
    - make a video & communicate on it

## Codebase:
- Migrate to Next.js & react
- Implement login & payment
