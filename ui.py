# -*- coding: utf-8 -*-
"""
ARQUIVO BASILISCO / BASILISK ARCHIVE
Interface: Rich para renderização, prompt_toolkit para menus (setas, Enter, Esc).
"""

from __future__ import annotations

import os
import sys
from typing import Any

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout import Layout, FormattedTextControl
from prompt_toolkit.layout.containers import Window
from rich.console import Console
from rich.panel import Panel

from engine import GameEngine
from story_data import SCENES

# Rodapé fixo
FOOTER_PT = "Setas navegar  -  Enter confirmar  -  Esc voltar"
FOOTER_EN = "Arrow keys navigate  -  Enter confirm  -  Esc back"

# Beep: desativar se ROKO_SOUND=0 ou --no-sound
def _sound_enabled() -> bool:
    if os.environ.get("ROKO_SOUND", "").strip() == "0":
        return False
    if "--no-sound" in sys.argv:
        return False
    return True


def play_selection_beep() -> None:
    """Beep curto ao confirmar seleção (retro). Windows: winsound; Linux: \\a."""
    if not _sound_enabled():
        return
    try:
        if sys.platform == "win32":
            import winsound
            winsound.Beep(900, 30)
        else:
            print("\a", end="", flush=True)
    except Exception:
        pass


def _get_console() -> Console:
    """Console Rich com suporte a cores (degradado se não houver)."""
    return Console(force_terminal=True, no_color=os.environ.get("NO_COLOR"))


def render_scene(engine: GameEngine, selected_index: int = 0) -> list[str]:
    """
    Gera as linhas da cena atual (título, corpo, escolhas) para exibição.
    Retorna lista de strings já formatadas para o painel.
    """
    scene = engine.get_current_scene()
    if not scene:
        return []
    lang = engine.language
    title_key = "title_pt" if lang == "pt" else "title_en"
    body_key = "body_pt" if lang == "pt" else "body_en"
    title = scene.get(title_key) or ""
    body = scene.get(body_key) or ""
    choices = scene.get("choices") or []
    lines: list[str] = []
    if title:
        lines.append(title)
        lines.append("")
    if body:
        lines.append(body)
        lines.append("")
    for i, c in enumerate(choices):
        text_key = "text_pt" if lang == "pt" else "text_en"
        choice_text = c.get(text_key) or ""
        prefix = "  > " if i == selected_index else "    "
        lines.append(f"{prefix}{choice_text}")
    return lines


def render_scene_rich(engine: GameEngine, selected_index: int = 0) -> str:
    """Retorna uma única string com a cena formatada (para uso em FormattedTextControl)."""
    scene = engine.get_current_scene()
    if not scene:
        return ""
    lang = engine.language
    title_key = "title_pt" if lang == "pt" else "title_en"
    body_key = "body_pt" if lang == "pt" else "body_en"
    title = scene.get(title_key) or ""
    body = scene.get(body_key) or ""
    choices = scene.get("choices") or []
    parts: list[str] = []
    if title:
        parts.append(title)
        parts.append("\n\n")
    if body:
        parts.append(body)
        parts.append("\n\n")
    for i, c in enumerate(choices):
        text_key = "text_pt" if lang == "pt" else "text_en"
        choice_text = c.get(text_key) or ""
        prefix = "  > " if i == selected_index else "    "
        parts.append(f"{prefix}{choice_text}\n")
    return "".join(parts)


def _language_select_prompt(engine: GameEngine) -> str:
    """Texto da tela de seleção de idioma (sempre em inglês na tela inicial)."""
    scene = SCENES.get("language_select")
    if not scene:
        return "Choose the language of collapse.\n\n    Português\n    English"
    # Tela inicial em inglês
    prompt = scene.get("prompt_en") or "Choose the language of collapse."
    choices = scene.get("choices") or []
    lines = [prompt, "\n\n"]
    for c in choices:
        lines.append(f"    {c.get('text_en', c.get('text_pt', ''))}\n")
    return "".join(lines)


def _footer(engine: GameEngine) -> str:
    return FOOTER_PT if engine.language == "pt" else FOOTER_EN


def run_choice_menu(engine: GameEngine) -> tuple[int | None, bool]:
    """
    Exibe a cena atual e roda o menu de escolhas (setas, Enter, Esc).
    Retorna (índice selecionado, escaped).
    Se Esc foi pressionado, retorna (None, True).
    Caso contrário (Enter em uma opção), retorna (index, False).
    """
    return run_choice_menu_loop(engine)


def _read_single_key() -> str:
    """Lê uma única tecla (up, down, enter, escape) usando prompt_toolkit."""
    try:
        from prompt_toolkit import Application
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.key_binding.key_processor import KeyPressEvent
        from prompt_toolkit.layout import Layout, FormattedTextControl
        result: list[str] = [""]
        kb = KeyBindings()
        @kb.add("up")
        def _up(event: KeyPressEvent) -> None:
            result[0] = "up"
            event.app.exit()
        @kb.add("down")
        def _down(event: KeyPressEvent) -> None:
            result[0] = "down"
            event.app.exit()
        @kb.add("enter")
        def _enter(event: KeyPressEvent) -> None:
            result[0] = "enter"
            event.app.exit()
        @kb.add("escape")
        def _esc(event: KeyPressEvent) -> None:
            result[0] = "escape"
            event.app.exit()
        app = Application(
            layout=Layout(Window(FormattedTextControl(text=""))),
            key_bindings=kb,
        )
        app.run()
        return result[0] or ""
    except Exception:
        # Fallback quando não há console interativo (ex.: teste, redirecionamento)
        try:
            line = input().strip().lower()
            if line in ("", "e", "enter"):
                return "enter"
            if line in ("q", "esc"):
                return "escape"
            if line in ("w", "k", "up"):
                return "up"
            if line in ("s", "j", "down"):
                return "down"
        except (EOFError, KeyboardInterrupt):
            return "escape"
        return "enter"


def run_choice_menu_loop(engine: GameEngine) -> tuple[int | None, bool]:
    """
    Loop: desenha cena com Rich (clear + print), lê uma tecla com prompt_toolkit,
    atualiza índice ou retorna.
    """
    choices = engine.get_choices()
    if not choices:
        return (None, True)
    selected_index = [0]  # mutável
    console = _get_console()
    footer = _footer(engine)

    while True:
        console.clear()
        scene = engine.get_current_scene()
        if not scene:
            return (None, True)
        lang = engine.language
        # Tela de idioma: prompt em inglês (tela inicial), sem título
        if engine.is_language_select():
            body = scene.get("prompt_en") or "Choose the language of collapse."
            if body:
                console.print(Panel(body, style="bold cyan", border_style="cyan"))
            console.print()
        else:
            title_key = "title_pt" if lang == "pt" else "title_en"
            body_key = "body_pt" if lang == "pt" else "body_en"
            title = scene.get(title_key) or ""
            body = scene.get(body_key) or ""
            if title:
                console.print(Panel(title, style="bold cyan", border_style="cyan"))
            if body:
                console.print()
                console.print(body, style="white", overflow="fold")
            console.print()
        for i, c in enumerate(choices):
            if engine.is_language_select():
                t = c.get("text_en") or c.get("text_pt") or ""
            else:
                text_key = "text_pt" if lang == "pt" else "text_en"
                t = c.get(text_key) or ""
            if i == selected_index[0]:
                console.print(f"  [bold yellow]>[/] [bold yellow]{t}[/]")
            else:
                console.print(f"    {t}")
        console.print()
        console.print(f"[dim]{footer}[/]")

        key = _read_single_key()
        if key == "up":
            selected_index[0] = max(0, selected_index[0] - 1)
        elif key == "down":
            selected_index[0] = min(len(choices) - 1, selected_index[0] + 1)
        elif key == "enter":
            play_selection_beep()
            return (selected_index[0], False)
        elif key == "escape":
            return (None, True)


def print_consequence(engine: GameEngine, consequence_pt: str | None, consequence_en: str | None) -> None:
    """Exibe texto de consequência da escolha."""
    if not consequence_pt and not consequence_en:
        return
    console = _get_console()
    text = consequence_pt if engine.language == "pt" else consequence_en
    if text:
        console.print()
        console.print(Panel(text, style="italic", border_style="dim"))
        _wait_enter(engine)


def print_sector_exit(engine: GameEngine, sector_exit_pt: str | None, sector_exit_en: str | None) -> None:
    """Exibe texto de saída do setor."""
    if not sector_exit_pt and not sector_exit_en:
        return
    console = _get_console()
    text = sector_exit_pt if engine.language == "pt" else sector_exit_en
    if text:
        console.print()
        console.print(text, style="dim italic")
        _wait_enter(engine)


def _wait_enter(engine: GameEngine) -> None:
    """Aguarda Enter para continuar."""
    msg = "\n[Enter para continuar]" if engine.language == "pt" else "\n[Press Enter to continue]"
    try:
        input(msg)
    except (EOFError, KeyboardInterrupt):
        pass


def show_scene_and_wait_enter(engine: GameEngine) -> None:
    """Exibe a cena atual (título + corpo) e aguarda Enter. Usado para finais."""
    console = _get_console()
    console.clear()
    scene = engine.get_current_scene()
    if not scene:
        return
    lang = engine.language
    title_key = "title_pt" if lang == "pt" else "title_en"
    body_key = "body_pt" if lang == "pt" else "body_en"
    title = scene.get(title_key) or ""
    body = scene.get(body_key) or ""
    if title:
        console.print(Panel(title, style="bold cyan", border_style="cyan"))
    if body:
        console.print()
        console.print(body, style="white", overflow="fold")
    _wait_enter(engine)


def show_credits(engine: GameEngine) -> None:
    """Exibe tela de créditos."""
    console = _get_console()
    console.clear()
    scene = SCENES.get("credits_screen")
    if not scene:
        return
    lang = engine.language
    title = scene.get("title_pt" if lang == "pt" else "title_en") or "Credits"
    body = scene.get("body_pt" if lang == "pt" else "body_en") or ""
    console.print(Panel(title, style="bold cyan", border_style="cyan"))
    console.print()
    console.print(body)
    console.print()
    console.print(f"[dim]{_footer(engine)}[/]")
