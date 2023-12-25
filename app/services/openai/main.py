from app.services.openai.transform import to_openai_finetune, to_json_l
from app.services.openai.validate import validate_finetuning_dataset_openai


def format_for_openai_finetuning(
    system_message: str,
    messages: dict
) -> str:
    dataset_json = to_openai_finetune(
        system_message=system_message,
        messages=messages
    )

    res = validate_finetuning_dataset_openai(
        dataset=dataset_json
    )

    if not res:
        return

    return to_json_l(json_list=dataset_json)
