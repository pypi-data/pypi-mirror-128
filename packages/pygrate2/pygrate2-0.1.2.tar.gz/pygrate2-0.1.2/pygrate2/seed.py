from .settings import find_seeds, load_state_object
import sys
from typing import List
import importlib.util


def load_seeds() -> List[callable]:
    """Load the seeds."""
    loaded_seeds = []
    seeds = find_seeds()
    for seed in seeds:
        print(f" --- {seed}")

        module_name = f"seed_{seed.split('/')[-1].replace('.', '_')}"
        spec = importlib.util.spec_from_file_location(module_name, seed)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        sys.modules[module_name] = foo

        if not hasattr(foo, "Seed"):
            raise ValueError(f"seed {seed} has no class named Seed. Quitting")

        seed_object = foo.Seed()

        if not hasattr(seed_object, "apply"):
            raise ValueError(f"{seed} must have a 'apply' method")

        if not hasattr(seed_object, "rollback"):
            raise ValueError(f"{seed} must have a 'rollback' method")

        if not hasattr(seed_object, "version"):
            raise ValueError(f"{seed} must have a 'version' attribute")

        loaded_seeds.append(seed_object)

    return loaded_seeds


def apply():
    pygrate_config = load_state_object()
    last_seed_version = pygrate_config.get_seed_version()
    print("Loading seeds")
    seeds = load_seeds()

    # Applying seeds
    for seed_instance in seeds:
        if seed_instance.version > last_seed_version:
            print(f"Applying seed {seed_instance.__class__} ... ", end="")
            seed_instance.apply()
            pygrate_config.set_seed_version(seed_instance.version)
            assert pygrate_config.get_seed_version() == seed_instance.version
            print("[Done]")
