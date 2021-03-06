# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : Kiosk2.0(modularized).py & Last Modded : 2021.03.19. ###
문제적 상황 : 중고폰을 자동으로 매입하고 판매하는 키오스크를 만들려고 한다.

문장 :
-시스템을 시작한 후 스마트폰 판매(기계 입장에서는 매입)와 스마트폰 구매(기계 입장에서는 판매), 시스템 종료 세 옵션 중 하나가 선택되기를 대기한다.
-고객이 와서 옵션을 선택하면 그에 따른 절차를 진행한다.
-고객이 스마트폰 판매를 선택한 경우 스마트폰을 입력받아 상태를 체크하고 상태에 따른 가격을 책정한다. 가격 책정이 끝나면 고객에게 돈을 인출해준다.
-고객이 스마트폰 구매를 선택한 경우 고객이 구매하고자 하는 스마트폰의 종류를 입력받고 목록에 있다면 가격을 알려준다. 고객이 구매를 선택하면 결제를 진행하고 스마트폰을 출력한다.
-한 고객이 거래를 마치면 다른 고객이 올 때까지 대기한다.
-시스템 종료 버튼이 눌러지면 시스템을 종료한다.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import os
import sys

#sys.path.append('/content/drive/MyDrive/')
from module import *


if __name__ == '__main__':
    cnuKiosk = Kiosk()  # 키오스크 인스턴스 생성
    cnuKiosk.boot()  # 키오스크 부팅
    while cnuKiosk.printMainMenu():  # 메인화면 출력 & 종료 옵션 입력 전까지 반복
        cnuKiosk.clear()
    cnuKiosk.shutdown()  # 키오스크 종료
    del cnuKiosk  # 키오스크 인스턴스 닫기

    os.system("pause")
