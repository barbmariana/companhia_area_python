from Enumerações.ClasseAssento import ClasseAssento
from Enumerações.StatusReserva import StatusReserva
import threading


class Assento:
    """Representa um assento de voo com classe, posição, preço e status."""

    VALORES = {
        ClasseAssento.PRIMEIRA_CLASSE: 10000.00,
        ClasseAssento.ECONOMICA: 1000.00,
        ClasseAssento.EXECUTIVA: 5000.00,
    }

    def __init__(self, numero, posicao, classe, valor, emergencia=False):
        """
        Cria um assento em determinado vôo

        :param numero: Identificação do assento (ex.: '12A') - str
        :param posicao: Posição no avião (janela, corredor, meio) - PosicaoAssento
        :param classe: Classe do assento (econômica, executiva, primeira) - ClasseAssento
        :param valor: Preço do assento - float
        :param emergencia: Se é assento de saída de emergência - bool
        """
        self.numero = numero
        self.posicao = posicao
        self.classe = classe
        self.valor = valor
        self.emergencia = emergencia
        self.status = StatusReserva.LIVRE_PARA_RESERVA
        self.lock = threading.Lock()
        self.passageiro_cpf = None  # atributo passageiro_cpf iniciado com valor None

    def reservar(self, passageiro_cpf):
        """
        Reserva o assento para o CPF informado.

        :param passageiro_cpf: CPF do passageiro que está fazendo a reserva - str
        :return: True em caso de sucesso - bool
        :raises ValueError: se o assento não estiver livre para reserva.
        """
        with self.lock:
            if self.status != StatusReserva.LIVRE_PARA_RESERVA:
                raise ValueError("Assento já está reservado")

            self.status = StatusReserva.RESERVADO
            self.passageiro_cpf = passageiro_cpf
            return True

    def cancelar(self):
        """
        Cancela a reserva do assento e o torna livre novamente.

        :raises ValueError: se o assento não estiver reservado.
        """
        with self.lock:

            if self.status != StatusReserva.RESERVADO:
                raise ValueError(">>> Assento não está reservado")

            cpf_anterior = self.passageiro_cpf
            self.status = StatusReserva.LIVRE_PARA_RESERVA
            self.passageiro_cpf = None

    def verificaDonoReserva(self, passageiro_cpf):
        """
        Retorna se o CPF informado é o dono da reserva.

        :param passageiro_cpf: CPF do passageiro a ser verificado - str
        :return: True se o passageiro for o dono da reserva, False caso contrário - bool
        """
        resultado = self.status == StatusReserva.RESERVADO and self.passageiro_cpf == passageiro_cpf
        return resultado

    def podeSerReservado(self, passageiro):
        """
        Indica se o passageiro pode reservar este assento (inclui regra de emergência).

        :param passageiro: O passageiro que deseja fazer a reserva - Passageiro
        :return: True se o assento pode ser reservado pelo passageiro, false caso contrário - bool
        """
        print(f">>>Verificando se o assento {self.numero} pode ser reservado pelo passageiro {passageiro.nome}...")
        if self.status != StatusReserva.LIVRE_PARA_RESERVA:
            mensagem = f"Assento {self.numero} não está livre para reserva"
            print(mensagem)
            return False
        if self.emergencia and not passageiro.passageiroMaior():
            mensagem = f">>> Assento {self.numero} não disponível para o passageiro {passageiro.nome} (menor de idade)"
            print(mensagem)
            return False
        print(f">>> Assento de emergencia - {self.emergencia}")
        mensagem = f">>> Assento {self.numero} disponível para ser reservado pelo passageiro {passageiro.nome}. Valor a pagar: R$ {self.valor:.2f}"
        print(mensagem)
        return True