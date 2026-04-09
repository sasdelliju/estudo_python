import random
import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_titulo():
    print("=" * 40)
    print("🎯  JOGO DA ADIVINHAÇÃO  🎯")
    print("=" * 40)

def jogar():
    nivel = 1
    pontuacao = 0

    while True:
        limpar_tela()
        mostrar_titulo()
        print(f"\n📈 Nível: {nivel}")
        print(f"⭐ Pontuação: {pontuacao}\n")

        numero_max = nivel * 10
        numero_secreto = random.randint(1, numero_max)
        tentativas = 3

        print(f"Estou pensando em um número entre 1 e {numero_max}")
        print(f"Você tem {tentativas} tentativas!\n")

        ganhou = False

        while tentativas > 0:
            try:
                chute = int(input("Digite seu palpite: "))
            except ValueError:
                print("⚠️ Digite um número válido!")
                continue

            if chute == numero_secreto:
                print("🎉 Acertou!")
                pontuacao += nivel * 10
                ganhou = True
                break
            elif chute < numero_secreto:
                print("📉 Muito baixo!")
            else:
                print("📈 Muito alto!")

            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}\n")

        if not ganhou:
            print(f"❌ Você perdeu! O número era {numero_secreto}")
            print(f"Pontuação final: {pontuacao}")
            break

        input("\nPressione ENTER para ir ao próximo nível...")
        nivel += 1

    print("\nObrigado por jogar!")

if __name__ == "__main__":
    jogar()
