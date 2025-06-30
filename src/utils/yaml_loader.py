import yaml

def read_yaml(file_path: str) -> dict:
    """Read and parse a YAML file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML data as a dictionary.
    """
    # Open and load the YAML file contents into a dictionary
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data