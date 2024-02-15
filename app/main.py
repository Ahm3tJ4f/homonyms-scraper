from app.database_operations import insert_data_to_database
from app.scraper import main_scrape


def main():
    scraped_data = main_scrape()
    insert_data_to_database(scraped_data)


if __name__ == "__main__":
    main()
