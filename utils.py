import os


def is_within_directory(working_directory: str, target_path: str) -> bool:
    # Resolve both paths to absolute, real paths
    working_directory = os.path.realpath(working_directory)
    target_path = os.path.realpath(target_path)

    # Check if target path starts with working directory path
    return os.path.commonpath([working_directory]) == os.path.commonpath(
        [working_directory, target_path]
    )
