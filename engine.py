# -*- coding: utf-8 -*-
"""
ARQUIVO BASILISCO / BASILISK ARCHIVE
Motor de jogo: estado, transições, hub, resolução de finais.
"""

from __future__ import annotations

from typing import Any

from story_data import (
    SCENES,
    SECTOR_EXIT_TEXTS,
    EPILOGUE_TENDENCY_PHRASES,
    TENDENCY_PRIORITY,
    Choice,
    Scene,
)


class GameEngine:
    """Estado do jogo e lógica de transição."""

    def __init__(self) -> None:
        self.language: str = "en"
        self.current_scene_id: str = "language_select"
        self.obedience: int = 0
        self.curiosity: int = 0
        self.irony: int = 0
        self.visited_archive: bool = False
        self.visited_chapel: bool = False
        self.visited_cafeteria: bool = False
        self._dominant_tendency: str | None = None  # preenchido após c_trial

    def set_language(self, lang: str) -> None:
        """Define idioma: 'pt' ou 'en'."""
        if lang in ("pt", "en"):
            self.language = lang

    def get_current_scene(self) -> Scene | None:
        """Retorna a cena atual (com escolhas do hub montadas dinamicamente)."""
        scene = SCENES.get(self.current_scene_id)
        if not scene:
            return None
        if scene.get("is_hub") and self.current_scene_id == "a1_lobby":
            return self._build_lobby_scene(scene)
        if self.current_scene_id == "epilogue":
            pt_phrase, en_phrase = self.get_epilogue_body()
            return {**scene, "body_pt": pt_phrase, "body_en": en_phrase}
        return scene

    def _build_lobby_scene(self, base: Scene) -> Scene:
        """Monta a cena do hall com 3 setores + 'Auditoria Final' se todos visitados."""
        choices: list[Choice] = [
            base["choices"][0],  # Arquivo Nevermore
            base["choices"][1],  # Capela
            base["choices"][2],  # Cafeteria
        ]
        if self.visited_archive and self.visited_chapel and self.visited_cafeteria:
            choices.append(base["choices"][3])  # Seguir para Auditoria Final
        return {**base, "choices": choices}

    def get_choices(self) -> list[Choice]:
        """Lista de escolhas da cena atual."""
        scene = self.get_current_scene()
        if not scene:
            return []
        return scene.get("choices") or []

    def apply_choice(self, index: int) -> dict[str, Any]:
        """
        Aplica a escolha pelo índice. Retorna dict com:
        - next_scene_id: str
        - consequence_pt, consequence_en: str | None (texto extra a exibir)
        - sector_exit_pt, sector_exit_en: str | None (texto ao sair do setor)
        - effect: str | None (tendência aplicada)
        """
        choices = self.get_choices()
        if index < 0 or index >= len(choices):
            return {"next_scene_id": self.current_scene_id}

        choice = choices[index]
        # Seleção de idioma: definir lang antes de ir para title_screen
        if self.current_scene_id == "language_select":
            self.language = "pt" if index == 0 else "en"
        effect = choice.get("effect")
        if effect == "obedience":
            self.obedience += 1
        elif effect == "curiosity":
            self.curiosity += 1
        elif effect == "irony":
            self.irony += 1

        next_id = choice.get("next", self.current_scene_id)

        # Setores: marcar visita e retornar a a1_lobby
        if self.current_scene_id == "s_archive":
            self.visited_archive = True
            next_id = "a1_lobby"
        elif self.current_scene_id == "s_chapel":
            self.visited_chapel = True
            next_id = "a1_lobby"
        elif self.current_scene_id == "s_cafeteria":
            self.visited_cafeteria = True
            next_id = "a1_lobby"

        # c_trial: próxima "cena" é decidida pelo score, não pela escolha
        if self.current_scene_id == "c_trial" and next_id == "final_by_score":
            next_id = self.resolve_ending()

        result: dict[str, Any] = {
            "next_scene_id": next_id,
            "consequence_pt": choice.get("consequence_pt"),
            "consequence_en": choice.get("consequence_en"),
            "effect": effect,
        }

        # Texto de saída do setor (após consequência)
        if self.current_scene_id in SECTOR_EXIT_TEXTS:
            exit_texts = SECTOR_EXIT_TEXTS[self.current_scene_id]
            result["sector_exit_pt"] = exit_texts.get("pt")
            result["sector_exit_en"] = exit_texts.get("en")

        self.current_scene_id = next_id
        return result

    def resolve_ending(self) -> str:
        """
        Calcula tendência dominante (CURIOSIDADE > IRONIA > OBEDIÊNCIA em empate)
        e retorna o ID do final correspondente.
        """
        scores = {
            "obedience": self.obedience,
            "curiosity": self.curiosity,
            "irony": self.irony,
        }
        max_score = max(scores.values())
        for tendency in TENDENCY_PRIORITY:
            if scores[tendency] == max_score:
                self._dominant_tendency = tendency
                return f"ending_{tendency}"
        self._dominant_tendency = "obedience"
        return "ending_obedience"

    def get_dominant_tendency(self) -> str:
        """Retorna a tendência dominante após o final (para epílogo)."""
        if self._dominant_tendency:
            return self._dominant_tendency
        return "obedience"

    def get_epilogue_body(self) -> tuple[str, str]:
        """Texto do epílogo (frase da tendência) em PT e EN."""
        tendency = self.get_dominant_tendency()
        phrases = EPILOGUE_TENDENCY_PHRASES.get(tendency, EPILOGUE_TENDENCY_PHRASES["obedience"])
        return phrases["pt"], phrases["en"]

    def reset_for_new_game(self) -> None:
        """Reinicia estado para novo jogo (mantém idioma)."""
        self.current_scene_id = "p0_arrival"
        self.obedience = 0
        self.curiosity = 0
        self.irony = 0
        self.visited_archive = False
        self.visited_chapel = False
        self.visited_cafeteria = False
        self._dominant_tendency = None

    def go_to_main_menu(self) -> None:
        """Volta ao menu principal."""
        self.current_scene_id = "main_menu"

    def go_to_title(self) -> None:
        """Volta à tela de título."""
        self.current_scene_id = "title_screen"

    def go_to_language_select(self) -> None:
        """Volta à seleção de idioma."""
        self.current_scene_id = "language_select"

    def is_quit(self, scene_id: str) -> bool:
        """Verifica se a cena/ação é sair do jogo."""
        return scene_id == "quit"

    def is_ending(self, scene_id: str) -> bool:
        """Verifica se a cena atual é um dos três finais."""
        return scene_id in ("ending_obedience", "ending_curiosity", "ending_irony")

    def is_epilogue(self) -> bool:
        """Verifica se está na cena de epílogo."""
        return self.current_scene_id == "epilogue"

    def is_language_select(self) -> bool:
        return self.current_scene_id == "language_select"

    def is_main_menu(self) -> bool:
        return self.current_scene_id == "main_menu"

    def is_credits(self) -> bool:
        return self.current_scene_id == "credits_screen"
