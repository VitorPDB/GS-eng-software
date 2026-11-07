---
name: Radar da Mooca
description: Boletim urbano legível para acompanhar alertas e sua confiança.
colors:
  ink: "#153a42"
  muted: "#52656b"
  paper: "#f4f5f1"
  surface: "#fff"
  line: "#d5dedb"
  accent: "#b54728"
  accent-hover: "#94371f"
  soft: "#e8eeea"
  high: "#a52c26"
  high-bg: "#fcebe7"
  medium: "#795111"
  medium-bg: "#fcf1d8"
  low: "#286243"
  low-bg: "#e9f3e9"
typography:
  display:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "34px"
    fontWeight: 650
    lineHeight: "1.2"
    letterSpacing: "-.03em"
  headline:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "26px"
    fontWeight: 700
    lineHeight: "1.25"
    letterSpacing: "-.02em"
  title:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "20px"
    fontWeight: 700
    lineHeight: "1.55"
    letterSpacing: "normal"
  body:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: "1.55"
    letterSpacing: "normal"
  label:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 650
    lineHeight: "1.55"
    letterSpacing: "normal"
rounded:
  panel: "14px"
  control: "7px"
  navigation: "8px"
  badge: "5px"
  symbol: "10px"
spacing:
  inline: "8px"
  compact: "12px"
  item: "16px"
  group: "24px"
  panel: "28px"
  page: "40px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    padding: "10px 18px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
  button-secondary:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 18px"
  button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 18px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "12px 13px"
  badge-high:
    backgroundColor: "{colors.high-bg}"
    textColor: "{colors.high}"
    rounded: "{rounded.badge}"
    padding: "4px 10px"
    typography: "{typography.label}"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
    padding: "28px"
  navigation-active:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.navigation}"
    padding: "12px 14px"
---
# Design System: Radar da Mooca

## Overview

**Creative North Star: "Boletim de bairro legível"**

Uma linguagem de boletim urbano: superfícies claras, tinta azul-petróleo, divisórias precisas e ações em terracota. A tipografia humanista de sistema mantém títulos, explicações e dados legíveis sem depender de fontes externas.

A composição usa agrupamentos espaçosos e listas compactas. Gravidade e confiança recebem rótulos explícitos; cores reforçam a leitura, enquanto textos e ícones SVG de traço preservam o significado.

**Key Characteristics:**

- Superfícies claras e navegação azul-petróleo.
- Segoe UI com números tabulares.
- Etiquetas textuais para gravidade e confiança.
- Colunas que se empilham e navegação horizontal no celular.

## Colors

O azul-petróleo organiza a interface; o terracota destaca ações, com neutros claros e pares semânticos para etiquetas.

### Primary

- **Terracota de ação** (`accent`): ações principais e foco; a variante `accent-hover` escurece o botão ao apontar.
- **Tinta azul-petróleo** (`ink`): texto principal, navegação lateral e toast.

### Secondary

- **Vermelho de gravidade** (`high`, `high-bg`): gravidade alta e confiança baixa.
- **Âmbar de atenção** (`medium`, `medium-bg`): gravidade moderada e confiança média.
- **Verde de confirmação** (`low`, `low-bg`): gravidade baixa e confiança alta.

### Neutral

- **Papel claro** (`paper`): fundo geral.
- **Branco de superfície** (`surface`): painéis, campos e item ativo da navegação.
- **Cinza de leitura** (`muted`): explicações, datas e metadados.
- **Divisória suave** (`line`): contornos e separadores.
- **Verde névoa** (`soft`): botões secundários, símbolos e etiquetas neutras.

**The Estado com Texto Rule.** Toda cor semântica deve acompanhar um rótulo legível que identifica o estado e sua dimensão.

## Typography

**Display Font:** Segoe UI, com Arial e sans-serif como alternativas.
**Body Font:** a mesma família, sem downloads externos.

**Character:** humanista e utilitária. Os números usam variantes tabulares para facilitar comparações.

### Hierarchy

- **Display:** título de página; reduz para (29px) no celular.
- **Headline:** destaque principal; reduz para (23px) no celular.
- **Title:** títulos de seção e painel; seções reduzem para (18px) no celular.
- **Body:** texto base; explicações e descrições recorrentes usam (14px), metadados usam (12–13px).
- **Label:** etiquetas de estado com peso forte. Botões usam (14px), peso (600).

O corpo de explicações em painéis limita-se a (72ch). Não há família monoespaçada distinta.

## Layout

Grade desktop com barra lateral de (236px) e área fluida. O conteúdo tem largura máxima de (1400px), respiro lateral de (40px) e intervalos principais de (24px). O destaque usa proporção (1.7fr / 1fr); páginas de detalhe usam (1.5fr / 1fr). Painéis têm preenchimento de (28px).

Até (1100px), a navegação lateral passa a (205px), o respiro lateral a (24px) e as grades principais se empilham. Até (760px), a barra lateral se torna cabeçalho estático com navegação horizontal rolável; o perfil ocupa uma linha própria, formulários se empilham e o conteúdo usa (20px) nas laterais. Painéis usam (22px). A lista reposiciona metadados abaixo do título e mantém a seta na direita. A ação do cabeçalho ocupa a largura disponível. A composição deve continuar legível em (360px).

A partir de (1600px), o respiro superior da página passa a (40px). Controles principais têm altura mínima de (44px); a variante compacta de botão usa (36px).

## Elevation & Depth

A hierarquia usa contraste tonal, separadores finos e espaços. Painéis e listas permanecem planos. A única sombra de interface é a do toast fixo: (0 5px 18px #153a4229), que o separa do conteúdo sem criar uma família de cartões elevados.

A entrada de conteúdo dura (.28s), com curva (cubic-bezier(.16,1,.3,1)), opacidade e recorte discretos. Links e botões transicionam cor e fundo em (.16s). Com preferência por movimento reduzido, animações e transições são desativadas e a rolagem suave cessa.

## Shapes

Painéis usam cantos suaves do token `panel`; controles usam `control`, etiquetas usam `badge` e itens de navegação usam `navigation`. Símbolos de evento usam recipientes arredondados de (38px), reduzidos a (32px) no celular. Separadores e contornos têm (1px). A linha do tempo usa haste fina e pontos circulares de (9px). Os ícones SVG compartilham tamanho nominal de (20px) e traços simples.

## Components

### Buttons

Ações claras, textuais e compactas. O primário usa terracota sobre branco, escurecendo no hover; o secundário usa `soft` sobre `ink`, com hover (#d6e2dc). O discreto é transparente, com contorno `line`; herda o fundo terracota no hover conforme a implementação. Todos compartilham alinhamento central, intervalo de (8px), foco externo de (3px) com afastamento de (4px). Desabilitados usam opacidade (.55) e cursor indisponível.

### Chips

Etiquetas retangulares suaves, com preenchimento compacto e peso forte. São indicadores de estado, sem aparência de controle selecionável. Gravidade e confiança usam textos distintos, mesmo quando compartilham cores.

### Cards / Containers

Superfícies brancas, sem sombra, com cantos `panel`. Listas agrupadas recortam os cantos e separam linhas por bordas; linhas apontáveis recebem fundo (#f6f8f5) no hover. Resumos de fontes usam fundo (#e4ece7) e divisórias (#bdcec4).

### Inputs / Fields

Campos brancos com contorno (#9db0aa), preenchimento (`12px 13px`), altura mínima de (44px) e rótulos explícitos acima. Placeholders usam (#677a73). Textareas têm altura mínima de (125px) e redimensionamento vertical. Compartilham o foco externo dos botões. Erros e confirmações aparecem em blocos textuais próprios.

### Navigation

Faixa azul-petróleo com links em (#d4e0de), ícone e texto. Hover em (#254d54); item ativo branco, texto `ink` e peso (650). O padrão permanece textual no celular, em rolagem horizontal. O link de salto fica visível ao receber foco.

### Event list and timeline

Linhas de evento unem símbolo, título, local, etiqueta, data e seta. No celular, metadados passam para a segunda linha. A linha do tempo mantém data, título e explicação em sequência vertical, conectados por haste discreta.

## Do's and Don'ts

### Do:

- **Do** manter rótulos explícitos junto aos estados de gravidade e confiança.
- **Do** preservar foco visível e alvos principais com altura mínima de 44px.
- **Do** usar ícones SVG de traço junto a textos de navegação e ações.
- **Do** verificar a composição a partir de 360px e respeitar movimento reduzido.

### Don't:

- **Don't** representar gravidade ou confiança somente por cor.
- **Don't** substituir Segoe UI por uma fonte externa sem revisar o sistema.
- **Don't** aplicar sombras a todos os painéis: o relevo observado pertence ao toast.
- **Don't** manter colunas fixas ou ocultar os textos de navegação no celular.
