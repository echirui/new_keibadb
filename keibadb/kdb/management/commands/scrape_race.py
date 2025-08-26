# -*- coding: utf8 -*-
"""
Web scraper
"""

import time
from collections import defaultdict
import csv
import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


REG = re.compile(
    "(?P<surface>.)(?P<direction>.).*(?P<distance>....)m / 天候 : (?P<weather>.+) / .+ : (?P<track_condition>.+) / 発走 : (?P<date>.....)"
)


class Command(BaseCommand):
    help = "データをスクレイピングする"

    def add_arguments(self, parser):
        parser.add_argument(
            "--data_path", type=str, help="data file path", required=False, default="../csv_data/"
        )
        parser.add_argument(
            "--start_year", type=int, help="Start year for scraping", required=False, default=2025
        )
        parser.add_argument(
            "--end_year", type=int, help="End year for scraping (exclusive)", required=False, default=2026
        )

    def handle(self, *args, **options):
        data_path = options["data_path"]
        start_year = options["start_year"]
        end_year = options["end_year"]
        create_race(data_path, start_year, end_year)


def create_race(data_path: str, year_start: int, year_end: int) -> None:
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    d_race_course = {
        "01": "札幌",
        "02": "函館",
        "03": "福島",
        "04": "新潟",
        "05": "東京",
        "06": "中山",
        "07": "中京",
        "08": "京都",
        "09": "阪神",
        "10": "小倉",
    }

    d_race_course_max = defaultdict(int)

    for year in range(year_start, year_end):
        sub_set = set()
        d_race_course_max = defaultdict(int)
        try:
            with open(data_path + str(year) + ".csv", encoding="utf8", newline="") as fs:
                csvreader = csv.reader(fs)
                for row in csvreader:
                    sub_set.add(row[0])
                    d_race_course_max[row[0][4:6]] = max(
                        int(row[0]), int(d_race_course_max[row[0][4:6]])
                    )
        except FileNotFoundError:
            # If the file doesn't exist, start with empty sets/dicts
            pass

        with open(
            data_path + str(year) + ".csv", "a", newline="", encoding="UTF-8"
        ) as f:
            for k_race, v_race in d_race_course.items():
                for y in range(1, 8):
                    # 開催日数分ループ（12日）
                    race_number = 0
                    for z in range(1, 13):
                        # generate race_id
                        day_id = f"{year}{k_race}{y:02}{z:02}"

                        race_number = 0
                        # レース数分ループ（12R）
                        for x in range(1, 13):
                            race_id = f"{day_id}{x:02}"
                            if int(race_id) < d_race_course_max[k_race]:
                                print(f"diffrence skip {race_id}")
                                continue
                            if race_id in sub_set:
                                race_number = x
                                continue
                            url = f"https://db.netkeiba.com/race/{race_id}"
                            try:
                                time.sleep(0.5)
                                r = requests.get(url, headers=header)
                                print(r.status_code)
                            except requests.exceptions.RequestException as e:
                                print(f"Error: {e}")
                                print("Retrying in 10 seconds...")
                                time.sleep(5)
                                r = requests.get(url)

                            soup = BeautifulSoup(
                                r.content.decode("euc-jp", "ignore"), "html.parser"
                            )

                            race_number = x
                            # result
                            table = soup.find(
                                "table", class_="race_table_01 nk_tb_common"
                            )
                            if not table:
                                print(f"no-data: {url}")
                                if race_number <= 1:
                                    break
                                continue
                            headers = [
                                th.text.strip()
                                for th in table.find_all("th")
                                if th.text.strip()
                            ]
                            excluded_headers = [
                                "調教ﾀｲﾑ",
                                "厩舎ｺﾒﾝﾄ",
                                "賞金(万円)",
                                "ﾀｲﾑ指数",
                            ]
                            data_rows = []
                            # lap time
                            lap = [
                                d.text.strip()
                                for d in soup.find_all("td", class_="race_lap_cell")
                            ]
                            if not lap:
                                lap = ["", ""]
                            # race info
                            table_title = soup.find("dl", class_="racedata fc")
                            smalltxt = (
                                soup.find("p", class_="smalltxt").text.strip().split()
                            )
                            title = table_title.find("h1").text.strip()
                            title_data = table_title.find("span").text.strip()
                            print(title_data)
                            title_data = title_data.replace("\n", "")
                            match_title = REG.match(title_data)
                            if not match_title:
                                print(f"no-match for title_data: {title_data} in {url}")
                                continue
                            title_dict = match_title.groupdict()

                            for tr in table.find_all("tr")[1:]:
                                row_data = {"race_id": race_id}
                                for i, td in enumerate(tr.find_all("td")):
                                    if i == 3:
                                        horse_name = td.find("a").text.strip()
                                        horse_id = td.find("a")["href"]
                                        row_data[headers[i]] = horse_name + horse_id
                                    else:
                                        row_data[headers[i]] = td.text.strip()
                                    for excluded_header in excluded_headers:
                                        row_data.pop(excluded_header, None)

                                data_rows.append(row_data)

                            for d in data_rows:
                                weight = ""
                                weight_diff = ""
                                if d["馬体重"] == "計不":
                                    weight = ""
                                    weight_diff = ""
                                else:
                                    weight = int(d["馬体重"].split("(")[0])
                                    weight_diff = int(
                                        d["馬体重"].split("(")[1][:-1].replace("+", "")
                                    )
                                race_data = [
                                    d["race_id"],
                                    d["馬名"].split("/")[0],
                                    d["馬名"].split("/")[2],
                                    d["騎手"],
                                    d["馬番"],
                                    d["タイム"],
                                    d["単勝"],
                                    d["通過"],
                                    d["着順"],
                                    weight,
                                    weight_diff,
                                    d["性齢"][0],
                                    d["性齢"][1],
                                    d["斤量"],
                                    d["上り"],
                                    d["人気"],
                                    title,
                                    smalltxt[0],
                                    smalltxt[1],
                                    smalltxt[2],
                                    title_dict["surface"],
                                    title_dict["distance"],
                                    title_dict["direction"],
                                    title_dict["track_condition"],
                                    title_dict["weather"],
                                    title_dict["date"],
                                    k_race,
                                    v_race,
                                    lap[0].replace(" ", ""),
                                    lap[1].replace(" ", ""),
                                    d["調教師"].split()[0][1],
                                    d["調教師"].split()[1],
                                    d["馬主"],
                                ]
                                csv.writer(f).writerow(race_data)

                        if race_number <= 1:
                            break
        print("終了")
