# -*- coding: utf-8 -*-

class Passenger:
    def __init__(self,passenger_id, name, age, gender, nationality, passport_number, ticket_status):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.gender = gender
        self.nationality = nationality
        self.passport_number = passport_number
        self.checked_in = False
        self.baggage_weight = 0
        self.ticket_status = ticket_status
    
    def __str__(self):
        return (f"ID: {self.passenger_id} | Nome: {self.name} | Passaporte: {self.passport_number} | Status: {self.ticket_status}")
    
    passengers = []

    def add_passenger(passenger_id, name, passport_number, nationality, flight_id, seat_number):
        new_passenger = Passenger(passenger_id, name, passport_number, nationality, flight_id, seat_number)
        passengers.append(new_passenger)
        print(f" Passageiro {name} adicionado com sucesso!\n")

        
#ALTERAR 

#Criar class passenger manager para gerir os passageiros e encapsular todas as funções utilizadas para tal