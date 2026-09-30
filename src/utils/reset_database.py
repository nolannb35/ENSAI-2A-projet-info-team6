import os
import sys
from pathlib import Path

import dotenv

from src.DAO.DBConnector import DBConnector
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

logger = get_logger(__name__)

# src/utils/reset_database.py -> parents[2] = root of the repository
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class ResetDatabase(metaclass=Singleton):
    """Database reset utility: (re)creates the schema, the tables and the data."""

    @log
    def run(self, test_dao: bool = False) -> bool:
        """Run the database reset.
        Args:
            test_dao (bool): if True, reset the TEST schema with pop_db_test.sql,
                otherwise reset the application schema with pop_db.sql
        Returns:
            True if the reset is successful
        """
        dotenv.load_dotenv()

        if test_dao:
            schema = os.environ.get("POSTGRES_SCHEMA_TEST", "projet_test_dao")
            pop_data_path = DATA_DIR / "pop_db_test.sql"
        else:
            schema = os.environ["POSTGRES_SCHEMA"]
            pop_data_path = DATA_DIR / "pop_db.sql"

        init_db_path = DATA_DIR / "init_db.sql"

        try:
            init_db_as_string = init_db_path.read_text(encoding="utf-8")
            pop_db_as_string = pop_data_path.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            logger.error(f"Impossible de trouver le fichier {e.filename}")
            raise

        # The schema is dropped and recreated, then the scripts are executed inside it
        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"
        set_schema = f"SET search_path TO {schema};"

        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(set_schema)
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)
                    # Go back to the application schema for the next queries
                    cursor.execute(f"SET search_path TO {DBConnector().schema};")
        except Exception as e:
            logger.error(e)
            raise

        return True


if __name__ == "__main__":
    ResetDatabase().run(test_dao="--test" in sys.argv)
