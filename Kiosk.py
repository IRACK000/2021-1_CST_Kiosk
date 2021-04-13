# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : Kiosk.py & Last Modded : 2021.03.12. ###
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
import time


class Kiosk():
    def __init__(self):
        super(Kiosk, self).__init__()
        self.bootEnv = 0  # 부팅 환경 저장용 변수
        self.option = 0  # 고객이 선택한 메뉴 옵션 저장용 변수
        self.phone = list()  # 스마트폰 정보 저장용 리스트
        
    def clear(self):
        if self.bootEnv:
            from IPython.display import clear_output  # Colab용 출력물 지우기 함수 임포트
            clear_output()
        else:
            os.system("cls")  # 리눅스/유닉스 환경은 고려하지 않음

    def boot(self):
        self.bootEnv = int(input("1.Colab\n0.Other\n부팅 환경 선택 : "))
        self.clear()
        print("키오스크 OS를 부팅합니다.\n")

    def shutdown(self):
        print("키오스크 OS를 종료합니다.")

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
            price = 0
            while True:
                status = input("스마트폰의 상태를 입력해주세요(S/A/B/C) : ")  # 스마트폰의 상태는 S/A/B/C 중 하나 선택
                if status == 'S':
                    price = 600000
                    print("\n해당 기기의 견적 산출가는 " + str(price) + "원 입니다.")
                    break
                elif status == 'A':
                    price = 300000
                    print("\n해당 기기의 견적 산출가는 " + str(price) + "원 입니다.")
                    break
                elif status == 'B':
                    price = 100000
                    print("\n해당 기기의 견적 산출가는 " + str(price) + "원 입니다.")
                    break
                elif status == 'C':
                    price = 50000
                    print("\n해당 기기의 견적 산출가는 " + str(price) + "원 입니다.")
                    break
                else:
                    print("잘못된 문자가 입력되었습니다.")
            if int(input("판매하시겠습니까?(Yes = 1, No = 0) : ")):
                self.phone.append(Phone())  # 리스트 마지막에 Phone 클래스의 인스턴스 생성하여 추가
                self.phone[len(self.phone)-1].name = name  # 임시로 저장했던 값 인스턴스 멤버 변수에 대입
                self.phone[len(self.phone)-1].stat = status
                self.phone[len(self.phone)-1].price = price
                input("스마트폰을 키오스크에 넣은 다음 아무키나 눌러주세요... ")
                print("현금 " + str(price) + "원을 받아주세요.\n\n판매해주셔서 감사합니다! 3초 후 메인 메뉴로 돌아갑니다.")
                time.sleep(3)
            else:
                print("\n다음에 만나요! 3초 후 메인메뉴로 돌아갑니다.")
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
                print("\n해당 기기의 판매가는 " + str(self.phone[index].price) + "원 입니다.")
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
        else:
            print("지원되지 않는 명령어입니다. 3초 후 메인메뉴로 돌아갑니다.")
            time.sleep(3)
            return 1


class Phone(object):
    def __init__(self):
        super(Phone, self).__init__()
        self.name = "nonamed"
        self.stat = "notclassified"
        self.price = "0"

    def __del__(self):
        pass


if __name__ == '__main__':
    cnuKiosk = Kiosk()  # 키오스크 인스턴스 생성
    cnuKiosk.boot()  # 키오스크 부팅
    while cnuKiosk.printMainMenu():  # 메인화면 출력 & 종료 옵션 입력 전까지 반복
        cnuKiosk.clear()
    cnuKiosk.shutdown()  # 키오스크 종료
    del cnuKiosk  # 키오스크 인스턴스 닫기

    os.system("pause")
