from src.DAO.DBConnector import DBConnector
from src.Model.Pricing import Pricing
from src.utils.log_utils import get_logger, log
from src.utils.singleton import Singleton

logger = get_logger(__name__)


class PricingRepo(metaclass=Singleton):
    """Class containing methods to access Pricings in the database."""

    @log
    def get_by_id(self, pricing_id: int) -> Pricing | None:
        """Find a pricing by its id.
        Args:
            pricing_id (int): The ID of the pricing to find
        Returns:
            Pricing matching the given id, None if not found
        """
        try:
            with DBConnector().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                          "
                        "  FROM pricings                     "
                        " WHERE pricing_id = %(pricing_id)s;   ",
                        {"pricing_id": pricing_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        pricing = None
        if res:
            pricing = Pricing(
                pricing_id=res["pricing_id"],
                name=res["name"],
                description=res["description"],
                price=res["price"],
            )

        return pricing
