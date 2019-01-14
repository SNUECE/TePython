# -*- coding: utf-8 -*-

import os
import time
import math

화면지우기 = lambda: os.system("cls" if os.name=="nt" else "clear")

평점대응목록 = {
    'A+': 4.3,
    'A0': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B0': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C0': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D0': 1.0,
    'D-': 0.7,
    'F': 0,
}

class 학기:
    def __init__(self, 연도, 계절, 수강강의목록=[]):
        assert type(연도)==int
        assert type(계절)==str
        for 수강강의 in 수강강의목록:
            assert isinstance(수강강의, 강의)
        self.연도 = 연도
        self.계절 = 계절
        self.수강강의목록 = []

        self.수강학점 = 0
        self.평점산정학점 = 0
        self.평균평점 = 0
        for 수강강의 in 수강강의목록:
            self.강의추가(수강강의)

    def 강의추가(self, 수강강의):
        self.수강강의목록.append(수강강의)

        if 수강강의.학점 is None:
            print(수강강의.강의명 + "의 학점이 지정되지 않았습니다!")
            return

        self.수강학점 += 수강강의.학점

        if 수강강의.평점 is None:
            print(수강강의.강의명 + "의 평점이 지정되지 않았습니다!")
            return

        # TODO - 정확한 분수 나눗셈
        self.평균평점 = (self.평균평점 * self.평점산정학점 + 평점대응목록[수강강의.평점] * 수강강의.학점) / (self.평점산정학점 + 수강강의.학점)
        self.평점산정학점 += 수강강의.학점

    def 통계(self):
        if self.평균평점 > 0:
            print("%d년 %s학기의 수강 학점은 %d이고 평균 평점은 %.2f입니다." % (self.연도, self.계절, self.수강학점, math.floor(self.평균평점 * 100) / 100))
        else:
            print("%d년 %s학기의 수강 학점은 %d입니다." % (self.연도, self.계절, self.수강학점))


class 강의:
    def __init__(self, 강의명, 수강학기, 학점=None, 평점=None):
        assert type(강의명)==str
        assert isinstance(수강학기, 학기)
        assert 학점 is None or type(학점)==int
        assert 평점 is None or 평점 in 평점대응목록
        self.강의명 = 강의명
        self.학기 = 학기
        self.학점 = 학점
        self.평점 = 평점

    def __repr__(self):
        출력값 = "강의명: " + self.강의명
        if 학점 is not None:
            출력값 += "\n학점: " + str(self.학점)
        if 평점 is not None:
            출력값 += "\n평점: " + self.평점
        return 출력값


전체수강학기 = []
수강강의목록 = []
while True:
    화면지우기()
    print("학기를 추가하려면 1, 강의를 추가하려면 2, 학기 정보를 확인하려면 3을 입력하세요.")
    입력모드 = int(input())
    if 입력모드 not in list(range(4)):
        print("잘못 입력하셨습니다. ",)
        time.sleep(0.5)
        continue
    if 입력모드==1:
        print("추가할 학기 연도를 입력하세요. (예: 2018)")
        # TODO - 예외 처리 (연도나 계절이 각각 정수나 문자열이 아닐 경우)
        입력연도 = int(input())
        print("추가할 학기 계절을 입력하세요. (예: 봄)")
        입력계절 = input()
        전체수강학기.append(학기(입력연도, 입력계절))
        print("%d년 %s학기가 추가되었습니다." % (입력연도, 입력계절))
        time.sleep(0.5)
    elif 입력모드==2:
        if 전체수강학기 == []:
            print("학기를 먼저 추가하세요!")
            time.sleep(0.5)
            continue
        print("강의를 추가할 학기 번호를 선택하세요.")
        for i in range(len(전체수강학기)):
            print("%d: %d년 %s학기" % (i, 전체수강학기[i].연도, 전체수강학기[i].계절))
        # TODO - 예외 처리 (학기 선택 번호 범위)
        선택학기 = 전체수강학기[int(input())]
        print("%d년 %s학기를 선택하셨습니다." % (선택학기.연도, 선택학기.계절))
        print("추가할 강의의 명칭을 입력하세요. (예: 서양 철학의 이해)")
        강의명 = input()
        print("추가할 강의의 학점을 입력하세요. (예: 3)")
        학점 = int(input())
        print("추가할 강의의 평점을 입력하세요. 그냥 엔터를 치시면 평균평점에 반영되지 않습니다. (예: A+)")
        평점 = input()
        # TODO - 예외 처리 (평점 재입력 가능하게)
        assert 평점 in 평점대응목록
        추가강의 = 강의(강의명, 선택학기, 학점=학점, 평점=평점)
        선택학기.강의추가(추가강의)
    elif 입력모드==3:
        print("정보를 확인할 학기 번호를 선택하세요.")
        for i in range(len(전체수강학기)):
            print("%d: %d년 %s학기" % (i, 전체수강학기[i].연도, 전체수강학기[i].계절))
        # TODO - 예외 처리 (학기 선택 번호 범위)
        선택학기 = 전체수강학기[int(input())]
        print("%d년 %s학기를 선택하셨습니다." % (선택학기.연도, 선택학기.계절))
        for 수강강의 in 선택학기.수강강의목록:
            print(수강강의.강의명)
            print(수강강의.__repr__())
            print()
        선택학기.통계()
        print("돌아가려면 엔터를 누르세요...")
        엔터 = input()
    elif 입력모드==0:
        break

