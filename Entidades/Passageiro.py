
from datetime import datetime

class Passageiro:

    def __init__(self, nome, cpf, data_nascimento, email):
        """
        Cria um passageiro.

        :param nome: Nome completo do passageiro - str
        :param cpf: CPF do passageiro - str
        :param data_nascimento: Data de nascimento no formato 'dd/mm/aa' - str
        :param email: E-mail do passageiro - str
        """
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.reservas = []

    def passageiroMaior(self):
        """
        Indica se o passageiro é maior de 18 anos.

        :return: True se o passageiro for maior (ou completar 18 hoje). False caso contrário - bool
        """
        print(">>> Calculando se o passageiro é maior de idade...")
        dataAtual = datetime.now()
        mesAtual = str(dataAtual.month)
        diaAtual = str(dataAtual.day)
        anoAtual = str(dataAtual.year)
        anoAtualSplit = anoAtual[2:4]
        diaAniversario = self.data_nascimento[0:2]
        mesAniversario = self.data_nascimento[3:5]
        anoAniversario = self.data_nascimento[6:8]
        diffAnos = int(anoAniversario) - int(anoAtualSplit)

        resultado = False
        if diffAnos < 18:
            resultado = False
        elif diffAnos > 18:
            resultado = True
        elif diffAnos == 18:
            if int(mesAtual) > int(mesAniversario):
                resultado = True
            elif int(mesAtual) == int(mesAniversario):
                if int(diaAtual) >= int(diaAniversario):
                    resultado = True
        return resultado

    def __str__(self):
        """
        :return: String com nome e CPF do passageiro - str
        """
        string = f'>>> {self.nome} {self.cpf}'
        return string
