import requests
from bs4 import BeautifulSoup
import re

def get_recent_lotto_number():
    """
    동행복권 메인 페이지에서 최신 회차 번호를 가져옵니다.
    """
    url = "https://dhlottery.co.kr/common.do?method=main"
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        # id="lottoDrwNo" 인 span 태그 찾기
        drw_no_tag = soup.find("strong", id="lottoDrwNo")
        if drw_no_tag:
            return int(drw_no_tag.text)
        return 1100 # Fallback
    except:
        return 1100

def crawl_lotto_numbers(drw_no):
    """
    특정 회차의 당첨 번호를 크롤링합니다.
    """
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={drw_no}"
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        
        # 당첨 번호 추출 (ball_645 클래스)
        nums = []
        ball_tags = soup.select(".ball_645")
        for tag in ball_tags:
            # 보너스 번호 제외하고 앞의 6개만 가져오거나 구분 필요
            # 보통 6개 + 1개(보너스) 순서로 나옴
            try:
                nums.append(int(tag.text))
            except ValueError:
                pass
                
        if len(nums) >= 6:
            return {
                "drw_no": drw_no,
                "numbers": nums[:6],
                "bonus": nums[6] if len(nums) > 6 else None
            }
        return None
    except Exception as e:
        print(f"Error crawling {drw_no}: {e}")
        return None

