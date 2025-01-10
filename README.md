
# 이울진료회 대량문자 전송 스크립트

<p align="center">
    <img src="ewoollogo.png" alt="E-Wool Logo" />
</p>


이 스크립트는 알리고 API를 이용하여 동아리 주소록에 저장된 전화번호로 SMS 또는 MMS를 전송하는 Python 프로그램입니다. 메시지와 제목, 이미지 파일을 입력받아 지정된 번호로 전송합니다.

## 1. 가상환경 세팅 및 요구사항 설치

### 가상환경 생성 및 활성화
가상환경의 이름을 `ewool`로 설정하고 설치를 진행합니다.

```bash
# 가상환경 생성
python -m venv ewool

# 가상환경 활성화 (Windows)
ewool\Scripts\activate

# 가상환경 활성화 (macOS / Linux)
source ewool/bin/activate
```

### 요구사항 설치
`requirements.txt` 파일에 정의된 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 2. 환경변수 SMARTSMS_API_KEY 설정

알리고 API 키를 환경변수로 설정해야 합니다.

### `.env` 파일 생성
다음 내용을 포함한 `.env` 파일을 프로젝트 루트 디렉토리에 생성합니다.

```
SMARTSMS_API_KEY=(API키)
```

### `.env` 파일이 설정되면 프로그램은 이를 자동으로 로드합니다.

## 3. 작동 방법

### 명령어 실행
다음 명령어 형식을 사용하여 스크립트를 실행합니다.

```bash
python script.py --excel <엑셀 파일 경로> --image <이미지 파일 경로> --msg <메시지 내용> --title <MMS 제목>
```

### 명령어 인자 설명
- `--excel`: 전화번호가 저장된 Excel 파일의 경로를 입력합니다.
- `--image`: MMS 전송에 사용할 이미지 파일의 경로를 입력합니다.
- `--msg`: 보낼 메시지 내용을 입력합니다.
- `--title`: MMS 제목을 입력합니다.

### 예제
```bash
python script.py --excel ewool_address.xlsx --image image.jpg --msg "(공지 내용)" --title "이울진료회 공지"
```

## 4. 코드 설명
### 주요 기능
1. **Excel 파일 읽기**: 전화번호 리스트를 각 시트 별로 읽어옵니다.
2. **전화번호 유효성 검사**: 정규 표현식 (`^\d{3}-\d{4}-\d{4}$`)을 이용하여 올바른 형식의 전화번호만 처리합니다.
3. **SMS 데이터 생성**: `StaticFuncs.getSMSData` 메서드를 이용해 메시지 데이터를 구성합니다.
4. **MMS 전송**: 알리고 API에 데이터를 전송합니다.
5. **에러 처리**: 전송 실패한 건수를 기록하며 진행 상황을 표시합니다.

## 주의사항
- Excel 파일의 시트별로 `휴대폰 (연락처)` 열이 존재해야 합니다.
- 이미지 파일의 크기와 형식은 알리고 API의 요구사항을 준수해야 합니다.
