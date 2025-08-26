# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from django.db import transaction
from kdb.models import Race, Horse, Jockey, HorseRacing, Odds
import io

class Command(BaseCommand):
    help = 'Imports race data from a specified CSV file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file',
            type=str,
            help='The path to the CSV file to be imported.',
            required=True
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.stdout.write(self.style.SUCCESS(f'Starting import from {csv_file_path}...'))

        try:
            headers = [
                'race_id', '馬名', '馬ID', '騎手', '馬番', 'タイム', '単勝', '通過', '着順',
                '馬体重', '馬体重増減', '性別', '年齢', '斤量', '上り', '人気', 'レース名',
                '開催日', '開催場所', 'レース種別', 'コース', '距離', '方向', '馬場状態',
                '天気', '発走時間', '競馬場コード', '競馬場名', 'ラップタイム', 'pace', '調教師所属',
                '調教師名', '馬主'
            ]
            df = pd.read_csv(
                csv_file_path,
                header=None,
                names=headers,
                encoding='utf-8',
                encoding_errors='ignore'
            )
            
            df['開催日'] = df['開催日'].str.strip()
            df['開催日'] = pd.to_datetime(df['開催日'], format='%Y年%m月%d日', errors='coerce')
            df.dropna(subset=['開催日'], inplace=True)

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {csv_file_path}'))
            return
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred during file reading: {e}'))
            return

        races_processed = 0
        horseracing_records_processed = 0

        try:
            with transaction.atomic():
                for race_id, group in df.groupby('race_id'):
                    races_processed += 1
                    race_info = group.iloc[0]

                    race, _ = Race.objects.update_or_create(
                        race_id=race_id,
                        defaults={
                            'race_name': race_info['レース名'],
                            'date': race_info['開催日'],
                            'venue': race_info['開催場所'],
                            'venue_code': race_info['競馬場コード'],
                            'race_class': race_info['レース種別'],
                            'surface': race_info['コース'],
                            'distance': race_info['距離'],
                            'direction': race_info['方向'],
                            'track_condition': race_info['馬場状態'],
                            'weather': race_info['天気'],
                            'start_at': race_info['発走時間'],
                            'lap': race_info['ラップタイム'],
                            'pace': race_info['pace'],
                        }
                    )

                    win_odds_dict = group.set_index('馬番')['単勝'].to_dict()
                    Odds.objects.update_or_create(
                        race=race,
                        defaults={'win_odds': win_odds_dict}
                    )

                    for _, row in group.iterrows():
                        horseracing_records_processed += 1
                        
                        # --- Preprocess data to handle NaN and other errors ---
                        try:
                            finish_position = int(row['着順'])
                        except (ValueError, TypeError):
                            finish_position = 0

                        weight = row['馬体重'] if pd.notna(row['馬体重']) else None
                        weight_change = row['馬体重増減'] if pd.notna(row['馬体重増減']) else None
                        final_600m_time = row['上り'] if pd.notna(row['上り']) else None
                        
                        try:
                            odds = float(row['単勝'])
                        except (ValueError, TypeError):
                            odds = 0.0

                        try:
                            popularity = int(row['人気'])
                        except (ValueError, TypeError):
                            popularity = 0

                        try:
                            handicap = float(row['斤量'])
                        except (ValueError, TypeError):
                            handicap = 0.0
                        # --- End Preprocessing ---

                        horse, _ = Horse.objects.update_or_create(
                            horse_key=row['馬ID'],
                            defaults={'name': row['馬名'], 'owner_name': row['馬主']}
                        )

                        jockey, _ = Jockey.objects.get_or_create(name=row['騎手'])

                        HorseRacing.objects.update_or_create(
                            race_id=race.race_id,
                            horse=horse,
                            defaults={
                                'horse_key': horse.horse_key,
                                'jockey': jockey,
                                'horse_number': row['馬番'],
                                'finish_position': finish_position,
                                'running_time': row['タイム'],
                                'odds': odds,
                                'popularity': popularity,
                                'weight': weight,
                                'weight_change': weight_change,
                                'sex': row['性別'],
                                'age': row['年齢'],
                                'handicap': handicap,
                                'final_600m_time': final_600m_time,
                                'passing_order': row['通過'],
                                'training_center': row['調教師所属'],
                                'trainer_name': row['調教師名'],
                                'owner': row['馬主'],
                                'race_name': race.race_name,
                                'date': race.date,
                                'venue': race.venue,
                                'race_class': race.race_class,
                                'surface': race.surface,
                                'distance': race.distance,
                                'direction': race.direction,
                                'track_condition': race.track_condition,
                                'weather': race.weather,
                                'start_at': race.start_at,
                                'venue_code': race.venue_code,
                                'lap': race.lap,
                                'pace': race.pace,
                            }
                        )
            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported {races_processed} races and '
                f'{horseracing_records_processed} horse racing records.'
            ))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred during the import process: {e}'))