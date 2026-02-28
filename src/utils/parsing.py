import html
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup


def get_products_sum_date(html_content:str) -> tuple[str, int | None, datetime]:
    soup = BeautifulSoup(html_content, 'html.parser')

    container = soup.find('div', id='fido_cheque_container')
    decoded_html = html.unescape(container.text)

    inner_soup = BeautifulSoup(decoded_html, 'html.parser')

    products = ''
    for b_tag in inner_soup.find_all('b'):
        text = b_tag.get_text(strip=True)
        if text and text[0].isdigit() and ':' in text:
            products += text[3:].split(',')[0] + ', '
    products = products[:-2]

    final_sum = None
    for b_tag in inner_soup.find_all('b'):
        text = b_tag.get_text(strip=True)
        if 'ИТОГ' in text:
            parent = b_tag.find_parent('td')
            if parent:
                row = parent.find_parent('tr')
                tds = row.find_all('td')
                if len(tds) >= 2:
                    final_sum = int(tds[1].get_text(strip=True)[1:-3])

    receipt_date = None
    for span in inner_soup.find_all('span'):
        text = span.get_text(strip=True)
        if len(text) == 16 and text[2] == '.' and text[5] == '.' and text[10] == ' ':
            receipt_date = datetime.strptime(text, '%d.%m.%Y %H:%M')
            break


    return products, final_sum, receipt_date


async def parse_cheque(url: str) -> tuple[str, int | None, datetime]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5), ssl=False) as response:
            html_content = await response.text()
            return get_products_sum_date(html_content)
