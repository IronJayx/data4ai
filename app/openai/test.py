from main import format_for_openai_finetuning
from data_setup_constants import (
    template_input_list,
    template_output_list,
    template_system_message
)

if __name__ == "__main__":
    format_for_openai_finetuning(
        system_message=template_system_message,
        input_list=template_input_list,
        output_list=template_output_list
    )
