# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : PhoneChecker.py & Last Modded : 2021.03.19. ###
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import time


class PhoneChecker():
    def __init__(self):
        super(PhoneChecker, self).__init__()

    def getSensorValue(self, kiosk):
        statList = ['S', 'A', 'B', 'C']  # 스마트폰의 상태는 S/A/B/C 중 하나 선택
        if not kiosk.randDisable:
            input("스마트폰을 키오스크에 넣은 다음 아무키나 눌러주세요... ")
            print("스캐너가 고객님의 스마트폰의 상태를 분석중입니다. 잠시만 기다려주세요!")
            time.sleep(2)
            status = statList[kiosk.getPseudoRandNum(3)]
        else:
            while True:
                status = input("센서에 오류가 발견되어 사용이 불가능합니다. 사용자 입력 모드로 전환합니다.\n스마트폰의 상태를 입력해주세요(S/A/B/C) : ")  # 스마트폰의 상태는 S/A/B/C 중 하나 선택
                if status == 'S' or status == 'A' or status == 'B' or status == 'C':
                    break
                else:
                    print("잘못된 문자가 입력되었습니다.")
        if status == 'S':
            price = 600000 + kiosk.getPseudoRandNum(600) * 1000
        elif status == 'A':
            price = 300000 + kiosk.getPseudoRandNum(300) * 1000
        elif status == 'B':
            price = 100000 + kiosk.getPseudoRandNum(100) * 1000
        elif status == 'C':
            price = 50000 + kiosk.getPseudoRandNum(50) * 1000
        return status, price
