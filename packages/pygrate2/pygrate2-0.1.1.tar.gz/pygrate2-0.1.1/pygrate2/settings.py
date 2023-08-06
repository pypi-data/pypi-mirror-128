"""Configuration of pygrate."""

from os import getenv
from os.path import join, exists
from typing import Dict, List, Union
import yaml
import importlib.util

CONFIG_DIRECTORY = getenv("PYGRATE_DIR", "resources/pygrate")
CONFIG_FILE = join(CONFIG_DIRECTORY, "configuration.yml")


def load_config():
    """Load the pygrate2 configuration."""
    return yaml.load(open(CONFIG_FILE, "r"))


def find_migrations() -> List[str]:
    """Find migrations for this project."""
    configuration: Dict[str, Union[List[str], int, float]] = load_config()

    migrations_directory = join(CONFIG_DIRECTORY, "migrations")
    return [
        join(migrations_directory, migration)
        for migration in configuration.get("migrations", [])
    ]


def find_seeds() -> List[str]:
    """Find seeds for this project."""
    configuration: Dict[str, Union[List[str], int, float]] = load_config()

    seeds_directory = join(CONFIG_DIRECTORY, "seeds")
    return [join(seeds_directory, seed) for seed in configuration.get("seeds", [])]


def load_state_object() -> object:
    """Load the state object of pygrate.

    This object allow to modify the current migration
    or seed version
    """
    state_file = join(CONFIG_DIRECTORY, "Pygrate.py")

    if not exists(state_file):
        raise ValueError(f"Cannot find {state_file}")

    spec = importlib.util.spec_from_file_location(f"PygrateState", state_file)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    if not hasattr(foo, "Pygrate"):
        raise ValueError("Pygrate.py must contain a pygrate2 class")

    state_object = foo.Pygrate()

    if not hasattr(state_object, "get_migration_version"):
        raise ValueError("pygrate2 class must contain a 'get_migration_version' method")

    if not hasattr(state_object, "set_migration_version"):
        raise ValueError("pygrate2 class must contain a 'set_migration_version' method")

    if not hasattr(state_object, "get_seed_version"):
        raise ValueError("pygrate2 class must contain a 'get_seed_version' method")

    if not hasattr(state_object, "set_seed_version"):
        raise ValueError("pygrate2 class must contain a 'set_seed_version' method")

    return state_object
