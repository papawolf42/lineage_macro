# 14_sanghpar 사용법

## 개요

이 저장소는 Windows 환경에서 `Lineage Classic` 클라이언트를 대상으로 동작하는 매크로 프로젝트다. 구조는 크게 4개다.

- `server.py`: 교환 감지, 아데나 계산, 픽업 분배를 담당하는 메인 프로세스
- `client.py`: 서버 지시를 받아 픽업과 포션 사용을 수행하는 보조 클라이언트
- `arduino_proxy.py`: Python과 Arduino HID 장치 사이의 로컬 프록시
- `macro.py`: 스크린샷 OCR, 입력 전송, 창 탐색, 방향 전환 등 핵심 로직

핵심 동작은 다음 흐름이다.

1. 서버가 로컬 게임 화면을 스크린샷으로 읽는다.
2. 닉네임, MP, 아데나, 교환 슬롯 밝기를 OCR과 픽셀 분석으로 판정한다.
3. 교환으로 받은 아데나를 `adena_per_pickup` 값으로 나눠 픽업 횟수를 계산한다.
4. 서버 자신과 연결된 클라이언트들에게 픽업 명령을 분배한다.

## 처음 익히는 순서

처음 쓰는 사람은 문서를 처음부터 끝까지 한 번에 읽기보다, 아래 순서로 이해하는 편이 빠르다. 이 프로젝트는 하드웨어, 게임 창, 네트워크, 좌표 설정이 모두 맞아야 돌아가므로 "실행 순서"보다 먼저 "무엇이 필요한지"를 잡는 게 중요하다.

### 1. 먼저 전체 구조부터 이해한다

아래 순서로 읽는다.

1. `개요`
2. `파일별 역할`
3. `동작 방식`

여기서 먼저 이해해야 하는 건 아래 4개다.

- `server.py`가 중심이다.
- `client.py`는 보조 유닛이다.
- `arduino_proxy.py`와 `macro_hid.ino`가 실제 키보드/마우스 입력을 만들어낸다.
- `macro.py`가 OCR, 클릭, 방향 전환 같은 핵심 로직을 담당한다.

이 단계에서는 아직 실행하지 말고, "어떤 프로세스가 어떤 역할을 하는지"만 이해하면 된다.

### 2. 내 환경에서 바꿔야 하는 값부터 찾는다

그 다음은 아래 항목을 확인한다.

1. `arduino_proxy.py`의 `SERIAL_PORT`
2. `client.py`의 `SERVER_HOST`
3. `macro_data.json`의 좌표값

즉, 처음 보는 사람은 코드를 고치기 전에 아래 3가지를 먼저 메모하는 게 좋다.

- Arduino가 실제로 어느 COM 포트에 잡히는지
- 서버 PC IP가 무엇인지
- 게임 창 위치와 UI 배치가 현재 좌표와 맞는지

이 단계는 `전제 조건`, `설정 파일`, `트러블슈팅`을 같이 보면서 확인하면 된다.

### 3. 실행은 항상 작은 단위부터 확인한다

처음부터 전체 자동화를 돌리면 어디서 깨졌는지 찾기 어렵다. 아래 순서로 한 단계씩 확인한다.

1. `arduino_proxy.py` 단독 실행
2. `server.py` 단독 실행
3. `client.py 1` 단독 실행
4. 서버와 클라이언트 연결 확인
5. 마지막에 exchange 루프 시작

즉, 처음 목표는 "자동 사냥 전체 성공"이 아니라 아래를 하나씩 통과하는 것이다.

- 프록시가 뜨는가
- 서버가 게임 창을 찾는가
- 클라이언트가 서버에 붙는가
- MP / OCR / 포션 / 픽업 로그가 정상적으로 보이는가

### 4. 막히면 ASCII 워크플로우를 본다

본문의 `실행 순서`는 실제 실행용 체크리스트이고, `ASCII 워크플로우`는 내부 동작을 머릿속에 그리기 위한 설명이다. 따라서 읽는 순서는 아래처럼 잡는 게 좋다.

1. `실행 순서`를 먼저 따라간다.
2. 어느 단계에서 왜 필요한지 헷갈리면 `ASCII 워크플로우`를 본다.
3. 특정 로그나 동작이 이해되지 않으면 `동작 방식`으로 내려간다.

즉, `ASCII 워크플로우`는 처음부터 정독하는 장이 아니라, 실행 중에 참조하는 장에 가깝다.

### 5. 첫 실행 목표를 낮게 잡는다

처음에는 아래까지만 성공해도 충분하다.

1. 프록시 실행
2. 서버 실행
3. 클라이언트 1대 연결
4. 창 탐색과 MP 읽기 로그 확인

첫날부터 완전 자동 교환/픽업까지 한 번에 검증하려고 하지 않는 편이 좋다. 이 프로젝트는 좌표, OCR, 포트, 창 제목, Arduino 입력이 모두 엮여 있어서 한 번에 보면 원인 분리가 안 된다.

### 6. 추천 학습 루트 요약

처음 익힐 때는 아래 순서로 진행한다.

1. `개요`와 `파일별 역할`을 읽는다.
2. `전제 조건`과 `설정 파일`에서 내 환경 차이를 체크한다.
3. `실행 순서`대로 프록시, 서버, 클라이언트를 하나씩 띄운다.
4. 문제가 생기면 `트러블슈팅`을 먼저 본다.
5. 그래도 이해가 안 되면 `ASCII 워크플로우`와 `동작 방식`으로 내려간다.

이 문서는 위 순서대로 따라갈 때 가장 읽기 쉽도록 정리되어 있다고 생각하면 된다.

## 전제 조건

- OS: Windows
- Python: `pywin32`, `Pillow`, `pyserial`, `numpy` 사용 가능 환경
- 하드웨어: Arduino Leonardo / Micro / Pro Micro 같이 USB HID를 지원하는 보드
- 게임 창: `Lineage Classic`으로 시작하는 창이 최소 1개 이상 열려 있어야 함
- 입력 방식: Windows Message가 아니라 Arduino HID + 일부 Win32 창 제어 혼합 방식

## 파일별 역할

- `server.py`
  교환 감시 루프를 실행한다. 로컬 창을 `server`로 잡고, TCP `9999` 포트에서 클라이언트를 받는다.

- `client.py`
  `python client.py <idx>` 형태로 실행한다. 서버에서 `ping`, `pickup`, `potion`, `reset_target` 명령을 받는다.

- `arduino_proxy.py`
  `COM5`를 열고 `127.0.0.1:9998`에서 TCP 요청을 받아 Arduino 시리얼 명령으로 바꾼다. 서버/클라이언트보다 먼저 실행해야 한다.

- `macro_hid.ino`
  Arduino 스케치다. `KD`, `KU`, `KP`, `CL`, `CR`, `MM`, `BS`, `INIT` 같은 명령을 받아 실제 HID 키보드/마우스 입력으로 처리한다.

- `macro_data.json`
  서버/클라이언트별 클릭 좌표, 방향 전환 좌표, 픽업 단가, 방향 전환 기준값을 저장한다.

- `converted_data.json`
  OCR 문자 매핑 데이터다. 스크린샷에서 뽑은 문자 픽셀 패턴을 실제 문자로 변환할 때 사용한다.

## 설치

### 1. Python 의존성 설치

```powershell
pip install -r requirements.txt
```

`requirements.txt` 내용은 아래 4개다.

- `pywin32`
- `Pillow`
- `pyserial`
- `numpy`

### 2. Arduino 스케치 업로드

`macro_hid.ino`를 USB HID 지원 보드에 업로드한다.

- 권장 보드: Leonardo, Micro, Pro Micro
- 시리얼 속도: `115200`
- 업로드 후 Windows에서 COM 포트를 확인한다.

### 3. 프록시 포트 확인

`arduino_proxy.py` 기본값은 아래와 같다.

```python
SERIAL_PORT = 'COM5'
BAUD_RATE   = 115200
PROXY_HOST  = '127.0.0.1'
PROXY_PORT  = 9998
```

보드가 `COM5`가 아니면 `SERIAL_PORT`를 수정해야 한다.

### 4. 서버 IP 확인

`client.py`는 서버 주소가 하드코딩되어 있다.

```python
SERVER_HOST = '220.119.210.140'
SERVER_PORT = 9999
```

실제 서버 PC의 IP와 다르면 `SERVER_HOST`를 수정해야 한다.

## 실행 순서

### 1. Arduino 프록시 실행

서버를 돌리는 PC에서 먼저 실행한다.

```powershell
python .\arduino_proxy.py
```

정상 실행되면 아래 성격의 로그가 보인다.

```text
[proxy] Arduino 연결됨: COM5 @ 115200
[proxy] 대기 중: 127.0.0.1:9998
```

### 2. 서버 실행

서버용 `Lineage Classic` 창을 연 뒤 실행한다.

```powershell
python .\server.py
```

실행 직후 `macro.init_setting("server")`가 수행된다. 이 함수는 다음 동작을 한다.

- 보이는 윈도우를 검사한다.
- `Lineage Classic`으로 시작하는 창을 찾는다.
- 해당 창 제목을 `server`로 바꾼다.
- 창 위치를 `(0, 0)`으로 옮긴다.
- `macro_data.json`에서 좌표와 방향 설정을 로드한다.

서버 콘솔에서 사용할 수 있는 명령은 다음과 같다.

- `1`: exchange 루프 시작
- `2`: exchange 루프 중지
- `q`: 서버 종료

### 3. 클라이언트 실행

클라이언트는 서버와 같은 PC 또는 다른 PC에서 실행할 수 있다.

```powershell
python .\client.py 1
```

`1`은 클라이언트 인덱스다. 같은 물리 PC에서 여러 클라이언트를 돌리면 같은 `idx`를 쓸 수 있게 설계되어 있다. 실행 후 콘솔 명령은 아래와 같다.

- `1`: 서버 연결 시작
- `2`: 서버 연결 중지
- `q`: 클라이언트 종료

클라이언트도 시작 시 `macro.init_setting("client")`를 호출한다. 이때 창 제목은 `client`, `client2`, `client3`처럼 자동 지정된다.

### 4. 단일 PC로 최소 구성 실행

클라이언트 없이 서버만으로도 일부 동작은 가능하다. `server.py`는 시작 시 자기 자신을 `idx=0` 클라이언트처럼 내부 등록한다.

- 로컬 MP 측정
- 로컬 포션 사용
- 로컬 픽업 실행

다만 원래 설계는 여러 클라이언트의 MP를 합산해 픽업을 분배하는 형태다.

## ASCII 워크플로우

### 1. 전체 구성도

```text
+--------------------------------------------------------------------------------------+
|                                      운영 전체 구조                                   |
+--------------------------------------------------------------------------------------+

  [서버 PC]
  +----------------------------------------------------------------------------------+
  |  Lineage Classic 창                                                              |
  |    -> 실행 후 제목이 "server" 로 변경될 수 있음                                  |
  |    -> 위치는 (0, 0) 으로 이동됨                                                  |
  |                                                                                  |
  |  server.py                                                                       |
  |    -> 교환 감시                                                                  |
  |    -> MP/아데나/OCR 읽기                                                         |
  |    -> 픽업 분배                                                                  |
  |    -> TCP 9999 listen                                                            |
  |                                                                                  |
  |  macro.py                                                                        |
  |    -> screenshot()                                                               |
  |    -> readMp(), readAdena(), readExchangeNickname()                              |
  |    -> pickup_lineage1(), use_potion(), arduino_type_string()                     |
  |                                                                                  |
  |  arduino_proxy.py                                                                |
  |    -> COM5 open                                                                  |
  |    -> 127.0.0.1:9998 listen                                                      |
  |                                                                                  |
  |  macro_hid.ino on Arduino                                                        |
  |    -> Serial command 수신                                                        |
  |    -> 실제 HID 키보드/마우스 입력 발생                                           |
  +----------------------------------------------------------------------------------+
                |                                                 ^
                | TCP 9999                                         | TCP 127.0.0.1:9998
                v                                                 |
  [클라이언트 PC or 같은 PC의 다른 게임 창들]                      |
  +----------------------------------------------------------------------------------+
  |  client.py                                                                       |
  |    -> 서버 register                                                              |
  |    -> ping 수신 시 MP 읽어서 pong 응답                                           |
  |    -> pickup 수신 시 pickup_lineage1() 실행                                      |
  |    -> potion 수신 시 use_potion() 실행                                           |
  |                                                                                  |
  |  macro.py                                                                        |
  |    -> 로컬 게임창 제목을 client / client2 / client3 로 맞춤                      |
  |    -> 필요 시 프록시로 HID 명령 전달                                             |
  +----------------------------------------------------------------------------------+

  [설정 / 데이터 파일]
  +----------------------------------------------------------------------------------+
  |  requirements.txt     -> Python 패키지 목록                                      |
  |  macro_data.json      -> 좌표 / 방향 / 단가 설정                                 |
  |  converted_data.json  -> OCR 문자 매핑                                           |
  |  tools/*.py           -> 창 확인 / OCR 디버그 / 데이터 생성                      |
  +----------------------------------------------------------------------------------+
```

### 2. 부팅 순서와 프로세스 연결

```text
+--------------------------------------------------------------------------------------+
|                                 실행 준비부터 운영 시작까지                          |
+--------------------------------------------------------------------------------------+

  Step 0. 사전 준비
    |
    +--> Arduino 보드에 macro_hid.ino 업로드
    |      |
    |      +--> 보드는 Leonardo / Micro / Pro Micro 계열이어야 함
    |      +--> COM 포트 확인
    |
    +--> 게임창 실행
    |      |
    |      +--> 최소 1개 이상 Lineage Classic 창 필요
    |      +--> 여러 클라이언트면 게임창 여러 개 필요
    |
    +--> 설정 확인
           |
           +--> arduino_proxy.py 의 SERIAL_PORT 확인
           +--> client.py 의 SERVER_HOST 확인
           +--> macro_data.json 좌표 확인

  Step 1. 서버 PC에서 프록시 실행
    |
    +--> python .\arduino_proxy.py
           |
           +--> COM5 open
           +--> 127.0.0.1:9998 listen
           +--> 이후 server.py / client.py 의 HID 명령을 받아줄 준비 완료

  Step 2. 서버 PC에서 서버 실행
    |
    +--> python .\server.py
           |
           +--> macro.init_setting("server")
           |      |
           |      +--> visible window enumerate
           |      +--> "Lineage Classic*" 창 하나 선택
           |      +--> 창 제목을 "server" 로 세팅할 수 있음
           |      +--> 창 위치를 (0, 0) 으로 이동
           |      +--> macro_data.json 로드
           |      +--> server_mouse_x_y, 방향 정보, 단가 정보 적용
           |
           +--> TCP 9999 bind/listen
           +--> 자기 자신을 idx=0 로 내부 _clients 에 등록
           +--> 콘솔 대기
                  |
                  +--> 입력 1 = exchange 루프 시작
                  +--> 입력 2 = exchange 루프 중지
                  +--> 입력 q = 종료

  Step 3. 각 클라이언트에서 클라이언트 실행
    |
    +--> python .\client.py 1
           |
           +--> macro.init_setting("client")
           |      |
           |      +--> visible window enumerate
           |      +--> "Lineage Classic*" 창 하나 선택
           |      +--> 창 제목을 client / client2 / client3 로 세팅
           |      +--> 창 위치를 (0, 0) 으로 이동
           |      +--> client_mouse_x_y 또는 client_numbering_mouse_x_y 적용
           |
           +--> 콘솔 대기
                  |
                  +--> 입력 1 = 서버 연결 시작
                  +--> 입력 2 = 연결 중지
                  +--> 입력 q = 종료

  Step 4. 클라이언트 연결 시도
    |
    +--> client.py
           |
           +--> connect(SERVER_HOST, 9999)
           +--> {"cmd":"register","idx":CLIENT_IDX} 전송
           +--> 서버는 _clients 에 등록
           +--> 연결 유지 루프 진입

  Step 5. 서버에서 exchange 시작
    |
    +--> server 콘솔에서 1 입력
           |
           +--> exchange_thread 시작
           +--> exchange_loop() 진입
           +--> WAIT_NICKNAME 상태부터 반복 시작
```

### 3. 서버 상태 머신 상세도

```text
+--------------------------------------------------------------------------------------+
|                               server.py exchange_loop() 상태도                       |
+--------------------------------------------------------------------------------------+

  +-------------------+
  |   WAIT_NICKNAME   |
  +-------------------+
            |
            | 1) macro.screenshot(hwnd=server_hwnd)
            | 2) readMp(img)
            | 3) 서버 자신의 mp/available 갱신
            | 4) 연결된 클라이언트들의 마지막 mp/available 합산
            | 5) total_count 출력
            | 6) total_count 와 direction_threshold 비교
            | 7) 필요 시 low/high 방향으로 회전
            | 8) 30초마다 광고 문구 타이핑
            | 9) readExchangeNickname(img)
            |
            +--> 닉네임 없음
            |      |
            |      +--> F7 입력
            |      +--> sleep
            |      +--> WAIT_NICKNAME 반복
            |
            +--> 닉네임 있음
                   |
                   +--> greeted_nickname 저장
                   +--> stage = READ_ADENA
                   v

  +-------------------+
  |    READ_ADENA     |
  +-------------------+
            |
            | 1) 교환 닉네임이 여전히 있는지 다시 확인
            | 2) 없으면 WAIT_NICKNAME 으로 롤백
            | 3) readAdena() 로 교환 전 아데나 읽기
            | 4) F7 입력
            | 5) stage = MONITOR_BRIGHTNESS
            v

  +----------------------+
  |  MONITOR_BRIGHTNESS  |
  +----------------------+
            |
            | 1) screenshot()
            | 2) 교환 닉네임이 사라졌는지 확인
            | 3) 슬롯 영역 crop(258,677,30,30)
            | 4) 평균 밝기 계산
            | 5) 이전 밝기와 비교
            |
            +--> 밝기 변화 없음
            |      |
            |      +--> prev_brightness 갱신
            |      +--> 0.5초 sleep
            |      +--> MONITOR_BRIGHTNESS 반복
            |
            +--> 밝기 변화 있음
            |      |
            |      +--> brightness_changed = True
            |      +--> acceptExchange()
            |      +--> 계속 감시
            |
            +--> 닉네임 사라짐
                   |
                   +--> stage = PICKUP
                   v

  +-------------------+
  |      PICKUP       |
  +-------------------+
            |
            | 1) brightness_changed 가 False 면 아무것도 안 하고 초기화
            | 2) readAdena() 로 교환 후 아데나 읽기
            | 3) received = adena_after - adena_before
            | 4) pickup_count = received // adena_per_pickup
            | 5) clients_snapshot 기반 pickup_avail 복제
            | 6) remaining = min(pickup_count, total_available)
            | 7) 분배 루프 수행
            | 8) 감사 메시지 입력
            | 9) stage = WAIT_NICKNAME 로 복귀
            v

  +-------------------+
  |   WAIT_NICKNAME   |
  +-------------------+

  상태 복귀 시 추가 동작
    |
    +--> 이전 stage 가 READ_ADENA 이상이었다면
           |
           +--> TAB 입력
           +--> macro.target_locked = False
           +--> 모든 클라이언트에 {"cmd":"reset_target"} 브로드캐스트
```

### 4. ping, MP 수집, 포션 사용 흐름

```text
+--------------------------------------------------------------------------------------+
|                             ping / pong / MP / potion 루프                           |
+--------------------------------------------------------------------------------------+

  server.py _handle_client(thread per client)
    |
    +--> while connected:
           |
           +--> send {"cmd":"ping"}
           |
           +--> client.py 수신
           |      |
           |      +--> macro.readMp()
           |      |      |
           |      |      +--> screenshot()
           |      |      +--> MP 영역 crop
           |      |      +--> converted_data.json 으로 OCR
           |      |
           |      +--> {"status":"pong","mp":<value>} 응답
           |
           +--> server 가 mp 저장
           +--> available = mp // 20 계산
           +--> _try_use_potion(client) 판단
                  |
                  +--> available != 0 이면 포션 안 씀
                  |
                  +--> available == 0 이고 쿨다운 경과
                         |
                         +--> 서버 로컬 유닛이면
                         |      |
                         |      +--> macro.use_potion()
                         |      +--> F8 입력
                         |
                         +--> 원격 클라이언트면
                                |
                                +--> send {"cmd":"potion"}
                                +--> client 가 use_potion() 수행
                                +--> {"status":"ok"} ack
```

### 5. 픽업 분배 흐름 상세도

```text
+--------------------------------------------------------------------------------------+
|                                아데나 수령 후 픽업 분배                              |
+--------------------------------------------------------------------------------------+

  교환 완료 직후
    |
    +--> server.readAdena() = adena_after
    +--> received = adena_after - adena_before
    +--> pickup_count = received // adena_per_pickup
    +--> total_available = sum(client.available)
    +--> remaining = min(pickup_count, total_available)
    |
    +--> while remaining > 0:
           |
           +--> available > 0 인 유닛만 추림
           +--> 그중 최대 available 값 찾음
           +--> max available 인 후보들만 추림
           +--> idx 내림차순 정렬
           |
           +--> 각 후보에 대해:
                  |
                  +--> 같은 idx 로 최근 전송 후 1초 미만이면 대기
                  |
                  +--> 서버 로컬 유닛인가?
                  |      |
                  |      +--> YES
                  |      |      |
                  |      |      +--> macro.pickup_lineage1(target_nickname)
                  |      |      +--> remaining -= 1
                  |      |      +--> pickup_avail[server] -= 1
                  |      |
                  |      +--> NO, 원격 클라이언트
                  |             |
                  |             +--> send {"cmd":"pickup","target":"lineage1","nickname":...}
                  |             +--> client.pickup_lineage1(target_nickname)
                  |             +--> {"status":"ok"} ack
                  |             +--> remaining -= 1
                  |             +--> pickup_avail[client] -= 1
                  |
                  +--> last_idx_time 갱신
           |
           +--> 더 이상 보낼 수 없으면 루프 종료
```

### 6. 단일 픽업 명령이 실제 입력으로 변환되는 과정

```text
+--------------------------------------------------------------------------------------+
|                           pickup_lineage1() -> proxy -> Arduino -> 게임              |
+--------------------------------------------------------------------------------------+

  server.py 또는 client.py
    |
    +--> macro.pickup_lineage1(target_nickname)
           |
           +--> macro_data.json 에서 현재 역할용 x,y 로드
           +--> force_set_foreground_window(lineage1_hwnd)
           +--> win32api.SetCursorPos((x,y))
           |
           +--> target_locked == False ?
           |      |
           |      +--> YES
           |      |      |
           |      |      +--> 최대 4회 반복:
           |      |             |
           |      |             +--> arduino_mouse_shift_click_right(x, y)
           |      |             |      |
           |      |             |      +--> proxy 로 KD, CL, KU 류 명령 전송
           |      |             |      +--> Arduino 가 Shift + 우클릭 HID 수행
           |      |             |
           |      |             +--> screenshot()
           |      |             +--> readInputText()
           |      |             +--> target_nickname 과 비교
           |      |             +--> 맞으면 target_locked = True
           |      |
           |      +--> NO
           |             |
           |             +--> 바로 픽업 단계 진행
           |
           +--> key_press(F5)
           +--> mouse_click_left(x, y)
           +--> 실제 픽업 완료


  proxy 와 Arduino 내부 경로

    macro.py
      |
      +--> _arduino_send("KP,116") 같은 문자열 전송
             |
             +--> TCP 127.0.0.1:9998
                    |
                    +--> arduino_proxy.py 가 수신
                           |
                           +--> serial.write("KP,116\n")
                                  |
                                  +--> Arduino macro_hid.ino
                                         |
                                         +--> VK -> HID 코드 변환
                                         +--> Keyboard.press/release 또는 Mouse.press/release
                                         +--> "OK\n" 응답
                           |
                           +--> proxy 가 Python 쪽에 "OK\n" 반환
```

### 7. OCR 데이터 흐름

```text
+--------------------------------------------------------------------------------------+
|                                   OCR 판독 경로                                      |
+--------------------------------------------------------------------------------------+

  screenshot() 결과 이미지
    |
    +--> crop()
           |
           +--> 필요한 UI 영역만 잘라냄
                  |
                  +--> MP 영역
                  +--> 아데나 영역
                  +--> 교환 닉네임 영역
                  +--> 입력 텍스트 영역
                  +--> 교환 슬롯 밝기 영역
           |
           +--> read_text()
                  |
                  +--> 10px 또는 20px 폭 단위로 슬라이딩
                  +--> image_to_coord_string()
                  |      |
                  |      +--> 특정 RGB 값과 일치하는 픽셀만 마스크
                  |      +--> 좌표 목록을 문자열로 직렬화
                  |
                  +--> converted_data.json lookup
                  +--> 문자 누적
                  +--> 최종 문자열 반환

  converted_data.json 생성 경로
    |
    +--> data2/*.png
           |
           +--> string_writer.py
                  |
                  +--> 문자별 흰색 픽셀 좌표 추출
                  +--> 좌표 문자열 -> 문자 매핑 생성
                  +--> converted_data.json 저장
```

### 8. 운영자가 실제로 따라가는 순서

```text
+--------------------------------------------------------------------------------------+
|                                   운영자 기준 체크리스트                             |
+--------------------------------------------------------------------------------------+

  [준비]
    |
    +--> Arduino 연결
    +--> 게임창 열기
    +--> COM 포트 확인
    +--> SERVER_HOST 확인
    +--> macro_data.json 좌표 확인

  [기동]
    |
    +--> proxy 실행
    +--> server 실행
    +--> 각 client 실행
    +--> server/client 콘솔에서 연결 시작

  [운영]
    |
    +--> server 콘솔에서 1 입력
    +--> WAIT_NICKNAME 로그 확인
    +--> idx/mp/잔여 로그 확인
    +--> 광고 입력이 정상인지 확인
    +--> 닉네임 감지 -> 아데나 감지 -> 슬롯 밝기 변화 -> 픽업 분배 순서 확인

  [문제 발생 시]
    |
    +--> 창을 못 찾으면 list_windows.py
    +--> OCR 이상하면 convert_show.py
    +--> 포트 문제면 COM / 9999 / 9998 확인
    +--> 좌표 문제면 macro_data.json 수정
```

## 동작 방식

### 서버 상태 머신

`server.py`의 `exchange_loop()`는 아래 4단계로 돈다.

1. `WAIT_NICKNAME`
   MP를 읽고, 총 픽업 가능 횟수를 계산하고, 방향을 조정하고, 교환 닉네임이 나타날 때까지 기다린다.

2. `READ_ADENA`
   교환 전 아데나를 한 번 읽는다.

3. `MONITOR_BRIGHTNESS`
   교환 슬롯 밝기가 바뀌는지 감시하고, 바뀌면 교환 수락을 시도한다.

4. `PICKUP`
   받은 아데나 차액을 계산하고, `adena_per_pickup` 기준으로 픽업 횟수를 산출해 서버/클라이언트에 분배한다.

### MP 기반 분배 방식

- 각 유닛의 가용 횟수는 `available = mp // 20`
- 서버는 모든 유닛의 `available` 합계를 계산
- 같은 시점에 가용 수가 가장 큰 유닛부터 픽업을 배정
- 같은 `idx`에는 `SAME_UNIT_DELAY = 1`초 간격을 둠
- 포션은 `POTION_COOLDOWN = 600`초 제한이 있음

### 방향 전환

총 가용 픽업 수가 `direction_threshold`보다 작은지에 따라 서버가 자동으로 방향을 바꾼다.

- 낮을 때: `low_count_direction`
- 높을 때: `high_count_direction`

실제 클릭 좌표는 `macro_data.json`의 `turn_*_xy` 값으로 정해진다.

### 채팅 입력

광고 문구, 감사 메시지, 일부 한글 입력은 Arduino HID 기반 타이핑으로 처리한다.

- 한글: `tools/hangul.py`의 자모 분해 로직 사용
- 영문/숫자/특수문자: Windows VK 코드 기반 전송
- IME 전환: `VK_HANGUL`을 보내 토글

## 설정 파일

### `macro_data.json`

현재 기본 값은 아래와 같다.

```json
{
  "server_mouse_x_y": [605, 358],
  "client_mouse_x_y": [565, 338],
  "client_numbering_mouse_x_y": [1359, 314],
  "direction_threshold": 1,
  "adena_per_pickup": 200,
  "current_direction": "north",
  "low_count_direction": "southeast",
  "high_count_direction": "northwest"
}
```

자주 손보게 되는 항목은 다음이다.

- `server_mouse_x_y`
  서버 창에서 픽업 클릭에 쓸 기준 좌표

- `client_mouse_x_y`
  첫 번째 클라이언트 창에서 픽업 클릭에 쓸 기준 좌표

- `client_numbering_mouse_x_y`
  `client2`, `client3` 같은 번호 붙은 클라이언트에 쓸 좌표

- `direction_threshold`
  총 가용 픽업 횟수가 이 값보다 작으면 `low_count_direction` 사용

- `adena_per_pickup`
  받은 아데나를 몇으로 나눠 픽업 횟수를 계산할지 결정

- `turn_north_xy` ~ `turn_northwest_xy`
  방향 전환용 클릭 좌표

좌표가 어긋나면 실제 게임 해상도, 창 위치, UI 배치와 맞지 않아 오동작한다. 이 프로젝트는 좌표 의존성이 강하다.

## 보조 도구

### 창 목록 확인

```powershell
python .\tools\list_windows.py
```

보이는 윈도우의 `HWND`와 제목을 출력한다. 창 탐색이 꼬였을 때 확인용이다.

### OCR 디버그

```powershell
python .\tools\convert_show.py .\some_capture.png
```

지정한 이미지에서 문자로 간주되는 픽셀을 빨간색으로 표시해 보여준다. OCR 인식 실패 원인을 볼 때 유용하다.

### 수동 문자 캡처 예제

```powershell
python .\tools\passivity_char_capture.py
```

특정 `HWND`를 하드코딩해서 문자를 캡처하는 실험용 스크립트다. 바로 실전에 쓰기보다는 좌표 실험용으로 보는 편이 맞다.

### OCR 데이터 재생성

`string_writer.py`는 `data2/` 폴더의 문자 이미지들을 읽어 `converted_data.json`을 다시 만든다.

```powershell
python .\string_writer.py
```

`tools\duplicate_checker.py`는 동일 픽셀 패턴이 여러 파일로 중복됐는지 점검한다.

```powershell
python .\tools\duplicate_checker.py
```

현재 `.gitignore`에 `data/`, `data2/`, `image/`가 포함되어 있으므로, OCR 원본 자료는 로컬에서만 관리하는 전제로 보인다.

## 자주 보는 로그

### 프록시

```text
[proxy] Arduino 연결됨: COM5 @ 115200
[proxy] 대기 중: 127.0.0.1:9998
[proxy] 클라이언트 연결: ('127.0.0.1', 54321)
```

### 서버

```text
[server] 대기 중: 0.0.0.0:9999
idx(0): MP: 80, 잔여: 4
총 4
[server] 슬롯 밝기: 112.37
[server] 아데나 변화 감지: 120000 → 120400
remaining pickup count: 2 (received: 400, available: 4)
```

### 클라이언트

```text
[client] 서버에 연결 시도 중: 220.119.210.140:9999
[client] 서버 연결됨
[client] ping 수신 → MP: 80
[client] 픽업 명령 수신: lineage1 (12:34:56)
```

## 트러블슈팅

### `Lineage Classic` 창을 찾지 못함

- 게임 창이 실제로 열려 있는지 확인
- 창 제목이 이미 `server`, `client` 같은 이름으로 바뀌어 있는지 확인
- `python .\tools\list_windows.py`로 현재 제목을 확인

### Arduino 연결 실패

- `arduino_proxy.py`의 `SERIAL_PORT`가 실제 COM 포트와 맞는지 확인
- 다른 프로그램이 해당 COM 포트를 점유 중인지 확인
- 보드가 HID 지원 모델인지 확인

### 클라이언트가 서버에 연결되지 않음

- `client.py`의 `SERVER_HOST`가 실제 서버 IP인지 확인
- 서버에서 `server.py`가 실행 중인지 확인
- 방화벽이나 사설망 문제로 `9999` 포트 연결이 막히지 않았는지 확인

### 클릭 위치나 방향 전환이 틀어짐

- `macro_data.json` 좌표를 다시 맞춰야 한다
- 게임 창 크기, UI 배치, 해상도가 캡처 당시와 다르면 좌표가 틀어진다
- 서버/클라이언트 창은 실행 시 `(0, 0)`으로 이동되므로 이를 기준으로 좌표를 잡아야 한다

### OCR이 닉네임, 아데나, MP를 잘못 읽음

- UI 색상과 `converted_data.json`이 만들어진 환경이 다른지 확인
- `tools\convert_show.py`로 실제 문자 픽셀이 기대한 색 범위로 잡히는지 확인
- 필요하면 문자 이미지셋을 다시 모아 `string_writer.py`로 `converted_data.json`을 재생성

## 주의 사항

- 이 프로젝트는 좌표 기반 자동화라서 해상도와 UI 배치가 바뀌면 쉽게 깨진다.
- `client.py`의 서버 IP와 `arduino_proxy.py`의 COM 포트는 환경별 수정이 거의 필수다.
- `macro.py`는 창 제목을 자동으로 바꾸므로, 다른 자동화 도구와 같이 쓸 때 창 제목 의존성이 생길 수 있다.
- 실제 게임과 Arduino 장비가 없는 상태에서는 이 문서를 코드 기준으로 정리했으며, 현재 환경에서 엔드투엔드 실행 검증까지는 하지 않았다.
