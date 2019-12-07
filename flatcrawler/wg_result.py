
class WGResult(object):

    def __init__(self,
                 url: str,
                 title: str,
                 size: str,
                 cost: str,
                 address: str,
                 available_from: str,
                 available_to: str,
                 city: str,
                 advert_nr: str):
        self.url = url
        self.title = title
        self.size_of_room = size
        self.room_cost = cost
        self.address = address
        self.availability_from = available_from
        self.availability_to = available_to
        self.city = city
        self.id = advert_nr

    def as_string(self):
        result = "Title: " + self.title + "\n" \
                  + "Size: " + self.size_of_room + "\n" \
                  + "Cost: " + self.room_cost + "\n" \
                  + "Available from: " + self.availability_from + "\n" \
                  + "Available to: " + self.availability_to + "\n" \
                  + "Address: " + self.address + "\n" \
                  + "id: " + self.id + "\n" \
                  + "URL: " + self.url
        return result
