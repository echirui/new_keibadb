import requests
from bs4 import BeautifulSoup
import sys
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from kdb.models import Horse, Stallion # HorseモデルとStallionモデルをインポート

class Command(BaseCommand):
    help = 'Scrapes horse information from netkeiba.com and saves it to the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--horse_id',
            type=str,
            help='The netkeiba.com horse ID to scrape (e.g., 2012104889).',
            required=True
        )

    def handle(self, *args, **options):
        horse_id = options['horse_id']
        url = f"https://db.netkeiba.com/horse/{horse_id}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        # Check if horse already has father_key and mother_key
        try:
            horse = Horse.objects.get(horse_key=horse_id)
            if horse.father_key and horse.mother_key:
                self.stdout.write(self.style.SUCCESS(f"Horse ID: {horse_id} already has parent information. Skipping scraping."))
                return
        except Horse.DoesNotExist:
            pass # Horse does not exist, proceed with scraping

        self.stdout.write(self.style.SUCCESS(f'Scraping data for horse ID: {horse_id} from {url}'))

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.content, 'html.parser')

            # --- Extracting information ---
            horse_info = {}
            profile_table = soup.find('table', class_='db_prof_table')
            if profile_table:
                for row in profile_table.find_all('tr'):
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        key = th.get_text(strip=True)
                        value = td.get_text(strip=True)
                        horse_info[key] = value

            birth_date = horse_info.get('生年月日', 'N/A')
            trainer = horse_info.get('調教師', 'N/A')
            owner = horse_info.get('馬主', 'N/A')
            producer = horse_info.get('生産者', 'N/A')
            origin = horse_info.get('産地', 'N/A')

            # 調教師ID
            trainer_id = 'N/A'
            trainer_element = soup.find('th', string='調教師').find_next_sibling('td')
            if trainer_element:
                trainer_a_tag = trainer_element.find('a')
                if trainer_a_tag and 'href' in trainer_a_tag.attrs:
                    match = re.search(r'/trainer/(\d+)/', trainer_a_tag['href'])
                    if match:
                        trainer_id = match.group(1)

            # 馬主ID
            owner_id = 'N/A'
            owner_element = soup.find('th', string='馬主').find_next_sibling('td')
            if owner_element:
                owner_a_tag = owner_element.find('a')
                if owner_a_tag and 'href' in owner_a_tag.attrs:
                    match = re.search(r'/owner/(\d+)/', owner_a_tag['href'])
                    if match:
                        owner_id = match.group(1)

            # 生産者ID
            producer_id = 'N/A'
            producer_element = soup.find('th', string='生産者').find_next_sibling('td')
            if producer_element:
                producer_a_tag = producer_element.find('a')
                if producer_a_tag and 'href' in producer_a_tag.attrs:
                    match = re.search(r'/breeder/(\d+)/', producer_a_tag['href'])
            if match:
                producer_id = match.group(1)

            # 獲得賞金 (中央)
            prize_money_central = 'N/A'
            prize_money_element = soup.find('th', string='獲得賞金 (中央)') # 修正
            if prize_money_element:
                next_td = prize_money_element.find_next_sibling('td')
                if next_td:
                    prize_text = next_td.get_text(strip=True)
                    match = re.search(r'(\d[\d,]*)(億)?(\d[\d,]*万円)', prize_text)
                    if match:
                        if match.group(2):
                            oku = int(match.group(1).replace(',','')) * 10000
                            man = int(match.group(3).replace('万円','').replace(',',''))
                            prize_money_central = f"{oku + man}万円"
                        else:
                            prize_money_central = match.group(1) + match.group(3)

            # 通算成績
            career_record = 'N/A'
            career_record_element = soup.find('th', string='通算成績')
            if career_record_element:
                next_td = career_record_element.find_next_sibling('td')
                if next_td:
                    career_record = next_td.get_text(strip=True)

            # 近親馬
            related_horses = 'N/A'
            related_horses_ids = [] # IDを格納するリスト
            related_horses_element = soup.find('th', string='近親馬') # 修正
            if related_horses_element:
                next_td = related_horses_element.find_next_sibling('td')
                if next_td:
                    related_horses_list = []
                    for a_tag in next_td.find_all('a'):
                        horse_name = a_tag.get_text(strip=True)
                        related_horses_list.append(horse_name)
                        if 'href' in a_tag.attrs:
                            match = re.search(r'/horse/(\d+)/', a_tag['href'])
                            if match:
                                related_horses_ids.append(match.group(1))
            related_horses = ', '.join(related_horses_list)

            # 血統父, 血統母
            sire = 'N/A'
            sire_id = 'N/A'
            dam = 'N/A'
            dam_id = 'N/A'
            pedigree_url = f"https://db.netkeiba.com/horse/ajax_horse_pedigree.html?id={horse_id}"
            try:
                pedigree_response = requests.get(pedigree_url, headers=headers)
                pedigree_response.raise_for_status()
                pedigree_soup = BeautifulSoup(pedigree_response.content.decode('euc-jp', 'ignore'), 'html.parser')

                blood_table = pedigree_soup.find('table', class_='blood_table')
                if blood_table:
                    td_elements = blood_table.find_all('td')
                    if len(td_elements) >= 3:
                        sire_a_tag = td_elements[0].find('a')
                        dam_a_tag = td_elements[2].find('a')
                        if sire_a_tag:
                            sire = sire_a_tag.get_text(strip=True)
                            if 'href' in sire_a_tag.attrs:
                                match = re.search(r'/(?:horse|ped)/([0-9a-fA-F]+)/', sire_a_tag['href'])
                                if match:
                                    sire_id = match.group(1)
                        if dam_a_tag:
                            dam = dam_a_tag.get_text(strip=True)
                            if 'href' in dam_a_tag.attrs:
                                match = re.search(r'/(?:horse|ped)/([0-9a-fA-F]+)/', dam_a_tag['href'])
                                if match:
                                    dam_id = match.group(1)

            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f"Error fetching pedigree URL: {e}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"An error occurred during pedigree parsing: {e}"))

            # --- Save to Database ---
            horse_name_element = soup.find('div', class_='horse_title')
            if horse_name_element:
                horse_name_h1 = horse_name_element.find('h1')
                if horse_name_h1:
                    horse_name_from_h1 = horse_name_h1.get_text(strip=True)
                else:
                    horse_name_from_h1 = '' # h1が見つからない場合
            else:
                horse_name_from_h1 = '' # div.horse_titleが見つからない場合

            self.stdout.write(f"DEBUG: Horse name from H1 (before save): '{horse_name_from_h1}'")

            with transaction.atomic():
                # 1. Stallionモデルに父と母を登録/更新
                father_stallion = None
                if sire_id != 'N/A':
                    father_stallion, _ = Stallion.objects.update_or_create(
                        horse_key=sire_id,
                        defaults={'name': sire}
                    )

                mother_stallion = None
                if dam_id != 'N/A':
                    mother_stallion, _ = Stallion.objects.update_or_create(
                        horse_key=dam_id,
                        defaults={'name': dam}
                    )

                # 2. Horseモデルを更新
                horse, created = Horse.objects.update_or_create(
                    horse_key=horse_id,
                    defaults={
                        'name': horse_name_from_h1, # 馬名
                        'birth_year': birth_date, # 生年月日
                        'father_key': sire_id if sire_id != 'N/A' else None, # 父のhorse_key
                        'mother_key': dam_id if dam_id != 'N/A' else None, # 母のhorse_key
                        'owner_name': owner, # 馬主
                        'relatives': related_horses, # 近親馬
                        # prize は更新しない
                        # coat_color, farm_name, farm_key, owner_key, trainer_name, trainer_key はスクレイピングしていないので更新しない
                    }
                )

            self.stdout.write(self.style.SUCCESS(f"Successfully scraped and saved data for {horse.name} (ID: {horse_id})."))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching URL: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred during scraping or saving: {e}"))