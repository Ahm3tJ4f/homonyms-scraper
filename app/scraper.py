# scraper.py

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://obastan.com'


def remove_em_tags(text):
    """Remove content within <em> tags."""
    return re.sub(r'<em>.*?</em>', '', text)


def get_text_without_tags(html_content):
    """Convert HTML content to text and remove leading/trailing whitespace."""
    return BeautifulSoup(html_content, 'html.parser').get_text().strip()


def extract_meaning_and_usage(clean_text):
    """Split the clean text into actual meaning and usage examples."""
    sentences = re.split(r'(?<=[.!?]) +', clean_text)
    actual_meaning = re.sub(r"^\w+\s?(I|II|III|IV|V|VI|VII|VIII|IX|X)\s", '', sentences[0]) if sentences else ''
    usage_examples = ' '.join(sentences[1:]) if len(sentences) > 1 else ''
    return actual_meaning, usage_examples


def clean_meaning(meaning):
    """Clean the meaning text by removing unwanted characters."""
    return re.sub(r'\[\s*\]', '', meaning).strip()


def scrape_word_details(href_link):
    """Scrape the details of a word from its individual page."""
    full_url = f'{BASE_URL}{href_link}'
    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    details = []
    for p in soup.find('div', itemprop='articleBody').find_all('p', recursive=False):
        part_of_speech = p.find('em').text if p.find('em') else None
        origin_match = re.search(r'\[\s*<em>(.*?)<\/em>\s*\]', str(p))
        origin = origin_match.group(1) if origin_match else None
        clean_p_text = get_text_without_tags(remove_em_tags(str(p)))
        actual_meaning, usage_examples = extract_meaning_and_usage(clean_p_text)
        details.append({
            'part_of_speech': part_of_speech,
            'origin': origin,
            'meaning': clean_meaning(actual_meaning),
            'usage': usage_examples
        })
    return details


def scrape_main_list(page_number):
    """Scrape the main list of words from the given page number."""
    page_url = f'{BASE_URL}/azerbaycan-dilinin-omonimler-lugeti/?l=az&p={page_number}'
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    words = [{'word': li.find('h3', class_='wli-title').text.strip(),
              'link': li.find('a', class_='wli-link')['href'].strip()}
             for li in soup.find_all('li', class_='wli')]
    return words


def main_scrape():
    all_details = []
    for page in range(1, 17):
        print(f'Scraping page {page}...')
        words_list = scrape_main_list(page)
        if not words_list:
            print(f"No words found on page {page}. Stopping scrape.")
            break
        for word_info in words_list:
            details = scrape_word_details(word_info['link'])
            for detail in details:
                detail['word'] = word_info['word']  # Assign word here to ensure it's correctly associated
                all_details.append(detail)
    # Here you would insert all_details into the database instead of creating a DataFrame
    print("Scraping done. Total words details scraped:", len(all_details))
    return all_details


if __name__ == "__main__":
    main_scrape()
