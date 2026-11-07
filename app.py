#!/usr/bin/env python3
import os
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path.home() / ".todo.db"
LARGURA = 40
SEPARADOR = "#" * LARGURA

# --- Colors (ANSI escape codes, no extra libraries needed) ---
# Colors are turned off automatically when the output is not a terminal
# (for example when piping to a file) or if the NO_COLOR variable is set.
USAR_COR = sys.stdout.isatty() and "NO_COLOR" not in os.environ
if os.name == "nt":
    os.system("")  # enables ANSI colors in the Windows terminal

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
STRIKE = "\033[9m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def cor(texto, *estilos):
    if not USAR_COR:
        return texto
    return "".join(estilos) + texto + RESET


def sucesso(texto):
    print(cor(f"  {texto}", GREEN))


def erro(texto):
    print(cor(f"  {texto}", RED))


def aviso(texto):
    print(cor(f"  {texto}", YELLOW))


def limpar_ecra():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input(cor("\nPress Enter to continue...", DIM))


def titulo(texto):
    print(cor(SEPARADOR, CYAN))
    print(cor(f"# {texto}", CYAN, BOLD))
    print(cor(SEPARADOR, CYAN))


def fim_bloco():
    print(cor(SEPARADOR, CYAN))


def ligar_bd():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    return conn


def adicionar_tarefa(conn, descricao):
    conn.execute("INSERT INTO tarefas (descricao) VALUES (?)", (descricao,))
    conn.commit()


def procurar_tarefa(conn, descricao):
    """Return (id, concluida) of a task with the same description, or None.

    The comparison ignores upper/lower case and extra spaces. It is done in
    Python because SQLite's LOWER() does not handle accented letters.
    """
    alvo = " ".join(descricao.split()).casefold()
    for tarefa_id, texto, concluida in listar_tarefas(conn):
        if " ".join(texto.split()).casefold() == alvo:
            return tarefa_id, concluida
    return None


def listar_tarefas(conn):
    return conn.execute(
        "SELECT id, descricao, concluida FROM tarefas ORDER BY id"
    ).fetchall()


def concluir_tarefa(conn, tarefa_id):
    cur = conn.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (tarefa_id,))
    conn.commit()
    return cur.rowcount > 0


def remover_tarefa(conn, tarefa_id):
    row = conn.execute(
        "SELECT descricao FROM tarefas WHERE id = ?", (tarefa_id,)
    ).fetchone()
    if row is None:
        return None
    conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    return row[0]


def mostrar_tarefas(conn):
    tarefas = listar_tarefas(conn)
    if not tarefas:
        aviso("No tasks yet.")
        return False

    for tarefa_id, descricao, concluida in tarefas:
        if concluida:
            print(cor(f"  {tarefa_id}. [x] ", GREEN) + cor(descricao, GREEN, DIM, STRIKE))
        else:
            print(cor(f"  {tarefa_id}. [ ] ", YELLOW) + descricao)

    total = len(tarefas)
    feitas = sum(1 for t in tarefas if t[2])
    print(cor(f"\n  {feitas}/{total} completed", DIM))
    return True


def menu():
    limpar_ecra()
    titulo("TO-DO LIST")
    print(f"  {cor('1.', CYAN, BOLD)} Add a task")
    print(f"  {cor('2.', CYAN, BOLD)} Show tasks")
    print(f"  {cor('3.', CYAN, BOLD)} Complete a task")
    print(f"  {cor('4.', CYAN, BOLD)} Remove a task")
    print(f"  {cor('0.', RED, BOLD)} Exit")
    fim_bloco()
    return input("Choose an option: ").strip()


# Each action returns True if the program should pause afterwards,
# and False if the user cancelled (so we go straight back to the menu).

def acao_adicionar(conn):
    limpar_ecra()
    titulo("ADD A TASK, PUT 0 TO CANCEL")
    descricao = input("Task description: ").strip()
    if descricao == "0":
        return False
    elif not descricao:
        erro("Task description cannot be empty.")
    elif not any(c.isalpha() for c in descricao):
        erro("The task must be a sentence, not just numbers or symbols.")
    else:
        existente = procurar_tarefa(conn, descricao)
        if existente:
            tarefa_id, concluida = existente
            estado = "completed" if concluida else "pending"
            aviso(f"That task already exists (#{tarefa_id}, {estado}).")
        else:
            adicionar_tarefa(conn, descricao)
            sucesso("Task added.")
    fim_bloco()
    return True


def acao_mostrar(conn):
    limpar_ecra()
    titulo("YOUR TASKS")
    mostrar_tarefas(conn)
    fim_bloco()
    return True


def acao_concluir_ou_remover(conn, concluir):
    limpar_ecra()
    titulo(
        "COMPLETE A TASK, 0 TO CANCEL" if concluir else "REMOVE A TASK, PUT 0 TO CANCEL"
    )
    if not mostrar_tarefas(conn):
        fim_bloco()
        return True

    print()
    try:
        tarefa_id = int(input("Task number: "))
    except ValueError:
        erro("Please enter a valid task number.")
        fim_bloco()
        return True

    if tarefa_id == 0:
        return False

    if concluir:
        if concluir_tarefa(conn, tarefa_id):
            sucesso("Task completed.")
        else:
            erro("That task number does not exist.")
    else:
        removida = remover_tarefa(conn, tarefa_id)
        if removida is None:
            erro("That task number does not exist.")
        else:
            sucesso(f"Removed: {removida}")
    fim_bloco()
    return True


def main():
    conn = ligar_bd()

    while True:
        escolha = menu()
        limpar_ecra()

        if escolha == "0":
            titulo("GOODBYE!")
            fim_bloco()
            break
        elif escolha == "1":
            fazer_pausa = acao_adicionar(conn)
        elif escolha == "2":
            fazer_pausa = acao_mostrar(conn)
        elif escolha == "3":
            fazer_pausa = acao_concluir_ou_remover(conn, concluir=True)
        elif escolha == "4":
            fazer_pausa = acao_concluir_ou_remover(conn, concluir=False)
        else:
            erro("Please choose one of the listed options.")
            fazer_pausa = True

        if fazer_pausa:
            pausa()

    conn.close()


if __name__ == "__main__":
    main()