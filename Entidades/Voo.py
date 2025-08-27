from Entidades.Assento import Assento
from Enumerações.ClasseAssento import ClasseAssento
from Enumerações.PosicaoAssento import PosicaoAssento
import threading

class Voo:
    def __init__(self, codigo_voo, fileiras, assento_fileiras=6):
        """
        Inicializa as informações do voo incluindo código do voo, fileiras e assentos por fileira, que tem um valor padrao de 6.
        Cria a disposição dos assentos para o voo.

        :param codigo_voo: O identificador único para o voo - str
        :param fileiras: Número de fileiras presentes no voo - int
        :param assento_fileiras: Número de assentos disponíveis em cada fileira do voo - int
        """
        self.codigo_voo = codigo_voo
        self.assentos_voo = []
        self.lock = threading.Lock() #threading para garantir que so um passageiro pode reservar um assento
        self.reservas_voo = {} # Dicionário que vai ter como chave o passageiro e como valor o assento
        self.criaAssento(fileiras, assento_fileiras)

    def criaAssento(self, fileiras, assento_fileiras):
        """
        Cria os assentos do voo baseado no número de fileiras e assentos por fileira.
        Define a posição, classe e valor de cada assento, além de marcar assentos de emergência.

        :param fileiras: Número total de fileiras do avião - int
        :param assento_fileiras: Número de assentos por fileira - valor default 6
        """
        letrasAssento = ["A", "B", "C", "D", "E", "F"]

        for i in range(1, fileiras + 1):
            for j in range(assento_fileiras):
                numero = f"{i}{letrasAssento[j]}"
                if letrasAssento[j] in ["A", "F"]:
                    posicao = PosicaoAssento.JANELA
                elif letrasAssento[j] in ["C", "D"]:
                    posicao = PosicaoAssento.CORREDOR
                else:
                    posicao = PosicaoAssento.MEIO

                if i<= 2:
                    classe = ClasseAssento.PRIMEIRA_CLASSE
                    valor = Assento.VALORES[classe]
                elif i <= 5:
                    classe = ClasseAssento.EXECUTIVA
                    valor = 5000
                else:
                    classe = ClasseAssento.ECONOMICA
                    valor = 1000

                emergencia = (i == 10 and letrasAssento[j] in ["B", "C", "D", "E"])

                assento = Assento(numero, posicao, classe, valor, emergencia)
                self.assentos_voo.append(assento)

    def mostrarAssentos(self):
        """
        Exibe todos os assentos do voo com as suas informações.
        Mostra número, posição, classe, status e passageiro que reservou (se houver).
        """
        for assento in self.assentos_voo:
            status = assento.status
            reservado_por = assento.passageiro_cpf if assento.passageiro_cpf else "Nenhum"
            print(f">>> Numero: {assento.numero} - Posicao: {assento.posicao.name} - Classe: {assento.classe.name} - Status: {status} - Reservado por {reservado_por} - Valor: {assento.valor}")


    def reservarAssento(self, passageiro, numero):
        """
        Reserva um assento para o passageiro.
        :param passageiro: Passageiro a ser reservado - Passageiro
        :param numero: Assento a ser reservado - str
        """
        with self.lock:
            if passageiro.cpf in self.reservas_voo:
                return f">>> {passageiro.nome} já tem reserva no voo {self.codigo_voo}"

            assentoAlvo = None
            for a in self.assentos_voo:
                if a.numero == numero:
                    assentoAlvo = a
                    break
            if not assentoAlvo:
                return ">>> Assento não foi encontrado"
            if assentoAlvo.podeSerReservado(passageiro):
                try:
                    assentoAlvo.reservar(passageiro.cpf)
                except Exception:
                    return ">>> Assento não está mais disponível"

            self.reservas_voo[passageiro.cpf] = assentoAlvo
            if isinstance(passageiro.reservas, list) and self.codigo_voo not in passageiro.reservas:
                passageiro.reservas.append(self.codigo_voo)
            return f">>> {passageiro.nome} - reservou {numero} com sucesso"

    def cancelarReserva(self, passageiro):
        """
        Cancela a reserva do passageiro neste voo.
        Libera o assento e sincroniza passageiro.reservas.
        """
        with self.lock:
            if passageiro.cpf in self.reservas_voo:
                assento = self.reservas_voo[passageiro.cpf]
                try:
                    assento.cancelar()
                except Exception:
                    pass
                del self.reservas_voo[passageiro.cpf]

                if isinstance(passageiro.reservas, list):
                    if self.codigo_voo in passageiro.reservas:
                        passageiro.reservas.remove(self.codigo_voo)

                return f">>> Reserva de passageiro {passageiro.nome} cancelada"

            return f">>> {passageiro.nome} não foi encontrado"

    def modificarReserva(self, passageiro, numero_novo):
        """
        Troca o assento do passageiro
        """
        with self.lock:
            atual = self.reservas_voo.get(passageiro.cpf)
            if not atual:
                return f">>> {passageiro.nome} não possui reserva neste voo"
            if atual.numero == numero_novo:
                return ">>> O novo assento é o mesmo do atual"
            novo = None
            for a in self.assentos_voo:
                if a.numero == numero_novo:
                    novo = a
                    break
            if not novo:
                return ">>> Assento não foi encontrado"

            if novo.emergencia and not passageiro.passageiroMaior():
                return ">>> Passageiro menor de 18 anos, não é permitido reservar saída de emergência"

            if not novo.podeSerReservado(passageiro):
                return ">>> Novo assento não está disponível"
            try:
                novo.reservar(passageiro.cpf)
            except Exception:
                return ">>> Novo assento não está mais disponível"
            try:
                atual.cancelar()
            except Exception:
                try:
                    novo.cancelar()
                except Exception:
                    pass
                return ">>> Não foi possível concluir a modificação da reserva"

            self.reservas_voo[passageiro.cpf] = novo
            if isinstance(passageiro.reservas, dict):
                passageiro.reservas[self.codigo_voo] = novo.numero

            return f">>> Reserva alterada de {atual.numero} para {novo.numero}"
