import requests
from bs4 import BeautifulSoup


class AuctionException(Exception):
    pass


class Vehicle:

    url = "https://www.auto24.ee/used/"

    def __init__(self, identifier):
        self.identifier = identifier
        self.soup = self._get_listing_page(self.identifier)
        self.raw_data = self._get_vehicle_data()
        self.data = self._populate_data()

    def _get_listing_page(self, identifier: str):
        page = requests.get(self.url+str(identifier))
        return BeautifulSoup(page.content, "html.parser")

    def _populate_data(self) -> dict:
        dictionary = {
            "Identifier": self.identifier,
            "Name": self._get_name(),
            "Price": self._get_price(),
            "Category": self._get_category(),
            "Bodytype": self._get_bodytype(),
            "First reg": self._get_first_reg(),
            "Engine size": self._get_engine_size(),
            "Engine power": self._get_engine_kw(),
            "Fuel": self._get_fuel(),
            "Odometer": self._get_odometer(),
            "Drive": self._get_drive(),
            "Transmission": self._get_transmission(),
            "Color": self._get_color()
        }
        print(dictionary["Name"])
        return dictionary

    @staticmethod
    def _pretty_price(raw_price: str) -> int:
        pretty = raw_price[:raw_price.find("\xa0")]
        return int(pretty or -1)

    def _get_vehicle_data(self) -> dict:
        """Gets data."""
        init_dict = dict()
        labels = self.soup.find_all(class_="label")
        fields = self.soup.find_all(class_="field")
        for x in range(len(fields)):
            label = labels[x].text.replace(":", "")
            field = fields[x].text
            init_dict[label] = field
        return init_dict

    def _get_value(self, entry: str) -> str:
        if value := self.raw_data[entry]:
            return value
        else:
            return ""

    def _get_name(self) -> str:
        return self.soup.find("title").text.replace(" - auto24.ee", "")

    def _get_price(self) -> int:
        if "Parim pakkumine" in self.soup.text:
            raise AuctionException
        return self._pretty_price(self._get_value("Hind"))

    def _get_category(self) -> str:
        return self._get_value("Liik")

    def _get_bodytype(self) -> str:
        return self._get_value("Keretüüp")

    def _get_first_reg(self) -> str:
        return self._get_value("Esmane reg")

    def _get_engine_size(self) -> str:
        engine = self._get_value("Mootor")
        return engine.split(" (")[0] or ""

    def _get_engine_kw(self) -> int:
        engine = self._get_value("Mootor")
        return int(engine.split("(")[1].replace(" kW)", "")) or -1

    def _get_fuel(self) -> str:
        return self._get_value("Kütus")

    def _get_odometer(self) -> int:
        raw_odometer = self._get_value("Läbisõidumõõdiku näit")
        if raw_odometer:
            odometer = raw_odometer.replace("\xa0", "").replace(" km", "")
        return int(odometer) or -1

    def _get_drive(self) -> str:
        return self._get_value("Vedav sild")

    def _get_transmission(self) -> str:
        return self._get_value("Käigukast")

    def _get_color(self) -> str:
        return self._get_value("Värvus")


if __name__ == "__main__":
    #auctionVehicle = Vehicle("3415526")
    normalVehicle = Vehicle("3405505")
    print(normalVehicle.data)

"""     

dataname = self._get_name()
price = self._get_price()
category = self._get_category()
bodytype = self._get_bodytype()
first_reg = self._get_first_reg()
engine_size = self._get_engine_size()
engine_kw = self._get_engine_kw()
fuel = self._get_fuel()
odometer = self._get_odometer()
drive = self._get_drive()
transmission = self._get_transmission()
color = self._get_color()

"""