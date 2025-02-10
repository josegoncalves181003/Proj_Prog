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
    
    def check_duplicate_passport(self, passport_number):
        return any(p.passport_number == passport_number for p in self.passengers)
    
    def check_luggage_size(self, weight,length, width, height):
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
        
def press_enter_to_continue():
    input("\nPressione ENTER para continuar...")
    
def menu():
    manager = PassengerManager()
    while True:
        print("\nSistema de Gestão de Passageiros")
        print("1. Adicionar passageiro")
        print("2. Listar todos os passageiros")
        print("3. Atualizar dados o passageiro")
        print("4. Remover passageiro")
        print("5. Pesquisar passageiro")
        print("6. Check-in de passageiro")
        print("7. Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            manager.add_passenger()
        elif choice == "2":
            manager.list_passengers()
            press_enter_to_continue()
        elif choice == "3":
            manager.update_passenger()
        elif choice == "4":
            manager.remove_passenger()
        elif choice == "5":
            manager.search_passenger()
            press_enter_to_continue()
        elif choice == "6":
            manager.check_in_passenger()
            press_enter_to_continue()
        elif choice == "7":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
