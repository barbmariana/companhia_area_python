from Entidades.Passageiro import Passageiro

class CLI:
    def __init__(self, voos):
        self.voos = {v.codigo_voo: v for v in voos}
        self.passageiros = {}
        self.usuario_logado = None

    def executar(self):
        while True:
            print("\n=== SISTEMA DE RESERVA DE VOOS ===")
            if self.usuario_logado:
                print(f"Logado como: {self.usuario_logado}")
                print("1. Visualizar voos")
                print("2. Visualizar assentos do seu voo")
                print("3. Reservar assento")
                print("4. Modificar reserva")
                print("5. Cancelar reserva")
                print("6. Logout")
            else:
                print("1. Cadastrar passageiro")
                print("2. Login")
                print("0. Sair")

            opcao = input("Escolha: ").strip()
            try:
                if self.usuario_logado:
                    if opcao == "1":
                        self.listarVoos()
                    elif opcao == "2":
                        self.visualizarAssentos()
                    elif opcao == "3":
                        self.reservarAssento()
                    elif opcao == "4":
                        self.modificarReserva()
                    elif opcao == "5":
                        self.cancelarReserva()
                    elif opcao == "6":
                        self.usuario_logado = None
                    else:
                        print("Opção inválida")
                else:
                    if opcao == "1":
                        self.cadastrar()
                    elif opcao == "2":
                        self.login()
                    elif opcao == "0":
                        break
                    else:
                        print("Opção inválida")
            except Exception as e:
                print("Erro:", e)

    def cadastrar(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        data_nascimento = input("Data de nascimento (dd/mm/aa): ")
        if not data_nascimento or not len(data_nascimento) == 8 or data_nascimento[2] != '/' or data_nascimento[
            5] != '/':
            print("Data deve estar no formato dd/mm/aa")
            return
        email = input("E-mail: ")
        if cpf in self.passageiros:
            print("CPF já cadastrado")
            return
        self.passageiros[cpf] = Passageiro(nome, cpf, data_nascimento, email)
        print("Cadastro realizado")

    def login(self):
        cpf = input("CPF: ")
        usuario = self.passageiros.get(cpf)
        if not usuario:
            print("Passageiro não encontrado")
            return
        self.usuario_logado = usuario
        print(f"Bem-vindo {usuario.nome}")

    def listarVoos(self):
        print("Voos disponíveis:")
        for codigo in self.voos.keys():
            print("-", codigo)

    def visualizarAssentos(self):
        voo = self.selecionarVooUsuario()
        if voo:
            voo.mostrarAssentos()

    def reservarAssento(self):
        voo = self._selecionar_voo_por_codigo()
        if voo:
            numero = input("Assento que deseja reservar: ").strip().upper()
            resp = voo.reservarAssento(self.usuario_logado, numero)
            print(resp)

    def cancelarReserva(self):
        voo = self.selecionarVooUsuario()
        if voo:
            resp = voo.cancelarReserva(self.usuario_logado)
            print(resp)

    def modificarReserva(self):
        voo = self.selecionarVooUsuario()
        if voo:
            novo = input("Novo assento que deseja reservar: ").strip().upper()
            if hasattr(voo, "modificarReserva"):
                resp = voo.modificarReserva(self.usuario_logado, novo)
            print(resp)

    def selecionarVooUsuario(self):
        if not self.usuario_logado:
            print("Você precisa estar logado.")
            return None
        return self._selecionar_voo_por_codigo()

    def _selecionar_voo_por_codigo(self):
        while True:
            self.listarVoos()
            codigo = input("Digite o código do voo (ou pressione ENTER para cancelar): ").strip().upper()
            if codigo == "":
                print("Operação cancelada.")
                return None
            voo = self.voos.get(codigo)
            if voo:
                return voo
            print("Voo não encontrado. Tente novamente.")



