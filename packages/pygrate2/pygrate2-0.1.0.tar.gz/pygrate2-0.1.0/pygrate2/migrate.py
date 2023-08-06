from .settings import find_migrations, load_state_object
import sys
from typing import List
import importlib.util


def load_migrations() -> List[callable]:
    """Load the migrations."""
    loaded_migrations = []
    migrations = find_migrations()
    for migration in migrations:
        print(f" --- {migration}")

        module_name = f"migration_{migration.split('/')[-1].replace('.', '_')}"
        spec = importlib.util.spec_from_file_location(module_name, migration)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        sys.modules[module_name] = foo

        if not hasattr(foo, "Migration"):
            raise ValueError(
                f"Migration {migration} has no class named Migration. Quitting"
            )

        migration_object = foo.Migration()

        if not hasattr(migration_object, "apply"):
            raise ValueError(f"{migration} must have a 'apply' method")

        if not hasattr(migration_object, "rollback"):
            raise ValueError(f"{migration} must have a 'rollback' method")

        if not hasattr(migration_object, "version"):
            raise ValueError(f"{migration} must have a 'version' attribute")

        loaded_migrations.append(migration_object)

    return loaded_migrations


def apply():
    pygrate_config = load_state_object()
    last_migration = pygrate_config.get_migration_version()

    print("Loading migrations")
    migrations = load_migrations()

    # Applying migrations
    for migration_instance in migrations:
        if migration_instance.version > last_migration:
            print(
                f"Applying migration {migration_instance.__class__} ... ",
                end="",
            )
            migration_instance.apply()
            pygrate_config.set_migration_version(migration_instance.version)
            assert (
                pygrate_config.get_migration_version()
                == migration_instance.version
            )
            print("[Done]")
