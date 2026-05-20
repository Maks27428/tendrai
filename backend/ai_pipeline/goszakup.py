import re
import requests
from bs4 import BeautifulSoup


SEARCH_URL = 'https://goszakup.gov.kz/ru/search/lots'
ANNOUNCE_BASE = 'https://goszakup.gov.kz'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.5',
}


def search_tenders(query: str, page: int = 1, year: int = 2026) -> dict:
    params = {
        'filter[name]': query,
        'filter[year]': year,
        'page': page,
    }
    try:
        resp = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return _parse_results(resp.text)
    except requests.Timeout:
        return {'results': [], 'total': 0, 'error': 'Таймаут соединения с goszakup.gov.kz'}
    except requests.RequestException as e:
        return {'results': [], 'total': 0, 'error': f'Ошибка соединения: {str(e)[:200]}'}
    except Exception as e:
        return {'results': [], 'total': 0, 'error': f'Ошибка парсинга: {str(e)[:200]}'}


def _parse_results(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    tables = soup.find_all('table')
    target_table = None
    for table in tables:
        if table.find('a', href=re.compile(r'/announce/index/')):
            target_table = table
            break

    if not target_table:
        return {'results': [], 'total': 0}

    rows = target_table.find_all('tr')

    for row in rows[1:]:
        try:
            cells = row.find_all('td')
            if len(cells) < 7:
                continue

            outer = cells[0]

            lot_strong = outer.find('strong', recursive=False)
            lot_number = lot_strong.get_text(strip=True) if lot_strong else ''

            # cells[1..6] = announce title, description, quantity, amount, method, status
            announce_cell = cells[1]
            announce_link = announce_cell.find('a', href=re.compile(r'/announce/index/'))

            announce_url = ''
            announce_id = ''
            title = ''
            customer = ''

            if announce_link:
                href = announce_link.get('href', '')
                announce_url = href if href.startswith('http') else ANNOUNCE_BASE + href
                id_match = re.search(r'/announce/index/(\d+)', href)
                if id_match:
                    announce_id = id_match.group(1)
                title = announce_link.get_text(strip=True)

            small = announce_cell.find('small')
            if small:
                customer_text = small.get_text(strip=True)
                customer = re.sub(r'^Заказчик:\s*', '', customer_text)

            description = cells[2].get_text(strip=True)
            quantity = cells[3].get_text(strip=True)
            amount_raw = cells[4].get_text(strip=True)
            method = cells[5].get_text(strip=True)
            status_text = cells[6].get_text(strip=True)

            amount = _clean_amount(amount_raw)

            results.append({
                'lot_number': lot_number,
                'announce_id': announce_id,
                'title': title,
                'description': description,
                'customer': customer,
                'quantity': quantity,
                'amount': amount,
                'amount_raw': amount_raw,
                'method': method,
                'status': status_text,
                'url': announce_url,
            })
        except Exception:
            continue

    total = _parse_total(soup)
    return {
        'results': results,
        'total': total or len(results),
    }


def _clean_amount(raw: str) -> float:
    cleaned = re.sub(r'[^\d,.]', '', raw.replace('\xa0', ''))
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return 0


def _parse_total(soup) -> int:
    try:
        pagination = soup.find('ul', class_=re.compile(r'pagination'))
        if pagination:
            items = pagination.find_all('li')
            nums = []
            for item in items:
                link = item.find('a')
                if link:
                    text = link.get_text(strip=True)
                    if text.isdigit():
                        nums.append(int(text))
            if nums:
                return max(nums) * 50
    except Exception:
        pass
    return 0
