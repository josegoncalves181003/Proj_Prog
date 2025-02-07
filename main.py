# -*- coding: utf-8 -*-

class Passenger:
    def __init__(self,passenger_id, name, age, gender, passport_number, ticket_status):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.gender = gender
        self.passport_number = passport_number
        self.checked_in = False
        self.baggage_weight = 0
        self.ticket_status = ticket_status
