# AutoMoney 개발 계획 (Spring + FastAPI Hybrid)

## 1. 프로젝트 개요
**AutoMoney**는 Spring Boot의 안정성과 Python의 데이터 분석/자동화 강점을 결합한 금융 플랫폼입니다.  
사용자 데이터 기반의 웹/앱 서비스 확장을 고려하여 PostgreSQL을 도입하고, Google Analytics(GA4)를 통해 사용자 행동 데이터를 수집/분석하여 포트폴리오의 통계 역량을 강조합니다.

## 2. 시스템 아키텍처 (Hybrid Architecture)

```mermaid
graph TD
    User[사용자 (Web/Mobile)] -->|HTTP/HTTPS| Frontend[Frontend (React)]
    Frontend -->|Tracking| GA4[Google Analytics 4]
    Frontend -->|API Call| SpringBoot[Main Backend (Spring Boot)]
    
    subgraph "Main Service (Java)"
        SpringBoot --> Auth[인증/권한]
        SpringBoot --> AssetCore[자산 관리 코어]
        SpringBoot -->|REST Client| FastAPIService
    end
    
    subgraph "Data & Bot Service (Python)"
        FastAPIService[FastAPI Server]
        FastAPIService --> StockBot[주식 매매 봇 (KIS)]
        FastAPIService --> LottoAnal[로또 분석기]
        FastAPIService --> StatsEngine[통계 엔진 (Pandas/Scipy)]
    end
    
    subgraph "Infrastructure"
        SpringBoot --> DB[(PostgreSQL)]
        FastAPIService --> DB[(PostgreSQL)]
        StockBot <--> KIS[한국투자증권 API]
        LottoAnal <--> Crawl[동행복권]
    end
```

## 3. 기술 스택 (Tech Stack)

| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Frontend** | **React**, TypeScript | Vite, Tailwind CSS, Recharts (차트) |
| **Analytics** | **Google Analytics 4** | 사용자 행동 추적, 커스텀 이벤트 설정 |
| **Main Backend** | **Spring Boot (Java 17)** | Spring Data JPA, Spring Security, Gradle |
| **Sub Backend** | **FastAPI (Python 3.10+)** | Pandas, Numpy (데이터 분석), APScheduler |
| **Database** | **PostgreSQL** | 관계형 데이터베이스 (Docker Compose 권장) |
| **External** | 한국투자증권 API | 주식 매매 및 시세 조회 |

## 4. 상세 기능 및 역할 분담

### A. Spring Boot (Main Backend)
*   **역할:** 사용자 요청의 진입점, 비즈니스 로직(CRUD), 데이터 무결성 관리.
*   **기능:**
    *   **사용자 관리:** 회원가입, 로그인 (JWT), 권한 관리.
    *   **자산 관리 (가계부):** 수입/지출 내역 CRUD, 자산 현황 조회 API.
    *   **프록시 역할:** 프론트엔드에서 요청한 주식/로또 데이터를 FastAPI로 전달받아 응답.

### B. FastAPI (Data & Bot Service)
*   **역할:** Python 생태계가 강점인 주식 매매, 데이터 크롤링, 고급 통계 분석 수행.
*   **기능:**
    *   **주식 봇:** KIS API 토큰 관리, 자동 매매 로직 수행, 실시간 감시.
    *   **로또 분석:** 과거 데이터 크롤링, 회귀 분석/확률 모델링을 통한 번호 추출.
    *   **통계 분석:** 자산 데이터 및 사용자 활동 데이터를 기반으로 통계적 인사이트 도출 (R/SAS 경험 활용 포인트).

### C. 데이터 분석 및 통계 (Portfolio Point)
*   **GA4 연동:** 페이지 방문, 버튼 클릭, 체류 시간 등 사용자 행동 로그 수집.
*   **통계 대시보드:**
    *   자산 변동성에 대한 표준편차, 샤프 지수 등 금융 통계 지표 계산 (Python).
    *   GA4 데이터를 BigQuery 등으로 내보내거나, 자체 DB 로그를 분석하여 "주간 금융 습관 리포트" 생성.

## 5. 개발 로드맵

### Phase 1: 인프라 및 환경 설정 (Infrastructure) - **[완료]**
*   PostgreSQL Docker 컨테이너 구동.
*   Spring Boot & FastAPI 프로젝트 초기 세팅 및 DB 연결 테스트.
*   React 프로젝트 생성 및 GA4 스크립트 삽입.

### Phase 2: 메인 백엔드 및 자산 관리 (Core Features) - **[진행 중]**
*   [Spring] 회원가입/로그인 구현 (Spring Security).
*   [Spring] 자산(가계부) 입력/수정/삭제 API 구현.
*   [React] 대시보드 UI 및 자산 입력 폼 구현.

### Phase 3: 주식 봇 및 로또 서비스 (Python Services)
*   [FastAPI] 한국투자증권 API 연동 및 매매 모듈 구현.
*   [FastAPI] 로또 크롤러 및 번호 추천 알고리즘 구현.
*   [Spring-FastAPI] 서버 간 통신 (RestTemplate or WebClient) 구현.

### Phase 4: 고도화 및 분석 (Analytics & Advanced)
*   통계 엔진 구현 (내 자산 흐름 회귀 분석 등).
*   텔레그램 알림 연동 (매매 체결 시).
*   최종 통합 테스트 및 배포 준비.

## 6. 디렉토리 구조
```
AutoMoney/
├── backend-java/       # Spring Boot Project
│   ├── src/main/java/com/automoney/...
│   └── build.gradle
├── backend-python/     # FastAPI Project
│   ├── app/
│   │   ├── bot/        # 주식 봇 로직
│   │   ├── analysis/   # 통계/분석 로직
│   │   └── main.py
│   └── requirements.txt
├── frontend/           # React Project
│   ├── src/
│   │   ├── api/
│   │   ├── pages/
│   │   └── App.tsx
└── docker-compose.yml  # DB 및 서비스 오케스트레이션
```

