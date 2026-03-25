# CampusMarket AI
image TODO

**CampusMarket** 캠퍼스 중고거래 플랫폼의 AI 백엔드 서비스입니다.
<br>
##### 3가지 AI 기능: Google Gemini와 rembg(U2Net)를 기반으로 상품 이미지 분석, 배경 제거, 시간표 파싱
---

## 📢 시스템 아키텍처 & IA

TODO


---

## ⚜️ 주요 기능

| 기능 | 엔드포인트 | 설명 |
|---|---|---|
| 상품 분석 | `POST /api/v1/images/analyze-product` | 상품 이미지를 분석해 카테고리, 상품명, 색상, 상태, 설명을 Gemini로 추출 |
| 배경 제거 | `POST /api/v1/images/remove-background` | U2Net(rembg)으로 배경을 제거하고 base64 인코딩된 WebP를 반환 |
| 시간표 파싱 | `POST /api/v1/timetable/parse-timetable` | 에브리타임 시간표 스크린샷에서 수업 일정을 Gemini로 파싱 |

---

## 🧩 기술 스택

- **런타임**: Python 3.11+
- **프레임워크**: FastAPI
- **AI / ML**
  - [Google Gemini](https://ai.google.dev/) (`gemini-2.0-flash`) — 이미지 이해를 위한 멀티모달 LLM
  - [rembg](https://github.com/danielgatis/rembg) (U2Net) — 배경 제거 AI 모델
- **이미지 처리**: Pillow, OpenCV
- **데이터 검증**: Pydantic v2

---

## ⭐ 프로젝트 구조

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── background_removal.py   # POST /images/remove-background
│       │   ├── product_analysis.py     # POST /images/analyze-product
│       │   └── timetable.py            # POST /timetable/parse-timetable
│       └── router.py
├── constants/
│   └── categories.py   # 메이저/서브 카테고리 정의
├── core/
│   ├── config.py        # 환경변수 설정 (pydantic-settings)
│   ├── dependencies.py  # 파일 유효성 검증 의존성
│   └── gemini_client.py # Gemini 클라이언트 싱글턴
├── schemas/
│   ├── background_removal.py  # BackgroundRemovalResponse
│   ├── product_analysis.py    # ProductAnalysisResponse, ProductCondition
│   └── timetable.py           # ClassEntry, TimetableResponse
├── services/
│   ├── background_removal_service.py  # rembg 배경 제거 로직
│   ├── product_analysis_service.py    # Gemini 상품 분석 로직
│   └── timetable_service.py           # Gemini 시간표 파싱 로직
├── utils/
│   └── image.py   # PIL 유틸리티
└── main.py        # FastAPI 앱 진입점
```

---

## ⭐ API 명세

### `POST /api/v1/images/analyze-product`

상품 이미지를 분석해 구조화된 메타데이터 반환

**요청** — `multipart/form-data`

| 필드 | 타입 | 설명 |
|---|---|---|
| `files` | `UploadFile[]` | 상품 이미지 (JPEG / PNG / WebP, 최대 5장) |

**응답** — `application/json`

```json
{
  "major": "디지털기기",
  "sub_category": "노트북",
  "product_name": "MacBook Air M2",
  "color": "스페이스그레이",
  "condition": "최상",
  "description": "2023년형 맥북 에어 M2 모델입니다. ..."
}
```

| 필드 | 타입 | 값 |
|---|---|---|
| `major` | `string` | 메이저 카테고리 (12개, 아래 참조) |
| `sub_category` | `string` | 서브 카테고리 |
| `product_name` | `string` | 상품명 |
| `color` | `string` | 대표 색상 |
| `condition` | `enum` | `미개봉` / `최상` / `양호` / `보통` |
| `description` | `string` | 상품 설명 (3~5문장) |

---

### `POST /api/v1/images/remove-background`

상품 이미지의 배경을 제거하고 투명 WebP 반환

**요청** — `multipart/form-data`

| 필드 | 타입 | 설명 |
|---|---|---|
| `files` | `UploadFile[]` | 상품 이미지 (JPEG / PNG / WebP, 최대 5장) |

**응답** — `application/json`

```json
{
  "images": ["<base64-encoded WebP>", "..."],
  "count": 2
}
```

반환되는 이미지는 **투명 배경(RGBA) WebP**를 base64 인코딩한 문자열.
처리 전 긴 변 기준 1024px로 리사이즈.

---

### `POST /api/v1/timetable/parse-timetable`

시간표 스크린샷(에브리타임 등)을 분석해 수업 일정 반환

**요청** — `multipart/form-data`

| 필드 | 타입 | 설명 |
|---|---|---|
| `file` | `UploadFile` | 시간표 이미지 (JPEG / PNG / WebP) |

**응답** — `application/json`

```json
{
  "classes": [
    {
      "name": "운영체제",
      "day": "월",
      "start_time": "09:00",
      "end_time": "10:30",
      "location": "공학관 301"
    }
  ],
  "count": 5
}
```

Gemini가 중복으로 인식한 수업 슬롯은 시작 시간을 자동으로 조정해 충돌 해소.


---

## ⭐ 카테고리 참조

| 메이저 카테고리 | 서브 카테고리 |
|---|---|
| 디지털기기 | 노트북, 태블릿, 휴대폰, 스마트워치, 이어폰/헤드폰, 키보드/마우스, 충전기/케이블, 모니터, 기타 전자기기 |
| 전공책 / 교재 | 전공서적, 교양서적, 문제집, 자격증 교재, 어학 교재, 필기노트 / 제본자료, 기타 도서 |
| 문구 / 학용품 | 필기구, 노트 / 다이어리, 파일 / 바인더, 계산기, 독서대, 필통, 기타 학용품 |
| 패션 | 아우터, 상의, 하의, 원피스 / 스커트, 신발, 가방, 모자, 액세서리, 기타 패션잡화 |
| 생활용품 | 수납용품, 침구 / 쿠션, 조명, 거울, 청소용품, 세탁용품, 욕실용품, 기타 생활용품 |
| 자취 / 원룸용품 | 행거, 선반, 테이블, 의자, 소형가전, 주방도구, 식기 / 컵, 전기장판 / 히터, 기타 자취용품 |
| 뷰티 / 미용 | 화장품, 향수, 헤어기기, 미용소품, 네일용품, 기타 뷰티용품 |
| 스포츠 / 취미 | 운동기구, 요가 / 필라테스 용품, 자전거 / 킥보드 용품, 악기, 게임용품, 피규어 / 굿즈, 기타 취미용품 |
| 티켓 / 이용권 | 공연 / 전시, 영화, 스터디룸 / 공간이용권, 헬스장 / 운동권, 기타 이용권 |
| 생활가전 | 드라이기, 고데기, 선풍기, 가습기, 전자레인지, 밥솥, 청소기, 기타 소형가전 |
| 식품 / 소모품 | 미개봉 식품, 음료, 영양제, 생필품, 기타 소모품 |
| 기타 | 분류 어려운 상품, 직접 입력 |

---

## ☀️ 시작하기

### 사전 요구사항

- Python 3.11+
- Google Gemini API 키

### 설치

```bash
git clone https://github.com/SWAG-Graduation-Project/CampusMarket-AI.git
cd CampusMarket-AI
python -m venv .venv
source .venv\Scripts\activate 
pip install -r requirements.txt
```

### 환경변수

프로젝트 루트에 `.env` 파일 생성

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

| 변수 | 기본값 | 설명 |
|---|---|---|
| `GEMINI_API_KEY` | — | Google Gemini API 키 (필수) |
| `MAX_UPLOAD_IMAGES` | `5` | 요청당 최대 이미지 수 |
| `MAX_IMAGE_SIZE_MB` | `10` | 이미지 최대 크기 (MB) |
| `ALLOWED_ORIGINS` | `["*"]` | CORS 허용 오리진 |

### 실행

```bash
uvicorn app.main:app --reload
```

---

## ✨ 에러 코드

| 상태 코드 | 발생 조건 |
|---|---|
| `400 Bad Request` | 파일 미업로드 또는 최대 개수 초과 |
| `415 Unsupported Media Type` | JPEG / PNG / WebP 외 파일 형식 |
| `502 Bad Gateway` | Gemini 응답 파싱 실패 또는 필수 항목 누락 |
| `504 Gateway Timeout` | Gemini API 응답 60초 초과 (시간표 파싱) |

---

## ✨ 설계 결정 사항

**배경 제거는 스레드 풀에서 실행**
`rembg.remove()`는 CPU-bound 연산(신경망 추론)입니다. `async` 함수 내에서 직접 호출하면 이벤트 루프가 블로킹되어 동시 요청 처리 성능이 저하. `asyncio.to_thread`로 각 이미지를 별도 스레드에서 처리해 이벤트 루프를 비워둠.

**Gemini 응답 파싱 방어 처리**
Gemini는 JSON을 `` ```json ... ``` `` 마크다운 블록으로 감싸서 반환하는 경우가 있음. 파서는 해당 래핑을 제거한 뒤 `json.loads`를 시도하며, 파싱 실패 시 원시 예외 대신 `502`를 반환.

**시간표 충돌 해소**
Gemini가 겹치는 수업 슬롯을 할루시네이션으로 생성할 수 있음. 서비스에서 요일별로 시작 시간순 정렬 후 겹치는 항목의 시작 시간을 앞 수업 종료 시간으로 밀어내어 클라이언트에 중복 없는 결과를 반환함.
