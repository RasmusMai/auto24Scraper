import requests
from bs4 import BeautifulSoup
import Vehicle
import json


def parse_page(page):
    return BeautifulSoup(page.content, "html.parser")


def dump_dict(dictionary):
    with open("results.json", "w", encoding="utf8") as file:
        json.dump(dictionary, file, ensure_ascii=False)


def populate_vehicle_data(vehicle):
    vehicle.populate_data()
    return vehicle


class Auto24:
    """
    giga nigga
    """

    def __init__(self):
        self.master_dict = {}
        self.URL = "https://www.auto24.ee/kasutatud/nimekiri.php?bn=2&a=101&ae=2&af=50&ag=1&otsi=otsi&ak="
        self.ak = 50
        self.cars_per_page = 0
        self.pages_to_scrape = 1

    def scrape(self, pages: int):
        self.pages_to_scrape = pages
        for x in range(self.pages_to_scrape):
            self.read_single_search_page()
            self.increase_ak()
        dump_dict(self.master_dict)
        print(self.master_dict)

    def get_search_page(self):
        request_url = self.URL + str(self.ak)
        print(f"Requesting URL: {request_url}")
        return requests.get(request_url)

    def increase_ak(self):
        self.ak += self.cars_per_page

    def add_to_dict(self, identifier, vehicle):
        if identifier not in self.master_dict.keys():
            self.master_dict[identifier] = vehicle.data

    def read_single_search_page(self):
        page = self.get_search_page()
        soup = parse_page(page)

        car_rows = soup.find_all(class_="make_and_model")

        for car_row in car_rows:
            car = car_row.find("a")
            identifier = car["href"].replace("/used/", "")
            if identifier.isnumeric():
                print(f"Doing URL https://www.auto24.ee/used/{identifier}\t", end="")
                try:
                    vehicle = Vehicle.Vehicle(identifier)
                    self.add_to_dict(identifier, vehicle)
                except Vehicle.AuctionException:
                    print("Auction, skipping.")


if __name__ == "__main__":
    auto24 = Auto24()
    auto24.scrape(1)
