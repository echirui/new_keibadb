# レーステーブルの定義
kdb_race:
  columns:
    race_id:
      type: string
      nullable: False
      description: レースID
    race_name:
      type: string
      nullable: False
      description: レース名
    date:
      type: date
      nullable: False
      description: 開催日
    details:
      type: string
      nullable: False
      description: レース詳細
    debut:
      type: boolean
      nullable: False
      default: False
      description: デビュー戦
    race_class:
      type: string
      nullable: False
      description: レースクラス
    surface:
      type: string
      nullable: False
      description: 馬場
    distance:
      type: integer
      nullable: False
      description: 距離
    direction:
      type: string
      nullable: False
      description: 方向
    track_condition:
      type: string
      nullable: False
      description: 馬場状態
    weather:
      type: string
      nullable: False
      description: 天気
    start_at:
      type: string
      nullable: False
      description: 発走時間
    venue_code:
      type: string
      nullable: False
      description: 競馬場コード
    venue:
      type: string
      nullable: False
      description: 競馬場
    lap:
      type: string
      nullable: False
      description: ラップタイム
    pace:
      type: string
      nullable: False
      description: ペース

# 騎手テーブルの定義
kdb_jockey:
  columns:
    name:
      type: string
      nullable: False
      description: 騎手名
    birth_year:
      type: string
      nullable: True
      description: 生年月日

# 馬テーブルの定義
kdb_horse:
  columns:
    horse_key:
      type: string
      nullable: False
      primary_key: True
      description: 馬ID
    name:
      type: string
      nullable: False
      description: 馬名
    birth_year:
      type: string
      nullable: True
      description: 生年月日
    coat_color:
      type: string
      nullable: True
      description: 毛色
    father_key:
      type: string
      nullable: True
      description: 父馬ID
    mother_key:
      type: string
      nullable: True
      description: 母馬ID
    relatives:
      type: string
      nullable: True
      description: 近親
    prize:
      type: string
      nullable: True
      description: 獲得賞金
    owner_name:
      type: string
      nullable: True
      description: 馬主名
    owner_key:
      type: string
      nullable: True
      description: 馬主ID
    farm_name:
      type: string
      nullable: True
      description: 生産牧場
    farm_key:
      type: string
      nullable: True
      description: 生産牧場ID

# オッズテーブルの定義
kdb_odds:
  columns:
    race:
      type: integer
      nullable: False
      description: レースID
    win_odds:
      type: json
      nullable: True
      description: 単勝オッズ
    show_odds:
      type: json
      nullable: True
      description: 複勝オッズ
    quinella_odds:
      type: json
      nullable: True
      description: 馬連オッズ
    quinella_place_odds:
      type: json
      nullable: True
      description: ワイドオッズ
    trio_odds:
      type: json
      nullable: True
      description: 3連複オッズ

# 種牡馬テーブルの定義
kdb_stallion:
  columns:
    horse_key:
      type: string
      nullable: False
      primary_key: True
      description: 種牡馬ID
    name:
      type: string
      nullable: False
      description: 種牡馬名
    father_key:
      type: string
      nullable: True
      description: 父馬ID
    mother_key:
      type: string
      nullable: True
      description: 母馬ID
    birth_year:
      type: string
      nullable: True
      description: 生年月日
    sex:
      type: string
      nullable: True
      description: 性別
    prize:
      type: string
      nullable: True
      description: 獲得賞金
    trainer_name:
      type: string
      nullable: True
      description: 調教師名
    trainer_key:
      type: string
      nullable: True
      description: 調教師ID
    owner_name:
      type: string
      nullable: True
      description: 馬主名
    owner_key:
      type: string
      nullable: True
      description: 馬主ID
    farm_name:
      type: string
      nullable: True
      description: 生産牧場
    farm_key:
      type: string
      nullable: True
      description: 生産牧場ID
    race_text:
      type: string
      nullable: True
      description: 戦績
    relatives:
      type: string
      nullable: True
      description: 近親

# 競走成績テーブルの定義
kdb_horseracing:
  columns:
    race_id:
      type: string
      nullable: False
      default: ''
      description: レースID
    horse:
      type: integer
      nullable: False
      description: 馬ID
    horse_key:
      type: string
      nullable: False
      default: ''
      description: 馬ID
    jockey:
      type: integer
      nullable: False
      description: 騎手ID
    horse_number:
      type: integer
      nullable: False
      default: 0
      description: 馬番
    running_time:
      type: string
      nullable: False
      default: ''
      description: 走破タイム
    odds:
      type: decimal
      nullable: False
      default: 0.0
      description: 単勝オッズ
    passing_order:
      type: string
      nullable: False
      default: ''
      description: 通過順
    finish_position:
      type: integer
      nullable: False
      default: 0
      description: 着順
    weight:
      type: integer
      nullable: True
      description: 馬体重
    weight_change:
      type: integer
      nullable: True
      description: 馬体重増減
    sex:
      type: string
      nullable: False
      default: ''
      description: 性別
    age:
      type: integer
      nullable: False
      default: 0
      description: 年齢
    handicap:
      type: decimal
      nullable: False
      default: 0.0
      description: 斤量
    final_600m_time:
      type: decimal
      nullable: True
      description: 上がり3F
    popularity:
      type: integer
      nullable: False
      default: 0
      description: 人気
    race_name:
      type: string
      nullable: False
      default: ''
      description: レース名
    date:
      type: date
      nullable: False
      default: current_timestamp
      description: 開催日
    details:
      type: string
      nullable: False
      default: ''
      description: レース詳細
    debut:
      type: boolean
      nullable: False
      default: False
      description: デビュー戦
    race_class:
      type: string
      nullable: False
      default: ''
      description: レースクラス
    surface:
      type: string
      nullable: False
      default: ''
      description: 馬場
    distance:
      type: integer
      nullable: False
      default: 0
      description: 距離
    direction:
      type: string
      nullable: False
      default: ''
      description: 方向
    track_condition:
      type: string
      nullable: False
      default: ''
      description: 馬場状態
    weather:
      type: string
      nullable: False
      default: ''
      description: 天気
    start_at:
      type: string
      nullable: False
      default: ''
      description: 発走時間
    venue_code:
      type: string
      nullable: False
      default: ''
      description: 競馬場コード
    venue:
      type: string
      nullable: False
      default: ''
      description: 競馬場
    lap:
      type: string
      nullable: False
      default: ''
      description: ラップタイム
    pace:
      type: string
      nullable: False
      default: ''
      description: ペース
    training_center:
      type: string
      nullable: False
      default: ''
      description: 所属
    trainer_name:
      type: string
      nullable: False
      default: ''
      description: 調教師名
    owner:
      type: string
      nullable: False
      default: ''
      description: 馬主
    farm:
      type: string
      nullable: False
      default: ''
      description: 生産牧場


