import os
import sys


def corrigir(proj):
    bg = os.path.join(proj, "app", "build.gradle")
    if not os.path.exists(bg):
        print(f"build.gradle nao encontrado em: {bg}")
        return False

    with open(bg) as f:
        conteudo = f.read()

    # Adiciona namespace se nao tiver
    if "namespace" not in conteudo:
        conteudo = conteudo.replace(
            "android {",
            "android {\n    namespace 'org.baixetube'"
        )
        with open(bg, "w") as f:
            f.write(conteudo)
        print(f"namespace adicionado em: {bg}")
    else:
        print("namespace ja existe")

    return True


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""

    if modo == "pre":
        # Modo pre-build: ainda nao tem o projeto gerado, nao faz nada
        print("Modo pre-build: aguardando buildozer gerar o projeto")

    else:
        # Modo pos-build: recebe o caminho do projeto como argumento
        proj = sys.argv[1]
        if corrigir(proj):
            print("build.gradle corrigido com sucesso!")
        else:
            print("Nao foi possivel corrigir")
