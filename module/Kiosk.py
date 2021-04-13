# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : Kiosk.py & Last Modded : 2021.03.19. ###
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import os
import time
import datetime
import csv
from .Phone import *
from .PhoneChecker import *


class Kiosk():
    def __init__(self):
        super(Kiosk, self).__init__()
        self.bootEnv = 0  # 부팅 환경 저장용 변수
        self.option = 0  # 고객이 선택한 메뉴 옵션 저장용 변수
        self.phone = list()  # 스마트폰 정보 저장용 리스트
        self.version = "2.0"  # 난수 사용 가능 버전
        self.randDisable = False  # 의사 난수 비활성화 여부
        self.randSeed = 0  # 의사 난수 시드
        self.inspector = PhoneChecker()  # 스마트폰 상태 확인 장치
        self.filePath = "KioskStock.csv"

    def clear(self):
        if self.bootEnv:
            from IPython.display import clear_output  # Colab용 출력물 지우기 함수 임포트
            clear_output()
        else:
            os.system("cls")  # 리눅스/유닉스 환경은 고려하지 않음

    def boot(self):
        self.bootEnv = int(input("1.Colab(최초 부팅인 경우 2 입력)\n0.Other\n부팅 환경 선택 : "))
        if self.bootEnv:
            if self.bootEnv == 2:
                from google.colab import drive
                drive.mount('/content/drive')
            self.filePath = "/content/drive/MyDrive/KioskStock.csv"
        try:
            file = open(self.filePath, 'r', encoding='utf-8')
            rdr = csv.reader(file)
            next(rdr)
            for row in rdr:
                self.phone.append(Phone())  # 리스트 마지막에 Phone 클래스의 인스턴스 생성하여 추가
                self.phone[len(self.phone)-1].name = row[0]
                self.phone[len(self.phone)-1].stat = row[1]
                self.phone[len(self.phone)-1].price = int(row[2])
            file.close()
        except FileNotFoundError:
            pass
        self.clear()
        bootTime = datetime.datetime.now()
        self.randSeed = bootTime.timestamp()
        print("키오스크 OS " + self.version + "을 부팅합니다.\n부팅 완료 시간 : " + str(bootTime) + "\n")

    def shutdown(self):
        file = open(self.filePath, 'w', encoding='utf-8', newline='')
        wr = csv.writer(file)
        wr.writerow(['Name', 'Status', 'Price'])
        for stock in range(len(self.phone)):
            wr.writerow([self.phone[stock].name, self.phone[stock].stat, self.phone[stock].price])
        file.close()
        print("재고 목록을 저장했습니다.\n키오스크 OS를 종료합니다.")

    def getPseudoRandNum(self, maxInt):
        self.randSeed = int((self.randSeed*1103515245+12345) / 65536) % 10000000000
        return self.randSeed % (maxInt+1)

    def passwdGen(self):
        domains = [['A', 'A', 'A', 'A', 'A'], ['B', 'B', 'B', 'B', 'B'], ['C', 'C', 'C', 'C', 'C'], ['D', 'D', 'D', 'D', 'D']]
        chrList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for i in range(4):
            for j in range(5):
                domains[i][j] = chrList[self.getPseudoRandNum(34)]
        return domains

    def passwdEecrypt(self, pidkey):  # PIDEY to ECDATA (한컴오피스 설치파일의 시리얼넘버 암호화 방식)
        ecdata = list()
        domain_code = [-3, 1, 2, -9]
        for domain in [1, 3, 0, 2]:
            for i in range(5):
                if pidkey[domain][i] >= 'A' and pidkey[domain][i] <= 'Z':  # 대문자일 때
                    ecdata.append(chr((ord(pidkey[domain][i]) - ord('A') + domain_code[domain] + 26) % 26 + ord('A')))
                else:  # 숫자 문자일 때
                    ecdata.append(chr((ord(pidkey[domain][i]) - ord('0') + domain_code[domain] + 10) % 10 + ord('0')))
        return ecdata

    def printMainMenu(self):
        print("현재 입력 대기중입니다.\n\n" +
                " +-------------------------------+\n" +
                " |        스마트폰 '판매'        |\n" +
                " |                               |\n" +
                " |        스마트폰 '구매'        |\n" +
                " |                               |\n" +
                " |         시스템 '종료'         |\n" +
                " +-------------------------------+\n")
        self.option = input("원하시는 기능을 입력해주세요 : ")
        if self.option == "종료":
            return 0
        elif self.option == "판매":
            name = input("\n\n스마트폰의 기기명을 입력해주세요 : ")  # 스트링 입력받기
            status, price = self.inspector.getSensorValue(self)
            print("\n해당 기기의 등급은 " + status + "급, 견적 산출가는 " + str(format(price, ",")) + "원 입니다.")
            if int(input("판매하시겠습니까?(Yes = 1, No = 0) : ")):
                self.phone.append(Phone())  # 리스트 마지막에 Phone 클래스의 인스턴스 생성하여 추가
                self.phone[len(self.phone)-1].name = name  # 임시로 저장했던 값 인스턴스 멤버 변수에 대입
                self.phone[len(self.phone)-1].stat = status
                self.phone[len(self.phone)-1].price = price
                print("현금 " + str(format(price, ",")) + "원을 받아주세요.\n\n판매해주셔서 감사합니다! 3초 후 메인 메뉴로 돌아갑니다.")
                time.sleep(3)
            else:
                print("\n기기를 받아주세요.\n다음에 만나요! 3초 후 메인메뉴로 돌아갑니다.")
                time.sleep(3)
            return 1
        elif self.option == "구매":
            name = input("\n\n구매를 원하시는 스마트폰의 기기명을 입력해주세요 : ")  # 스트링 입력받기
            while True:
                status = input("스마트폰의 상태를 입력해주세요(S/A/B/C) : ")  # 스마트폰의 상태는 S/A/B/C 중 하나 선택
                if status == 'S' or status == 'A' or status == 'B' or status == 'C':
                    break
                else:
                    print("잘못된 문자가 입력되었습니다.")
            index = -1
            for i in range(0, len(self.phone)):
                if self.phone[i].name == name and self.phone[i].stat == status:
                    index = i  # 기기명과 상태가 같은 재고의 경우 먼저 매입한 순서대로 판매되도록 함
                    break
            if index >= 0:
                print("\n해당 기기의 판매가는 " + str(format(self.phone[index].price, ",")) + "원 입니다.")
                if int(input("구매하시겠습니까?(Yes = 1, No = 0) : ")):
                    input("결제를 진행해주세요. 결제가 끝나면 아무키나 눌러주세요... ")
                    print("기기를 받아주세요.\n\n판매해주셔서 감사합니다! 3초 후 메인 메뉴로 돌아갑니다.")
                    del self.phone[index]
                    time.sleep(3)
                else:
                    print("\n다음에 만나요! 3초 후 메인메뉴로 돌아갑니다.")
                    time.sleep(3)
            else:
                print("원하시는 기기는 재고가 없습니다.ㅠㅠ 3초 후 메인메뉴로 돌아갑니다.")
                time.sleep(3)
            return 1
        elif self.option == "HiddenMenu":
            self.clear()
            print("Hidden Menu에 접속하기 위해 관리자 로그인이 필요합니다.")
            while not input("ID : ") == 'root':
                print("등록되지 않은 사용자 계정입니다.")
            print("제시되는 코드를 미리 정해진 규약에 따라 암호화한 결과를 입력하세요.")
            for i in range(3):
                pidkey = self.passwdGen()
                print("PIDKEY : ", end='')
                for j in range(4):
                    print(''.join(pidkey[j]), end='-')
                print("\b ")
                if input("ECDATA : ") == ''.join(self.passwdEecrypt(pidkey)):
                    while True:
                        self.clear()
                        print("관리자 로그인 성공! 현재 입력 대기중입니다.\n\n" +
                                " +-------------------------------+\n" +
                                " |   1) 재고 목록 출력           |\n" +
                                " |                               |\n" +
                                " |   2) 의사 난수 사용 설정      |\n" +
                                " |                               |\n" +
                                " |   etc) 히든메뉴 종료          |\n" +
                                " +-------------------------------+\n")
                        opt = int(input("원하시는 기능을 입력해주세요 : "))
                        if opt == 1:
                            if len(self.phone):
                                for stock in range(len(self.phone)):
                                    print("\nSTOCK #" + str(stock) + "\nNAME : " + self.phone[stock].name + "\nSTATUS : " + self.phone[stock].stat + "\nPRICE : " + str(format(self.phone[stock].price, ",")))
                                print("\n재고 목록 출력을 완료하였습니다.")
                            else:
                                print("재고 목록이 비어있습니다.")
                            input("\n아무키나 누르면 히든메뉴로 돌아갑니다.")
                        elif opt == 2:
                            print("현재 의사 난수 모드 " + ("비활성화 됨" if self.randDisable else "활성화 됨"))
                            if int(input("활성화 상태를 변경할까요?(Yes = 1, No = 0) : ")):
                                self.randDisable = not self.randDisable
                                print("의사 난수 모드가 " + ("비활성화 되었습니다." if self.randDisable else "활성화 되었습니다."))
                            print("\n3초 후 히든메뉴로 돌아갑니다.")
                            time.sleep(3)
                        else:
                            print("히든메뉴를 종료합니다.")
                            break
                    break
                else:
                    print("잘못된 코드를 입력하셨습니다. 재시도 해주세요." if i != 2 else "관리자 로그인 실패!")
            print("\n3초 후 메인메뉴로 돌아갑니다.")
            time.sleep(3)
            return 1
        else:
            print("지원되지 않는 명령어입니다. 3초 후 메인메뉴로 돌아갑니다.")
            time.sleep(3)
            return 1
