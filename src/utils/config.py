from dataclasses import dataclass
from pathlib import Path

from alembic.config import Config
from dotenv import load_dotenv
from envclasses import envclass, load_env
from serde import serde
from serde.toml import from_toml


@dataclass
@envclass
@serde
class DbInfo:
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str


@dataclass
@envclass
@serde
class ProjectConfig:
    db_info: DbInfo


def load_project_config(path: Path = Path("config.toml")) -> ProjectConfig:
    with open(path) as f:
        config = from_toml(ProjectConfig, f.read())

    load_dotenv()
    load_env(config, prefix="")
    return config


def update_alembic_config(alembic_config: Config, db_info: DbInfo) -> None:
    print(db_info)
    section = alembic_config.config_ini_section
    alembic_config.set_section_option(section, "DB_USER", db_info.db_user)
    alembic_config.set_section_option(section, "DB_PASSWORD", db_info.db_password)
    alembic_config.set_section_option(section, "DB_HOST", db_info.db_host)
    alembic_config.set_section_option(section, "DB_PORT", db_info.db_port)
    alembic_config.set_section_option(section, "DB_NAME", db_info.db_name)


def get_db_url(db_info: DbInfo) -> str:
    return f"postgresql://{db_info.db_user}:{db_info.db_password}@{db_info.db_host}:{db_info.db_port}/{db_info.db_name}"
