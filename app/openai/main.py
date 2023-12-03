from app.openai.transform import to_json, to_json_l
from app.openai.validate import validate_finetuning_dataset_openai


def format_for_openai_finetuning(
    system_message: str,
    input_list: list,
    output_list: list
) -> str:
    dataset_json = to_json(
        system_message=system_message,
        input_list=input_list,
        output_list=output_list
    )

    res = validate_finetuning_dataset_openai(
        dataset=dataset_json
    )

    if not res:
        return

    return to_json_l(json_list=dataset_json)
