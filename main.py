# -*- coding: utf-8 -*-
"""
ARQUIVO BASILISCO / BASILISK ARCHIVE
Bootstrap: loop principal, tratamento de exceção, fluxo de telas.
Desenvolvedor: Pablo Murad - 2026
contato@pablomurad.com
versão 0.0.1
"""

from __future__ import annotations

import io
import sys

# Garantir UTF-8 na saída para caracteres acentuados (Windows)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    from engine import GameEngine
    from ui import (
        run_choice_menu,
        print_consequence,
        print_sector_exit,
        show_scene_and_wait_enter,
        show_credits,
        _get_console,
    )

    engine = GameEngine()
    console = _get_console()

    while True:
        scene_id = engine.current_scene_id

        # Sair do jogo
        if engine.is_quit(scene_id):
            return 0

        # Cena sem escolhas: exibir e aguardar Enter (finais narrativos)
        if engine.is_ending(scene_id):
            show_scene_and_wait_enter(engine)
            engine.current_scene_id = "epilogue"
            continue

        # Epílogo: menu Jogar novamente / Menu principal / Sair
        if engine.is_epilogue():
            index, escaped = run_choice_menu(engine)
            if escaped:
                engine.go_to_main_menu()
                continue
            if index is not None:
                choices = engine.get_choices()
                if 0 <= index < len(choices):
                    next_id = choices[index].get("next", "")
                    if next_id == "p0_arrival":
                        engine.reset_for_new_game()
                    elif next_id == "main_menu":
                        engine.go_to_main_menu()
                    elif next_id == "quit":
                        return 0
            continue

        # Créditos: tela especial com uma opção Voltar
        if engine.is_credits():
            show_credits(engine)
            index, escaped = run_choice_menu(engine)
            if escaped:
                engine.go_to_main_menu()
                continue
            if index is not None:
                result = engine.apply_choice(index)
                if engine.is_quit(result.get("next_scene_id")):
                    return 0
            continue

        # Demais cenas com escolhas
        index, escaped = run_choice_menu(engine)

        if escaped:
            if engine.is_main_menu():
                return 0
            if engine.is_language_select():
                continue
            engine.go_to_main_menu()
            continue

        if index is None:
            continue

        result = engine.apply_choice(index)
        next_id = result.get("next_scene_id", "")

        if engine.is_quit(next_id):
            return 0

        # Consequência da escolha (texto extra, apenas em cenas narrativas)
        print_consequence(
            engine,
            result.get("consequence_pt"),
            result.get("consequence_en"),
        )
        # Texto de saída do setor
        print_sector_exit(
            engine,
            result.get("sector_exit_pt"),
            result.get("sector_exit_en"),
        )

    return 0


def run() -> None:
    """Entry point com tratamento de exceção."""
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        import traceback
        # Evitar stack trace feio para o usuário final em erro previsível
        if "NO_COLOR" not in __import__("os").environ:
            from rich.console import Console
            from rich.panel import Panel
            Console().print(Panel(
                f"Ocorreu um erro. Tente novamente.\n\nErro: {e}",
                title="Erro",
                border_style="red",
            ))
        else:
            print("Ocorreu um erro. Tente novamente. Erro:", e)
        sys.exit(1)


if __name__ == "__main__":
    run()
