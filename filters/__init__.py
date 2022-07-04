from filters.is_admin_filter import Is_Admin
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(Is_Admin)