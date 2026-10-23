# 데이터 출처와 이용 조건

## 차량 메타데이터
`data/cars_source.json` — 제조사 공개 제원과 위키백과를 참고해 직접 정리. 트림(`trim`) 기준 값이며 연식·시장에 따라 다를 수 있음. 비어 있던 치수·중량은 영문 위키백과 인포박스 값으로 채우고 `filledFromWiki`에 기록.

## 외부 문서
한국어·영어 위키백과 본문 — CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). 원문 URL은 `cars_enriched.json`의 각 문서 `url`과 Chroma 청크 메타데이터에 기록.

## 차량 사진 (Wikimedia Commons)
각 사진의 저작자와 라이선스를 화면에 함께 표시한다.

| 차량 | 파일 | 저작자 | 라이선스 |
|---|---|---|---|
| 1886 벤츠 파텐트 모토르바겐 | [1885Benz.jpg](https://commons.wikimedia.org/wiki/File:1885Benz.jpg) | Supplied by Benz to William Worby Beaumont and used in his book Motor Vehicles and Motors (1900) | Public domain |
| 1908 포드 모델 T | [1925_Ford_Model_T_touring.jpg](https://commons.wikimedia.org/wiki/File:1925_Ford_Model_T_touring.jpg) | ModelTMitch | Public domain |
| 1936 메르세데스-벤츠 260 D | [Mercedes-Benz-Museum_2015-01_by-RaBoe_116.jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz-Museum_2015-01_by-RaBoe_116.jpg) | © Ra Boe / Wikipedia | CC BY-SA 3.0 de |
| 1938 폭스바겐 비틀 | [VW_Käfer_Baujahr_1966.jpg](https://commons.wikimedia.org/wiki/File:VW_K%C3%A4fer_Baujahr_1966.jpg) | Vwexport1300 | CC BY-SA 3.0 |
| 1941 윌리스 MB | [Covered_Willy's_jeep_Wings_Over_Wine_Country_2007.JPG](https://commons.wikimedia.org/wiki/File:Covered_Willy%27s_jeep_Wings_Over_Wine_Country_2007.JPG) | BrokenSphere | CC BY 3.0 |
| 1948 시트로엥 2CV | [Citroen_2CV_1X7A7979.jpg](https://commons.wikimedia.org/wiki/File:Citroen_2CV_1X7A7979.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 1954 메르세데스-벤츠 300 SL | [Fox_Classic_Car_Collection,_2008_(02).JPG](https://commons.wikimedia.org/wiki/File:Fox_Classic_Car_Collection,_2008_(02).JPG) | Bahnfrend | CC BY-SA 4.0 |
| 1955 시트로엥 DS | [Bornholm_Rundt_2012_(2012-07-08),_by_Klugschnacker_modified.jpg](https://commons.wikimedia.org/wiki/File:Bornholm_Rundt_2012_(2012-07-08),_by_Klugschnacker_modified.jpg) | Klugschnacker | CC BY-SA 3.0 |
| 1959 모리스 미니 | [Morris_Mini-Minor_1959_(621_AOK).jpg](https://commons.wikimedia.org/wiki/File:Morris_Mini-Minor_1959_(621_AOK).jpg) | DeFacto | CC BY-SA 2.5 |
| 1963 포르쉐 911 (초대) | [Porsche_911E_ca_1969.jpg](https://commons.wikimedia.org/wiki/File:Porsche_911E_ca_1969.jpg) | Charles01 | CC BY-SA 3.0 |
| 1964 포드 머스탱 (1세대) | [1965_Ford_Mustang_2D_Hardtop_Front.jpg](https://commons.wikimedia.org/wiki/File:1965_Ford_Mustang_2D_Hardtop_Front.jpg) | Kroelleboelle | CC BY-SA 3.0 |
| 1966 람보르기니 미우라 | [1971_Lamborghini_Miura_P400_SV.jpg](https://commons.wikimedia.org/wiki/File:1971_Lamborghini_Miura_P400_SV.jpg) | Chelsea Jay | CC BY-SA 4.0 |
| 1975 현대 포니 | [Hyundai_Pony_II_CX_1400_GLS_110_Beige_(1).jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Pony_II_CX_1400_GLS_110_Beige_(1).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 1976 폭스바겐 골프 GTI (1세대) | [Volkswagen_Golf_1-2_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Volkswagen_Golf_1-2_(cropped).jpg) | Kazuyanagae | CC BY-SA 4.0 |
| 1980 아우디 콰트로 | [1985_Audi_Quattro.jpg](https://commons.wikimedia.org/wiki/File:1985_Audi_Quattro.jpg) | Calreyn88 | CC0 |
| 1986 BMW M3 (E30) | [BMW M3 (E30) IMG 4388.jpg](https://commons.wikimedia.org/wiki/File:BMW_M3_(E30)_IMG_4388.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 1989 마쯔다 MX-5 (NA) | [Eunos.jpg](https://commons.wikimedia.org/wiki/File:Eunos.jpg) | Francigf at en.wikipedia | CC BY-SA 3.0 |
| 1990 혼다 NSX (1세대) | [Honda_NSX_red.jpg](https://commons.wikimedia.org/wiki/File:Honda_NSX_red.jpg) | ed g2s • talk | CC BY-SA 3.0 |
| 1992 맥라렌 F1 | [1996_McLaren_F1_Chassis_No_63_6.1_Front.jpg](https://commons.wikimedia.org/wiki/File:1996_McLaren_F1_Chassis_No_63_6.1_Front.jpg) | Chelsea Jay | CC BY-SA 4.0 |
| 1997 토요타 프리우스 (1세대) | [1998_Toyota_Prius_NHW10_Silver_Strara_Metallic_(front).jpg](https://commons.wikimedia.org/wiki/File:1998_Toyota_Prius_NHW10_Silver_Strara_Metallic_(front).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2005 부가티 베이론 16.4 | [Bugatti_Veyron_16.4_–_Frontansicht_(1),_5._April_2012,_Düsseldorf.jpg](https://commons.wikimedia.org/wiki/File:Bugatti_Veyron_16.4_%E2%80%93_Frontansicht_(1),_5._April_2012,_D%C3%BCsseldorf.jpg) | M 93 | CC BY-SA 3.0 de |
| 2008 테슬라 로드스터 (1세대) | [Roadster_San_Diego.jpg](https://commons.wikimedia.org/wiki/File:Roadster_San_Diego.jpg) | Tesla Motors Inc. | Copyrighted free use |
| 2010 닛산 리프 (1세대) | [2017_Nissan_LEAF_(ZE0_MY17)_hatchback_(2018-11-02)_01.jpg](https://commons.wikimedia.org/wiki/File:2017_Nissan_LEAF_(ZE0_MY17)_hatchback_(2018-11-02)_01.jpg) | EurovisionNim | CC BY-SA 4.0 |
| 2012 테슬라 모델 S | [Tesla_Model_S_(Facelift_ab_04-2016)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Tesla_Model_S_(Facelift_ab_04-2016)_(cropped).jpg) | Peteratkins | CC BY-SA 4.0 |
| 2017 기아 스팅어 | [Kia_Stinger_Facelift_IMG_4468.jpg](https://commons.wikimedia.org/wiki/File:Kia_Stinger_Facelift_IMG_4468.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2019 포르쉐 911 카레라 (992) | [2025_Porsche_992_Carrera_convertible_DSC_7026.jpg](https://commons.wikimedia.org/wiki/File:2025_Porsche_992_Carrera_convertible_DSC_7026.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2019 포르쉐 타이칸 | [2020_Porsche_Taycan_4S_79kWh_Front.jpg](https://commons.wikimedia.org/wiki/File:2020_Porsche_Taycan_4S_79kWh_Front.jpg) | Vauxford | CC BY-SA 4.0 |
| 2020 제네시스 G80 (3세대) | [Genesis_G80_IAA_2021_1X7A0229.jpg](https://commons.wikimedia.org/wiki/File:Genesis_G80_IAA_2021_1X7A0229.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2021 현대 아이오닉 5 | [Hyundai_Ioniq_5_AWD_Techniq-Paket_–_f_31122024.jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Ioniq_5_AWD_Techniq-Paket_%E2%80%93_f_31122024.jpg) | © M 93 | CC BY-SA 3.0 de |
| 2021 메르세데스-벤츠 EQS | [Mercedes-Benz_V297_Classic-Days_2022_DSC_0016.jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz_V297_Classic-Days_2022_DSC_0016.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2021 기아 EV6 | [2021_Kia_EV6_GT-Line_S.jpg](https://commons.wikimedia.org/wiki/File:2021_Kia_EV6_GT-Line_S.jpg) | Vauxford | CC BY-SA 4.0 |
| 2022 BYD 씰 | [2022_BYD_Seal.jpg](https://commons.wikimedia.org/wiki/File:2022_BYD_Seal.jpg) | User3204 | CC BY-SA 4.0 |
| 2022 현대 아이오닉 6 | [2023_Hyundai_Ioniq_6_Limited,_front_4.27.23.jpg](https://commons.wikimedia.org/wiki/File:2023_Hyundai_Ioniq_6_Limited,_front_4.27.23.jpg) | Kevauto | CC BY-SA 4.0 |
| 2023 테슬라 사이버트럭 | [2024_Tesla_Cybertruck_Foundation_Series,_front_left_(Greenwich).jpg](https://commons.wikimedia.org/wiki/File:2024_Tesla_Cybertruck_Foundation_Series,_front_left_(Greenwich).jpg) | Mr.choppers | CC BY-SA 3.0 |
| 2024 포르쉐 마칸 일렉트릭 | [Porsche_Macan_4_IMG_2153.jpg](https://commons.wikimedia.org/wiki/File:Porsche_Macan_4_IMG_2153.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 2024 기아 EV3 | [Kia_EV3_GT-Line_Automesse_Ludwigsburg_2025_DSC_2635_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Kia_EV3_GT-Line_Automesse_Ludwigsburg_2025_DSC_2635_(cropped).jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2025 현대 아이오닉 9 | [Hyundai_Ioniq_9_IMG_5950.jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Ioniq_9_IMG_5950.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2025 메르세데스-벤츠 CLA (3세대) | [Mercedes-Benz CLA 250+, Heddesheim (P1048671).jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz_CLA_250%2B,_Heddesheim_(P1048671).jpg) | Matti Blume | CC BY-SA 4.0 |
| 2025 기아 EV4 | [Kia_EV4_GT-Line_Automesse_Ludwigsburg_2025_DSC_2535.jpg](https://commons.wikimedia.org/wiki/File:Kia_EV4_GT-Line_Automesse_Ludwigsburg_2025_DSC_2535.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2026 현대 팰리세이드 (2세대) | [Hyundai_Palisade_2.5T_Calligraphy_LX3_Creamy_White_Pearl_(46)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Palisade_2.5T_Calligraphy_LX3_Creamy_White_Pearl_(46)_(cropped).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2026 BMW iX3 (노이어 클라쎄) | [BMW_iX3_50_xDrive_M_Sportpaket_Pro_(NA5)_–_f_17052026.jpg](https://commons.wikimedia.org/wiki/File:BMW_iX3_50_xDrive_M_Sportpaket_Pro_(NA5)_%E2%80%93_f_17052026.jpg) | © M 93 | CC BY-SA 3.0 de |
| 2026 메르세데스-벤츠 GLC (EQ 테크놀로지) | [Mercedes-Benz_GLC_with_EQ_Technology_IMG_6095.jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz_GLC_with_EQ_Technology_IMG_6095.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 1993 쌍용 무쏘 | [SsangYong Musso front 20080320.jpg](https://commons.wikimedia.org/wiki/File:SsangYong_Musso_front_20080320.jpg) | Rudolf Stricker | CC BY-SA 3.0 |
| 1995 쌍용 이스타나 | [00_SsangYong_istana_1.jpg](https://commons.wikimedia.org/wiki/File:00_SsangYong_istana_1.jpg) | Benespit | CC BY-SA 4.0 |
| 1997 쌍용 체어맨 | [20111014_ssangyong_new_chairman_w_1.jpg](https://commons.wikimedia.org/wiki/File:20111014_ssangyong_new_chairman_w_1.jpg) | Chu | CC BY-SA 3.0 |
| 2004 쌍용 로디우스 | [SsangYong_Rodius_XDi_(53188811619).jpg](https://commons.wikimedia.org/wiki/File:SsangYong_Rodius_XDi_(53188811619).jpg) | Rutger van der Maar | CC BY 2.0 |
| 2005 쌍용 카이런 | [SsangYong_Kyron_Facelift.JPG](https://commons.wikimedia.org/wiki/File:SsangYong_Kyron_Facelift.JPG) | Thomas doerfer | CC BY-SA 3.0 |
| 2005 쌍용 액티언 | [2007_SsangYong_Actyon_(C100)_A230_wagon_(2015-07-03)_01.jpg](https://commons.wikimedia.org/wiki/File:2007_SsangYong_Actyon_(C100)_A230_wagon_(2015-07-03)_01.jpg) | OSX | Public domain |
| 2015 쌍용 티볼리 | [KGM_Tivoli_Auto_Zuerich_2023_1X7A1040.jpg](https://commons.wikimedia.org/wiki/File:KGM_Tivoli_Auto_Zuerich_2023_1X7A1040.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 2017 쌍용 렉스턴 (G4) | [SsangYong_Rexton_Y450_front.jpg](https://commons.wikimedia.org/wiki/File:SsangYong_Rexton_Y450_front.jpg) | SmartTalk | CC BY-SA 4.0 |
| 2019 쌍용 코란도 (4세대) | [Ssangyong_Korando_(4th_generation)_IMG_3084.jpg](https://commons.wikimedia.org/wiki/File:Ssangyong_Korando_(4th_generation)_IMG_3084.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2022 KGM 토레스 | [KGM_Torres_Hybrid_Automesse_Ludwigsburg_2025_DSC_2567.jpg](https://commons.wikimedia.org/wiki/File:KGM_Torres_Hybrid_Automesse_Ludwigsburg_2025_DSC_2567.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2023 KGM 토레스 EVX | [KGM_Torres_Hybrid_Automesse_Ludwigsburg_2025_DSC_2567.jpg](https://commons.wikimedia.org/wiki/File:KGM_Torres_Hybrid_Automesse_Ludwigsburg_2025_DSC_2567.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2024 KGM 액티언 (2세대) | [KGM_Actyon_J120_Royal_Copper_(5).jpg](https://commons.wikimedia.org/wiki/File:KGM_Actyon_J120_Royal_Copper_(5).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2014 현대 제네시스 (DH) | [2015_Hyundai_Genesis_3.8L_front.jpg](https://commons.wikimedia.org/wiki/File:2015_Hyundai_Genesis_3.8L_front.jpg) | Kevauto | CC BY-SA 4.0 |
| 2008 현대 제네시스 쿠페 | [2010_Hyundai_Genesis_Coupe_3_--_08-28-2009.jpg](https://commons.wikimedia.org/wiki/File:2010_Hyundai_Genesis_Coupe_3_--_08-28-2009.jpg) | IFCAR | Public domain |
| 2017 제네시스 G70 | [2022_Genesis_G70_2.0T_Prestige,_front_left,_09-09-2023.jpg](https://commons.wikimedia.org/wiki/File:2022_Genesis_G70_2.0T_Prestige,_front_left,_09-09-2023.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 2020 제네시스 GV80 | [2021_Genesis_GV80_3.5T_Advanced,_front_left,_09-09-2023.jpg](https://commons.wikimedia.org/wiki/File:2021_Genesis_GV80_3.5T_Advanced,_front_left,_09-09-2023.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 2020 제네시스 GV70 | [Genesis_GV70_IAA_2021_1X7A0228.jpg](https://commons.wikimedia.org/wiki/File:Genesis_GV70_IAA_2021_1X7A0228.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2021 제네시스 GV60 | [Genesis_GV60_1X7A5760.jpg](https://commons.wikimedia.org/wiki/File:Genesis_GV60_1X7A5760.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2022 제네시스 G90 (RS4) | [Genesis_G90_3.5T_RS4_Savile_Silver_(1)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Genesis_G90_3.5T_RS4_Savile_Silver_(1)_(cropped).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 1953 쉐보레 콜벳 (C1) | [Chevrolet_Corvette_C1_front-right_2016_Shanghai_Auto_Museum.jpg](https://commons.wikimedia.org/wiki/File:Chevrolet_Corvette_C1_front-right_2016_Shanghai_Auto_Museum.jpg) | Morio | CC BY-SA 4.0 |
| 1955 쉐보레 벨 에어 | [57_Chevy_BelAir.jpg](https://commons.wikimedia.org/wiki/File:57_Chevy_BelAir.jpg) | Chevrolet pre-1978 | Public domain |
| 1963 쉐보레 콜벳 스팅레이 (C2) | [1963_Chevrolet_Corvette_Sting_Ray_Sport_Coupe,_front_left,_08-25-2024.jpg](https://commons.wikimedia.org/wiki/File:1963_Chevrolet_Corvette_Sting_Ray_Sport_Coupe,_front_left,_08-25-2024.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 1967 쉐보레 카마로 (1세대) | [Chevrolet_Camaro_RS_327_1968_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Chevrolet_Camaro_RS_327_1968_(cropped).jpg) | Sicnag | CC BY 2.0 |
| 1986 대우 르망 | [20101003_daewoo_lemans_1.jpg](https://commons.wikimedia.org/wiki/File:20101003_daewoo_lemans_1.jpg) | Chu | CC BY-SA 3.0 |
| 1991 대우 티코 | [Daewoo_Tico_vl_(cropped).png](https://commons.wikimedia.org/wiki/File:Daewoo_Tico_vl_(cropped).png) | Stahlkocher | CC BY 4.0 |
| 1997 대우 라노스 | [Daewoo_Lanos_hatchback_--_04-22-2011_front.jpg](https://commons.wikimedia.org/wiki/File:Daewoo_Lanos_hatchback_--_04-22-2011_front.jpg) | IFCAR | Public domain |
| 1997 대우 레간자 | [2002_(52)_Daewoo_Leganza_CDX_Automatic_-_1998cc_2.0_(135PS)_Petrol_-_Poly_Silver_Metallic_-_21-01-2024,_Front_Right.jpg](https://commons.wikimedia.org/wiki/File:2002_(52)_Daewoo_Leganza_CDX_Automatic_-_1998cc_2.0_(135PS)_Petrol_-_Poly_Silver_Metallic_-_21-01-2024,_Front_Right.jpg) | DieselFordMondeo | CC BY-SA 4.0 |
| 1998 대우 마티즈 | [2020_Chevrolet_Spark_LS,_front_right,_09-07-2024.jpg](https://commons.wikimedia.org/wiki/File:2020_Chevrolet_Spark_LS,_front_right,_09-07-2024.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 2016 쉐보레 크루즈 (2세대) | [2017_Chevrolet_Cruze_LT_in_Arctic_Blue_Metallic,_Front_Left.jpg](https://commons.wikimedia.org/wiki/File:2017_Chevrolet_Cruze_LT_in_Arctic_Blue_Metallic,_Front_Left.jpg) | Elise240SX | CC BY-SA 4.0 |
| 2015 쉐보레 스파크 (M400) | [2020_Chevrolet_Spark_LS,_front_right,_09-07-2024.jpg](https://commons.wikimedia.org/wiki/File:2020_Chevrolet_Spark_LS,_front_right,_09-07-2024.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 2011 쉐보레 볼트 (1세대) | [2011_Chevrolet_Volt_2_--_04-21-2010.jpg](https://commons.wikimedia.org/wiki/File:2011_Chevrolet_Volt_2_--_04-21-2010.jpg) | IFCAR | Public domain |
| 2011 쉐보레 올란도 | [2013_Chevrolet_Orlando_1LT_in_Silver_Ice_Metallic,_Front_Left,_10-08-2022.jpg](https://commons.wikimedia.org/wiki/File:2013_Chevrolet_Orlando_1LT_in_Silver_Ice_Metallic,_Front_Left,_10-08-2022.jpg) | Elise240SX | CC BY-SA 4.0 |
| 2016 쉐보레 말리부 (9세대) | [Chevrolet_Malibu_LT_(IX,_Facelift)_–_f_02112024.jpg](https://commons.wikimedia.org/wiki/File:Chevrolet_Malibu_LT_(IX,_Facelift)_%E2%80%93_f_02112024.jpg) | © M 93 | CC BY-SA 3.0 de |
| 2016 쉐보레 카마로 (6세대) | [2019_Chevrolet_Camaro_2SS_6.2L_front_3.16.19.jpg](https://commons.wikimedia.org/wiki/File:2019_Chevrolet_Camaro_2SS_6.2L_front_3.16.19.jpg) | Kevauto | CC BY-SA 4.0 |
| 2017 쉐보레 볼트 EV | [2022_Chevrolet_Bolt_EV_2LT,_NYC_official_fleet_1.2.23.jpg](https://commons.wikimedia.org/wiki/File:2022_Chevrolet_Bolt_EV_2LT,_NYC_official_fleet_1.2.23.jpg) | Kevauto | CC BY-SA 4.0 |
| 2019 쉐보레 실버라도 | [2022_Chevrolet_Silverado_2500HD_High_Country,_Front_Left,_11-21-2021.jpg](https://commons.wikimedia.org/wiki/File:2022_Chevrolet_Silverado_2500HD_High_Country,_Front_Left,_11-21-2021.jpg) | Elise240SX | CC BY-SA 4.0 |
| 2020 쉐보레 트레일블레이저 | [2021_Chevrolet_TrailBlazer_RS_AWD,_front_7.11.20.jpg](https://commons.wikimedia.org/wiki/File:2021_Chevrolet_TrailBlazer_RS_AWD,_front_7.11.20.jpg) | Kevauto | CC BY-SA 4.0 |
| 2020 쉐보레 콜벳 (C8) | [Chevrolet_Corvette_C8_IAA_2021_1X7A0156.jpg](https://commons.wikimedia.org/wiki/File:Chevrolet_Corvette_C8_IAA_2021_1X7A0156.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2021 쉐보레 타호 | [2022_Chevrolet_Tahoe_RST,_front_3.7.22.jpg](https://commons.wikimedia.org/wiki/File:2022_Chevrolet_Tahoe_RST,_front_3.7.22.jpg) | Kevauto | CC BY-SA 4.0 |
| 2023 쉐보레 트랙스 크로스오버 | [2024_Chevrolet_Trax_2RS,_front_left,_12-10-2023.jpg](https://commons.wikimedia.org/wiki/File:2024_Chevrolet_Trax_2RS,_front_left,_12-10-2023.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 2024 쉐보레 이쿼녹스 EV | [2025_Chevrolet_Equinox_EV,_front_left_4.26.25.jpg](https://commons.wikimedia.org/wiki/File:2025_Chevrolet_Equinox_EV,_front_left_4.26.25.jpg) | Kevauto | CC BY-SA 4.0 |
| 1930 캐딜락 V-16 | [1931_Cadillac_V-16_Sport_Phaeton.jpg](https://commons.wikimedia.org/wiki/File:1931_Cadillac_V-16_Sport_Phaeton.jpg) | Rex Gray | CC BY 2.0 |
| 2009 캐딜락 CTS-V (2세대) | [2nd_Cadillac_CTS_.jpg](https://commons.wikimedia.org/wiki/File:2nd_Cadillac_CTS_.jpg) | IFCAR | Public domain |
| 2016 캐딜락 CT6 | [2018_Cadillac_CT6_Premium_Luxury_AWD_Super_Cruise,_front_right.jpg](https://commons.wikimedia.org/wiki/File:2018_Cadillac_CT6_Premium_Luxury_AWD_Super_Cruise,_front_right.jpg) | Mr.choppers | CC BY-SA 3.0 |
| 2020 캐딜락 CT5 | [2024_Cadillac_CT5-V_AWD,_front_12.20.24.jpg](https://commons.wikimedia.org/wiki/File:2024_Cadillac_CT5-V_AWD,_front_12.20.24.jpg) | Kevauto | CC BY-SA 4.0 |
| 2021 캐딜락 에스컬레이드 (5세대) | [2026_Cadillac_Escalade_ESV.jpg](https://commons.wikimedia.org/wiki/File:2026_Cadillac_Escalade_ESV.jpg) | BuickCentury04 | CC BY-SA 4.0 |
| 2023 캐딜락 리릭 | [2023_Cadillac_Lyriq_in_Satin_Steel_Metallic,_front_left.jpg](https://commons.wikimedia.org/wiki/File:2023_Cadillac_Lyriq_in_Satin_Steel_Metallic,_front_left.jpg) | Mr.choppers | CC BY-SA 3.0 |
| 2024 캐딜락 셀레스틱 | [2025_Cadillac_Celestiq_"Vale",_front_right_(Greenwich_2025).jpg](https://commons.wikimedia.org/wiki/File:2025_Cadillac_Celestiq_%22Vale%22,_front_right_(Greenwich_2025).jpg) | Mr.choppers | CC BY-SA 4.0 |
| 2025 캐딜락 에스컬레이드 IQ | [2025_Cadillac_Escalade_IQ_(cropped).jpg](https://commons.wikimedia.org/wiki/File:2025_Cadillac_Escalade_IQ_(cropped).jpg) | Wlb5V | CC BY-SA 4.0 |
| 1961 르노 4 | [1984_Renault_4_GTL,_front_left_(Germany).jpg](https://commons.wikimedia.org/wiki/File:1984_Renault_4_GTL,_front_left_(Germany).jpg) | Mr.choppers | CC BY-SA 3.0 |
| 1972 르노 5 | [1990_Renault_5_1.4_Auto_(9743019740).jpg](https://commons.wikimedia.org/wiki/File:1990_Renault_5_1.4_Auto_(9743019740).jpg) | Charlie from United Kingdom | CC BY 2.0 |
| 2015 르노 에스파스 (5세대) | [2015-present_Renault_Espace_Front.jpg](https://commons.wikimedia.org/wiki/File:2015-present_Renault_Espace_Front.jpg) | Vauxford | CC BY-SA 4.0 |
| 2010 르노삼성 SM5 (3세대) | [16_Samsung_SM5_(third_generation).jpg](https://commons.wikimedia.org/wiki/File:16_Samsung_SM5_(third_generation).jpg) | Benespit | CC BY-SA 4.0 |
| 2012 르노 트위지 | [Eng_Renault_Twizy_ZE.jpg](https://commons.wikimedia.org/wiki/File:Eng_Renault_Twizy_ZE.jpg) | Jwh | CC BY-SA 3.0 lu |
| 2012 르노 조에 | [Renault_Zoe_R110_Z.E._50_Experience_(Facelift)_–_f_22112020.jpg](https://commons.wikimedia.org/wiki/File:Renault_Zoe_R110_Z.E._50_Experience_(Facelift)_%E2%80%93_f_22112020.jpg) | © M 93 | CC BY-SA 3.0 de |
| 2016 르노삼성 SM6 (탈리스만) | [Renault_Talisman_bei_Albert_Heijn_Kerkrade_03.jpg](https://commons.wikimedia.org/wiki/File:Renault_Talisman_bei_Albert_Heijn_Kerkrade_03.jpg) | Charles01 | CC BY-SA 4.0 |
| 2016 르노 콜레오스 (QM6) | [2018_Renault_Koleos_Initiale_Paris_DCi_4X4_2.0_Front.jpg](https://commons.wikimedia.org/wiki/File:2018_Renault_Koleos_Initiale_Paris_DCi_4X4_2.0_Front.jpg) | Vauxford | CC BY-SA 4.0 |
| 2017 알핀 A110 | [Alpine_A110_S_Automesse_Ludwigsburg_2022_1X7A5946.jpg](https://commons.wikimedia.org/wiki/File:Alpine_A110_S_Automesse_Ludwigsburg_2022_1X7A5946.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2020 르노 아르카나 (XM3) | [Renault_Arkana_(CMF-B)_Facelift_IMG_9961.jpg](https://commons.wikimedia.org/wiki/File:Renault_Arkana_(CMF-B)_Facelift_IMG_9961.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 2022 르노 메간 E-Tech 일렉트릭 | [Renault_Mégane_E-Tech_IMG_4064.jpg](https://commons.wikimedia.org/wiki/File:Renault_M%C3%A9gane_E-Tech_IMG_4064.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 2024 르노 5 E-Tech | [Renault_5_E-Tech_Electric_DSC_7279.jpg](https://commons.wikimedia.org/wiki/File:Renault_5_E-Tech_Electric_DSC_7279.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2024 르노 그랑 콜레오스 | [2024 Renault Grand Koleos E-Tech Hybrid Iconic front view.jpg](https://commons.wikimedia.org/wiki/File:2024_Renault_Grand_Koleos_E-Tech_Hybrid_Iconic_front_view.jpg) | jasonryudotnet | CC BY 3.0 |
| 1983 현대 스텔라 | [1985_Hyundai_Stellar_1600_GSL_Front.jpg](https://commons.wikimedia.org/wiki/File:1985_Hyundai_Stellar_1600_GSL_Front.jpg) | Vauxford | CC BY-SA 4.0 |
| 1985 현대 엑셀 (포니 엑셀) | [1989_Hyundai_Excel_GL_Front_Left.jpg](https://commons.wikimedia.org/wiki/File:1989_Hyundai_Excel_GL_Front_Left.jpg) | SealyPhoto | CC BY-SA 4.0 |
| 1990 현대 스쿠프 | [1991_Hyundai_Scoupe_1.5i_GTX_Automatic_002_(cropped).jpg](https://commons.wikimedia.org/wiki/File:1991_Hyundai_Scoupe_1.5i_GTX_Automatic_002_(cropped).jpg) | Rutger van der Maar | CC BY 2.0 |
| 1991 현대 갤로퍼 | [Hyundai_Galloper_XL_2.5d_Turbo_Wagon_1996_(15767100351).jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Galloper_XL_2.5d_Turbo_Wagon_1996_(15767100351).jpg) | order_242 from Chile | CC BY-SA 2.0 |
| 1996 현대 티뷰론 | [2007_Hyundai_Tiburon_-_USA_(cropped).jpg](https://commons.wikimedia.org/wiki/File:2007_Hyundai_Tiburon_-_USA_(cropped).jpg) | Cryostasis | CC BY-SA 2.0 |
| 2018 현대 넥쏘 | [Hyundai_Nexo_IAA_2021_1X7A0241.jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Nexo_IAA_2021_1X7A0241.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2019 현대 쏘나타 (DN8) | [2024_Hyundai_Sonata_SEL,_front_right.jpg](https://commons.wikimedia.org/wiki/File:2024_Hyundai_Sonata_SEL,_front_right.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 2020 현대 아반떼 (CN7) | [2023_Hyundai_Elantra_Limited_in_Silver,_front_left,_04-04-2026.jpg](https://commons.wikimedia.org/wiki/File:2023_Hyundai_Elantra_Limited_in_Silver,_front_left,_04-04-2026.jpg) | Cutlass | CC0 |
| 2020 현대 투싼 (NX4) | [Hyundai_Tucson_1.6_T-GDI_PHEV_Prime_(IV)_–_f_05072025.jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Tucson_1.6_T-GDI_PHEV_Prime_(IV)_%E2%80%93_f_05072025.jpg) | © M 93 | CC BY-SA 3.0 de |
| 2021 현대 스타리아 | [Hyundai_Staria_1X7A0321.jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Staria_1X7A0321.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2021 현대 캐스퍼 | [Hyundai_Casper_Active_Inspiration_AX1_PE_Tomboy_Khaki_(5)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Casper_Active_Inspiration_AX1_PE_Tomboy_Khaki_(5)_(cropped).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2022 현대 그랜저 (GN7) | [Hyundai_Grandeur_Calligraphy_GN7_Biophilic_Blue_Pearl_(5)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Hyundai_Grandeur_Calligraphy_GN7_Biophilic_Blue_Pearl_(5)_(cropped).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2023 현대 싼타페 (MX5) | [2024_Hyundai_Santa_Fe_Luxury_AWD_in_Hampton_Grey,_front_left,_2024-06-30.jpg](https://commons.wikimedia.org/wiki/File:2024_Hyundai_Santa_Fe_Luxury_AWD_in_Hampton_Grey,_front_left,_2024-06-30.jpg) | Elise240SX | CC BY-SA 4.0 |
| 1974 기아 브리사 | [20141005 Kia Brisa 01.jpg](https://commons.wikimedia.org/wiki/File:20141005_Kia_Brisa_01.jpg) | Chu | CC BY 4.0 |
| 1987 기아 프라이드 | [Kia_Pride_silver_vl.jpg](https://commons.wikimedia.org/wiki/File:Kia_Pride_silver_vl.jpg) | Stahlkocher | CC BY-SA 3.0 |
| 2008 기아 모하비 | [00_Kia_Mohave_1.jpg](https://commons.wikimedia.org/wiki/File:00_Kia_Mohave_1.jpg) | Benespit | CC BY-SA 4.0 |
| 2011 기아 레이 | [0_Kia_Ray_5.jpg](https://commons.wikimedia.org/wiki/File:0_Kia_Ray_5.jpg) | Benespit | CC BY-SA 4.0 |
| 2019 기아 셀토스 | [Kia_Seltos_SP2_PE_Snow_White_Pearl_(17)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Kia_Seltos_SP2_PE_Snow_White_Pearl_(17)_(cropped).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2019 기아 K5 (3세대) | [2022_Kia_K5_GT-Line_in_Pacific_Blue,_Front_Left,_09-05-2022.jpg](https://commons.wikimedia.org/wiki/File:2022_Kia_K5_GT-Line_in_Pacific_Blue,_Front_Left,_09-05-2022.jpg) | Elise240SX | CC BY-SA 4.0 |
| 2020 기아 쏘렌토 (MQ4) | [2024_Kia_Sorento_X-Line_SX_Prestige_(facelift),_front_12.20.24.jpg](https://commons.wikimedia.org/wiki/File:2024_Kia_Sorento_X-Line_SX_Prestige_(facelift),_front_12.20.24.jpg) | Kevauto | CC BY-SA 4.0 |
| 2020 기아 카니발 (KA4) | [2025_Kia_Carnival_Hybrid_EX,_front_right,_10-12-2025.jpg](https://commons.wikimedia.org/wiki/File:2025_Kia_Carnival_Hybrid_EX,_front_right,_10-12-2025.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 2021 기아 K8 | [Kia_K8_Hybrid_GL3_HEV_Snow_White_Pearl_(1)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Kia_K8_Hybrid_GL3_HEV_Snow_White_Pearl_(1)_(cropped).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2021 기아 스포티지 (NQ5) | [2025_Kia_Sportage_S_front_only.jpg](https://commons.wikimedia.org/wiki/File:2025_Kia_Sportage_S_front_only.jpg) | LuvsMG481 | CC BY-SA 4.0 |
| 2023 기아 EV9 | [Kia_EV9_1X7A2472.jpg](https://commons.wikimedia.org/wiki/File:Kia_EV9_1X7A2472.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 1966 토요타 코롤라 (1세대) | [Toyota_Corolla_First-generation_001.jpg](https://commons.wikimedia.org/wiki/File:Toyota_Corolla_First-generation_001.jpg) | D.Bellwood | CC BY-SA 3.0 |
| 1967 토요타 2000GT | [TOYOTA_2000GT.jpg](https://commons.wikimedia.org/wiki/File:TOYOTA_2000GT.jpg) | Unknown | CC BY-SA 3.0 |
| 2017 렉서스 LS (5세대) | [2019_Lexus_LS_500_AWD_beige,_front_Hagerty_6.1.19.jpg](https://commons.wikimedia.org/wiki/File:2019_Lexus_LS_500_AWD_beige,_front_Hagerty_6.1.19.jpg) | Kevauto | CC BY-SA 4.0 |
| 2019 토요타 GR 수프라 (A90) | [2020_Toyota_GR_Supra_(United_States).png](https://commons.wikimedia.org/wiki/File:2020_Toyota_GR_Supra_(United_States).png) | Gold Pony | CC BY 3.0 |
| 2010 렉서스 LFA | [Lexus_LFA_001.JPG](https://commons.wikimedia.org/wiki/File:Lexus_LFA_001.JPG) | Tennen-Gas | CC BY-SA 3.0 |
| 2017 토요타 캠리 (XV70) | [2018_Toyota_Camry_(ASV70R)_Ascent_sedan_(2018-08-27)_01.jpg](https://commons.wikimedia.org/wiki/File:2018_Toyota_Camry_(ASV70R)_Ascent_sedan_(2018-08-27)_01.jpg) | EurovisionNim | CC BY-SA 4.0 |
| 2020 토요타 미라이 (2세대) | [Toyota_Mirai_(JPD20)_IMG_5303.jpg](https://commons.wikimedia.org/wiki/File:Toyota_Mirai_(JPD20)_IMG_5303.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2021 토요타 랜드크루저 (J300) | [2021_Toyota_Land_Cruiser_300_3.4_ZX_(Colombia)_front_view_04.png](https://commons.wikimedia.org/wiki/File:2021_Toyota_Land_Cruiser_300_3.4_ZX_(Colombia)_front_view_04.png) | Autosdeprimera | CC BY 3.0 |
| 2022 토요타 bZ4X | [Toyota_bZ4X_Automesse_Ludwigsburg_2022_1X7A5895.jpg](https://commons.wikimedia.org/wiki/File:Toyota_bZ4X_Automesse_Ludwigsburg_2022_1X7A5895.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 1969 닛산 페어레이디 Z (S30) | [1970-1973_Nissan_Fairlady_Z.jpg](https://commons.wikimedia.org/wiki/File:1970-1973_Nissan_Fairlady_Z.jpg) | TTTNIS | CC0 |
| 1972 혼다 시빅 (1세대) | [Honda_Civic_CVCC.jpg](https://commons.wikimedia.org/wiki/File:Honda_Civic_CVCC.jpg) | Kzaral[1] | CC BY 2.0 |
| 1999 닛산 스카이라인 GT-R | [Nissan_Skyline_GT-R_R34_V_Spec_II.jpg](https://commons.wikimedia.org/wiki/File:Nissan_Skyline_GT-R_R34_V_Spec_II.jpg) | TTTNIS | CC0 |
| 1992 마쯔다 RX-7 (FD) | [1994_Mazda_RX-7_R2_in_Vintage_Red,_front_left_(Lime_Rock).jpg](https://commons.wikimedia.org/wiki/File:1994_Mazda_RX-7_R2_in_Vintage_Red,_front_left_(Lime_Rock).jpg) | Mr.choppers | CC BY-SA 3.0 |
| 1992 스바루 임프레자 WRX (1세대) | [1998 Subaru Impreza (GC8 MY98) WRX sedan (13869590783).jpg](https://commons.wikimedia.org/wiki/File:1998_Subaru_Impreza_(GC8_MY98)_WRX_sedan_(13869590783).jpg) | FotoSleuth | CC BY 2.0 |
| 1999 혼다 S2000 | [HondaS2000-004.jpg](https://commons.wikimedia.org/wiki/File:HondaS2000-004.jpg) | Rich Niewiroski Jr. | CC BY 2.5 |
| 2007 닛산 GT-R (R35) | [2009-2010_Nissan_GT-R_(R35)_coupe_01.jpg](https://commons.wikimedia.org/wiki/File:2009-2010_Nissan_GT-R_(R35)_coupe_01.jpg) | OSX | Public domain |
| 2015 마쯔다 MX-5 (ND) | [Mazda_MX-5_(ND)_1X7A7471.jpg](https://commons.wikimedia.org/wiki/File:Mazda_MX-5_(ND)_1X7A7471.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 2020 혼다 e | [Honda_e_Advance_–_f_18102020.jpg](https://commons.wikimedia.org/wiki/File:Honda_e_Advance_%E2%80%93_f_18102020.jpg) | © M 93 | CC BY-SA 3.0 de |
| 1955 BMW 이세타 | [BMW_Isetta_-_Flickr_-_mick_-_Lumix.jpg](https://commons.wikimedia.org/wiki/File:BMW_Isetta_-_Flickr_-_mick_-_Lumix.jpg) | Mick from Northamptonshire, England | CC BY 2.0 |
| 1956 BMW 507 | [BMW_507.jpg](https://commons.wikimedia.org/wiki/File:BMW_507.jpg) | Stefan Krause, Germany | CC BY-SA 3.0 |
| 1968 BMW 2002 | [Blackrock,_Co_Dublin_-_Ireland_(4799982672).jpg](https://commons.wikimedia.org/wiki/File:Blackrock,_Co_Dublin_-_Ireland_(4799982672).jpg) | Mic from Reading - Berkshire, United Kingdom | CC BY 2.0 |
| 1971 BMW 3.0 CSL (E9) | [BMWE9CSc.jpg](https://commons.wikimedia.org/wiki/File:BMWE9CSc.jpg) | Olli1800 | CC BY-SA 3.0 |
| 1978 BMW M1 | [BMW_M1,_front_right_(Brooklyn).jpg](https://commons.wikimedia.org/wiki/File:BMW_M1,_front_right_(Brooklyn).jpg) | Mr.choppers | CC BY-SA 3.0 |
| 2013 BMW i3 | [2013 BMW i3 I01 Solarorange mit Frozen Grey Metallic.jpg](https://commons.wikimedia.org/wiki/File:2013_BMW_i3_I01_Solarorange_mit_Frozen_Grey_Metallic.jpg) | Mario von Berg | CC BY-SA 2.0 |
| 2014 BMW i8 | [2016_BMW_i8.jpg](https://commons.wikimedia.org/wiki/File:2016_BMW_i8.jpg) | Vauxford | CC BY-SA 4.0 |
| 2022 BMW 7시리즈 (G70) | [BMW_7-Series_(G70)_750e_IMG_9358.jpg](https://commons.wikimedia.org/wiki/File:BMW_7-Series_(G70)_750e_IMG_9358.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 2023 BMW 5시리즈 · i5 (G60) | [BMW_G60_520i_1X7A2443.jpg](https://commons.wikimedia.org/wiki/File:BMW_G60_520i_1X7A2443.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 1901 메르세데스 35 hp | [Mercedes_35hp_by_Wilhelm_Maybach.jpg](https://commons.wikimedia.org/wiki/File:Mercedes_35hp_by_Wilhelm_Maybach.jpg) | Mercedes-Benz-Werkphoto | Public domain |
| 1963 메르세데스-벤츠 600 | [Mercedes-Benz_600_vl_silver_TCE.jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz_600_vl_silver_TCE.jpg) | Stahlkocher | CC BY-SA 3.0 |
| 1976 메르세데스-벤츠 W123 | [1984_Mercedes-Benz_280E_Sedan_(cropped).jpg](https://commons.wikimedia.org/wiki/File:1984_Mercedes-Benz_280E_Sedan_(cropped).jpg) | Verdict09 | CC0 |
| 1982 메르세데스-벤츠 190 E (W201) | [1993_190E_2.3.jpg](https://commons.wikimedia.org/wiki/File:1993_190E_2.3.jpg) | Bretbmorgan | CC BY-SA 4.0 |
| 2014 메르세데스-AMG GT | [Festival_automobile_international_2015_-_Mercedes_AMG_GT_-_003.jpg](https://commons.wikimedia.org/wiki/File:Festival_automobile_international_2015_-_Mercedes_AMG_GT_-_003.jpg) | Thesupermat | CC BY-SA 4.0 |
| 2018 메르세데스-벤츠 G-클래스 (W463) | [Mercedes-Benz_W463_G_350_BlueTEC_01.jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz_W463_G_350_BlueTEC_01.jpg) | Julian Herzog (Website) | CC BY 4.0 |
| 2020 메르세데스-벤츠 S-클래스 (W223) | [Mercedes-Benz_W223_IMG_3951.jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz_W223_IMG_3951.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2023 메르세데스-벤츠 E-클래스 (W214) | [Mercedes-Benz_W214_1X7A1841.jpg](https://commons.wikimedia.org/wiki/File:Mercedes-Benz_W214_1X7A1841.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 1968 아우디 100 (C1) | [Audi 100 C 1, Bj. 1972 (6703 r schmal).JPG](https://commons.wikimedia.org/wiki/File:Audi_100_C_1,_Bj._1972_(6703_r_schmal).JPG) | Lothar Spurzem | CC BY-SA 2.0 de |
| 1998 아우디 TT (1세대) | [Audi TT coupé (8N) front.JPG](https://commons.wikimedia.org/wiki/File:Audi_TT_coup%C3%A9_(8N)_front.JPG) | Tokumeigakarinoaoshima | CC0 |
| 2006 아우디 R8 (1세대) | [2010_Audi_R8_Spyder_Quattro_V10_5.2.jpg](https://commons.wikimedia.org/wiki/File:2010_Audi_R8_Spyder_Quattro_V10_5.2.jpg) | Vauxford | CC BY-SA 4.0 |
| 2021 아우디 e-트론 GT | [Audi_e-tron_GT_IMG_5689.jpg](https://commons.wikimedia.org/wiki/File:Audi_e-tron_GT_IMG_5689.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2021 아우디 Q4 e-트론 | [2021_Audi_Q4_e-tron_Sport_35.jpg](https://commons.wikimedia.org/wiki/File:2021_Audi_Q4_e-tron_Sport_35.jpg) | Vauxford | CC BY-SA 4.0 |
| 1950 폭스바겐 타입 2 | [0385_Porsche_Diesel_Bus_blau.jpg](https://commons.wikimedia.org/wiki/File:0385_Porsche_Diesel_Bus_blau.jpg) | Raizy | CC BY-SA 3.0 |
| 2019 폭스바겐 골프 (8세대) | [2020_Volkswagen_Golf_Style_1.5_Front.jpg](https://commons.wikimedia.org/wiki/File:2020_Volkswagen_Golf_Style_1.5_Front.jpg) | Vauxford | CC BY-SA 4.0 |
| 2020 폭스바겐 ID.4 | [2025_Volkswagen_ID4_Pro_Redspot_front.jpg](https://commons.wikimedia.org/wiki/File:2025_Volkswagen_ID4_Pro_Redspot_front.jpg) | LuvsMG481 | CC BY-SA 4.0 |
| 2022 폭스바겐 ID. 버즈 | [Volkswagen_ID._Buzz_1X7A6263.jpg](https://commons.wikimedia.org/wiki/File:Volkswagen_ID._Buzz_1X7A6263.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 1948 포르쉐 356 | [2007-07-08_Porsche_356_C_(01_kl_ret).jpg](https://commons.wikimedia.org/wiki/File:2007-07-08_Porsche_356_C_(01_kl_ret).jpg) | Unknown | CC BY-SA 2.0 de |
| 1986 포르쉐 959 | [Porsche_959_–_Frontansicht_(2),_21._März_2013,_Düsseldorf.jpg](https://commons.wikimedia.org/wiki/File:Porsche_959_%E2%80%93_Frontansicht_(2),_21._M%C3%A4rz_2013,_D%C3%BCsseldorf.jpg) | M 93 | CC BY-SA 3.0 de |
| 2004 포르쉐 카레라 GT | [Porsche_Carrera_GT_-_Goodwood_Breakfast_Club_(July_2008).jpg](https://commons.wikimedia.org/wiki/File:Porsche_Carrera_GT_-_Goodwood_Breakfast_Club_(July_2008).jpg) | Brian Snelson from Hockley, Essex, England | CC BY 2.0 |
| 2013 포르쉐 918 스파이더 | [2015_Porsche_918_Spyder_Platinum_Silver_Metallic_SCD_24.jpg](https://commons.wikimedia.org/wiki/File:2015_Porsche_918_Spyder_Platinum_Silver_Metallic_SCD_24.jpg) | MrWalkr | CC BY-SA 4.0 |
| 1957 피아트 500 (누오바 500) | [1970_Fiat_500_L_--_2011_DC_1.jpg](https://commons.wikimedia.org/wiki/File:1970_Fiat_500_L_--_2011_DC_1.jpg) | IFCAR | Public domain |
| 1962 페라리 250 GTO | [1962_Ferrari_250_GTO_SP25.jpg](https://commons.wikimedia.org/wiki/File:1962_Ferrari_250_GTO_SP25.jpg) | MrWalkr | CC BY-SA 4.0 |
| 1973 란치아 스트라토스 | [1974_Lancia_Stratos_Stradale_at_Greenwich_2021,_front_left.jpg](https://commons.wikimedia.org/wiki/File:1974_Lancia_Stratos_Stradale_at_Greenwich_2021,_front_left.jpg) | Mr.choppers | CC BY-SA 3.0 |
| 1974 람보르기니 쿤타치 | [Lamborghini_Countach_-_Flickr_-_exfordy_(2)_(cropped-2).jpg](https://commons.wikimedia.org/wiki/File:Lamborghini_Countach_-_Flickr_-_exfordy_(2)_(cropped-2).jpg) | Brian Snelson from Hockley, Essex, England | CC BY 2.0 |
| 1987 페라리 F40 | [F40_Ferrari_20090509.jpg](https://commons.wikimedia.org/wiki/File:F40_Ferrari_20090509.jpg) | Will ainsworth | CC BY-SA 3.0 |
| 2013 라페라리 | [LaFerrari_in_Beverly_Hills_(14563979888).jpg](https://commons.wikimedia.org/wiki/File:LaFerrari_in_Beverly_Hills_(14563979888).jpg) | Axion23 | CC BY 2.0 |
| 2016 알파 로메오 줄리아 | [Alfa_952_26.06.19_JM_(1)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Alfa_952_26.06.19_JM_(1)_(cropped).jpg) | Johannes Maximilian | GFDL 1.2 |
| 2019 페라리 SF90 스트라달레 | [Red_2019_Ferrari_SF90_Stradale_(48264238897)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Red_2019_Ferrari_SF90_Stradale_(48264238897)_(cropped).jpg) | Alexandre Prevot from Nancy, France | CC BY-SA 2.0 |
| 2023 람보르기니 레부엘토 | [Lamborghini_Revuelto_DSC_6985_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Lamborghini_Revuelto_DSC_6985_(cropped).jpg) | Alexander Migl | CC BY-SA 4.0 |
| 1927 포드 모델 A | [1928_Ford_Phaeton,_front_right,_06-08-2024.jpg](https://commons.wikimedia.org/wiki/File:1928_Ford_Phaeton,_front_right,_06-08-2024.jpg) | MercurySable99 | CC BY-SA 4.0 |
| 1964 포드 GT40 | [GT40_at_Goodwood.jpg](https://commons.wikimedia.org/wiki/File:GT40_at_Goodwood.jpg) | edvvc from London, UK | CC BY 2.0 |
| 2018 지프 랭글러 (JL) | [Jeep_Wrangler_Unlimited_(JL)_PHEV_IMG_5808.jpg](https://commons.wikimedia.org/wiki/File:Jeep_Wrangler_Unlimited_(JL)_PHEV_IMG_5808.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2020 포드 머스탱 마하-E | [2021_Ford_Mustang_Mach-E_Standard_Range_Front.jpg](https://commons.wikimedia.org/wiki/File:2021_Ford_Mustang_Mach-E_Standard_Range_Front.jpg) | Vauxford | CC BY-SA 4.0 |
| 2021 포드 브롱코 (6세대) | [Ford_Bronco_(6th_generation)_Outer_Banks_1X7A0384.jpg](https://commons.wikimedia.org/wiki/File:Ford_Bronco_(6th_generation)_Outer_Banks_1X7A0384.jpg) | Alexander Migl | CC BY-SA 4.0 |
| 2022 포드 F-150 라이트닝 | [2022_Ford_F-150_Lightning_Lariat_in_Atlas_Blue_Metallic,_Front_Right,_08-06-2022.jpg](https://commons.wikimedia.org/wiki/File:2022_Ford_F-150_Lightning_Lariat_in_Atlas_Blue_Metallic,_Front_Right,_08-06-2022.jpg) | Elise240SX | CC BY-SA 4.0 |
| 2023 포드 머스탱 (7세대) | [Seventh_generation_2024_Ford_Mustang_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Seventh_generation_2024_Ford_Mustang_(cropped).jpg) | WMrapids | CC0 |
| 1948 랜드로버 시리즈 | [Land_Rover_Series_I_1948_(HUE_166).jpg](https://commons.wikimedia.org/wiki/File:Land_Rover_Series_I_1948_(HUE_166).jpg) | DeFacto | CC BY-SA 4.0 |
| 1961 재규어 E-타입 | [Jaguar_E-Type_Series_1_3.8_Litre_1961.jpg](https://commons.wikimedia.org/wiki/File:Jaguar_E-Type_Series_1_3.8_Litre_1961.jpg) | DeFacto | CC BY-SA 4.0 |
| 1961 볼보 P1800 | [1969_P1800_S.jpg](https://commons.wikimedia.org/wiki/File:1969_P1800_S.jpg) | Calreyn88 | CC BY-SA 4.0 |
| 1963 애스턴 마틴 DB5 | [Aston_Martin_DB5_(Skyfall).jpg](https://commons.wikimedia.org/wiki/File:Aston_Martin_DB5_(Skyfall).jpg) | DeFacto | CC BY-SA 4.0 |
| 2017 테슬라 모델 3 | [Tesla_Model_3_(2023)_Autofrühling_Ulm_IMG_9282.jpg](https://commons.wikimedia.org/wiki/File:Tesla_Model_3_(2023)_Autofr%C3%BChling_Ulm_IMG_9282.jpg) | Alexander-93 | CC BY-SA 4.0 |
| 2020 테슬라 모델 Y | [Tesla_Model_Y_Premium_(Facelift)_–_f_05052026.jpg](https://commons.wikimedia.org/wiki/File:Tesla_Model_Y_Premium_(Facelift)_%E2%80%93_f_05052026.jpg) | © M 93 | CC BY-SA 3.0 de |
| 2020 랜드로버 디펜더 (L663) | [Land_Rover_Defender_110_D40_SE_L663_Pangea_Green_(1)_(cropped).jpg](https://commons.wikimedia.org/wiki/File:Land_Rover_Defender_110_D40_SE_L663_Pangea_Green_(1)_(cropped).jpg) | Damian B Oh | CC BY-SA 4.0 |
| 2021 리비안 R1T | [2022_Rivian_R1T_(in_Glacier_White),_front_6.21.22.jpg](https://commons.wikimedia.org/wiki/File:2022_Rivian_R1T_(in_Glacier_White),_front_6.21.22.jpg) | Kevauto | CC BY-SA 4.0 |
