import os

from typing import Optional
from werkzeug.utils import secure_filename


WORKFLOW_FILE_INPUT = "file"


def file_with_suffix(file_path: str, suffix: int) -> str:
    file_parts = os.path.splitext(file_path)
    return "".join(("{}_{}".format(file_parts[0], suffix), file_parts[1]))


def output_file_name(file_name, output_params):
    return secure_filename(file_name.format(**output_params))


def namespaced_input(workflow_name: str, input_id: str) -> str:
    return "{}.{}".format(workflow_name, input_id)


def input_i(i: int) -> str:
    return "INPUT_{}".format(i)


def make_output_params(workflow_name: str, workflow_params: dict, workflow_inputs: list):
    output_params = {}

    for i, input_spec in enumerate(workflow_inputs):
        if input_spec["type"] != WORKFLOW_FILE_INPUT:
            # TODO: Handle non-file inputs
            continue

        output_params[input_i(i)] = workflow_params[namespaced_input(workflow_name, input_spec["id"])]

    return output_params


def find_common_suffix(base_path: str, workflow_metadata: dict, output_params: dict) -> Optional[int]:
    suffix = None
    for file in workflow_metadata["outputs"]:
        file_path = os.path.join(base_path, output_file_name(file, output_params))
        if os.path.exists(file_path):
            suffix = 1

    # Increase the suffix until a suitable one has been found
    duplicate_exists = suffix is not None
    while duplicate_exists:
        duplicate_exists = False
        for file in workflow_metadata["outputs"]:
            duplicate_exists = duplicate_exists or os.path.exists(
                file_with_suffix(os.path.join(base_path, output_file_name(file, output_params)), suffix))

        suffix += 1

    return suffix
