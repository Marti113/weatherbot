from geotext import GeoText

class NameSearch:
    def __init__(self, input):
        self.input = input
        place = GeoText(self.input)
        self.city = place.cities[0]

    def find_place(self):

        if ' ' in self.city:
            city_list = self.city.split()
            city_tag = city_list[0] + '+' + city_list[1]
            return city_tag

        else:
            return self.city

    def return_city(self):
        return self.city

#str = "The city is New York"

#print(NameSearch(str).find_place())
#print(NameSearch(str).return_city())
