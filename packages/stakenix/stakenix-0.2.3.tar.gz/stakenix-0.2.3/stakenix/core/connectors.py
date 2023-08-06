import json
from abc import ABC, ABCMeta
from contextlib import contextmanager
from os import getenv
from pathlib import Path
from typing import Dict, Optional

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import ProgrammingError
from sshtunnel import SSHTunnelForwarder
from stakenix import Session
from stakenix.config import Config


class SQLConnector(ABC):
    def __init__(self, schema: str, database: str) -> None:
        self.schema: str = schema
        self.database: str = database
        self.connection_args: Optional[Dict] = {}

    def _generate_session(self) -> Session:
        Session.configure(
            bind=create_engine(
                self._create_connection_url(), connect_args=self.connection_args
            )
        )
        return Session()

    @contextmanager
    def connection(self) -> Connection:
        session = self._generate_session()
        try:
            yield session
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            session.close()

    def _create_connection_url(self) -> str:
        ...


class NoSQLConnector(ABC):
    ssh_pkey: Path = Path.home().joinpath(".ssh").joinpath("id_rsa")


class MySQLConnector(SQLConnector):
    def __init__(self, schema: str, database: str = "default") -> None:
        super().__init__(schema=schema, database=database)

    def _create_connection_url(self) -> str:
        env_db_argument: str = self.database.upper()
        return URL(
            drivername="mysql+mysqlconnector",
            username=getenv(f"MYSQL_{env_db_argument}_USERNAME"),
            password=getenv(f"MYSQL_{env_db_argument}_PASSWORD"),
            host=getenv(f"MYSQL_{env_db_argument}_HOST"),
            port=getenv(f"MYSQL_{env_db_argument}_PORT"),
            database=self.schema,
        )


class PostgreSQLConnector(SQLConnector):
    def __init__(self, schema: str, database: str = "default") -> None:
        super().__init__(schema=schema, database=database)
        self._update_connection_arguments()

    def _update_connection_arguments(self) -> None:
        if self.database == "default":
            self.connection_args: Dict = {"options": f"-csearch_path={self.schema}"}

    def _create_connection_url(self) -> str:
        env_db_argument: str = self.database.upper()
        return URL(
            drivername="postgresql",
            username=getenv(f"PG_{env_db_argument}_USERNAME"),
            password=getenv(f"PG_{env_db_argument}_PASSWORD"),
            host=getenv(f"PG_{env_db_argument}_HOST"),
            port=getenv(f"PG_{env_db_argument}_PORT"),
            database=getenv(f"PG_{env_db_argument}_DB"),
        )


class MsSQLConnector(SQLConnector):
    def __init__(self, schema: str, database: str = "default") -> None:
        super().__init__(schema=schema, database=database)

    def _create_connection_url(self) -> str:
        env_db_argument: str = self.database.upper()
        url = "{driver}://{username}:{password}@{host}:{port}/{schema}"
        return url.format(
            driver="mssql+pymssql",
            username=getenv(f"MSSQL_{env_db_argument}_USERNAME"),
            password=getenv(f"MSSQL_{env_db_argument}_PASSWORD"),
            host=getenv(f"MSSQL_{env_db_argument}_HOST"),
            port=getenv(f"MSSQL_{env_db_argument}_PORT"),
            schema=getenv(f"MSSQL_{env_db_argument}_DB"),
        )


class ClickHouseConnector(SQLConnector):
    def __init__(self, schema: str, database: str = "default") -> None:
        super().__init__(schema=schema, database=database)

    def _create_connection_url(self) -> str:
        env_db_argument: str = self.database.upper()
        return URL(
            drivername="clickhouse",
            username=getenv(f"CH_{env_db_argument}_USERNAME"),
            password=getenv(f"CH_{env_db_argument}_PASSWORD"),
            host=getenv(f"CH_{env_db_argument}_HOST"),
            port=getenv(f"CH_{env_db_argument}_PORT"),
            database=self.schema,
        )


class BigQueryConnector(SQLConnector):
    def __init__(self, dataset: str, project: str = "") -> None:
        super().__init__(schema=dataset, database=project)
        self.schema: str = dataset
        self.project: str = project.upper()
        self.project_id: Optional[str] = getenv(f"BQ_{self.project}_PROJECT_ID")

    def _generate_credentials(self) -> Path:
        creds_folder: Path = Path.home().joinpath(".google")
        write_creds_path: Path = creds_folder.joinpath(
            f"credentials_{self.project.lower()}.json"
        )

        if not creds_folder.exists():
            creds_folder.mkdir()

        creds: Dict = {
            "type": "service_account",
            "project_id": self.project_id,
            "private_key_id": getenv(f"BQ_{self.project}_PRIVATE_KEY_ID"),
            "private_key": getenv(f"BQ_{self.project}_PRIVATE_KEY").encode("latin1").decode("unicode_escape"),  # type: ignore
            "client_email": getenv(f"BQ_{self.project}_CLIENT_EMAIL"),
            "client_id": getenv(f"BQ_{self.project}_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": getenv(f"GOOGLE_BQ_{self.project}_CLIENT_CERT_URL"),
        }

        with open(write_creds_path, "w") as file:
            json.dump(creds, file)

        return write_creds_path

    def _generate_session(self) -> Session:
        Session.configure(
            bind=create_engine(
                self._create_connection_url(),
                connect_args=self.connection_args,
                credentials_path=self._generate_credentials(),
            )
        )
        return Session()

    def _create_connection_url(self) -> str:
        return URL(drivername="bigquery", host=self.project_id, database=self.schema)


class MongoDBConnector(NoSQLConnector):
    def __init__(self, schema: str) -> None:
        super().__init__()
        self.schema = schema


class MongoDBSSHConnector(MongoDBConnector):
    def __init__(self, schema: str) -> None:
        super().__init__(schema)

    @contextmanager
    def connection(self) -> MongoClient:
        ssh_params = dict(
            ssh_address_or_host=getenv(f"{self.schema.upper()}_MONGODB_SSH_HOST"),
            ssh_username=getenv(f"{self.schema.upper()}_MONGODB_SSH_USERNAME"),
            ssh_pkey=str(self.ssh_pkey),
            remote_bind_address=(getenv(f"{self.schema.upper()}_MONGODB_HOST"), 27017),
        )
        try:
            ssh = SSHTunnelForwarder(**ssh_params)
            ssh.start()
            mongo_params = dict(
                host=getenv(f"{self.schema.upper()}_MONGODB_HOST"),
                port=ssh.local_bind_port,
                password=getenv(f"{self.schema.upper()}_MONGODB_PASSWORD"),
                username=getenv(f"{self.schema.upper()}_MONGODB_USERNAME"),
            )
            yield MongoClient(**mongo_params)[
                getenv(f"{self.schema.upper()}_MONGODB_DB")
            ]
        except Exception as exc:
            raise exc
        finally:
            ssh.close()


class MongoDBDirectConnector(MongoDBConnector):
    def __init__(self, schema: str) -> None:
        super().__init__(schema)

    @contextmanager
    def connection(self) -> MongoClient:
        try:
            mongo_params = dict(
                host=getenv(f"{self.schema.upper()}_MONGODB_HOST"),
                port=27017,
                password=getenv(f"{self.schema.upper()}_MONGODB_PASSWORD"),
                username=getenv(f"{self.schema.upper()}_MONGODB_USERNAME"),
            )
            yield MongoClient(**mongo_params)[
                getenv(f"{self.schema.upper()}_MONGODB_DB")
            ]
        except Exception as exc:
            raise exc
