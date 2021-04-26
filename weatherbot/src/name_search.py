from geotext import GeoText

class NameSearch:

    def find_place(input):

        place = GeoText(input)
        city = place.cities[0]

        if ' ' in city:
            city_list = city.split()
            city = city_list[0] + '+' +city_list[1]
        return city

    def return_city(input):
        place = GeoText(input)
        city = place.cities[0]
        return city
#str = "The city is New York"

#print(NameSearch.find_place(str))
