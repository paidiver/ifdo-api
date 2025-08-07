from logging.config import fileConfig  # noqa: INP001
from alembic import context
from ifdo_api.db.db import engine_create
from ifdo_api.models.base import Base
from geoalchemy2 import alembic_helpers

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def process_revision_directives(context, revision, directives):
    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []
        print("No changes in schema detected. No migration file generated.")



def user_include_object(object, name, type_, reflected, compare_to) -> bool:
    if hasattr(object, "schema") and object.schema in {"tiger", "topology"}:
        return False
    return not (
        type_ == "table"
        and name
        in {
            "spatial_ref_sys",
            "topology",
            "geometry_columns",
            "geography_columns",
            "street_type_lookup",
            "place_lookup",
            "pagc_rules",
            "zip_state_loc",
            "zcta5",
            "countysub_lookup",
            "addrfeat",
            "tiger",
            "tract",
            "place",
            "featnames",
            "zip_lookup",
            "county",
            "loader_variables",
            "loader_platform",
            "direction_lookup",
            "geocode_settings_default",
            "edges",
            "state_lookup",
            "faces",
            "county_lookup",
            "pagc_gaz",
            "state",
            "zip_lookup_all",
            "secondary_unit_lookup",
            "tabblock20",
            "zip_lookup_base",
            "cousub",
            "bg",
            "tabblock",
            "zip_state",
            "geocode_settings",
            "pagc_lex",
            "addr",
            "loader_lookuptables",
            "layer",
        }
    )


def combined_include_object(object, name, type_, reflected, compare_to) -> bool:
    return (
        user_include_object(object, name, type_, reflected, compare_to)
        and alembic_helpers.include_object(object, name, type_, reflected, compare_to)
    )

def skip_empty_and_write_script(context, revision, directives):
    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []
        print("No changes in schema detected. No migration file generated.")
    else:
        alembic_helpers.writer(context, revision, directives)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=combined_include_object,
        process_revision_directives=skip_empty_and_write_script,
        render_item=alembic_helpers.render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_create(alembic=True)

    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
            # include_object=include_object,
            include_object=combined_include_object,
            process_revision_directives=skip_empty_and_write_script,
            # process_revision_directives=alembic_helpers.writer,
            render_item=alembic_helpers.render_item,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
