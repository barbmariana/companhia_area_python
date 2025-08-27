import sys
from Entidades.Voo import Voo

def exibir_informacoes():
    print("-" * 50)
    print("Bem vindo ao sistema da companhia aerea CEDERJ-AERO")
    print("-" * 50)

def main():
    try:
        exibir_informacoes()
        voos = [Voo("A100", 20), Voo("B200", 15)]
        try:
            from cli import CLI
            cli = CLI(voos)
            cli.executar()
        except ImportError as e:
            print(f"Erro de importação: {e}, por favor verificar se todos os módulos estão instalados")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nSistema interrompido pelo usuário")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()