"""Rebuild the review PDF and vector diagrams. Requires reportlab and pypdf.

Run from any directory: python scripts/build_pdf.py
PlantUML sources document the same diagrams; SVGs are authored with ReportLab,
so rebuilding does not require Java, PlantUML or an external service.
"""
from pathlib import Path
import re
from html import escape
from math import atan2, cos, sin, pi
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, NextPageTemplate, Table, TableStyle, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle
from reportlab.graphics import renderSVG
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
DIAGRAMS = DOCS / 'diagramas'
DIAGRAMS.mkdir(parents=True, exist_ok=True)
for name, filename in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf'), ('Arial-Italic', 'ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / filename)))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-Bold')
INK = colors.HexColor('#16332f')
TEAL = colors.HexColor('#14796d')
PALE = colors.HexColor('#edf5f2')
MUTED = colors.HexColor('#52645f')
RULE = colors.HexColor('#c7d5d0')

def clean(s):
    return s.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-').replace('\u00a0', ' ')

def rich(s):
    s = escape(clean(s))
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#14796d"><u>\1</u></link>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<font color="#14796d">\1</font>', s)
    return s

ST = {
 'body': ParagraphStyle('body', fontName='Arial', fontSize=9.7, leading=14.3, textColor=INK, spaceAfter=7),
 'h1': ParagraphStyle('h1', fontName='Arial-Bold', fontSize=21, leading=25, textColor=TEAL, spaceBefore=6, spaceAfter=14, keepWithNext=True),
 'h2': ParagraphStyle('h2', fontName='Arial-Bold', fontSize=12.2, leading=16, textColor=INK, spaceBefore=12, spaceAfter=8, keepWithNext=True),
 'cell': ParagraphStyle('cell', fontName='Arial', fontSize=8.1, leading=11.3, textColor=INK),
 'th': ParagraphStyle('th', fontName='Arial-Bold', fontSize=8.2, leading=11.4, textColor=colors.white),
 'small': ParagraphStyle('small', fontName='Arial', fontSize=8.4, leading=12, textColor=MUTED, spaceAfter=7),
}

def p(s, style='body'):
    return Paragraph(rich(s), ST[style])

def textbox(d, x, top, w, h, lines, fill=PALE, fontsize=9, bold=False, radius=6):
    y = d.height - top - h
    d.add(Rect(x, y, w, h, rx=radius, ry=radius, fillColor=fill, strokeColor=RULE, strokeWidth=.8))
    if isinstance(lines, str): lines = lines.split('\n')
    lead = fontsize + 4
    start = y + h / 2 + (len(lines)-1) * lead / 2 - fontsize / 3
    for i, text in enumerate(lines):
        d.add(String(x+w/2, start-i*lead, clean(text), textAnchor='middle', fontName='Arial-Bold' if bold and i == 0 else 'Arial', fontSize=fontsize, fillColor=INK))

def label(d, x, top, text, size=8.3, anchor='middle', bold=False):
    for i, line in enumerate(text.split('\n')):
        d.add(String(x, d.height-top-i*(size+3), clean(line), textAnchor=anchor, fontName='Arial-Bold' if bold else 'Arial', fontSize=size, fillColor=INK))

def arrow(d, pts, text=None, lx=None, ly=None, dashed=False, size=8):
    pts = [(x,d.height-y) for x,y in pts]
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        d.add(Line(x1,y1,x2,y2,strokeColor=TEAL,strokeWidth=1,strokeDashArray=[4,3] if dashed else None))
    (x1,y1),(x2,y2)=pts[-2:]
    a=atan2(y2-y1,x2-x1)
    d.add(Polygon([x2,y2,x2-6*cos(a-.45),y2-6*sin(a-.45),x2-6*cos(a+.45),y2-6*sin(a+.45)],fillColor=TEAL,strokeColor=TEAL))
    if text: label(d,lx,ly,text,size)

SEQUENCE_PUML = '''@startuml
title Radar da Mooca - sequência do alerta simulado
actor "Fonte simulada / Morador" as F
actor "Agente (perfil demonstrativo)" as G
boundary "UI / Controller" as UI
control "Plataforma / Application" as APP
entity "Rules / Domain" as D
database "Repository local" as R
F -> UI: informar ocorrência fictícia
UI -> APP: createReport(input)
APP -> D: validateReport(input)
alt entrada inválida
D --> APP: erro de validação
APP --> UI: exibir erro, sem gravar
else entrada válida
D --> APP: dados válidos
APP -> R: save(reportado, fonte comunidade)
APP --> UI: protocolo e confiança inicial
end
G -> UI: iniciar validação + motivo
UI -> APP: transition(em_validacao, motivo)
APP -> D: validateTransition(...)
APP -> R: save(estado, histórico)
opt adicionar evidência simulada
G -> UI: adicionar sensor/base fictícios
UI -> APP: addDemoSource(tipo)
APP -> R: save(fontes fictícias)
end
G -> UI: confirmar + motivo
UI -> APP: transition(confirmado, motivo)
APP -> D: validar motivo e fonte fresca
APP -> R: save(verified=true, histórico)
G -> UI: publicar alerta
UI -> APP: transition(alerta_emitido, motivo)
APP -> D: calculateEvent + validateTransition
alt confirmado e fonte fresca e confiança>=50 e risco moderado/alto
APP -> APP: gerar notificação interna única
APP -> R: save(evento + notificação + histórico)
APP --> UI: alerta e central atualizados
else condição não atendida
APP --> UI: informar bloqueio sem alterar estado
end
note over F,R: Dados simulados; sem API externa, SMS, e-mail ou autenticação real.
@enduml
'''

STATES_PUML = '''@startuml
title Radar da Mooca - ciclo do evento
hide empty description
[*] --> reportado : registrar relato válido
reportado --> em_validacao : iniciar conferência / motivo
reportado --> descartado : descartar [motivo preenchido]
em_validacao --> descartado : descartar [motivo preenchido]
em_validacao --> confirmado : confirmar [motivo e fonte fresca] / verified=true
confirmado --> alerta_emitido : publicar [fonte fresca e confiança>=50 e risco moderado/alto]\n/ notificação interna única
confirmado --> em_monitoramento : acompanhar [risco baixo] / motivo
alerta_emitido --> em_monitoramento : acompanhar / motivo
em_monitoramento --> encerrado : encerrar / motivo
descartado --> [*]
encerrado --> [*]
note bottom: Outras transições são recusadas. Fresca: idade entre 0 e 30 minutos, inclusive.\nTodo o cenário e o perfil do agente são demonstrativos.
@enduml
'''

ARCH_PUML = '''@startuml
title Radar da Mooca - arquitetura implementada
package "Fontes representadas - simuladas" {
  component "Comunidade fictícia" as Community
  component "Sensor e base pública fictícios" as Sources
}
package "Apresentação" {
  component "app.js: UI/controller + views\nT01-T08; composição" as UI
}
package "Aplicação" {
  component "Platform: casos de uso\nregistro, validação, publicação\nnotificação interna e histórico" as App
}
package "Domínio" {
  component "Rules: risco, confiança, frescor\ntransições e validações" as Rules
}
package "Infraestrutura / dados" {
  database "Repository: localStorage\ncontingência em memória" as Repo
  component "seedFactory: fontes e eventos fictícios" as Seed
}
Community --> UI : entrada demonstrativa
Sources --> Seed : dados pré-carregados
UI --> App : chama casos de uso
UI ..> Repo : cria e injeta
UI ..> Seed : injeta seedFactory
App --> Rules : regras
App --> Repo : contrato injetado load/save
App --> Seed : função injetada
note right of Rules: Domínio sem DOM ou armazenamento.\nAplicação sem importar infraestrutura.
note bottom of Repo: Minimização: localização aproximada e sem identidade do relator.\nNenhuma integração urbana real ou canal externo de notificação.
package "Evolução futura - não implementada" {
  component "API, autenticação/autorização, banco,\nmonitoramento e fila conforme necessidade" as Future
}
@enduml
'''

def sequence():
    d=Drawing(760,445)
    xs=[55,180,305,445,575,705]
    names=['Fonte simulada /\nMorador','Agente\n(demonstração)','UI / Controller','Plataforma\nApplication','Rules\nDomain','Repository\nlocal']
    for x,name in zip(xs,names):
        textbox(d,x-51,0,102,36,name,fontsize=8.2,bold=True)
        d.add(Line(x,d.height-36,x,30,strokeColor=RULE,strokeWidth=.8,strokeDashArray=[4,3]))
    def msg(a,b,y,s,ret=False): arrow(d,[(xs[a],y),(xs[b],y)],s,(xs[a]+xs[b])/2,y-4,ret,size=7.5)
    msg(0,2,57,'1. informar ocorrência fictícia')
    msg(2,3,76,'2. createReport(input)')
    msg(3,4,95,'3. validateReport')
    # Combined fragment with two clearly labelled operands.
    d.add(Rect(282,d.height-181,465,76,fillColor=None,strokeColor=MUTED,strokeWidth=.8))
    label(d,288,116,'alt [entrada inválida]',7.4,'start',True)
    msg(4,3,133,'erro',True); msg(3,2,148,'exibir erro; sem gravar',True)
    d.add(Line(282,d.height-155,747,d.height-155,strokeColor=MUTED,strokeWidth=.6,strokeDashArray=[3,2]))
    label(d,288,166,'[entrada válida]',7.4,'start',True)
    msg(3,5,178,'4. save(reportado + fonte + histórico)')
    msg(3,2,197,'5. protocolo + confiança inicial',True)
    msg(1,2,216,'6. iniciar validação + motivo')
    msg(2,3,235,'transition(em_validacao)')
    msg(3,4,254,'validar transição')
    msg(3,5,273,'save(estado + histórico)')
    msg(1,2,292,'7. fonte fictícia opcional')
    msg(2,3,311,'addDemoSource(tipo)')
    msg(3,5,330,'save(fonte simulada)')
    msg(1,2,349,'8. confirmar + motivo')
    msg(2,3,368,'transition(confirmado)')
    msg(3,4,387,'motivo + fonte fresca')
    msg(3,5,406,'save(verified=true + histórico)')
    label(d,8,432,'Continua na próxima figura: classificação, publicação e notificação interna.',8.2,'start',True)
    return d

def publication():
    d=Drawing(760,385)
    xs=[65,230,400,565,705]
    names=['Agente\n(demonstração)','UI / Controller','Plataforma\nApplication','Rules\nDomain','Repository\nlocal']
    for x,name in zip(xs,names):
        textbox(d,x-52,0,104,37,name,fontsize=8.5,bold=True)
        d.add(Line(x,d.height-37,x,15,strokeColor=RULE,strokeWidth=.8,strokeDashArray=[4,3]))
    def msg(a,b,y,s,ret=False): arrow(d,[(xs[a],y),(xs[b],y)],s,(xs[a]+xs[b])/2,y-5,ret,size=8)
    msg(0,1,66,'9. publicar + motivo')
    msg(1,2,95,'transition(alerta_emitido)')
    msg(2,3,124,'calculateEvent + validateTransition')
    msg(3,2,153,'risco + confiança + elegibilidade',True)
    d.add(Rect(170,d.height-345,575,177,fillColor=None,strokeColor=MUTED,strokeWidth=.8))
    label(d,177,181,'alt [confirmado; fonte fresca; confiança >= 50; risco moderado/alto]',8,'start',True)
    arrow(d,[(400,205),(450,205),(450,224),(400,224)])
    label(d,463,214,'gerar notificação\ninterna única',8,'start')
    msg(2,4,248,'save(evento + notificação + histórico)')
    msg(2,1,278,'alerta e central atualizados',True)
    d.add(Line(170,d.height-292,745,d.height-292,strokeColor=MUTED,strokeWidth=.6,strokeDashArray=[3,2]))
    label(d,177,308,'[condição não atendida]',8,'start',True)
    msg(2,1,334,'informar bloqueio; estado preservado',True)
    label(d,8,374,'Fontes são simuladas e pré-carregadas. Sem API externa, SMS, e-mail ou autenticação real.',8.5,'start')
    return d

def states():
    d=Drawing(760,420)
    positions={'reportado':(55,70,125,45),'em_validacao':(245,70,130,45),'confirmado':(450,70,125,45),'alerta_emitido':(630,70,125,45),'em_monitoramento':(525,255,160,48),'encerrado':(280,255,130,48),'descartado':(75,275,130,45)}
    for name,(x,y,w,h) in positions.items(): textbox(d,x,y,w,h,name,fontsize=9.2,bold=True)
    d.add(Circle(18,d.height-92,6,fillColor=INK,strokeColor=INK))
    arrow(d,[(24,92),(55,92)])
    label(d,64,52,'registro válido',8.2)
    arrow(d,[(180,92),(245,92)],'iniciar / motivo',212,77)
    arrow(d,[(375,92),(450,92)],'confirmar',410,72)
    label(d,412,128,'[motivo + fonte fresca]\n/ verified=true',7.9)
    arrow(d,[(575,92),(630,92)],'publicar',602,77)
    label(d,640,145,'[fonte fresca; confiança >= 50;\nrisco moderado/alto]\n/ notificação interna única',8)
    arrow(d,[(117,115),(117,275)],'descartar\n[motivo]',69,190)
    arrow(d,[(310,115),(310,210),(175,210),(175,275)],'descartar [motivo]',280,195)
    arrow(d,[(512,115),(512,200),(605,200),(605,255)],'acompanhar [risco baixo]\n/ motivo',551,181)
    arrow(d,[(692,115),(735,172),(735,279),(685,279)],'acompanhar\n/ motivo',698,226)
    arrow(d,[(525,279),(410,279)],'encerrar / motivo',467,262)
    d.add(Circle(228,d.height-279,8,fillColor=None,strokeColor=INK,strokeWidth=1)); d.add(Circle(228,d.height-279,5,fillColor=INK,strokeColor=INK))
    arrow(d,[(280,279),(237,279)])
    d.add(Circle(140,d.height-365,8,fillColor=None,strokeColor=INK,strokeWidth=1)); d.add(Circle(140,d.height-365,5,fillColor=INK,strokeColor=INK))
    arrow(d,[(140,320),(140,356)])
    label(d,252,365,'Fresca: idade entre 0 e 30 minutos, inclusive. Todas as mudanças exigem motivo.',8.4,'start')
    label(d,252,384,'Estados terminais não reabrem. Transições não previstas são recusadas.',8.4,'start')
    label(d,252,403,'Dados e papéis simulados; não representa protocolo oficial de emergência.',8.4,'start')
    return d

def architecture():
    d=Drawing(760,420)
    textbox(d,5,15,165,105,['FONTES REPRESENTADAS','Comunidade fictícia','Sensor/base fictícios','Dados pré-carregados'],fontsize=9,bold=True)
    textbox(d,220,10,535,65,['APRESENTAÇÃO - app.js','UI/controller + views T01-T08; composição e injeção','Campos mínimos; localização aproximada; texto seguro'],fontsize=10,bold=True)
    textbox(d,220,115,535,65,['APLICAÇÃO - platform','Casos de uso: registro, validação, publicação e histórico','Gera notificação interna; recebe repository, seedFactory e clock'],fontsize=10,bold=True)
    textbox(d,220,220,535,65,['DOMÍNIO - rules','Risco, confiança, frescor e transições','Sem DOM, localStorage ou imports da infraestrutura'],fontsize=10,bold=True)
    textbox(d,220,325,535,65,['INFRAESTRUTURA / DADOS','Repository: localStorage com contingência em memória','Seed: fontes e eventos fictícios; sem conectores reais'],fontsize=10,bold=True)
    arrow(d,[(170,60),(220,43)])
    arrow(d,[(487,75),(487,115)],'chama casos de uso',580,98)
    arrow(d,[(487,180),(487,220)],'depende das regras',580,203)
    arrow(d,[(225,55),(191,55),(191,358),(220,358)],dashed=True)
    label(d,202,181,'cria e injeta',7.8,'middle')
    arrow(d,[(755,146),(759,146),(759,357),(755,357)],dashed=True)
    label(d,651,311,'load/save por contrato injetado',8.2)
    textbox(d,5,235,165,155,['EVOLUÇÃO FUTURA','Não implementada','API e banco','Autenticação/autorização','Monitoramento e filas','conforme necessidade'],fill=colors.HexColor('#f5f2e8'),fontsize=9,bold=True)
    label(d,8,411,'A aplicação não importa infraestrutura. Notificações locais; sem SMS/e-mail. Perfis apenas demonstrativos.',8.5,'start')
    return d

def page(c, doc):
    w,h=c._pagesize
    c.setStrokeColor(RULE); c.line(42,h-36,w-42,h-36)
    c.setFont('Arial-Bold',8); c.setFillColor(TEAL); c.drawString(42,h-27,'RADAR DA MOOCA / ENGENHARIA DE SOFTWARE')
    c.setFont('Arial',7.4); c.setFillColor(MUTED)
    c.drawString(42,25,'VERSÃO PARA REVISÃO - dados e fontes simulados')
    c.drawRightString(w-42,25,f'{doc.page}')

def markdown(text, width=511):
    lines=text.splitlines(); out=[]; i=0; acc=[]
    def flush():
        if acc: out.append(p(' '.join(acc))); acc.clear()
    while i<len(lines):
        line=lines[i].strip()
        if not line: flush(); i+=1; continue
        if line.startswith('|'):
            flush(); rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[: -]+',c) for c in cells): rows.append(cells)
                i+=1
            n=len(rows[0]); lens=[max(len(r[j]) for r in rows if len(r)>j) for j in range(n)]
            if n==4 and rows[0][0]=='ID': ratios=[.09,.24,.50,.17] if 'Característica' in rows[0][1] else [.075,.33,.09,.505]
            elif n==4: ratios=[.13,.18,.39,.30]
            elif n==3: ratios=[.18,.39,.43]
            elif n==2: ratios=[.28,.72]
            else: ratios=[1/n]*n
            data=[[p(c,'th' if k==0 else 'cell') for c in row] for k,row in enumerate(rows)]
            t=Table(data,colWidths=[width*r for r in ratios],repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),.5,RULE),('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
            out += [t,Spacer(1,10)]; continue
        if line.startswith('## '):
            flush(); title=line[3:]
            if re.match(r'[14568]\. ', title) and out: out.append(PageBreak())
            out.append(p(title,'h1')); i+=1; continue
        if line.startswith('### '): flush(); out.append(p(line[4:],'h2')); i+=1; continue
        if line.startswith('# '): flush(); out.append(p(line[2:],'h1')); i+=1; continue
        if re.match(r'^(- |\d+\. )',line):
            flush(); out.append(p(line)); i+=1; continue
        acc.append(line); i+=1
    flush(); return out

def build():
    diagrams=[('sequencia',sequence()),('sequencia-publicacao',publication()),('estados',states()),('arquitetura',architecture())]
    for name,d in diagrams: renderSVG.drawToFile(d,str(DIAGRAMS/f'{name}.svg'))
    for name,source in [('sequencia',SEQUENCE_PUML),('estados',STATES_PUML),('arquitetura',ARCH_PUML)]: (DIAGRAMS/f'{name}.puml').write_text(source,encoding='utf-8')
    out=DOCS/'radar-da-mooca-documentacao.pdf'
    pw,ph=A4; lw,lh=landscape(A4)
    doc=BaseDocTemplate(str(out),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=54,bottomMargin=43,title='Radar da Mooca - documentação técnica para revisão',author='Lucas Zolla Assis; Lucas Baraldi Rodrigues; Vitor Pantarotto de Brito')
    doc.addPageTemplates([PageTemplate(id='portrait',frames=[Frame(42,43,pw-84,ph-97,id='p',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page,pagesize=A4),PageTemplate(id='landscape',frames=[Frame(41,35,lw-82,lh-79,id='l',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page,pagesize=landscape(A4))])
    title=ParagraphStyle('cover',fontName='Arial-Bold',fontSize=36,leading=41,textColor=TEAL,spaceAfter=22)
    story=[Spacer(1,48),p('GLOBAL SOLUTION 2026.2 · CITIZENTECH','small'),Paragraph('Radar<br/>da Mooca',title),p('Urban Risk Intelligence Platform','h2'),p('Engenharia de Software · Documentação técnica e protótipo acadêmico'),Spacer(1,15),p('**VERSÃO PARA REVISÃO**'),p('Dados, fontes, eventos e perfis demonstrativos. Bairro da Mooca, São Paulo/SP.'),Spacer(1,18)]
    for name,rm in [('Lucas Zolla Assis','557952'),('Lucas Baraldi Rodrigues','555407'),('Vitor Pantarotto de Brito','554961')]: story.append(p(f'**{name}** · RM {rm}'))
    story += [Spacer(1,18),p('Prazo informado: **19/11/2026** · Meta interna: **16/11/2026**'),p('Repositório: [VitorPDB/GS-eng-software](https://github.com/VitorPDB/GS-eng-software)'),p('Protótipo: **publicação pendente**'),p('Vídeo: **gravação pendente**'),Spacer(1,12),p('O protótipo não é um serviço operacional de emergência. Fontes fictícias não representam integração com órgãos reais. Metas futuras de produção são distinguidas das capacidades demonstradas.','small'),PageBreak()]
    text=(DOCS/'especificacao.md').read_text(encoding='utf-8')
    text=text[text.index('## 1. Problema'):]
    story += markdown(text,pw-84)
    story += [NextPageTemplate('landscape'),PageBreak()]
    captions=[('Diagrama de sequência - recebimento e validação','Parte 1 de 2. Lifelines, mensagens e alternativa de entrada válida ou rejeitada. Os dados de sensores e bases são apenas simulados.'),('Diagrama de sequência - publicação','Parte 2 de 2. A aplicação gera a notificação interna apenas quando as guardas são atendidas; bloqueios preservam o estado.'),('Diagrama de estados - ciclo do evento','Estados e transições correspondem às regras RB05/RB06. A confirmação não publica automaticamente o evento.'),('Arquitetura em camadas - implementação','As setas sólidas representam chamadas; as tracejadas, composição/injeção ou uso do contrato injetado. Evolução futura está separada.')]
    for i,((name,d),(heading,caption)) in enumerate(zip(diagrams,captions)):
        if i: story.append(PageBreak())
        story += [p(heading,'h2'),p(caption,'small'),d]
    story += [NextPageTemplate('portrait'),PageBreak(),p('11. Verificação e fontes','h1'),p('Esta versão reúne documentação e diagramas para revisão. A equipe deve conferir o registro de resultados da versão final antes de assinalar requisitos como atendidos. O checklist deste pacote mantém verificações e pendências explícitas.'),p('Evidências existentes no trabalho local incluem a jornada de navegador registrada em work/qa/browser-results.json e capturas das oito telas em larguras de 360 e 1280 px. Isso não comprova disponibilidade ou escalabilidade de produção. A bateria de testes automatizados e o relatório final ainda devem ser consolidados no fechamento da entrega.'),p('Pendências de fechamento','h2'),p('Publicar o protótipo, gravar o vídeo, substituir os links pendentes na capa e executar a conferência final de acesso anônimo. Revisar o PDF após qualquer mudança relevante de comportamento.'),p('Referências','h2'),p('ISO. [ISO/IEC 25010:2023 - Product quality model](https://www.iso.org/standard/78176.html). Referência do modelo de qualidade; edição 2023 com nove características. Consulta: 06/11/2026.'),p('MARTIN, Robert C. [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), 13/08/2012. Referência para direção de dependências e separação de regras. O protótipo aplica princípios e não reivindica implementação integral do estilo.'),p('Enunciado da disciplina: sete imagens fornecidas pela equipe nesta conversa. Os critérios e regras acadêmicas foram extraídos dessas imagens; as fórmulas e metas do projeto são propostas próprias.'),NextPageTemplate('landscape'),PageBreak(),p('12. Roteiro do vídeo - duração alvo: 2min50s','h2'),p('Restaurar dados fictícios antes de gravar. Usar impacto 3 e urgência 2; fonte comunitária fresca gera confiança 30 e validação eleva a 70. Relógio fixo: 06/11/2026, 14h30, São Paulo. Limite final: três minutos.','small')]
    video=(DOCS/'roteiro-video.md').read_text(encoding='utf-8')
    video=video.split('## Percurso e narração sugerida',1)[1].split('## Conferência antes de publicar',1)[0]
    story += markdown(video,lw-82)
    doc.build(story)
    reader=PdfReader(out)
    text='\n'.join(page.extract_text() or '' for page in reader.pages)
    for required in ['Lucas Zolla Assis','557952','555407','554961','RF12','RNF08','Diagrama de estados','Arquitetura em camadas']:
        assert required in text, f'Missing PDF text: {required}'
    assert len(reader.pages)>10
    print(f'{out}\nPages: {len(reader.pages)}\nSVGs: {len(diagrams)}; PlantUML sources: 3')

if __name__=='__main__': build()
