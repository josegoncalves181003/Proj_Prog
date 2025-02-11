# -*- coding: utf-8 -*-
import json

class Flight:
    def __init__(self, flight_id, destination, departure_time, arrival_time, plane, status = "Scheduled", available_seats = None):
        self.flight_id = flight_id
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.plane = plane
        self.status = status

        if available_seats is None:
            self.available_seats = {
                "Primeira Classe": plane.executive_seats,
                "Classe Executiva": plane.business_seats,
                "Classe Econômica": plane.economy_seats
            }
        else:
            self.available_seats = available_seats

    def book_seat(self, seat_class):
        """Attempts to book a seat in the specified class."""
        if seat_class in self.available_seats and self.available_seats[seat_class] > 0:
            self.available_seats[seat_class] -= 1
            print(f"Reserva confirmada: 1 assento em {seat_class}. Assentos restantes: {self.available_seats[seat_class]}")
        else:
            print(f"Erro: Nenhum assento disponível na {seat_class}.")
            
    def to_dict(self):
        return {
            "flight_id": self.flight_id,
            "destination": self.destination,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "plane": self.plane.model_name,
            "status": self.status,
            "available_seats": self.available_seats
        }
    
    @staticmethod
    def from_dict(data, plane_manager):
        plane = plane_manager.find_plane_by_id(data["plane"]["plane_id"])
        if plane:
            return Flight(
                flight_id=data["flight_id"],
                destination=data["destination"],
                departure_time=data["departure_time"],
                arrival_time=data["arrival_time"],
                plane=plane,
                status=data.get("status", "Scheduled"),
                available_seats=data.get("available_seats", {})
            )
        return None

    def __str__(self):
        return (f"Voo ID: {self.flight_id} | Destino: {self.destination} | "
                f"Partida: {self.departure_time} | Chegada: {self.arrival_time} | "
                f"Avião: {self.plane.model_name} | Status: {self.status}")
        
class FlightManager:
    def __init__(self, plane_manager):
        self.flights = []
        self.id_counter = 1
        self.plane_manager = plane_manager
        self.filename = "flights.json"
        self.load_flights()
        
    def save_flights(self):
        with open(self.filename, "w") as file:
            json.dump([flight.to_dict() for flight in self.flights], file, indent=4)

    def load_flights(self):
        try:
            with open(self.filename, "r") as file:
                flights_data = json.load(file)
                self.flights = [Flight.from_dict(data, self.plane_manager) for data in flights_data if Flight.from_dict(data, self.plane_manager)]
                if self.flights:
                    self.id_counter = max(flight.flight_id for flight in self.flights) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.flights = []

    def add_flight(self):
        destination = input("Destino do voo: ")
        departure_time = input("Horário de partida (YYYY-MM-DD HH:MM): ")
        arrival_time = input("Horário de chegada (YYYY-MM-DD HH:MM): ")
        
        print("\nAviões disponiveis:")
        self.plane_manager.list_planes()
        while True:
            try:
                plane_id = int(input("Insira o ID do avião a ser atribuído ao voo: "))
                plane = self.plane_manager.find_plane_by_id(plane_id)
                if plane:
                    break
                else:
                    print("Erro: Avião não encontrado. Tente novamente.")
            except ValueError:
                print("Erro: Insira um número válido.")
        
        flight = Flight(self.id_counter, destination, departure_time, arrival_time, plane)
        self.flights.append(flight)
        self.id_counter += 1
        self.save_flights()
        print(f"Voo {flight.flight_id} adicionado com sucesso!\n")

    def list_flights(self):
        if not self.flights:
            print("Nenhum voo cadastrado.\n")
        else:
            print("\nLista de Voos:")
            for flight in self.flights:
                print(f"ID: {flight.flight_id} | Destino: {flight.destination} | "
                      f"Partida: {flight.departure_time} | Chegada: {flight.arrival_time} | "
                      f": {flight.status}")
                print("\n")
            print()

    def find_flight_by_id(self, flight_id):
        for flight in self.flights:
            if flight.flight_id == flight_id:
                return flight
        return None

    def update_flight_status(self):
        flight_id = self.get_valid_integer("ID do voo para atualizar o status: ")
        flight = self.find_flight_by_id(flight_id)

        if flight:
            new_status = input("Novo status do voo (On Time, Delayed, Canceled): ").strip()
            self.save_flights()
            flight.update_status(new_status)
            print(f"Status do voo {flight_id} atualizado para {new_status}.\n")
        else:
            print("Voo não encontrado.\n")

    def remove_flight(self):
        flight_id = self.get_valid_integer("ID do voo a remover: ")
        for flight in self.flights:
            if flight.flight_id == flight_id:
                self.flights.remove(flight)
                self.save_flights()
                print(f"Voo {flight_id} removido com sucesso!\n")
                return
        print("Voo não encontrado.\n")

    def get_valid_integer(self, prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Entrada inválida! Insira um número inteiro.\n")
                
class Plane:
    def __init__(self, model_name, plane_id, executive_seats, business_seats, economy_seats):
        self.model_name = model_name
        self.plane_id = plane_id
        self.executive_seats = executive_seats
        self.business_seats = business_seats
        self.economy_seats = economy_seats
        self.total_seats = executive_seats + business_seats + economy_seats

    def __str__(self):
        return (f"ID do Avião: {self.plane_id} | Modelo: {self.model_name} | "
                f"Assentos Primeira Classe: {self.executive_seats} | Assentos Classe Executiva: {self.business_seats} | "
                f"Assentos Classe Econômica: {self.economy_seats} | Total de Assentos: {self.total_seats}")
    
    def get_seat_distribution(self):
        return {
            "Primeira Classe": self.executive_seats,
            "Classe Executiva": self.business_seats,
            "Classe Econômica": self.economy_seats,
            "Total": self.total_seats
        }

    def get_plane_key(self):
        # Cria uma chave única para o avião com base no modelo e na distribuição dos assentos
        return (self.model_name, self.executive_seats, self.business_seats, self.economy_seats)

class PlaneManager:
    def __init__(self):
        self.planes = []
        self.id_counter = 1
        self.plane_type_count = {}  # Dicionário para contar aviões por tipo (modelo + distribuição de assentos)

    def create_plane(self):
        model_name = input("Introduza o modelo do avião: ")
        try:
            executive_seats = int(input("Insira o número de assentos de primeira classe: "))
            business_seats = int(input("Insira o número de assentos da classe executiva: "))
            economy_seats = int(input("Insira o número de assentos da classe econômica: "))
        except ValueError:
            print("ERRO! Por favor introduza números válidos.\n")
            return
        
        plane = Plane(model_name, self.id_counter, executive_seats, business_seats, economy_seats)
        plane_key = plane.get_plane_key()
        if plane_key in self.plane_type_count:
            # Se o avião já existe, incrementa a contagem
            self.plane_type_count[plane_key] += 1
            print(f"Avião já existente com as mesmas características. Foi adicionado mais um avião deste tipo à frota.\n")
        else:
            self.plane_type_count[plane_key] = 1
            print(f"Avião {model_name} (ID:{plane.plane_id}) adicionado à frota com sucesso.\n")
        
        self.planes.append(plane)
        self.id_counter += 1

    def remove_plane(self):
        try:
            plane_id = int(input("Insira o ID do avião que deseja remover da frota: "))
        except ValueError:
            print("O ID tem de ser um valor inteiro.\n")
            return
        
        plane = self.find_plane_by_id(plane_id)
        if plane:
            self.planes.remove(plane)
            plane_key = plane.get_plane_key()
            if plane_key in self.plane_type_count:
                self.plane_type_count[plane_key] -= 1
                if self.plane_type_count[plane_key] == 0:
                    del self.plane_type_count[plane_key]
            print(f"Avião {plane.model_name} (ID: {plane.plane_id}) removido com sucesso.\n")
        else:
            print("Avião não encontrado.\n")
    
    def update_plane(self):
        try:
            plane_id = int(input("Insira o ID do avião que deseja atualizar: "))
        except ValueError:
            print("O ID tem de ser um valor inteiro.\n")
            return
        
        plane = self.find_plane_by_id(plane_id)
        if plane:
            print(f"\nAtualizar Avião (ID: {plane.plane_id})")
            print("1. Atualizar nome do modelo do avião")
            print("2. Atualizar assentos primeira classe")
            print("3. Atualizar assentos classe executiva")
            print("4. Atualizar assentos classe econômica")
            print("5. Cancelar atualização")
            choice = input("Escolha uma opção: ")
            
            if choice == "1":
                new_model_name = input(f"Nome atual do modelo do avião: {plane.model_name}\nNovo nome do modelo do avião: ")
                plane.model_name = new_model_name
            elif choice == "2":
                try:
                    new_executive_seats = int(input(f"Número atual de assentos de primeira classe: {plane.executive_seats}\nNúmero atualizado de assentos de primeira classe: "))
                    plane.executive_seats = new_executive_seats
                except ValueError:
                    print("Introduza um número de assentos válido.\n")
            elif choice == "3":
                try:
                    new_business_seats = int(input(f"Número atual de assentos de classe executiva: {plane.business_seats}\nNúmero atualizado de assentos de classe executiva: "))
                    plane.business_seats = new_business_seats
                except ValueError:
                    print("Introduza um número de assentos válido.\n")
            elif choice == "4":
                try:
                    new_economy_seats = int(input(f"Número atual de assentos de classe econômica: {plane.economy_seats}\nNúmero atualizado de assentos de classe econômica: "))
                    plane.economy_seats = new_economy_seats
                except ValueError:
                    print("Introduza um número de assentos válido.\n")
            elif choice == "5":
                print("Atualização cancelada.\n")
            else:
                print("Opção inválida.\n")
            
            plane.total_seats = plane.executive_seats + plane.business_seats + plane.economy_seats
            print(f"Avião atualizado: {plane}\n")
        else:
            print("Avião não encontrado.\n")
    
    def list_planes(self):
        if not self.planes:
            print("Não existem aviões.\n")
        else:
            print("\nListagem de todos os aviões")
            for plane in self.planes:
                print(f"ID: {plane.plane_id} | Model: {plane.model_name} | Total_seats: {plane.total_seats}")
            print()
    
    def find_plane_by_id(self, plane_id):
        for plane in self.planes:
            if plane.plane_id == plane_id:
                return plane
        return None

    def count_planes_by_type(self):
        print("\nContagem de aviões por tipo (modelo + distribuição de assentos):")
        for plane_key, count in self.plane_type_count.items():
            print(f"Modelo: {plane_key[0]} | Primeira Classe: {plane_key[1]} | Executiva: {plane_key[2]} | Econômica: {plane_key[3]} | Quantidade: {count}")

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

    def update_ticket_status(self, ticket_status):
        self.ticket_status = ticket_status

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
        self.filepath = "passenger.json"
        self.load_passengers()
        
    def save_passengers(self):
        with open(self.filepath, "w") as file:
            json.dump([vars(p) for p in self.passengers], file, indent=4)
            
    def load_passengers(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                self.passengers = [Passenger(**p) for p in data]
                if self.passengers:
                    self.id_counter = max(p.passenger_id for p in self.passengers) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.passengers = []

    def add_passenger(self):
        name = input("Nome do passageiro: ")
        try:
            age = int(input("Idade do passageiro: "))
        except ValueError:
            print("Idade inválida! Deve ser um número inteiro.\n")
            return
        gender_choice = input("Gênero do passageiro (M/F/O): ").lower()
        gender_map = {
            "m": "Masculino",
            "f": "Feminino",
            "o": "Outro"
        }
        gender = gender_map.get(gender_choice)
        if not gender:
            print("Gênero inválido! Deve ser 'M', 'F' ou 'O'.\n")
            return
        nationality = input("Nacionalidade do passageiro: ")
        while True:
            passport_number = input("Número do passaporte (8 ou 9 dígitos): ")
            if passport_number.isdigit() and len(passport_number) in [8, 9]:
                if self.check_duplicate_passport(passport_number):
                    print(f"Erro: Já existe um passageiro com o número de passaporte {passport_number}.\n")
                else:
                    break
            else:
                print("Número de passaporte inválido! Deve ter 8 ou 9 dígitos.")
            
        passenger = Passenger(self.id_counter, name, age, gender, nationality, passport_number)
        self.passengers.append(passenger)
        self.id_counter += 1
        self.save_passengers()
        print(f"Passageiro {passenger.name} (ID: {passenger.passenger_id}) adicionado com sucesso!\n")

    def list_passengers(self):
        if not self.passengers:
            print("Nenhum passageiro cadastrado.\n")
        else:
            print("\nLista de Passageiros:")
            for passenger in self.passengers:
                print(f"ID: {passenger.passenger_id} | Nome: {passenger.name} | Status: {passenger.ticket_status}")
            print()

    def update_passenger(self):
        try:
            passenger_id = int(input("ID do Passageiro para atualizar: "))
        except ValueError:
            print("ID inválido! Deve ser um número inteiro.\n")
            return
        passenger = self.find_passenger_by_id(passenger_id)

        if passenger:
            print(f"Passageiro {passenger.name} encontrado.\nO que deseja atualizar?")
            while True:
                print("\n1. Atualizar nome")
                print("2. Atualizar idade")
                print("3. Atualizar gênero")
                print("4. Atualizar nacionalidade")
                print("5. Atualizar número do passaporte")
                print("6. Concluir atualização")
                choice = input("Escolha uma opção: ")
                
                if choice == "1":
                    self.update_name(passenger)
                elif choice == "2":
                    self.update_age(passenger)
                elif choice == "3":
                    self.update_gender(passenger)
                elif choice == "4":
                    self.update_nationality(passenger)
                elif choice == "5":
                    self.update_passport_number(passenger)
                elif choice == "6":
                    self.save_passengers(passenger)
                    print(f"Passageiro {passenger.name} atualizado com sucesso!\n")
                    return
                else:
                    print("Opção inválida!")
        else:
            print("Passageiro não encontrado.\n")

    def find_passenger_by_id(self, passenger_id):
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                return passenger
        return None

    def update_name(self, passenger):
        new_name = input(f"Nome atual: {passenger.name}\nNovo nome: ")
        passenger.name = new_name

    def update_age(self, passenger):
        while True:
            try:
                new_age = int(input(f"Idade atual: {passenger.age}\nNova idade: "))
                if new_age < 0:
                    print("Idade não pode ser negativa.")
                else:
                    passenger.age = new_age
                    break
            except ValueError:
                print("Por favor, insira um número válido para a idade.")

    def update_gender(self, passenger):
        gender_choice = input(f"Gênero atual: {passenger.gender}\nNovo gênero (M/F/O): ").lower()
        gender_map = {'m': 'Masculino', 'f': 'Feminino', 'o': 'Outro'}
        gender = gender_map.get(gender_choice)

        if gender:
            passenger.gender = gender
        else:
            print("Gênero inválido.\n")

    def update_nationality(self, passenger):
        new_nationality = input(f"Nacionalidade atual: {passenger.nationality}\nNova nacionalidade: ")
        passenger.nationality = new_nationality

    def update_passport_number(self, passenger):
        while True:
            new_passport_number = input(f"Número de passaporte atual: {passenger.passport_number}\nNovo número do passaporte (8 ou 9 dígitos): ")
            if new_passport_number.isdigit() and len(new_passport_number) in [8, 9]:
                passenger.passport_number = new_passport_number
                break
            print("Número de passaporte inválido! Deve ter 8 ou 9 dígitos.")

    def remove_passenger(self):
        try:
            passenger_id = int(input("ID do passageiro a remover: "))
        except ValueError:
            print("ID inválido! Deve ser um número inteiro.\n")
            return
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                self.passengers.remove(passenger)
                self.save_passengers()
                print(f"Passageiro {passenger.name}(ID:{passenger_id}), removido com sucesso!\n")
                return
        print("Passageiro não encontrado.\n")
        
    def search_passenger(self):
        print("\nPesquisar Passageiro")
        print("1. Pesquisar por ID")
        print("2. Pesquisar por Nome")
        print("3. Pesquisar por Número de Passaporte")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            try:
                passenger_id = int(input("Digite o ID do passageiro: "))
                found = [p for p in self.passengers if p.passenger_id == passenger_id]
            except ValueError:
                print("ID inválido! Deve ser um número inteiro.\n")
                return

        elif choice == "2":
            name = input("Digite o nome do passageiro: ").strip().lower()
            found = [p for p in self.passengers if p.name.lower() == name]

        elif choice == "3":
            passport_number = input("Digite o número do passaporte: ").strip()
            found = [p for p in self.passengers if p.passport_number == passport_number]

        else:
            print("Opção inválida!")
            return

        if found:
            print("\nPassageiro(s) encontrado(s):")
            for passenger in found:
                print(passenger)
        else:
            print("Nenhum passageiro encontrado com esses dados.\n")
            
    def book_flight(self):
        passenger_id = input("Digite o ID do passageiro: ")

        if not passenger_id.isdigit():
            print("Erro: O ID do passageiro deve ser um número.\n")
            return

        passenger_id = int(passenger_id)
        passenger = self.passenger_manager.find_passenger_by_id(passenger_id)

        if not passenger:
            print("Erro: Passageiro não encontrado.\n")
            return

        # Verificar se o passageiro já tem um voo reservado
        if passenger.flight_id:
            print(f"Erro: O passageiro {passenger.name} já está reservado no voo {passenger.flight_id}.\n")
            return

        flight_id = input("Digite o ID do voo que deseja reservar: ")
        flight = self.flight_manager.find_flight_by_id(flight_id)

        if not flight:
            print("Erro: Voo não encontrado.\n")
            return

        # Exibir assentos disponíveis por classe
        print("\nAssentos disponíveis por classe:")
        for class_name, seats in flight.available_seats.items():
            print(f"{class_name.capitalize()}: {seats} assentos")

        class_map = {
            "1": "first_class",
            "2": "business",
            "3": "economy"
        }

        class_choice = input("Escolha a classe (1 - Primeira Classe, 2 - Executiva, 3 - Econômica): ")
        chosen_class = class_map.get(class_choice)

        if not chosen_class:
            print("Erro: Classe inválida.\n")
            return

        if flight.available_seats[chosen_class] <= 0:
            print(f"Erro: Não há assentos disponíveis na classe {chosen_class.capitalize()}.\n")
            return

        # Atualizar os dados do passageiro e do voo
        passenger.assign_flight(flight_id)
        passenger.update_ticket_status("Confirmado")
        flight.available_seats[chosen_class] -= 1

        print(f"Reserva confirmada para {passenger.name} no voo {flight_id} (Classe: {chosen_class.capitalize()}).\n")
        
    def check_in_passenger(self):
        try:
            passenger_id = int(input("ID do Passageiro para check-in: "))
        except ValueError:
            print("ID inválido! Deve ser um número inteiro.\n")
            return

        passenger = self.find_passenger_by_id(passenger_id)
        if not passenger:
            print("Passageiro não encontrado.\n")
            return

        if passenger.checked_in:
            print("Passageiro já realizou o check-in.\n")
            return

        while True:
            try:
                weight = float(input("Peso da bagagem (kg): "))
                if weight <= 0:
                    print("Erro: O peso deve ser um valor positivo.")
                    continue
                break
            except ValueError:
                print("Entrada inválida! Certifique-se de inserir um número válido para o peso.")

        while True:
            try:
                length = float(input("Comprimento da bagagem (cm): "))
                width = float(input("Largura da bagagem (cm): "))
                height = float(input("Altura da bagagem (cm): "))
                if length <= 0 or width <= 0 or height <= 0:
                    print("Erro: As dimensões devem ser valores positivos.")
                    continue
                break
            except ValueError:
                print("Entrada inválida! Certifique-se de inserir números válidos para as dimensões.")
        
        if self.check_luggage_size(weight, length, width, height):
            passenger.check_in(weight)
            self.save_passengers()
            print(f"Check-in realizado com sucesso para {passenger.name} (ID: {passenger.passenger_id}).\n")

    def check_luggage_size(self, weight, length, width, height):
        MAX_WEIGHT = 23
        MAX_TOTAL_SIZE = 158
        
        total_size = length + width + height
        if weight > MAX_WEIGHT:
            print(f"Erro: Peso da bagagem ultrapassa o limite máximo de {MAX_WEIGHT} kg.\nCheck-in negado!")
            return False
        if total_size > MAX_TOTAL_SIZE:
            print(f"Erro: Tamanho total da bagagem ultrapassa o limite máximo de {MAX_TOTAL_SIZE} cm.\nCheck-in negado!")
            return False
        return True

    def check_duplicate_passport(self, passport_number):
        return any(p.passport_number == passport_number for p in self.passengers)
    
class MenuSystem:
    def __init__(self):
        self.passenger_manager = PassengerManager()
        self.plane_manager = PlaneManager()
        self.flight_manager = FlightManager()

    def passenger_menu(self):
        while True:
            print("\nSistema de Gestão de Passageiros")
            print("1. Adicionar passageiro")
            print("2. Listar todos os passageiros")
            print("3. Atualizar dados do passageiro")
            print("4. Remover passageiro")
            print("5. Pesquisar passageiro")
            print("6. Check-in de passageiro")
            print("7. Voltar ao menu principal")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.passenger_manager.add_passenger()
            elif choice == "2":
                self.passenger_manager.list_passengers()
                self.press_enter_to_continue()
            elif choice == "3":
                self.passenger_manager.update_passenger()
            elif choice == "4":
                self.passenger_manager.remove_passenger()
            elif choice == "5":
                self.passenger_manager.search_passenger()
                self.press_enter_to_continue()
            elif choice == "6":
                self.passenger_manager.check_in_passenger()
                self.press_enter_to_continue()
            elif choice == "7":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def plane_menu(self):
        while True:
            print("\nGestão de aviões")
            print("1. Adicionar um avião")
            print("2. Remover um avião")
            print("3. Atualizar um avião")
            print("4. Listar todos os aviões")
            print("5. Ver contagem de aviões por tipo")
            print("6. Regressar ao menu principal")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.plane_manager.create_plane()
            elif choice == "2":
                self.plane_manager.remove_plane()
            elif choice == "3":
                self.plane_manager.update_plane()
            elif choice == "4":
                self.plane_manager.list_planes()
            elif choice == "5":
                self.plane_manager.count_planes_by_type()
            elif choice == "6":
                print("Regressando ao menu principal....")
                break
            else:
                print("Opção inválida. Tente novamente.")


    def flight_menu(self):
        while True:
            print("\nGestão de voos")
            print("1. Criar voo")
            print("2. Listar todos os voos")
            print("3. Atualizar estado do voo")
            print("4. Apagar voo")
            print("5. Regressar ao menu principal")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.flight_manager.add_flight()
                self.press_enter_to_continue()
            elif choice == "2":
                self.flight_manager.list_flights()
                self.press_enter_to_continue()
            elif choice == "3":
                self.flight_manager.update_flight_status()
                self.press_enter_to_continue()
            elif choice == "4":
                self.flight_manager.remove_flight()
                self.press_enter_to_continue()
            elif choice == "5":
                print("Regressando ao menu principal...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def press_enter_to_continue(self):
        input("\nPressione ENTER para continuar...")

    def main_menu(self):
        while True:
            print("\nSistema de gestão aeroportuária")
            print("1. Gestão de passageiros")
            print("2. Gestão de aviões")
            print("3. Gestão de voos")
            print("4. Sair")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.passenger_menu()
            elif choice == "2":
                self.plane_menu()
            elif choice == "3":
                self.flight_menu()
            elif choice == "4":
                print("Fechando o programa...")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_system = MenuSystem()
    menu_system.main_menu()