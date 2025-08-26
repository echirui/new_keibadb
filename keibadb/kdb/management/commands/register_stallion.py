import requests
from bs4 import BeautifulSoup
import re
from django.core.management.base import BaseCommand, CommandError
from kdb.models import Stallion

class Command(BaseCommand):
    help = 'Scrapes stallion information from netkeiba.com and registers/updates it in the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--horse_key',
            type=str,
            help='The netkeiba.com horse_key (ID) of the stallion to scrape.',
            required=True
        )
        parser.add_argument(
            '--force-update',
            action='store_true',
            help='Force update the stallion record even if father_key and mother_key are already present.',
        )

    def handle(self, *args, **options):
        horse_key = options['horse_key']
        force_update = options['force_update']
        url = f"https://db.netkeiba.com/horse/{horse_key}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        # Add check for existing record with non-null father_key and mother_key
        if not force_update and Stallion.objects.filter(horse_key=horse_key, father_key__isnull=False, mother_key__isnull=False).exists():
            self.stdout.write(self.style.SUCCESS(f"Stallion with horse_key: {horse_key} already has both father_key and mother_key. Skipping processing. Use --force-update to override."))
            return

        self.stdout.write(self.style.SUCCESS(f'Scraping data for stallion_key: {horse_key} from {url}'))

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
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

            # Extract Stallion Name
            stallion_name = ''
            horse_name_element = soup.find('div', class_='horse_title')
            if horse_name_element:
                horse_name_h1 = horse_name_element.find('h1')
                if horse_name_h1:
                    stallion_name = horse_name_h1.get_text(strip=True)

            # Extract birth_year
            birth_year = horse_info.get('生年月日', None)
            if birth_year and '年' in birth_year:
                birth_year = birth_year.split('年')[0] # Extract only the year

            # Extract sex
            sex = horse_info.get('性別', None) # Assuming '性別' is the key for sex

            # Extract prize
            prize = horse_info.get('獲得賞金 (中央)', None)
            if prize:
                # Clean prize money (remove 億, 万円, commas)
                prize = re.sub(r'[億万円,]', '', prize)

            # Extract trainer_name and trainer_key
            trainer_name = horse_info.get('調教師', None)
            trainer_id = None
            trainer_element = soup.find('th', string='調教師').find_next_sibling('td')
            if trainer_element:
                trainer_a_tag = trainer_element.find('a')
                if trainer_a_tag and 'href' in trainer_a_tag.attrs:
                    match_trainer = re.search(r'/trainer/(\d+)/', trainer_a_tag['href'])
                    if match_trainer:
                        trainer_id = match_trainer.group(1)

            # Extract owner_name and owner_key
            owner_name = horse_info.get('馬主', None)
            owner_id = None
            owner_element = soup.find('th', string='馬主').find_next_sibling('td')
            if owner_element:
                owner_a_tag = owner_element.find('a')
                if owner_a_tag and 'href' in owner_a_tag.attrs:
                    match_owner = re.search(r'/owner/(\d+)/', owner_a_tag['href'])
                    if match_owner:
                        owner_id = match_owner.group(1)

            # Extract farm_name (producer) and farm_key (producer_id)
            farm_name = horse_info.get('生産者', None)
            farm_key = None
            producer_element = soup.find('th', string='生産者').find_next_sibling('td')
            if producer_element:
                producer_a_tag = producer_element.find('a')
                if producer_a_tag and 'href' in producer_a_tag.attrs:
                    match_producer = re.search(r'/breeder/(\d+)/', producer_a_tag['href'])
                    if match_producer:
                        farm_key = match_producer.group(1)

            # Extract race_text (通算成績)
            race_text = horse_info.get('通算成績', None)

            # Extract relatives
            relatives = horse_info.get('近親馬', None)

            # Extract Father and Mother Keys (from pedigree_url)
            sire_id = None
            dam_id = None
            pedigree_url = f"https://db.netkeiba.com/horse/ajax_horse_pedigree.html?id={horse_key}"
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
                        
                        match_sire = None 
                        if sire_a_tag:
                            if 'href' in sire_a_tag.attrs:
                                match_sire = re.search(r'/(?:horse|ped)/([0-9a-fA-F]+)/', sire_a_tag['href'])
                                if match_sire:
                                    sire_id = match_sire.group(1)
                        
                        match_dam = None
                        if dam_a_tag:
                            if 'href' in dam_a_tag.attrs:
                                match_dam = re.search(r'/(?:horse|ped)/([0-9a-fA-F]+)/', dam_a_tag['href'])
                                if match_dam:
                                    dam_id = match_dam.group(1)

            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f"Error fetching pedigree URL: {e}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"An error occurred during pedigree parsing: {e}"))

            # Register/Update Stallion
            defaults = {
                'name': stallion_name,
                'birth_year': birth_year,
                'sex': sex,
                'prize': prize,
                'trainer_name': trainer_name,
                'trainer_key': trainer_id,
                'owner_name': owner_name,
                'owner_key': owner_id,
                'farm_name': farm_name,
                'farm_key': farm_key,
                'race_text': race_text,
                'relatives': relatives,
                'father_key': sire_id,
                'mother_key': dam_id,
            }
            # Remove None values to avoid overwriting existing data with None if not found
            defaults = {k: v for k, v in defaults.items() if v is not None}


            stallion, created = Stallion.objects.update_or_create(
                horse_key=horse_key,
                defaults=defaults
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully registered new Stallion: {stallion.name} (Key: {stallion.horse_key})'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated Stallion: {stallion.name} (Key: {stallion.horse_key})'))

        except requests.exceptions.RequestException as e:
            raise CommandError(f"Error fetching URL: {e}")
        except Exception as e:
            raise CommandError(f"An error occurred during scraping or saving: {e}")