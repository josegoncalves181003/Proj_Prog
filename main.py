# -*- coding: utf-8 -*-

class Passenger:
    def __init__(self, passenger_id, name, age, gender, nationality, passport_number, ticket_status="Pending"):
        self.passenger_id = passenger_id
        self.name = name
        self.age = age
        self.gender = gender
        self.nationality = nationality
        self.passport_number = passport_number
        self.checked_in = False
        self.baggage_weight = 0
        self.ticket_status = ticket_status
        self.flight_id = None
        self.seat_number = None

    def assign_flight(self, flight_id):
        self.flight_id = flight_id

    def assign_seat(self, seat_number):
        self.seat_number = seat_number

    def update_ticket_status(self, status):
        self.ticket_status = status

    def check_in(self, baggage_weight):
        self.checked_in = True
        self.baggage_weight = baggage_weight

    def __str__(self):
        return (f"ID: {self.passenger_id} | Nome: {self.name} | Idade: {self.age} | Gênero: {self.gender} | "
                f"Passaporte: {self.passport_number} | Nacionalidade: {self.nationality} | "
                f"Voo: {self.flight_id if self.flight_id else 'N/A'} | Assento: {self.seat_number if self.seat_number else 'N/A'} | "
                f"Status: {self.ticket_status} | Check-in: {'Sim' if self.checked_in else 'Não'} | "
                f"Peso da Bagagem: {self.baggage_weight}kg")

class PassengerManager:
    def __init__(self):
        self.passengers = []
        self.id_counter = 1

    def add_passenger(self):
        name = input("Nome do passageiro: ")
        age = int(input("Idade do passageiro: "))
        gender_choice = input("Gênero do passageiro (M/F/O): ").lower()
        if gender_choice == 'm':
            gender = 'Masculino'
        elif gender_choice == 'f':
            gender = 'Feminino'
        elif gender_choice == 'o':
            gender = 'Outro'
        else:
            print("Gênero inválido.\n")
            return
        nationality = input("Nacionalidade do passageiro: ")
        passport_number = input("Número do passaporte: ")
        
        passenger = Passenger(self.id_counter, name, age, gender, nationality, passport_number)
        self.passengers.append(passenger)
        self.id_counter += 1
        print(f"Passageiro {passenger.name} adicionado com sucesso!\n")

    def list_passengers(self):
        if not self.passengers:
            print("Nenhum passageiro cadastrado.\n")
        else:
            print("\nLista de Passageiros:")
            for passenger in self.passengers:
                print(passenger)
            print()

    def update_passenger(self, passenger_id, new_flight_id=None, new_seat_number=None, new_status=None, check_in=False, baggage_weight=None):
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                if new_flight_id:
                    passenger.assign_flight(new_flight_id)
                if new_seat_number:
                    passenger.assign_seat(new_seat_number)
                if new_status:
                    passenger.update_ticket_status(new_status)
                if check_in and baggage_weight is not None:
                    passenger.check_in(baggage_weight)
                print(f"Passageiro {passenger_id} atualizado com sucesso!\n")
                return
        print("Passageiro não encontrado.\n")

    def remove_passenger(self,name):
        passenger_id = int(input("ID do passageiro a remover: "))
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                self.passengers.remove(passenger)
                print(f"Passageiro {name}(ID:{passenger_id}), removido com sucesso!\n")
                return
        print("Passageiro não encontrado.\n")
        
def press_enter_to_continue():
    input("\nPressione ENTER para continuar...")
    
def menu():
    manager = PassengerManager()
    while True:
        print("\nSistema de Gestão de Passageiros")
        print("1. Adicionar Passageiro")
        print("2. Listar Passageiros")
        print("3. Remover Passageiro")
        print("4. Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            manager.add_passenger()
        elif choice == "2":
            manager.list_passengers()
            press_enter_to_continue()
        elif choice == "3":
            manager.remove_passenger()
        elif choice == "4":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
