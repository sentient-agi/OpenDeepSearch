import yaml
from pathlib import Path

def load_config(key: str = None) -> dict:
    """
    Load the configuration from a YAML file.
    
    Args:
        key (str): The specific key to retrieve from the config. If None, returns the entire config.
        
    Returns:
        dict: The loaded configuration.
    """
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    if key:
        return config.get(key, {})
    
    return config