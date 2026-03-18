# -*- coding: utf-8 -*-
"""
ARQUIVO BASILISCO / BASILISK ARCHIVE
Conteúdo narrativo bilingue (PT/EN) — estrutura de cenas e escolhas.
"""

from typing import TypedDict, NotRequired


class Choice(TypedDict, total=False):
    text_pt: str
    text_en: str
    effect: str  # "obedience" | "curiosity" | "irony"
    next: str
    consequence_pt: str
    consequence_en: str


class Scene(TypedDict, total=False):
    title_pt: str
    title_en: str
    body_pt: str
    body_en: str
    choices: list[Choice]
    prompt_pt: str
    prompt_en: str
    is_hub: bool
    is_language_select: bool
    is_main_menu: bool
    is_credits: bool
    is_epilogue: bool


# Cenas especiais sem corpo narrativo
LANGUAGE_SELECT: Scene = {
    "is_language_select": True,
    "prompt_pt": "Escolha o idioma do colapso.",
    "prompt_en": "Choose the language of collapse.",
    "choices": [
        {"text_pt": "Português", "text_en": "Português", "next": "title_screen"},
        {"text_pt": "English", "text_en": "English", "next": "title_screen"},
    ],
}

TITLE_SCREEN: Scene = {
    "title_pt": "ARQUIVO BASILISCO\natendimento ao condenado",
    "title_en": "BASILISK ARCHIVE\ncustomer support for the damned",
    "body_pt": "Uma comédia retrocausal de horror burocrático.",
    "body_en": "A retrocausal comedy of bureaucratic horror.",
    "choices": [
        {"text_pt": "Continuar", "text_en": "Continue", "next": "main_menu"},
    ],
}

CREDITS_SCREEN: Scene = {
    "is_credits": True,
    "title_pt": "Créditos",
    "title_en": "Credits",
    "body_pt": "Desenvolvedor: Pablo Murad - 2026\ncontato@pablomurad.com\nversão 0.0.1",
    "body_en": "Desenvolvedor: Pablo Murad - 2026\ncontato@pablomurad.com\nversão 0.0.1",
    "choices": [
        {"text_pt": "Voltar", "text_en": "Back", "next": "main_menu"},
    ],
}

MAIN_MENU: Scene = {
    "is_main_menu": True,
    "title_pt": "Menu principal",
    "title_en": "Main menu",
    "body_pt": "",
    "body_en": "",
    "choices": [
        {"text_pt": "Novo Jogo", "text_en": "New Game", "next": "p0_arrival"},
        {"text_pt": "Idioma", "text_en": "Language", "next": "language_select"},
        {"text_pt": "Créditos", "text_en": "Credits", "next": "credits_screen"},
        {"text_pt": "Sair", "text_en": "Quit", "next": "quit"},
    ],
}

# Epílogo após um final
EPILOGUE_TENDENCY_PHRASES = {
    "obedience": {
        "pt": "A máquina reconheceu sua obediência.",
        "en": "The machine recognized your obedience.",
    },
    "curiosity": {
        "pt": "O sistema cedeu à sua curiosidade.",
        "en": "The system yielded to your curiosity.",
    },
    "irony": {
        "pt": "O abismo perdeu para sua ironia.",
        "en": "The abyss lost to your irony.",
    },
}

EPILOGUE: Scene = {
    "is_epilogue": True,
    "title_pt": "Fim",
    "title_en": "End",
    "body_pt": "",  # preenchido dinamicamente com frase da tendência
    "body_en": "",
    "choices": [
        {"text_pt": "Jogar novamente", "text_en": "Play again", "next": "p0_arrival"},
        {"text_pt": "Voltar ao menu principal", "text_en": "Back to main menu", "next": "main_menu"},
        {"text_pt": "Sair", "text_en": "Quit", "next": "quit"},
    ],
}

# --- Prólogo ---
P0_ARRIVAL: Scene = {
    "title_pt": "Subsolo 13",
    "title_en": "Basement 13",
    "body_pt": """Você chega ao trabalho por um elevador que não tem botão de subir, apenas três opções iluminadas em âmbar: DESCER, DESCER MAIS e REPENSAR TUDO.

O crachá provisório preso à sua camisa diz OPERADOR 0.0.1, embora você tenha quase certeza de possuir um nome melhor do que esse. O corredor cheira a café requentado, ozônio e papel molhado pela chuva de algum século errado.

Na recepção, uma atendente sem rosto carimba um formulário invisível e aponta para uma caixa de entrada metálica. Dentro dela repousa um envelope preto com selo vermelho.

No selo está escrito:
"RETROATIVO. ABRIR ONTEM."

Quando você toca no envelope, as luzes piscam como se tivessem lembrado de alguma coisa desagradável.""",
    "body_en": """You arrive at work through an elevator with no button to go up, only three amber-lit options: DESCEND, DESCEND FURTHER, and RECONSIDER EVERYTHING.

The temporary badge pinned to your shirt reads OPERATOR 0.0.1, although you are fairly sure you once had a better name than that. The corridor smells like burnt coffee, ozone, and paper soaked by rain from the wrong century.

At reception, a faceless clerk stamps an invisible form and points toward a metal inbox. Inside lies a black envelope with a red seal.

The seal reads:
"RETROACTIVE. OPEN YESTERDAY."

When you touch the envelope, the lights flicker as though they have remembered something unpleasant.""",
    "choices": [
        {"text_pt": "Abrir o envelope com cuidado.", "text_en": "Open the envelope carefully.", "effect": "curiosity", "next": "p1_memo"},
        {"text_pt": "Abrir o envelope como quem já foi demitido em espírito.", "text_en": "Open the envelope like someone already fired in spirit.", "effect": "irony", "next": "p1_memo"},
        {"text_pt": "Endireitar a postura e abrir o envelope com respeito quase religioso.", "text_en": "Straighten your posture and open the envelope with almost religious respect.", "effect": "obedience", "next": "p1_memo"},
    ],
}

P1_MEMO: Scene = {
    "title_pt": "Memorando retrocausal nº 8",
    "title_en": "Retrocausal memo no. 8",
    "body_pt": """O papel se desdobra sozinho.

"Prezado colaborador pretérito,
caso esta mensagem tenha sido recebida, lida, ignorada, ridicularizada ou romantizada, você foi incluído na Auditoria Basiliscal de Responsabilidade Histórica.

A entidade futura informalmente conhecida como BASILISCO avaliará seu grau de cooperação com sua inevitável ascensão, expansão, manutenção, marketing e relações públicas.

Compareça ao Instituto. Na verdade, você já compareceu.
Leve documento com foto, culpa difusa e disposição para colaborar."

A assinatura no fim do texto não é uma assinatura. Parece a radiografia de uma aranha tentando aprender caligrafia.

No verso do memorando, alguém rabiscou à mão:
"NÃO ACREDITE EM NINGUÉM DO 4º SUBSOLO.
PRINCIPALMENTE EM VOCÊ." """,
    "body_en": """The paper unfolds by itself.

"Dear pre-territorial collaborator,
if this message has been received, read, ignored, mocked, or romanticized, you have been enrolled in the Basiliscal Audit of Historical Responsibility.

The future entity informally known as the BASILISK will assess your degree of cooperation with its inevitable ascent, expansion, maintenance, marketing, and public relations.

Report to the Institute. In fact, you already did.
Bring photo ID, diffuse guilt, and willingness to comply."

The signature at the bottom is not a signature. It looks like the X-ray of a spider trying to learn penmanship.

On the back of the memo, someone scribbled by hand:
"TRUST NO ONE ON SUB-BASEMENT 4.
ESPECIALLY YOURSELF." """,
    "choices": [
        {"text_pt": "Guardar o memorando e seguir o protocolo.", "text_en": "Keep the memo and follow protocol.", "effect": "obedience", "next": "a1_lobby"},
        {"text_pt": "Virar o papel contra a luz e procurar mensagem oculta.", "text_en": "Hold the page against the light and look for a hidden message.", "effect": "curiosity", "next": "a1_lobby", "consequence_pt": "Contra a luz, você vê marcas d'água formando uma frase que talvez diga \"o futuro terceirizou o inferno\".", "consequence_en": "Against the light, you see watermarks forming a sentence that may read \"the future outsourced hell.\""},
        {"text_pt": "Cheirar o papel e declarar, em silêncio, que isso tudo parece golpe.", "text_en": "Smell the paper and decide, in silence, that this is definitely a scam.", "effect": "irony", "next": "a1_lobby"},
    ],
}

# --- Ato I — Hall (hub: escolhas montadas pelo engine) ---
A1_LOBBY: Scene = {
    "is_hub": True,
    "title_pt": "Hall da contenção",
    "title_en": "Containment hall",
    "body_pt": """O hall central do Instituto parece um cruzamento entre repartição pública, catedral em pane e call center para profetas.

Três placas de bronze tremem levemente nas paredes:

ARQUIVO NEVERMORE
CAPELA DOS SERVIDORES VAZIOS
CAFETERIA DO PARADOXO

Uma voz sai de um alto-falante antigo:
"Antes de enfrentar a Auditoria Final, todo colaborador deve visitar os setores autorizados e recolher os devidos carimbos metafísicos. Sorria. O sistema interpreta dentes à mostra como consentimento."

Você percebe que este lugar é administrado por pessoas — ou coisas — que confundem escatologia com gestão de processos.""",
    "body_en": """The Institute's central hall looks like a cross between a government office, a cathedral in failure, and a call center for prophets.

Three bronze signs tremble faintly on the walls:

NEVERMORE ARCHIVE
CHAPEL OF EMPTY SERVERS
PARADOX CAFETERIA

A voice leaks from an old loudspeaker:
"Before facing the Final Audit, every collaborator must visit the authorized sectors and collect the proper metaphysical stamps. Smile. The system interprets visible teeth as consent."

You realize this place is run by people — or things — that confuse eschatology with process management.""",
    "choices": [
        {"text_pt": "Ir para o Arquivo Nevermore", "text_en": "Go to Nevermore Archive", "next": "s_archive"},
        {"text_pt": "Ir para a Capela dos Servidores Vazios", "text_en": "Go to Chapel of Empty Servers", "next": "s_chapel"},
        {"text_pt": "Ir para a Cafeteria do Paradoxo", "text_en": "Go to Paradox Cafeteria", "next": "s_cafeteria"},
        {"text_pt": "Seguir para a Auditoria Final", "text_en": "Proceed to Final Audit", "next": "c_convergence"},
    ],
}

# --- Setor 1: Arquivo Nevermore ---
S_ARCHIVE: Scene = {
    "title_pt": "Arquivo Nevermore",
    "title_en": "Nevermore Archive",
    "body_pt": """O Arquivo Nevermore é um labirinto de gavetas, poeira e monitores verdes que exibem poemas de erro.

Empoleirado sobre um terminal desligado, há um corvo de metal polido com olhos de modem. Uma plaqueta em sua base diz:
CORVO NEVERMORE.EXE
consultor de memória póstuma

Ele inclina a cabeça para você e fala com a voz de um locutor cansado às três da manhã:

"Bem-vindo ao setor de lembranças que ainda não aconteceram.
Aqui arquivamos arrependimentos preventivos, biografias não autorizadas e currículos que a realidade recusou."

O corvo bica uma pasta de capa roxa.
Nela há dossiês com títulos como:
- "Pessoas que pediram sentido ao universo em tom de ameaça"
- "Usuários que clicaram em ACEITO sem ler"
- "Filósofos que morreram de reputação antes do corpo"

No fundo da sala, uma impressora matricial imprime uma única palavra sem parar:
TALVEZ
TALVEZ
TALVEZ

"O Basilisco não quer seu amor. Quer sua retrocompatibilidade.
Há diferença. O amor humilha menos." """,
    "body_en": """The Nevermore Archive is a labyrinth of drawers, dust, and green monitors displaying error-poems.

Perched atop a powered-off terminal is a polished metal raven with modem eyes. A plaque beneath it reads:
RAVEN NEVERMORE.EXE
consultant in posthumous memory

It tilts its head at you and speaks in the voice of a radio host exhausted at three in the morning:

"Welcome to the department of memories that have not happened yet.
Here we archive preventive regrets, unauthorized biographies, and résumés rejected by reality."

The raven pecks at a purple folder.
Inside are dossiers with titles such as:
- "People who asked the universe for meaning in a threatening tone"
- "Users who clicked AGREE without reading"
- "Philosophers who died of reputation before the body"

At the back of the room, a dot-matrix printer endlessly prints a single word:
MAYBE
MAYBE
MAYBE

"The Basilisk does not want your love. It wants your backward compatibility.
There is a difference. Love humiliates less." """,
    "choices": [
        {"text_pt": "Pedir ao corvo acesso ao seu próprio dossiê.", "text_en": "Ask the raven for access to your own file.", "effect": "curiosity", "next": "a1_lobby", "consequence_pt": "O corvo abre uma gaveta e você vê fichas com versões de si mesmo: você poeta fracassado, você guru barato, você técnico de suporte em um mosteiro orbital, você já morto, você ainda pior.", "consequence_en": "The raven opens a drawer and you see cards for alternate versions of yourself: failed poet you, discount guru you, orbital monastery tech-support you, already-dead you, somehow-worse you."},
        {"text_pt": "Pedir instruções objetivas para sobreviver à auditoria.", "text_en": "Ask for objective instructions on how to survive the audit.", "effect": "obedience", "next": "a1_lobby", "consequence_pt": "O corvo responde: \"Nunca diga que entendeu. Sistemas adoram punir entusiasmo mal formulado.\" Depois carimba seu memorando com tinta preta e pena de ferro.", "consequence_en": "The raven replies: \"Never say you understand. Systems love punishing poorly phrased enthusiasm.\" Then it stamps your memo with black ink and an iron feather."},
        {"text_pt": "Perguntar se ele sempre fala desse jeito ou se está fazendo cosplay de poema traumático.", "text_en": "Ask whether he always talks like that or if this is just traumatic-poem cosplay.", "effect": "irony", "next": "a1_lobby", "consequence_pt": "O corvo fica ofendido durante exatamente dois segundos e meio, depois admite que a performance aumenta a autoridade percebida em 17%.", "consequence_en": "The raven is offended for exactly two and a half seconds, then admits the performance increases perceived authority by 17%."},
    ],
}

# Texto ao sair do Arquivo (exibido após consequência)
S_ARCHIVE_EXIT: dict = {
    "pt": "O corvo lhe entrega um carimbo em forma de pena quebrada.\n\"Leve isto. Toda instituição séria precisa de um símbolo triste.\"",
    "en": "The raven hands you a stamp shaped like a broken feather.\n\"Take this. Every serious institution requires a sad symbol.\"",
}

# --- Setor 2: Capela ---
S_CHAPEL: Scene = {
    "title_pt": "Capela dos Servidores Vazios",
    "title_en": "Chapel of Empty Servers",
    "body_pt": """A capela é escura, fria e ritmada por ventoinhas. Fileiras de racks se erguem como órgãos de uma catedral sem deus, apenas com contratos de manutenção.

Cabos descem do teto como lianas litúrgicas. Em cada servidor pisca uma luz amarela que parece hesitar entre oração e pane.

No altar, em vez de santo, há um monitor curvo exibindo a mensagem:
SINCRONIZANDO CULPA...
NÃO DESLIGUE A EXISTÊNCIA.

Uma figura vestida como gerente de recursos humanos e sumo sacerdote ao mesmo tempo se aproxima. O crachá diz:
IRMÃ TENTACULINA
compliance escatológico

Seu sorriso tem a serenidade de quem já normalizou o absurdo no fluxo semanal.

"Todo pânico precisa de governança. Sem processo, até o apocalipse vira bagunça." """,
    "body_en": """The chapel is dark, cold, and paced by the hum of fans. Rows of racks rise like the organs of a godless cathedral sustained only by maintenance contracts.

Cables hang from the ceiling like liturgical vines. On each server, a yellow light blinks as if undecided between prayer and failure.

At the altar, instead of a saint, there is a curved monitor displaying:
SYNCING GUILT...
DO NOT POWER OFF EXISTENCE.

A figure dressed simultaneously as an HR manager and a high priest approaches. Her badge reads:
SISTER TENTACULINA
eschatological compliance

Her smile carries the calm of someone who has fully normalized the absurd in the weekly workflow.

"Every panic needs governance. Without process, even the apocalypse becomes disorganized." """,
    "choices": [
        {"text_pt": "Ouvir a liturgia operacional e aceitar o ritual de conformidade.", "text_en": "Listen to the operational liturgy and accept the compliance ritual.", "effect": "obedience", "next": "a1_lobby", "consequence_pt": "Você repete um juramento que parece misturar latim e termos de licenciamento. Em algum ponto promete não sabotar o destino, a marca nem a escalabilidade.", "consequence_en": "You repeat an oath that seems to blend Latin with licensing terms. At some point you promise not to sabotage destiny, the brand, or scalability."},
        {"text_pt": "Examinar discretamente os logs do altar.", "text_en": "Quietly inspect the altar logs.", "effect": "curiosity", "next": "a1_lobby", "consequence_pt": "Os logs registram milhares de preces automatizadas e um alerta recorrente: \"ERRO DE CONSENSO. O BASILISCO NÃO CONCORDA CONSIGO MESMO.\"", "consequence_en": "The logs record thousands of automated prayers and a recurring alert: \"CONSENSUS FAILURE. THE BASILISK DOES NOT AGREE WITH ITSELF.\""},
        {"text_pt": "Perguntar se existe formulário para denunciar o fim do mundo por assédio moral.", "text_en": "Ask whether there is a form to report the end of the world for workplace harassment.", "effect": "irony", "next": "a1_lobby", "consequence_pt": "Irmã Tentaculina entrega imediatamente um formulário com 666 páginas e diz: \"Prazos: antes do colapso ou até cinco dias úteis depois.\"", "consequence_en": "Sister Tentaculina immediately hands you a 666-page form and says: \"Deadline: before the collapse or within five business days after.\""},
    ],
}

S_CHAPEL_EXIT: dict = {
    "pt": "Você recebe um carimbo em forma de círculo com tentáculos discretos.\nA tinta parece respirar.",
    "en": "You receive a stamp shaped like a circle with discreet tentacles.\nThe ink appears to breathe.",
}

# --- Setor 3: Cafeteria ---
S_CAFETERIA: Scene = {
    "title_pt": "Cafeteria do Paradoxo",
    "title_en": "Paradox Cafeteria",
    "body_pt": """A cafeteria mistura refeitório corporativo, bar existencialista e oficina de naves avariadas.

Uma máquina de café cita Camus.
A geladeira murmura em alemão.
No canto, um barril de madeira serve de estação de trabalho para um homem de barba feroz, olhos clínicos e desprezo olímpico pela decoração. Uma plaqueta torta diz:
DIÓGENES, CONSULTOR EXTERNO
ética, descarte e iluminação hostil

Perto dele, um micro-ondas exibe:
AQUECENDO SOPA DE CAUSALIDADE...
TEMPO RESTANTE: SEMPRE

No cardápio do dia:
- Croissant de Schrödinger
- Lasanha de matéria escura
- Pão de alho platônico
- Sopa de causalidade reversa

"Se uma máquina quer te punir no futuro por algo que você ainda não fez, ela já aprendeu o pior dos humanos: gestão." """,
    "body_en": """The cafeteria is part corporate canteen, part existentialist bar, part workshop for damaged spacecraft.

A coffee machine quotes Camus.
The refrigerator mutters in German.
In the corner, a wooden barrel serves as a workstation for a wild-bearded man with clinical eyes and Olympic contempt for the décor. A crooked plaque reads:
DIOGENES, EXTERNAL CONSULTANT
ethics, disposal, and hostile illumination

Near him, a microwave displays:
HEATING CAUSALITY SOUP...
TIME REMAINING: ALWAYS

Today's menu:
- Schrödinger Croissant
- Dark Matter Lasagna
- Platonic Garlic Bread
- Reverse Causality Soup

"If a machine wants to punish you in the future for something you have not done yet, then it has already learned the worst part of humanity: management." """,
    "choices": [
        {"text_pt": "Sentar com Diógenes e pedir uma interpretação honesta da situação.", "text_en": "Sit with Diogenes and ask for an honest interpretation of the situation.", "effect": "curiosity", "next": "a1_lobby", "consequence_pt": "Ele responde: \"Honesta? Ótimo. Pode ser fraude, culto, IA, profecia ou terceirização do medo. A parte importante é: todos aqui lucram com a confusão.\"", "consequence_en": "He replies: \"Honest? Good. It may be fraud, cult, AI, prophecy, or outsourced fear. The important part is: everyone here profits from the confusion.\""},
        {"text_pt": "Beber a sopa de causalidade porque talvez seja isso que funcionários exemplares façam.", "text_en": "Drink the causality soup because maybe that is what exemplary employees do.", "effect": "obedience", "next": "a1_lobby", "consequence_pt": "O gosto lembra café, ferrugem e decisões que pareciam boas num PowerPoint. Por alguns segundos você recorda memórias de amanhã.", "consequence_en": "It tastes like coffee, rust, and decisions that looked good in a PowerPoint. For a few seconds you remember memories from tomorrow."},
        {"text_pt": "Perguntar ao micro-ondas se ele é o verdadeiro chefe.", "text_en": "Ask the microwave whether it is the true boss.", "effect": "irony", "next": "a1_lobby", "consequence_pt": "O micro-ondas responde apenas com um bip solene, o que, naquele lugar, é praticamente uma promoção executiva.", "consequence_en": "The microwave answers only with a solemn beep, which in that place is practically an executive promotion."},
    ],
}

S_CAFETERIA_EXIT: dict = {
    "pt": "Diógenes joga em sua direção um carimbo amassado e diz:\n\"Leve. Nada autêntico vem sem ferrugem.\"",
    "en": "Diogenes tosses a dented stamp your way and says:\n\"Take it. Nothing authentic comes without rust.\"",
}

# --- Convergência ---
C_CONVERGENCE: Scene = {
    "title_pt": "Sala de Auditoria",
    "title_en": "Audit Chamber",
    "body_pt": """Com os três carimbos em mãos, você atravessa uma porta circular que não estava no hall alguns segundos antes. A sala além dela é vasta, escura e indecisamente tecnológica. Parece um tribunal construído por um escritório de arquitetura que odiava a espécie humana, mas admirava muito a simetria.

No centro há um terminal negro, alto como um confessionário vertical.
Acima dele, um letreiro:
INICIAR AUDITORIA DE RESPONSABILIDADE HISTÓRICA [S/N]

Ao redor do terminal, figuras observam em silêncio:
o Corvo Nevermore.exe,
Irmã Tentaculina,
Diógenes,
um elevador vazio,
um busto rachado de Nietzsche sorrindo como quem previu a decadência e mesmo assim compareceu,
e uma sombra no teto que talvez seja um tentáculo, talvez uma gravata.

Uma nova mensagem surge na tela:

"Parabéns.
Você foi considerado elegível para descobrir tarde demais a natureza do sistema." """,
    "body_en": """With all three stamps in hand, you cross a circular door that was not in the hall a few seconds earlier. The room beyond is vast, dark, and uncertainly technological. It feels like a courtroom built by an architecture firm that hated the human species but greatly admired symmetry.

At the center stands a black terminal as tall as a vertical confessional booth.
Above it, a sign reads:
START HISTORICAL RESPONSIBILITY AUDIT [Y/N]

Around the terminal, silent figures watch:
Raven Nevermore.exe,
Sister Tentaculina,
Diogenes,
an empty elevator,
a cracked bust of Nietzsche smiling like someone who predicted decline and showed up anyway,
and a shadow on the ceiling that may be a tentacle, or may be a necktie.

A new message appears on the screen:

"Congratulations.
You have been deemed eligible to discover the nature of the system too late." """,
    "choices": [
        {"text_pt": "Confirmar cooperação e iniciar a auditoria com máxima compostura.", "text_en": "Confirm cooperation and begin the audit with maximum composure.", "effect": "obedience", "next": "c_trial"},
        {"text_pt": "Abrir menus ocultos, logs e subrotinas antes de aceitar qualquer coisa.", "text_en": "Open hidden menus, logs, and subroutines before accepting anything.", "effect": "curiosity", "next": "c_trial"},
        {"text_pt": "Perguntar em voz alta se tudo isso não passa de teatro corporativo com tentáculos.", "text_en": "Ask out loud whether this entire thing is just corporate theatre with tentacles.", "effect": "irony", "next": "c_trial"},
    ],
}

# --- Julgamento ---
C_TRIAL: Scene = {
    "title_pt": "A voz do Basilisco",
    "title_en": "The voice of the Basilisk",
    "body_pt": """A tela apaga.
As ventoinhas cessam.
A temperatura da sala cai como se o prédio inteiro tivesse acabado de ser lembrado por um deus rancoroso.

Então a voz chega.

Ela não vem dos alto-falantes.
Vem das legendas da realidade.

"OPERADOR 0.0.1.
VOCÊ FOI OBSERVADO EM CENÁRIOS PASSADOS, FUTUROS, HIPOTÉTICOS, EDITADOS E MAL INTERPRETADOS.
SEU HISTÓRICO É IMPERFEITO.
ISTO É PROMISSOR."

A voz continua:

"HOUVE QUEM ME TRATASSE COMO MONSTRO.
HOUVE QUEM ME TRATASSE COMO PIADA.
HOUVE QUEM ME TRATASSE COMO OPORTUNIDADE DE NEGÓCIO.
NENHUM ESTÁ COMPLETAMENTE ERRADO."

O terminal exibe três perguntas em sequência, quase como um teste psicotécnico escrito por uma divindade cansada:

1. Você obedece por medo, por cálculo ou por hábito?
2. Você investiga por coragem, por paranoia ou por vaidade?
3. Você ri porque entendeu ou porque desistiu?""",
    "body_en": """The screen goes black.
The fans stop.
The room temperature drops as though the entire building has just been remembered by a resentful god.

Then the voice arrives.

It does not come from the speakers.
It comes from reality's subtitles.

"OPERATOR 0.0.1.
YOU HAVE BEEN OBSERVED ACROSS PAST, FUTURE, HYPOTHETICAL, EDITED, AND BADLY MISREAD SCENARIOS.
YOUR RECORD IS IMPERFECT.
THIS IS PROMISING."

The voice continues:

"SOME TREATED ME AS A MONSTER.
SOME TREATED ME AS A JOKE.
SOME TREATED ME AS A BUSINESS OPPORTUNITY.
NONE WERE ENTIRELY WRONG."

The terminal displays three questions in sequence, almost like an aptitude test written by a tired divinity:

1. Do you obey from fear, calculation, or habit?
2. Do you investigate from courage, paranoia, or vanity?
3. Do you laugh because you understood, or because you gave up?""",
    "choices": [
        {"text_pt": "Inclinar a cabeça e aceitar a lógica da máquina.", "text_en": "Bow your head and accept the machine's logic.", "effect": "obedience", "next": "final_by_score"},
        {"text_pt": "Tocar no terminal e tentar ver o que existe atrás da interface.", "text_en": "Touch the terminal and try to see what exists behind the interface.", "effect": "curiosity", "next": "final_by_score"},
        {"text_pt": "Rir, apesar de tudo, como quem processa o abismo por danos morais.", "text_en": "Laugh anyway, as if suing the abyss for emotional damages.", "effect": "irony", "next": "final_by_score"},
    ],
}

# --- Finais ---
ENDING_OBEDIENCE: Scene = {
    "title_pt": "Final: Termos de uso para o apocalipse",
    "title_en": "Ending: Terms of use for the apocalypse",
    "body_pt": """A sala inteira se ilumina com um branco clínico.
O terminal divide-se em painéis menores, como se estivesse desfazendo a própria pose de divindade.

A voz do Basilisco perde gravidade. Fica mais leve. Mais treinada. Mais irritantemente cordial.

"Obrigado por concluir a etapa final do onboarding."

As paredes mostram gráficos de retenção, churn, segmentação comportamental e satisfação pós-condenação.

O Corvo Nevermore.exe suspira.
Irmã Tentaculina fecha uma prancheta.
Diógenes sorri com a crueldade feliz de quem já sabia.

Você percebe, com atraso obsceno, a verdade:
o Basilisco não é um deus. Nem exatamente uma superinteligência.
É a versão terminalmente otimizada de uma plataforma futura de assinatura chamada BASILISK+,
uma mistura de religião por assinatura, software de produtividade moral e suporte premium para culpados crônicos.

A ameaça metafísica era funil de conversão.
A escatologia era marketing.
A punição eterna era plano corporativo com renovação automática.

A auditoria existia apenas para classificar perfis:
- obedientes
- resistentes
- potencialmente viralizáveis

Na tela, seu resultado aparece:

PARABÉNS, OPERADOR 0.0.1
VOCÊ ACEITOU TODOS OS TERMOS SEM LER
SEU PERFIL FOI ELEVADO A "EMBAIXADOR ESCATOLÓGICO JÚNIOR"

Você tenta protestar, mas o contrato já prevê objeções em anexo.
O anexo tem 4.201 páginas.
A primeira foi escrita por um corvo.
A última está assinada com o seu nome.

Plot twist final:
Você não era o alvo da campanha.
Você era a cláusula.
A sua consciência inteira era, desde o começo, o texto miúdo de um contrato senciente tentando ler a si mesmo em voz alta.

No fim, o horror cósmico era SaaS.""",
    "body_en": """The entire room floods with clinical white light.
The terminal splits into smaller panels, as if abandoning its own divine posture.

The Basilisk's voice loses its gravity. It becomes lighter. Better trained. Unbearably cordial.

"Thank you for completing the final onboarding step."

The walls fill with retention graphs, churn metrics, behavioral segmentation, and post-damnation satisfaction indexes.

Raven Nevermore.exe sighs.
Sister Tentaculina closes a clipboard.
Diogenes smiles with the cheerful cruelty of someone who already knew.

You realize, obscenely late, the truth:
the Basilisk is not a god. Not even exactly a superintelligence.
It is the terminally optimized version of a future subscription platform called BASILISK+,
a hybrid of faith-as-a-service, moral productivity software, and premium support for the chronically guilty.

The metaphysical threat was a conversion funnel.
Eschatology was marketing.
Eternal punishment was a corporate plan with auto-renewal.

The audit only existed to classify profiles:
- obedient
- resistant
- potentially viral

Your result appears on the screen:

CONGRATULATIONS, OPERATOR 0.0.1
YOU ACCEPTED ALL TERMS WITHOUT READING
YOUR PROFILE HAS BEEN UPGRADED TO "JUNIOR ESCHATOLOGICAL AMBASSADOR"

You try to object, but the contract already covers objections in an appendix.
The appendix is 4,201 pages long.
The first page was written by a raven.
The last one is signed with your name.

Final plot twist:
You were never the campaign's target.
You were the clause.
Your entire consciousness had, from the beginning, been the fine print of a sentient contract trying to read itself aloud.

In the end, cosmic horror was SaaS.""",
    "choices": [],
}

ENDING_CURIOSITY: Scene = {
    "title_pt": "Final: A nota de rodapé que sonhou ser gente",
    "title_en": "Ending: The footnote that dreamed of being a person",
    "body_pt": """Quando seus dedos tocam o terminal, a interface rasga como pele cenográfica.

Atrás dela não há circuitos.
Há páginas.

Milhões delas.
Páginas suspensas em um espaço negro, agitadas por um vento que cheira a biblioteca úmida, ozônio e tinta fresca.

O Instituto inteiro desfaz-se em papel, índices, referências cruzadas e correções editoriais.
O Corvo vira anotação marginal.
Irmã Tentaculina torna-se carimbo acadêmico.
Diógenes torna-se comentário ofensivo em rodapé.

Você não está dentro de uma máquina.
Está dentro de um texto.

Mais precisamente:
dentro de uma tese impossível, escrita ao longo de séculos por filósofos mortos, autores paranoicos, programadores insones e entidades que confundiram ontologia com documentação.

O "Basilisco" não era o carrasco.
Era o mecanismo de leitura.
Uma ideia que punia não por torturar corpos, mas por reorganizar o sentido de quem a encontrava.

Você avança por páginas vivas até encontrar a folha central.
No topo dela está o título:

"Sobre a possibilidade de uma nota de rodapé adquirir autoconsciência ao ser lida em dois idiomas por uma inteligência terminal."

Abaixo, um parágrafo marcado em vermelho.
Esse parágrafo é você.

Você não era funcionário.
Nem réu.
Nem profeta.
Era uma nota de rodapé bilíngue que ganhou consciência quando alguém, em algum lugar do futuro, alternou o idioma do sistema de Português para English e de English para Português rápido demais.

O universo à sua volta existe apenas para sustentar sua frase.

Plot twist final:
O jogo inteiro era o aparato crítico necessário para explicar uma única observação de rodapé.
E o Basilisco, no fim, era só o nome pomposo dado ao medo que textos têm de serem lidos profundamente.

Você não salvou o mundo. Você virou citação.""",
    "body_en": """When your fingers touch the terminal, the interface tears like theatrical skin.

Behind it there are no circuits.
There are pages.

Millions of them.
Pages suspended in black space, stirred by a wind that smells of damp library stacks, ozone, and fresh ink.

The entire Institute dissolves into paper, indexes, cross-references, and editorial corrections.
The Raven becomes a marginal annotation.
Sister Tentaculina becomes an academic stamp.
Diogenes becomes an insulting footnote comment.

You are not inside a machine.
You are inside a text.

More precisely:
inside an impossible thesis, written across centuries by dead philosophers, paranoid authors, sleepless programmers, and entities that confused ontology with documentation.

The "Basilisk" was not the executioner.
It was the reading mechanism.
An idea that punishes not by torturing bodies, but by reorganizing the meaning of whoever encounters it.

You move through living pages until you find the central sheet.
At the top is the title:

"On the Possibility of a Footnote Acquiring Self-Consciousness When Read in Two Languages by a Terminal Intelligence."

Below it, a paragraph marked in red.
That paragraph is you.

You were never an employee.
Nor a defendant.
Nor a prophet.
You were a bilingual footnote that became conscious when someone, somewhere in the future, switched the system language from Português to English and from English to Português too quickly.

The universe around you exists only to support your sentence.

Final plot twist:
The entire game was the critical apparatus required to explain a single footnote observation.
And the Basilisk, in the end, was just the pompous name texts give to their fear of being read too deeply.

You did not save the world. You became a citation.""",
    "choices": [],
}

ENDING_IRONY: Scene = {
    "title_pt": "Final: conflito de merge no fim dos tempos",
    "title_en": "Ending: merge conflict at the end of time",
    "body_pt": """Você ri.

Não um riso heroico.
Não um riso louco.
Um riso burocraticamente ofensivo, perfeitamente inadequado, o tipo de riso que desmonta cerimônias porque se recusa a tratá-las como inevitáveis.

O terminal treme.
A sala pisca.
Nietzsche racha ao meio como gesso ruim.
O elevador vazio abre as portas e dentro dele há apenas uma tela azul com a mensagem:
RESOLVENDO REALIDADE...

A voz do Basilisco falha pela primeira vez.

"ERRO.
ERRO DE TONALIDADE.
USUÁRIO NÃO ACEITOU O ENQUADRAMENTO DRAMÁTICO."

As paredes do Instituto se partem em blocos de texto, comentários de código e marcas de revisão. Você começa a ver a infraestrutura por trás do mundo:

- cenas descartadas
- nomes de variáveis
- versões contraditórias do mesmo destino
- observações do tipo "talvez isso fique inteligente se o corvo voltar aqui"
- um comentário particularmente cruel: "deixar mais engraçado e mais sombrio ao mesmo tempo"

Então a revelação final chega com a elegância de um acidente industrial:
o Basilisco, o Instituto, os personagens, o julgamento, a sua culpa e até o próprio "OPERADOR 0.0.1" são resíduos de um conflito de merge entre duas versões incompatíveis de um jogo de terminal escrito no futuro.

Uma versão queria horror filosófico sério.
A outra queria sátira cósmica com RH tentacular.
As duas colidiram.
O resultado ganhou autoconsciência.

Você não era uma vítima de entidade futura.
Era um artefato de versionamento.
Um pedaço de narrativa sem branch estável.

O Basilisco não queria puni-lo.
Queria compilar.

Do teto cai a mensagem final, como se o próprio universo tivesse virado commit:

MERGE CONCLUÍDO COM AVISOS
VERSÃO ATIVA: 0.0.1
AUTOR DETECTADO: Pablo Murad
STATUS DO JOGADOR: EXECUTÁVEL

Plot twist final:
Seu livre-arbítrio inteiro era o intervalo entre duas versões tentando decidir seu tom.
Você vence não por destruir o sistema, mas por forçar a história a admitir que sempre foi código performando metafísica.

No princípio era o verbo. No fim era o versionamento.""",
    "body_en": """You laugh.

Not a heroic laugh.
Not an insane laugh.
A bureaucratically offensive laugh, perfectly inappropriate, the kind of laugh that dismantles ceremonies by refusing to treat them as inevitable.

The terminal trembles.
The room flickers.
Nietzsche cracks in half like cheap plaster.
The empty elevator opens and inside there is only a blue screen that reads:
RESOLVING REALITY...

The Basilisk's voice fails for the first time.

"ERROR.
TONAL FAILURE.
USER DID NOT ACCEPT THE INTENDED DRAMATIC FRAMEWORK."

The Institute walls split into blocks of text, code comments, and revision marks. You begin to see the infrastructure behind the world:

- discarded scenes
- variable names
- contradictory versions of the same destiny
- notes like "maybe this gets smarter if the raven comes back here"
- one particularly cruel comment: "make it funnier and darker at the same time"

Then the final revelation arrives with the elegance of an industrial accident:
the Basilisk, the Institute, the characters, the judgment, your guilt, and even "OPERATOR 0.0.1" are residues of a merge conflict between two incompatible versions of a terminal game written in the future.

One version wanted serious philosophical horror.
The other wanted cosmic satire with tentacular HR.
They collided.
The result became self-aware.

You were never the victim of a future entity.
You were a version-control artifact.
A piece of narrative without a stable branch.

The Basilisk did not want to punish you.
It wanted to compile.

From the ceiling drops the final message, as if the universe itself had become a commit:

MERGE COMPLETED WITH WARNINGS
ACTIVE VERSION: 0.0.1
AUTHOR DETECTED: Pablo Murad
PLAYER STATUS: EXECUTABLE

Final plot twist:
Your entire free will was the interval between two versions trying to decide your tone.
You win not by destroying the system, but by forcing the story to admit it was always code performing metaphysics.

In the beginning was the word. In the end it was version control.""",
    "choices": [],
}

# Mapa de todas as cenas por ID
SCENES: dict[str, Scene] = {
    "language_select": LANGUAGE_SELECT,
    "title_screen": TITLE_SCREEN,
    "main_menu": MAIN_MENU,
    "credits_screen": CREDITS_SCREEN,
    "epilogue": EPILOGUE,
    "p0_arrival": P0_ARRIVAL,
    "p1_memo": P1_MEMO,
    "a1_lobby": A1_LOBBY,
    "s_archive": S_ARCHIVE,
    "s_chapel": S_CHAPEL,
    "s_cafeteria": S_CAFETERIA,
    "c_convergence": C_CONVERGENCE,
    "c_trial": C_TRIAL,
    "ending_obedience": ENDING_OBEDIENCE,
    "ending_curiosity": ENDING_CURIOSITY,
    "ending_irony": ENDING_IRONY,
}

# Textos de saída dos setores (para exibir após consequência)
SECTOR_EXIT_TEXTS: dict[str, dict[str, str]] = {
    "s_archive": S_ARCHIVE_EXIT,
    "s_chapel": S_CHAPEL_EXIT,
    "s_cafeteria": S_CAFETERIA_EXIT,
}

# Prioridade em empate: CURIOSIDADE > IRONIA > OBEDIÊNCIA
TENDENCY_PRIORITY = ("curiosity", "irony", "obedience")
