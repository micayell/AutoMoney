from fastapi import APIRouter, HTTPException, Query
from .lotto_crawler import get_recent_lotto_number, crawl_lotto_numbers
import random
from collections import Counter

router = APIRouter(prefix="/lotto", tags=["lotto"])

# 간단한 인메모리 캐시
lotto_history = []

@router.get("/update")
def update_lotto_data():
    """최신 로또 데이터 업데이트"""
    global lotto_history
    recent_no = get_recent_lotto_number()
    
    # 최근 20회차 수집 (데이터 샘플 확보)
    new_data = []
    for no in range(recent_no, recent_no - 20, -1):
        data = crawl_lotto_numbers(no)
        if data:
            new_data.append(data)
            
    lotto_history = new_data
    return {"status": "updated", "recent_drw_no": recent_no, "count": len(lotto_history)}

@router.get("/recommend")
def recommend_numbers(strategy: str = Query("random", enum=["random", "hot", "cold", "balanced"])):
    """
    전략 기반 번호 추천
    - random: 완전 무작위
    - hot: 최근 자주 나온 번호 가중치
    - cold: 최근 안 나온 번호 우선
    - balanced: hot + cold + random 조합
    """
    if not lotto_history:
        update_lotto_data()
        
    all_nums = []
    for data in lotto_history:
        all_nums.extend(data['numbers'])
        
    # 빈도 분석
    counter = Counter(all_nums)
    
    # 1~45 전체 번호 준비
    all_candidates = list(range(1, 46))
    
    if strategy == "random":
        numbers = random.sample(all_candidates, 6)
        
    elif strategy == "hot":
        # 상위 15개 중에서 4개 + 나머지에서 2개
        most_common = [num for num, _ in counter.most_common(15)]
        if len(most_common) < 6:
            most_common = all_candidates # 데이터 부족 시 전체 대상
            
        hot_picks = random.sample(most_common, min(4, len(most_common)))
        remaining = [n for n in all_candidates if n not in hot_picks]
        others = random.sample(remaining, 6 - len(hot_picks))
        numbers = hot_picks + others
        
    elif strategy == "cold":
        # 빈도가 0이거나 적은 순서대로 정렬
        least_common = [num for num in all_candidates if counter[num] == 0]
        # 안 나온 번호가 부족하면 적게 나온 순으로 추가
        if len(least_common) < 10:
            least_common.extend([num for num, _ in counter.most_common()[:-10:-1]]) # 뒤에서 10개
            
        cold_picks = random.sample(least_common, min(4, len(least_common)))
        remaining = [n for n in all_candidates if n not in cold_picks]
        others = random.sample(remaining, 6 - len(cold_picks))
        numbers = cold_picks + others
        
    elif strategy == "balanced":
        # Hot 2개 + Cold 2개 + Random 2개
        most_common = [num for num, _ in counter.most_common(15)]
        least_common = [num for num in all_candidates if counter[num] == 0]
        if len(least_common) < 6:
             least_common.extend([num for num, _ in counter.most_common()[:-10:-1]])

        hot_picks = random.sample(most_common, 2)
        cold_picks = random.sample([n for n in least_common if n not in hot_picks], 2)
        
        fixed = hot_picks + cold_picks
        remaining = [n for n in all_candidates if n not in fixed]
        random_picks = random.sample(remaining, 2)
        
        numbers = fixed + random_picks
        
    else:
        numbers = random.sample(all_candidates, 6)

    return {"numbers": sorted(numbers), "strategy": strategy}
