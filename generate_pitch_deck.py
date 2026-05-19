"""Generate TendrAI Pitch Deck PDF — professional dark-theme presentation."""
import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

W, H = landscape(A4)

BG       = HexColor('#0f172a')
BG_CARD  = HexColor('#1e293b')
ACCENT   = HexColor('#3b82f6')
ACCENT2  = HexColor('#8b5cf6')
GREEN    = HexColor('#22c55e')
YELLOW   = HexColor('#eab308')
RED      = HexColor('#ef4444')
ORANGE   = HexColor('#f97316')
TXT      = HexColor('#f1f5f9')
TXT_DIM  = HexColor('#94a3b8')
TXT_WHITE = white

FONT_DIR = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')

def register_fonts():
    pairs = [
        ('MainFont', 'arial.ttf'),
        ('MainFont-Bold', 'arialbd.ttf'),
        ('MainFont-Italic', 'ariali.ttf'),
        ('Mono', 'consola.ttf'),
    ]
    for name, fname in pairs:
        path = os.path.join(FONT_DIR, fname)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
        else:
            pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, 'arial.ttf')))

register_fonts()


def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, H - 4*mm, W, 4*mm, fill=1, stroke=0)

def draw_footer(c, slide_num, total=11):
    c.setFillColor(TXT_DIM)
    c.setFont('MainFont', 9)
    c.drawString(30, 20, 'TendrAI — AlemAI Hackathon 2026')
    c.drawRightString(W - 30, 20, f'{slide_num}/{total}')

def draw_title(c, title, subtitle=None, y=None):
    if y is None:
        y = H - 80
    c.setFillColor(TXT_WHITE)
    c.setFont('MainFont-Bold', 32)
    c.drawString(60, y, title)
    if subtitle:
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 16)
        c.drawString(60, y - 30, subtitle)

def draw_card(c, x, y, w, h, color=BG_CARD):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=0)

def draw_bullet(c, x, y, text, font='MainFont', size=14, color=TXT, indent=15):
    c.setFillColor(ACCENT)
    c.circle(x + 4, y + 4, 3, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x + indent, y, text)
    return y - size - 8

def draw_table_row(c, x, y, cols, widths, bold=False, colors=None, size=12):
    font = 'MainFont-Bold' if bold else 'MainFont'
    for i, (text, w) in enumerate(zip(cols, widths)):
        clr = colors[i] if colors else TXT
        c.setFillColor(clr)
        c.setFont(font, size)
        c.drawString(x, y, str(text))
        x += w
    return y - size - 8


# ========== SLIDES ==========

def slide_cover(c):
    draw_bg(c)
    c.setFillColor(ACCENT)
    c.rect(0, H - 4*mm, W, 4*mm, fill=1, stroke=0)
    c.setFillColor(ACCENT2)
    c.rect(0, 0, W, 4*mm, fill=1, stroke=0)

    y = H // 2 + 60
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 56)
    c.drawCentredString(W/2, y, 'TendrAI')

    c.setFillColor(TXT_WHITE)
    c.setFont('MainFont', 22)
    c.drawCentredString(W/2, y - 50, 'AI-ассистент для госзакупок')
    c.drawCentredString(W/2, y - 80, 'Республики Казахстан')

    c.setFillColor(TXT_DIM)
    c.setFont('MainFont', 14)
    c.drawCentredString(W/2, y - 130, 'AlemAI Hackathon 2026  •  Астана')

    c.setFillColor(ACCENT)
    c.rect(W/2 - 60, y - 105, 120, 2, fill=1, stroke=0)


def slide_team(c):
    draw_bg(c)
    draw_title(c, 'Команда', 'TendrAI Team')
    draw_footer(c, 1)

    roles = [
        ('Участник 1', 'Backend / AI Pipeline'),
        ('Участник 2', 'Frontend / UX'),
        ('Участник 3', 'Data Engineering'),
        ('Участник 4', 'Business / Analytics'),
        ('Участник 5', 'DevOps / Интеграции'),
    ]
    card_w = 140
    gap = 18
    total_w = len(roles) * card_w + (len(roles)-1) * gap
    start_x = (W - total_w) / 2
    card_y = H/2 - 80

    for i, (name, role) in enumerate(roles):
        x = start_x + i * (card_w + gap)
        draw_card(c, x, card_y, card_w, 120)
        c.setFillColor(ACCENT)
        c.circle(x + card_w/2, card_y + 95, 20, fill=1, stroke=0)
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont-Bold', 11)
        c.drawCentredString(x + card_w/2, card_y + 50, name)
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 9)
        c.drawCentredString(x + card_w/2, card_y + 34, role)

    draw_card(c, 60, 50, W - 120, 50, HexColor('#1a2744'))
    c.setFillColor(YELLOW)
    c.setFont('MainFont-Italic', 12)
    c.drawCentredString(W/2, 68,
        'Fun fact: Мы проанализировали 50+ реальных тендеров с goszakup.gov.kz за 48 часов хакатона')


def slide_market(c):
    draw_bg(c)
    draw_title(c, 'Продукт + Рынок')
    draw_footer(c, 2)

    left_x, right_x = 60, W/2 + 20
    y = H - 130

    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 16)
    c.drawString(left_x, y, 'Размер рынка')

    metrics = [
        ('Procurement Software',  '$8.9B → $20.75B', '(CAGR 9.9%)'),
        ('GovTech глобально',     '$858B', ''),
        ('Госзакупки РК',         '4+ трлн тенге/год', ''),
        ('Поставщики РК',         '80 000+', 'активных'),
    ]
    y -= 30
    for label, val, note in metrics:
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 11)
        c.drawString(left_x + 15, y, label)
        c.setFillColor(GREEN)
        c.setFont('MainFont-Bold', 12)
        c.drawString(left_x + 210, y, val)
        if note:
            c.setFillColor(TXT_DIM)
            c.setFont('MainFont', 10)
            c.drawString(left_x + 350, y, note)
        y -= 22

    y -= 15
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 16)
    c.drawString(left_x, y, 'Тренды')
    y -= 25
    trends = [
        'McKinsey: ИИ повышает эффективность закупок на 25-40%',
        'Gartner: к 2027 — 50% организаций используют ИИ в procurement',
        'Digital Kazakhstan — курс на цифровизацию госуслуг',
    ]
    for t in trends:
        y = draw_bullet(c, left_x, y, t, size=11)

    # Right column — competitors
    ry = H - 130
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 16)
    c.drawString(right_x, ry, 'Конкуренты')

    headers = ['', 'GovDash', 'AutogenAI', 'TendrAI']
    ry -= 30
    hw = [140, 80, 80, 80]
    draw_table_row(c, right_x, ry, headers, hw, bold=True, colors=[TXT_DIM, TXT_DIM, TXT_DIM, ACCENT])

    rows = [
        ['Анализ PDF',       '+', '+', '+'],
        ['Генерация предл.', '+', '+', '+'],
        ['Детекция монополий','-', '-', '+'],
        ['Русский язык',     '-', '-', '+'],
        ['goszakup.gov.kz',  '-', '-', '+'],
        ['Цена',             '$500+', '$300+', 'Freemium'],
    ]
    for row in rows:
        ry -= 3
        colors_row = [TXT, TXT_DIM, TXT_DIM, GREEN]
        if row[3] == '+':
            colors_row[3] = GREEN
        ry = draw_table_row(c, right_x, ry, row, hw, size=11, colors=colors_row)


def slide_problem(c):
    draw_bg(c)
    draw_title(c, 'Проблема', 'Почему МСБ проигрывают тендеры')
    draw_footer(c, 3)

    y = H - 150
    problems = [
        ('40-60% МСБ', 'проигрывают из-за формальных ошибок'),
        ('3-7 дней', 'ручной анализ одного тендера'),
        ('150-500К тенге', 'стоимость консультанта'),
        ('Скрытые ловушки', 'нетипичные условия в документации'),
        ('Монополии', 'один поставщик побеждает в десятках тендеров'),
    ]
    for num_text, desc in problems:
        draw_card(c, 60, y - 5, W/2 - 80, 35, BG_CARD)
        c.setFillColor(RED)
        c.setFont('MainFont-Bold', 14)
        c.drawString(75, y + 5, num_text)
        c.setFillColor(TXT)
        c.setFont('MainFont', 13)
        c.drawString(250, y + 5, desc)
        y -= 45

    # Solution
    sol_y = H - 150
    sol_x = W/2 + 20
    c.setFillColor(GREEN)
    c.setFont('MainFont-Bold', 18)
    c.drawString(sol_x, sol_y, 'Решение: TendrAI')

    sol_y -= 35
    items = [
        'Чек-лист всех требований',
        'Оценка рисков 0-100',
        'Скрытые подводные камни',
        'Черновик технического предложения',
        'Детекция монополий',
    ]
    for item in items:
        c.setFillColor(GREEN)
        c.circle(sol_x + 5, sol_y + 5, 4, fill=1, stroke=0)
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont', 13)
        c.drawString(sol_x + 20, sol_y, item)
        sol_y -= 28

    draw_card(c, sol_x - 10, sol_y - 15, W/2 - 40, 45, HexColor('#14532d'))
    c.setFillColor(GREEN)
    c.setFont('MainFont-Bold', 13)
    c.drawString(sol_x, sol_y + 10, 'PDF → Полный анализ за 30 секунд')
    c.setFillColor(TXT_DIM)
    c.setFont('MainFont', 11)
    c.drawString(sol_x, sol_y - 5, 'вместо 3 дней и 500К тенге')


def slide_how_it_works(c):
    draw_bg(c)
    draw_title(c, 'Как это работает', '3 клика до результата')
    draw_footer(c, 4)

    # Target audience
    left_x = 60
    y = H - 140
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 15)
    c.drawString(left_x, y, 'Для кого')

    segments = [
        ('МСБ-поставщик', 'Автоматический чек-лист'),
        ('Тендерный консультант', 'Анализ за 30 сек, больше клиентов'),
        ('Крупная компания', 'Пакетный анализ + приоритизация'),
        ('Антикоррупционные органы', 'Детекция монополий'),
    ]
    y -= 30
    for seg, sol in segments:
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont-Bold', 11)
        c.drawString(left_x + 15, y, seg)
        c.setFillColor(GREEN)
        c.setFont('MainFont', 11)
        c.drawString(left_x + 230, y, '→ ' + sol)
        y -= 22

    # 3 steps
    y -= 20
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 15)
    c.drawString(left_x, y, '3 простых шага')
    y -= 35

    steps = [
        ('1', 'Загрузить', 'PDF с goszakup.gov.kz'),
        ('2', 'Подождать', '30 секунд (ИИ работает)'),
        ('3', 'Получить', 'чек-лист + риски + предложение'),
    ]
    for num, title, desc in steps:
        draw_card(c, left_x, y - 5, 350, 35, BG_CARD)
        c.setFillColor(ACCENT)
        c.setFont('MainFont-Bold', 20)
        c.drawString(left_x + 12, y + 3, num)
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont-Bold', 13)
        c.drawString(left_x + 45, y + 5, title)
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 12)
        c.drawString(left_x + 150, y + 5, desc)
        y -= 45

    # Pipeline diagram (right side)
    rx = W/2 + 40
    ry = H - 140
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 15)
    c.drawString(rx, ry, 'AI Pipeline')

    pipeline = [
        ('PDF документ', BG_CARD),
        ('PyMuPDF — извлечение текста', BG_CARD),
        ('AlemLLM — анализ требований', HexColor('#1e3a5f')),
        ('AlemLLM — оценка рисков', HexColor('#1e3a5f')),
        ('Embedder → Milvus (RAG)', HexColor('#2d1b4e')),
        ('AlemLLM — генерация предложения', HexColor('#1e3a5f')),
        ('Результат + Redis кеш', HexColor('#14532d')),
    ]
    ry -= 30
    box_w = W/2 - 80
    box_h = 28
    for label, color in pipeline:
        draw_card(c, rx, ry - 2, box_w, box_h, color)
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont', 11)
        c.drawString(rx + 12, ry + 5, label)
        ry -= 36
        if ry > 60:
            c.setStrokeColor(ACCENT)
            c.setLineWidth(1.5)
            c.line(rx + box_w/2, ry + 36, rx + box_w/2, ry + 8)


def slide_tech(c):
    draw_bg(c)
    draw_title(c, 'Технологии', '6 инструментов Alem Plus')
    draw_footer(c, 5)

    y = H - 140
    stack = [
        ('Frontend',    'React + TypeScript + Tailwind CSS v4', ACCENT),
        ('Backend',     'Django 5 + DRF',                      ACCENT),
        ('LLM',         'AlemLLM (247B параметров, MoE)',      ACCENT2),
        ('Database',    'PostgreSQL (Alem Plus)',               GREEN),
        ('Cache',       'Redis (Alem Plus)',                    GREEN),
        ('Embeddings',  'Alem Plus Embedder API (1024-dim)',    GREEN),
        ('Vector DB',   'Milvus (Alem Plus)',                   GREEN),
        ('CI/CD',       'GitLab (Alem Plus)',                   GREEN),
    ]

    left_x = 60
    for layer, tech, color in stack:
        draw_card(c, left_x, y - 5, W/2 - 80, 30, BG_CARD)
        c.setFillColor(color)
        c.setFont('MainFont-Bold', 11)
        c.drawString(left_x + 12, y + 3, layer)
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont', 11)
        c.drawString(left_x + 120, y + 3, tech)
        y -= 36

    # Right side — key metrics
    rx = W/2 + 40
    ry = H - 140
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 16)
    c.drawString(rx, ry, 'Ключевые метрики')

    stats = [
        ('48', 'часов разработки'),
        ('6', 'инструментов Alem Plus'),
        ('50+', 'протестированных тендеров'),
        ('30', 'секунд — время анализа'),
        ('0', 'секунд — повторный анализ (Redis)'),
        ('84%', 'маржа на Pro-тарифе'),
    ]
    ry -= 35
    for val, label in stats:
        draw_card(c, rx, ry - 5, W/2 - 80, 35, BG_CARD)
        c.setFillColor(ACCENT)
        c.setFont('MainFont-Bold', 20)
        c.drawString(rx + 12, ry + 3, val)
        c.setFillColor(TXT)
        c.setFont('MainFont', 12)
        c.drawString(rx + 80, ry + 3, label)
        ry -= 43


def slide_screenshots(c):
    draw_bg(c)
    draw_title(c, 'MVP — Скриншоты', '3 пользовательских сценария')
    draw_footer(c, 6)

    scenarios = [
        ('Сценарий 1: Загрузка', 'Drag-and-drop PDF с goszakup.gov.kz', 'Ноль настроек, ноль регистраций', ACCENT),
        ('Сценарий 2: Анализ', 'Risk Score + Чек-лист + Подводные камни', 'Полный отчет за 30 секунд', GREEN),
        ('Сценарий 3: Монополии', 'Кросс-тендерная детекция коррупции', 'Уникальная killer-feature', ACCENT2),
    ]

    card_w = (W - 150) / 3
    start_x = 60
    card_y = H/2 - 100

    for i, (title, desc, key, color) in enumerate(scenarios):
        x = start_x + i * (card_w + 15)
        draw_card(c, x, card_y, card_w, 200, BG_CARD)

        # Color accent bar at top
        c.setFillColor(color)
        c.roundRect(x, card_y + 192, card_w, 8, 4, fill=1, stroke=0)

        # Placeholder for screenshot
        c.setStrokeColor(TXT_DIM)
        c.setLineWidth(0.5)
        c.setDash(3, 3)
        c.rect(x + 10, card_y + 80, card_w - 20, 100, fill=0, stroke=1)
        c.setDash()
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 10)
        c.drawCentredString(x + card_w/2, card_y + 125, '[Скриншот MVP]')

        c.setFillColor(color)
        c.setFont('MainFont-Bold', 13)
        c.drawString(x + 10, card_y + 55, title)

        c.setFillColor(TXT)
        c.setFont('MainFont', 10)
        c.drawString(x + 10, card_y + 37, desc)

        c.setFillColor(TXT_DIM)
        c.setFont('MainFont-Italic', 10)
        c.drawString(x + 10, card_y + 18, key)


def slide_business(c):
    draw_bg(c)
    draw_title(c, 'Бизнес-модель', 'Freemium SaaS')
    draw_footer(c, 7)

    y = H - 130
    left_x = 60

    # Value prop
    c.setFillColor(GREEN)
    c.setFont('MainFont-Bold', 14)
    c.drawString(left_x, y, 'Ценность')
    y -= 25
    values = [
        'Экономия 150-500К тенге на каждом тендере',
        'Экономия 3-7 дней на каждом анализе',
        'Повышение win-rate на 25-40%',
        'Единственный инструмент с детекцией монополий',
    ]
    for v in values:
        y = draw_bullet(c, left_x, y, v, size=11)

    # Pricing
    y -= 15
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 14)
    c.drawString(left_x, y, 'Тарифы')
    y -= 25

    plans = [
        ('Free', '0 тенге', '3 анализа/месяц', TXT_DIM),
        ('Pro', '9 990 тенге/мес', 'Безлимит + генерация', ACCENT),
        ('Business', '49 990 тенге/мес', '+ монополии + API', ACCENT2),
        ('Enterprise', 'По запросу', 'Кастом + SLA', GREEN),
    ]
    for name, price, desc, color in plans:
        draw_card(c, left_x, y - 5, W/2 - 80, 28, BG_CARD)
        c.setFillColor(color)
        c.setFont('MainFont-Bold', 11)
        c.drawString(left_x + 10, y + 2, name)
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont', 11)
        c.drawString(left_x + 100, y + 2, price)
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 10)
        c.drawString(left_x + 280, y + 2, desc)
        y -= 35

    # Right: unit economics + GTM
    rx = W/2 + 40
    ry = H - 130
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 14)
    c.drawString(rx, ry, 'Unit-экономика (Pro)')

    ry -= 30
    econ = [
        ('Стоимость анализа:', '~200 тенге'),
        ('Среднее использование:', '8 анализов/мес'),
        ('Расходы:', '1 600 тенге'),
        ('Подписка:', '9 990 тенге'),
        ('Маржа:', '84%'),
    ]
    for label, val in econ:
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 11)
        c.drawString(rx + 15, ry, label)
        clr = GREEN if val == '84%' else TXT_WHITE
        c.setFillColor(clr)
        c.setFont('MainFont-Bold', 12)
        c.drawString(rx + 200, ry, val)
        ry -= 22

    ry -= 15
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 14)
    c.drawString(rx, ry, 'Go-to-Market')
    ry -= 25

    gtm = [
        'Мес 1-3: Бесплатно для 1000 пользователей',
        'Мес 3-6: Партнерство с НПП "Атамекен"',
        'Мес 6-12: API-интеграция с goszakup.gov.kz',
        'Год 2: Выход на рынки СНГ',
    ]
    for item in gtm:
        ry = draw_bullet(c, rx, ry, item, size=11)


def slide_mvp1(c):
    draw_bg(c)
    draw_title(c, 'MVP: Загрузка тендера', 'Сценарий 1 — Первое касание')
    draw_footer(c, 8)

    cx = W/2
    y = H - 140

    # Big screenshot placeholder
    draw_card(c, 60, 80, W - 120, H - 230, BG_CARD)
    c.setStrokeColor(TXT_DIM)
    c.setLineWidth(0.5)
    c.setDash(4, 4)
    c.rect(80, 100, W - 160, H - 270, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(TXT_DIM)
    c.setFont('MainFont', 14)
    c.drawCentredString(cx, H/2 - 20, '[Скриншот: Главная страница TendrAI]')
    c.drawCentredString(cx, H/2 - 40, 'Drag-and-drop зона загрузки PDF')

    # Key points at bottom
    c.setFillColor(GREEN)
    c.setFont('MainFont-Bold', 12)
    c.drawCentredString(cx, 55, 'Ноль настроек  •  Ноль регистраций  •  PDF → Результат')


def slide_mvp2(c):
    draw_bg(c)
    draw_title(c, 'MVP: Анализ тендера', 'Сценарий 2 — Ключевая фича')
    draw_footer(c, 9)

    cx = W/2

    draw_card(c, 60, 80, W - 120, H - 230, BG_CARD)

    # Risk score
    c.setFillColor(RED)
    c.setFont('MainFont-Bold', 48)
    c.drawString(100, H - 190, '75')
    c.setFillColor(TXT_DIM)
    c.setFont('MainFont', 16)
    c.drawString(165, H - 190, '/ 100')
    c.setFillColor(RED)
    c.setFont('MainFont-Bold', 14)
    c.drawString(220, H - 190, 'ВЫСОКИЙ РИСК')

    # Checklist
    y = H - 235
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 13)
    c.drawString(100, y, 'Чек-лист требований:')
    y -= 25

    checks = [
        ('Лицензия на деятельность', 'ОБЯЗАТЕЛЬНО', RED),
        ('Опыт работы от 3 лет', 'ОБЯЗАТЕЛЬНО', RED),
        ('Финансовая отчетность за 2 года', 'ОБЯЗАТЕЛЬНО', ORANGE),
        ('Срок поставки 30 дней', 'ВНИМАНИЕ: короткий', YELLOW),
        ('Штраф 0.1%/день просрочки', 'ВНИМАНИЕ', YELLOW),
    ]
    for text, status, color in checks:
        c.setFillColor(color)
        c.setFont('MainFont', 10)
        c.drawString(100, y, '■')
        c.setFillColor(TXT)
        c.setFont('MainFont', 11)
        c.drawString(118, y, text)
        c.setFillColor(color)
        c.setFont('MainFont-Bold', 10)
        c.drawString(370, y, status)
        y -= 20

    # Pitfalls (right side)
    rx = W/2 + 20
    ry = H - 235
    c.setFillColor(ORANGE)
    c.setFont('MainFont-Bold', 13)
    c.drawString(rx, ry, 'Подводные камни:')
    ry -= 25
    pitfalls = [
        'Короткий срок поставки (30 дней)',
        'Требуется авторизация вендора',
        'Совместимость с существующей инфраструктурой',
        'Штраф 0.1% за каждый день просрочки',
    ]
    for p in pitfalls:
        c.setFillColor(ORANGE)
        c.setFont('MainFont', 10)
        c.drawString(rx, ry, '⚠')
        c.setFillColor(TXT)
        c.setFont('MainFont', 11)
        c.drawString(rx + 18, ry, p)
        ry -= 22

    ry -= 15
    c.setFillColor(GREEN)
    c.setFont('MainFont-Bold', 13)
    c.drawString(rx, ry, 'Техническое предложение:')
    ry -= 20
    c.setFillColor(TXT_DIM)
    c.setFont('MainFont', 11)
    c.drawString(rx, ry, 'Сгенерировано AlemLLM')
    c.drawString(rx, ry - 18, 'Адаптировано под требования тендера')
    c.drawString(rx, ry - 36, 'Готово к редактированию и подаче')

    c.setFillColor(GREEN)
    c.setFont('MainFont-Bold', 11)
    c.drawCentredString(W/2, 60, '3 дня работы консультанта → 30 секунд с TendrAI')


def slide_mvp3(c):
    draw_bg(c)
    draw_title(c, 'MVP: Детекция монополий', 'Сценарий 3 — Killer-feature')
    draw_footer(c, 10)

    draw_card(c, 60, 80, W - 120, H - 230, BG_CARD)

    left_x = 100
    y = H - 160

    c.setFillColor(RED)
    c.setFont('MainFont-Bold', 16)
    c.drawString(left_x, y, 'Обнаружена монопольная схема')
    y -= 35

    findings = [
        ('Найдено похожих тендеров:', '23', TXT_WHITE),
        ('Один поставщик выиграл:', '17 из 23 (74%)', RED),
        ('Цена победы выше рыночной:', 'на 12%', ORANGE),
    ]
    for label, val, color in findings:
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 13)
        c.drawString(left_x, y, label)
        c.setFillColor(color)
        c.setFont('MainFont-Bold', 14)
        c.drawString(left_x + 290, y, val)
        y -= 28

    y -= 10
    c.setFillColor(RED)
    c.setFont('MainFont-Bold', 13)
    c.drawString(left_x, y, 'Красные флаги:')
    y -= 22
    flags = [
        'Нетипичные требования, совпадающие в 17 тендерах',
        'Сроки подачи укорочены (3 дня вместо 10)',
        'Техспецификация «заточена» под одного производителя',
    ]
    for f in flags:
        c.setFillColor(RED)
        c.setFont('MainFont', 10)
        c.drawString(left_x, y, '●')
        c.setFillColor(TXT)
        c.setFont('MainFont', 12)
        c.drawString(left_x + 15, y, f)
        y -= 22

    # Right side
    rx = W/2 + 30
    ry = H - 195
    draw_card(c, rx, ry - 10, W/2 - 80, 170, HexColor('#2d0f0f'))
    c.setFillColor(RED)
    c.setFont('MainFont-Bold', 14)
    c.drawString(rx + 15, ry + 135, 'Уникальность:')
    c.setFillColor(TXT_WHITE)
    c.setFont('MainFont', 12)
    c.drawString(rx + 15, ry + 110, 'Ни один конкурент в мире')
    c.drawString(rx + 15, ry + 90, 'не делает кросс-тендерную')
    c.drawString(rx + 15, ry + 70, 'детекцию монополий.')
    c.setFillColor(YELLOW)
    c.setFont('MainFont-Bold', 12)
    c.drawString(rx + 15, ry + 40, 'Это не только бизнес-инструмент —')
    c.drawString(rx + 15, ry + 20, 'это инструмент прозрачности')
    c.drawString(rx + 15, ry, 'госзакупок.')


def slide_alem_plus(c):
    draw_bg(c)
    draw_title(c, 'Инструменты Alem Plus', '6 из 6 — максимум')
    draw_footer(c, 11)

    y = H - 140
    tools = [
        ('1', 'PostgreSQL',       'Основная база данных', 'Хранение тендеров и анализов', GREEN),
        ('2', 'Redis',            'Кеш LLM-ответов', 'Повторный анализ = 0 секунд', GREEN),
        ('3', 'Embedder API',     '1024-мерные векторы', 'Семантическое представление', ACCENT2),
        ('4', 'Milvus',           'Векторный поиск', 'RAG + детекция монополий', ACCENT2),
        ('5', 'AlemLLM',          '247B параметров, MoE', 'Анализ + генерация', ACCENT),
        ('6', 'GitLab',           'CI/CD + деплой', 'gitlabapp.alem.ai', ACCENT),
    ]

    for num, name, desc, purpose, color in tools:
        draw_card(c, 60, y - 8, W - 120, 34, BG_CARD)
        c.setFillColor(color)
        c.setFont('MainFont-Bold', 16)
        c.drawString(75, y, num)
        c.setFillColor(TXT_WHITE)
        c.setFont('MainFont-Bold', 13)
        c.drawString(105, y, name)
        c.setFillColor(TXT_DIM)
        c.setFont('MainFont', 11)
        c.drawString(260, y, desc)
        c.setFillColor(TXT)
        c.setFont('MainFont', 11)
        c.drawString(480, y, purpose)
        y -= 42

    # Final quote
    draw_card(c, 100, 45, W - 200, 55, HexColor('#1a2744'))
    c.setFillColor(ACCENT)
    c.setFont('MainFont-Bold', 16)
    c.drawCentredString(W/2, 78,
        '80 000 поставщиков. 4 трлн тенге. Ноль ИИ-инструментов.')
    c.setFillColor(GREEN)
    c.setFont('MainFont-Bold', 18)
    c.drawCentredString(W/2, 52, 'TendrAI меняет это.')


# ========== MAIN ==========

def generate():
    out = os.path.join(os.path.dirname(__file__), 'TendrAI_PitchDeck.pdf')
    c = canvas.Canvas(out, pagesize=landscape(A4))
    c.setTitle('TendrAI — Pitch Deck')
    c.setAuthor('TendrAI Team')

    slides = [
        slide_cover,
        slide_team,
        slide_market,
        slide_problem,
        slide_how_it_works,
        slide_tech,
        slide_screenshots,
        slide_business,
        slide_mvp1,
        slide_mvp2,
        slide_mvp3,
        slide_alem_plus,
    ]

    for i, slide_fn in enumerate(slides):
        slide_fn(c)
        c.showPage()

    c.save()
    print(f'Pitch Deck saved: {out}')
    print(f'Slides: {len(slides)}')

if __name__ == '__main__':
    generate()
