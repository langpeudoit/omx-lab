# 피지컬AI 실험실 — 작업 노트

저장소: 공개(2026-11-23부터) `langpeudoit/omx-lab` = 로컬 `~/omx-lab/` (2026-11-22부터. 그 전 위치 ~/isaac/omx_isaac_lab/omx-lab 은 삭제됨). 사이트: https://omx-lab.pages.dev/ (Cloudflare Pages)

**경로 규칙**: 저장소 루트는 작업 공간(CLAUDE.md, docs/), **배포되는 건 `site/` 폴더뿐**. 아래 노트의 `common/lab.js`, `tools/...`, 문제 폴더(`torque/` 등)는 모두 `site/` 기준. 메모·설계·플랜은 `site/` 밖에 둔다 (site 안에 두면 공개됨). 설계 문서는 `docs/`, 구현 계획은 `docs/plans/`.

Isaac Sim 실습 폴더(omx_lab: lab01~10.py, usd_lab, mujoco_web)는 2026-11-22 사용자 결정으로 삭제됨. 아래 노트에 그 이름이 나오면 옛 기록.

## 지켜야 할 것

- **모든 답변은 한국어로** 쓴다. 최종 보고, 질문, 중간 안내, 긴 작업 보고·계획 요약도 예외 없음. 코드·명령·파일 경로만 원문 그대로. (영어로 보고했다가 "한글로 말해라" 지적받음)
- 사용자는 입문자이므로 단계별로 안내한다.
- **실험 단계는 학생이 계산한 예측값을 바로 확인하는 방식**: 2단계 예측 ×0.9 / 그대로 / ×1.1 세 번 실행해 양 끝이 기대대로면 맞음 (공통 `OmxLab.check3`). 경계 근처에서 결과가 뒤섞이면(관통처럼) 여러 값을 훑어 처음 바뀌는 지점으로 판정.
  - 이유: "계산한 값이 0.57인데 그 외의 값을 넣으라고 하니 이상하다"는 지적. 관계없는 값부터 넣어 경계를 좁히는 이분법은 싫어함. 판정 문구는 맞았는지 분명히 알려 줄 것
  - 새 문제를 만들 때 정답 예측을 넣으면 실제로 "맞음"이 나오는지 시뮬로 먼저 확인. 자유 실험 슬라이더는 `<details>` 선택 항목으로
- 목표는 **동역학 개념을 하나씩 익히는 것**. 상황 하나씩 끝까지(개념 → 실행 → 수정 → 채점) 완성한 뒤 다음으로 넘어간다.
- 코드나 샘플 파일을 만들기 전에 먼저 사용자에게 확인한다.
- `~/open_manipulator` (ROBOTIS 원본 저장소, 모델 다시 만들 때만 필요: `git clone https://github.com/ROBOTIS-GIT/open_manipulator.git ~/open_manipulator`)는 수정하지 않는다.
- sudo 비밀번호는 사용자가 직접 입력한다.

## ▶ 이어서 할 일 (2026-11-21 저녁 기준, 여기부터 읽기)

**지금 상태**: 피지컬AI 실험실 **https://omx-lab.pages.dev/** (Cloudflare Pages, 2026-11-22 이사). 저장소 = 공개(2026-11-23부터) `langpeudoit/omx-lab` = 로컬 `~/omx-lab/`. 옛 주소 langpeu.github.io/omx-lab/ 는 2026-11-22 블로그 저장소에서 삭제함(404, 사용자 결정).
- 22개 중 **14개 완성**: 0 기초, 1 FK, 2 IK, 3 특이점, 4 토크, 5 페이로드, 7 미끄러짐, 8 넘어짐, 13 떨림, 14 처짐, 16 지연, 19 발산, 20 관통, 21 Sim2Real + 도구 2개
- 준비 중 8개: 6 push(힘 방향 Jᵀ·F), 9 inertia(자세별 관성), 10 pendulum(손목 진자), 11 coupling(관절 결합), 12 centrifugal(원심력), 15 pid(적분), 17 speed-torque(토크-속도), 18 current(전류) + 도구 FK·IK 계산기
- 실험 방식: 2단계 예측값으로 ×0.9 / 그대로 / ×1.1 세 번 실행해 판정 (`OmxLab.check3`). 관통만 0.6~1.4배 9번
- 설계 문서 `docs/2026-11-21-kinematics-dynamics-expansion-design.md` 7장에 새 상황별 예측·실험 계획이 있음

**동역학 단원 남은 작업 (2026-11-23 정리, 이슈 등록 예정)**: 9 inertia → 10 pendulum → 11 coupling → 12 centrifugal (설계 문서 7장 순서, 11·12 는 앞 문제 해 본 뒤 뺄 수도 있음). 각 문제 = 손계산↔시뮬 확인 → 수치 보고 → 페이지(check3) → `lab.js` ready:true → check_site.py·브라우저 테스트. 이슈는 문제당 1개, 라벨 `dynamics`. GitHub 저장소 소유자는 `langpeudoit` (이슈 기능 켜짐, gh 는 langpeu 계정으로 로그인). Superpowers 플러그인(brainstorming·writing-plans 등)을 쓰더라도 이 문서의 규칙(한국어, 코드 만들기 전 확인)이 우선.

**다음 후보 (사용자에게 먼저 물어볼 것)**
1. 남은 문제 계속: 설계 순서는 9 관성 → 10 진자 → 15 PID → 6 힘 방향 → 17 토크-속도 → 11 결합 → 12 원심력 → 18 전류. 각 문제: 브라우저 MuJoCo(tools/probe.html + 스크래치 mn.py)로 손계산 ↔ 시뮬 확인 → 수치 보고 → 페이지 → check3 방식
2. **캐시 버전 표시** (사용자 답 아직 없음, 3번 제안함): 배포 직후 방문자 브라우저가 옛 lab.js/lab.css 를 10분간 섞어 써서 화면이 깨짐(사용자가 실제로 겪음). `lab.js?v=해시` 자동 붙이기(tools/stamp.py) 제안
3. 사용자가 로컬에서 기구학 1~3 과 바뀐 실험들을 써 보고 피드백 줄 예정이었음
4. 쇼츠: 아직 안 만듦. 이론 설명 + 상황 4 문제 내기 구성 제안해 둠

**작업 방법 메모**
- 로컬 확인: `cd ~/omx-lab/site && python3 -m http.server 8765` → http://localhost:8765/ (사용자에게는 Ctrl+Shift+R 안내)
- 검사: `python3 site/tools/check_site.py`, 브라우저 `tools/test.html`(42개)·`tools/calc_test.html`(13개). 헤드리스 Firefox Marionette 스크립트 mn.py 는 스크래치에 있었음(지워졌으면 다시 작성: 프로필 ~/snap/firefox/common/omxtest/prof, 캐시 끔, ExecuteAsyncScript)
- **main 반영은 PR 로만 (2026-11-23 사용자 결정)**: main 에 직접 commit·push 하지 않는다. 작업 브랜치(worktree)에서 push → `gh pr create` → 사용자 확인 후 merge. (저장소를 public 으로 바꾼 뒤 GitHub 브랜치 보호를 켬: PR 필수, 승인 0명, 관리자도 적용, 강제 push·삭제 금지)
- **GitHub flow (2026-11-23)**: 이슈 → 브랜치 → PR(`Closes #번호`) → merge. 템플릿은 `.github/` (새 문제 / 개선·버그 이슈, PR). 라벨: 종류 `새 문제`·`개선`·`문서`·`chore` + 단원 `기구학`·`정역학`·`동역학`·`제어`·`액추에이터`·`시뮬레이션`·`도구` + `공통코드`
- **PR·이슈는 템플릿 항목을 채워서 올린다 (2026-11-23)**: `gh pr create --body` 로 본문을 직접 쓰면 템플릿이 적용 안 되므로, 본문에 `.github/pull_request_template.md` 의 항목(변경 내용 / 관련 이슈 `Closes #번호` / 확인 체크리스트 / 참고)을 그대로 넣는다. 이슈도 `.github/ISSUE_TEMPLATE/` 항목대로 작성
- **브랜치 이름 (관례, GitHub 이 강제 못 함: 이름 규칙은 Enterprise 기능이라 Ruleset 으로 시도했으나 적용 안 됨, 2026-11-23)**: `feature/<이슈번호>-<id>` (새 문제·기능, 예 `feature/2-inertia`), `fix/…`, `docs/…`, `chore/…`, Claude 세션 자동 브랜치 `claude/…`
- 배포: PR 을 main 에 merge 하면 Cloudflare Pages 가 `site/` 를 자동 배포(약 1분). 배포는 사용자 요청이 있을 때만. 커밋에 Claude 표시(Co-Authored-By 등) 넣지 말 것
- pkill -f "http.server" 는 자기 셸까지 죽임 → `pgrep -f "^python3 -m http.server 8765" | xargs -r kill`
- 사용자 선호: 모든 답변 한국어, 계산한 값을 바로 확인하는 실험을 원함(이분법 싫어함), 인위적 받침대 금지, 원본 Claude Docs 문서는 더 이상 안 씀

## 기준 문서

- **(2026-11-21 사용자 결정) 실험실로 옮긴 뒤에는 이 문서를 더 이상 쓰지 않는다.** 앞으로의 기준은 실험실 사이트와 설계 문서 `docs/2026-11-21-kinematics-dynamics-expansion-design.md`. 문서와 번호를 맞추거나 문서를 고칠 필요 없음
- 실습 문서: https://claude.ai/artifact/SipCx2oL3q92wRKVKeDvUa
  - 제목: "로봇 트러블슈팅 개념 팁북 — 상황별 동역학 × AI 체크 프롬프트"
  - 탭 1 "상황별 트러블슈팅", 탭 2 "AI 답변 검증·계산기", **탭 3 "Isaac Sim 실습"** (`lab01~10.py`의 원본)
  - Claude Docs 문서이므로 Claude Docs 커넥터로 읽는다 (doc id `d04b0d84-ec1e-45d0-b12d-8f7f481e2523`, 탭 3 id `68d2865b-5a0b`).

## 현재 방향 (2026-11-21 결정): MuJoCo 웹 실험실

"틀린 값 찾아 고치기"(USD 수정 실습)는 UI 연습에 가깝고 동역학 공부에 도움이 적다고 판단해 **보류**.
새 방식: 상황마다 **손으로 예측 → 시뮬레이션 실험 → 예측과 비교**. 채점은 "예측이 실험과 맞았나".

- **공개 방식 (2026-11-22 변경): GitHub 저장소(공개) `langpeudoit/omx-lab` → Cloudflare Pages 프로젝트 `omx-lab` → https://omx-lab.pages.dev/**
  - Pages 설정: 프레임워크 없음, 빌드 명령 `rm -rf site/tools`, 출력 디렉터리 `site`, 브랜치 main. push 하면 자동 배포. (Workers 아님 — 사용자가 Pages 원함. wrangler 설정 파일 넣지 말 것)
  - 저장소 구조 (2026-11-22): 루트 = CLAUDE.md, README.md, docs/ / `site/` = 사이트 전체 + site/tools/(개발 도구, 배포 때 지움). tools 는 site 안에 있어서 `../torque/` 같은 상대 경로 그대로. build_xml.py 는 `site/../../open_manipulator` = `~/open_manipulator` 를 읽음
  - 커밋 기록은 블로그 저장소에서 omx-lab 부분만 뽑아 옮김(7개)
- (옛 방식, 2026-11-21~22, **삭제됨** 블로그 커밋 84c1649) 블로그 저장소 `langpeu/langpeu.github.io` 안의 `omx-lab/` 폴더 → https://langpeu.github.io/omx-lab/ . 아래는 그때 메모
  (저장소에 CNAME=lourcode.kr 파일이 있지만 Actions 배포라 무시됨. 실제 사이트는 langpeu.github.io 그대로. lourcode.kr 은 사용자 도메인 아님 — 다시 언급하지 말 것)
  목적: 학습자료로 문제를 하나씩 추가하고 유튜브 쇼츠로 알림.
  - 블로그 = Jekyll Chirpy, Notion 연동. 배포 워크플로(.github/workflows/pages-deploy.yml)는 **repository_dispatch 에서만 실행** → push만으로는 배포 안 됨
    (importer 가 Notion 글을 가져와 main 에 자동 커밋 → 다음 push 전 반드시 `git pull --rebase`)
  - **배포 실행(Claude 가 직접 가능, 2026-11-21 확인)**: `gh api repos/langpeu/langpeu.github.io/dispatches -f event_type=RUN_WORKFLOW_DISPATCH` → `gh run list` / `gh run watch <id> --exit-status` (약 1분). gh 는 langpeu 계정으로 로그인됨
  - 빌드에 htmlproofer --check-html 이 있음. omx-lab 포함해 Docker(ruby:3.1)로 똑같이 돌려 통과 확인 (2026-11-21)
  - 로컬 클론: `~/isaac/omx_isaac_lab/langpeu.github.io` (shallow). 갱신: `rsync -a --delete --delete-excluded --exclude tools/ ../omx-lab/ omx-lab/` 후 커밋
- **소스 = `~/omx-lab/site/`** (omx-lab 폴더가 곧 git 저장소 langpeudoit/omx-lab. rsync 불필요)
  - `index.html` 첫 화면(문제 목록), `common/lab.css` 공통 디자인, `common/lab.js` 공통 코드 (`window.OmxLab`)
    - **(2026-11-21 재정리) 아래 "피지컬AI 실험실 구조" 절이 최신. 이 절의 pNN 폴더·상황 번호는 옛 것**
    - `OmxLab.start()` → lab: `run({setup, control, duration, judge, done})`, `resetPose()`, `showPose(q)`, `showLever(bodyIds, pivotBody)`, `jointGauge(el, {...})`, `onFrame`, `onBusy`, `setPayload(kg)`
    - 실행/초기화 때마다 forcerange, frictionloss, damping, gainprm, biasprm, body_mass 를 원래 값으로 되돌림 → 문제 페이지 setup 에서만 바꾸면 됨
    - 꼬리말(출처, 비공식 표기)은 `<footer id="foot">` 가 있으면 자동
  - `p01-torque/index.html`(내용) + `p01.js`(실험). 저장 키 `omx-lab-1`
  - `lib/`: mujoco.js/.wasm (npm `@mujoco/mujoco` 3.17.0), three.min.js r128, OrbitControls.js 0.128.0, LICENSE-three.txt
  - `model/`: omx_lab.xml + meshes/*.stl ← `python3 tools/build_xml.py` 로 ROBOTIS 원본(`~/open_manipulator` = 저장소 옆)에서 다시 생성
  - `LICENSE`(Apache-2.0), `NOTICE`(ROBOTIS·MuJoCo·three.js 출처), `README.md`, `.nojekyll`
- 이전 폴더 `omx_lab/mujoco_web/` (단일 index.html + make_site.py → site/) 는 **더 이상 쓰지 않음**. 사용자 서버 https://langpeu.com/omx_pysical/mujoco_web/site/ 에 올라간 것도 이전 버전
- 배포 시 주의 (겪은 문제): 아티팩트는 doctype/charset/[hidden] 기본 스타일을 자동으로 붙여 줬으나 일반 서버에서는 없음 → 한글 깨짐, overlay 안 사라짐. 지금 소스에는 다 들어 있음. file:// 로 열면 fetch 막힘
- 브라우저 검증 방법: 스냅 firefox 는 /tmp 접근 불가 → `~/snap/firefox/common/omxtest/` 에 프로필. `firefox --headless --marionette` + 파이썬 소켓 Marionette 클라이언트로 로딩·클릭·실행·스크린샷 확인 (상황 1 전체 통과, 2026-11-21)
- Node 검증: 스크래치에 받은 Node v22로 MuJoCo WASM을 직접 돌려 수치 확인함 (사용자 승인). 스크래치는 지워질 수 있음
- MuJoCo 모델 특징: XL430 forcerange 1.5 Nm (ROBOTIS 값, Isaac 실습의 1.4와 다름), 모든 팔 관절 frictionloss 0.1 Nm, timestep 0.002
- 인덱스: qpos/dof joint1=0, joint2=1, joint3=2 / actuator 같음 / body link2=3, link3=4, link4=5, link5=6, end_effector=7, link6=8, link7=9

### 피지컬AI 실험실 구조 (2026-11-21 1단계 완료, 최신)

- 이름 "피지컬AI 실험실", 부제 "OMX-AI로 배우는 기구학·동역학", 주소 `omx-lab/` 그대로. 로고 `common/logo.jpg`(랑프 두잇), 제작자 Langpeu · https://www.youtube.com/@langpeudoit
- 설계: `docs/2026-11-21-kinematics-dynamics-expansion-design.md`, 계획: `docs/plans/2026-11-21-renumber-sidebar.md`
- **번호·단원·제목은 `common/lab.js` 의 `UNITS`/`PROBLEMS`/`TOOLS` 에만.** 폴더 = id(번호 없음). 페이지 HTML/JS 에 "상황 N" 직접 금지 → `<a data-ref="sag" href="../sag/">상황 {n}</a>` 또는 `OmxLab.label("sag")`. 한국어 조사 문제 때문에 번호 바로 뒤에 은/는·과/와 붙이지 말 것
- 번호표: 0 basics · 기구학 1 fk 2 ik 3 singularity · 정역학 4 torque 5 payload 6 push 7 slip 8 tipping · 동역학 9 inertia 10 pendulum 11 coupling 12 centrifugal · 제어 13 vibration 14 sag 15 pid 16 lag · 액추에이터 17 speed-torque 18 current · 시뮬레이션 19 diverge 20 contact 21 sim2real · 도구 tool-servo tool-estimate tool-kinematics. `ready:false` = 준비 중(폴더 없음). 2026-11-21: fk·ik·singularity ready
- 옛 순서와 대응: 옛 1→4, 2→13, 3→14, 4→7, 5→8, 6→21, 7→19, 8→20, 9→16, 10→5. 옛 주소 `p00-basics/`…`p10-payload/` 는 사용자 결정으로 삭제(2026-11-21, 쇼츠 전이라 불필요). check_site.py 가 다시 생기면 잡음
- 모든 페이지 JS 는 `OmxLab.shell("<id>")`(첫 화면 `shell(null)` + `renderHome`). shell 이 사이드바(로고·검색·진행·단원 접기·제작자), 폭 조절(220~520, 기본 288), 820px 이하 서랍, 경로 줄, 제목 번호, 단원 칩, 단계 진행줄(카드 `article.card[id^=c]`), 이전·다음(ready 만), 진행 기록을 만든다
- 저장 키: `omx-lab-<id>`, `omx-lab-progress`, `omx-lab-side-w`, `omx-lab-units`, `omx-lab-calc`, `omx-lab-jlabels`
- 떠 있는 계산기 `common/calc.js` (`OmxCalc.evaluate/open/close`, `\` 키, 답 넣기 = 마지막으로 누른 number 입력칸)
- PROBLEMS 설명의 q̇/q̈ 는 lab.js `rich()` 가 화면에 넣을 때 `<span class="d1/d2">` 로 바꿈 (그대로 써도 됨)
- 검사: `python3 site/tools/check_site.py` (번호 직접 씀·옛 링크·폴더·옛 주소 폴더 없음), 브라우저 `tools/test.html`(29개) · `tools/calc_test.html`(13개) — 스크래치 `mn.py`(Marionette, 캐시 끔, `--dark --sleep --ajs`)로 실행. 헤드리스 스크린샷은 웹 글꼴 로딩 전이면 글자가 빠져 보임 → `--sleep 4`
- 배포: 작업 브랜치 push → PR → main merge (Cloudflare Pages 빌드가 site/tools/ 를 지우고 site/ 배포). main 직접 push 금지
- 확인 값(재정리 뒤 브라우저): torque 1.0 Nm 버팀, 마찰 끔 0.55 떨어짐/0.58 버팀 · sag 3.27° · contact 10.5 mm

### 상황 4 torque 실험 방식 변경 (2026-11-21, 사용자 요청)

- "경계를 0.05 폭으로 좁혀라"(이분법) → **"내 예측 ×0.9 / ×1 / ×1.1 세 번 실행"**. 토크: ×0.9 떨어짐·×1.1 버팀이면 맞음. 물체: ×0.9 버팀·×1.1 떨어짐이면 맞음. 예측값 그대로의 결과도 보여 줌 (경계 근처라 어느 쪽이든 가능하다는 안내)
- 이유: 학생은 계산한 값(0.57, 0.47)을 확인하고 싶어 함. 관계없는 값부터 넣는 이분법이 이상하다는 사용자 피드백
- 마찰 켬 예측은 3단계 입력칸(pred-on). 자유 실험(슬라이더)은 `<details>` 선택 항목으로 남김. 실행 속도 3배(speed 3)
- 정밀 경계(4초 뒤 3° 안): 마찰 끔 0.565 떨어짐/0.57 버팀(2.6° 처짐), 켬 0.465/0.47, 손끝 235 g 버팀/240 g 떨어짐
- (2026-11-21) 나머지도 같은 틀로 변경: 공통 `OmxLab.check3({pred, lowGood, good, bad, run, fmt, round, fb, hint})` (lab.js)
  - payload: 접은 자세 ×0.9/1/1.1 + 무너지는 관절이 예측과 같아야 맞음, 그다음 '뻗은 자세로 같은 무게' 1번 (joint2 무너짐)
  - slip: μ0.5 τ0.2 무게 ×0.9/1/1.1 (227 → 204 버팀 / 250 미끄러짐)
  - tipping: 5초 무게추 ×0.9/1/1.1 (0.242 → 0.218 넘어짐 / 0.266 버팀), 그다음 같은 무게추(+10%) 0.4초 → 넘어짐
  - lag: 피드포워드 켬 T ×0.9/1/1.1 (0.522 → 0.470 늦음 / 0.574 따라감), 그다음 피드포워드 끔 +10% → 늦음
  - diverge: Kp200 Euler dt ×0.9/1/1.1 (20.3 → 18.3 안정 / 22.3 발산), 그다음 같은 dt RK4 → 안정
  - contact: **관통은 경계 근처에서 결과가 뒤섞임** (0.64 관통, 0.68 버팀, 0.72 관통, 0.74 버팀, 0.76 관통, 0.78 버팀, 0.84 관통 … 공이 닿는 순간이 dt 칸 어디인지에 따라). 그래서 ×0.6~1.4 를 0.1 간격 9번 떨어뜨려 처음 뚫린 높이가 예측 ±15% 면 맞음. 깊이(0.3 m → 10.5 mm, 식 9.7)는 따로 1번, τ 20 ms 0.3 m 관통 1번
  - vibration·sag·sim2real 은 원래 예측값으로 바로 비교하는 방식이라 그대로
  - 자유 실험(슬라이더)은 모두 `<details>` 선택 항목

### 기구학 단원 1~3 (omx-lab/fk, ik, singularity, 2026-11-21 구현, 브라우저 확인)

- 공통 `common/kin.js` (`OmxKin.fk/ik/world`, 어깨 joint2 축 원점 평면): L1 0.1205 (수직에서 앞 α 20.14°), L2 0.162, L3 0.1206, 어깨 세계좌표 (-0.01125, 0, 0.0975). MuJoCo end_effector 위치와 0.000 mm 일치
- `lab.marker(이름,{pos,color,r})`, `lab.path(이름,[[x,y,z]…],{color,dash})` 3D 표시 추가 (lab.js)
- 모두 힘 없는 기구학(showPose). 채점은 손끝 위치 5 mm

| 상황 | 예측 | 손계산 = 시뮬 |
|---|---|---|
| 1 fk | 0°,0°,0° / 45°,10°,−55° 손끝 (x,z), joint1 30° 의 y | (0.3241, 0.1132) / (0.3229, −0.0820) / 0.1621 (시뮬 0.1607, 손끝 y 오프셋 −1.6 mm) |
| 2 ik | 공 (0.35, 0): d, γ, θ2·θ3 (손 수평 θ4 = −(θ2+θ3)) | d 0.2294, γ 107.7°, 위 27.56°/2.49°, 아래 112.16°/−142.21°. (0.42, 0) 은 d 0.2994 > 0.2825 → 해 없음 |
| 3 singularity | 0° 자세 61 rpm(6.39 rad/s): 팔꿈치만 / 어깨만, 어깨 높이 손 수평 최대 x | 1.805 / 2.193 m/s, x 최대 0.4032 (0.4027 부터 관절 속도 한계) |

### 0 · 기초 개념 (omx-lab/p00-basics, 2026-11-21)

원본 = 실습 문서 탭 1의 "0단계 · 기초 개념" (운동방정식 항 표, 기호 읽는 법, 용어 사전). AI 프롬프트 부분은 뺌.
추가: 실험실 기호(Σ, I, b, ζ, ω, α, Δq, dt, Fn/Ft, e), 단위 표(rad↔deg 등), 관절 이름, 화면 보는 법, τ 두 가지 뜻(토크/상황 8 접촉 시간 상수) 경고.
- `PROBLEMS` 맨 앞 `{n:0, basics:true}` → 첫 화면 맨 위 넓은 카드 "처음이면 여기부터", 탭 "0 · 기초 개념"
- 상황 1~10 개념 카드 h2 아래 `<p class="basics-link">` 로 관련 항목(#s-…, #t-… 앵커) 연결
- q̇/q̈ 결합 문자(U+0307/0308)는 글꼴에서 점이 옆으로 밀림 → `<span class="d1">q</span>` / `d2` (CSS 원으로 점). 새 페이지도 이걸 쓸 것
- 휴대폰(≤600px)에서 `table.gloss` 는 행을 세로로 쌓음
- 문서 오타 "에프 익스텐드" → "에프 익스터널" 문서에서도 고침
- 검사: firefox --headless --screenshot (스냅 프로필 ~/snap/firefox/common/omxtest/prof), Docker ruby:3.1 + html-proofer 3.19.4 (블로그 Gemfile.lock 버전) `--disable-external --check-html --allow-hash-href` 통과

### 도구 (omx-lab/tool-servo, tool-estimate, 2026-11-21)

원본 = 실습 문서 탭 2 "AI 답변 검증·계산기". AI 프롬프트는 뺌. 문제가 아니라 도구라서 `PROBLEMS` 와 별도인 `TOOLS` 배열 → 첫 화면 "도구" 칸, 탭 끝(점선 테두리).
- `tool-servo/`: 문서 React 계산기를 일반 JS로 옮김 (프리셋 5개, 단위 환산, 팔 길이별 무게, 충분한지 판정) + "서보 스펙 읽기"
- `tool-estimate/`: 중력 토크(+cos θ), 가속 토크(+Δq·T로 α 구하기), 파지력(손가락 수), 단위 변환기(9개 물리량)
- 상황 1·10 → 서보 계산기, 상황 4 → #grip, 상황 9 → #acc, 기초 개념 단위 → #units 링크
- 사용자 결정: OMX-AI 는 XL430 12 V, XL330 5 V 로 계산 (11.1 V 권장전압 값은 쓰지 않음). 서보 목록은 OMX+SO-ARM 5개만. 문서 탭 2 계산기 프리셋도 같은 값으로 고침. 문서 탭 3·usd_lab 의 1.4 Nm 는 보류 (1.5 가 맞음)
- 참고: 서보 계산기에 XL430, 40.1 cm, 팔 무게 0 넣으면 381 g 이지만 실험실 상황 1 은 235 g — 차이는 팔 자체 g(q) 0.574 Nm

### 서보 스펙 기준 (ROBOTIS 공식 스펙 엑셀 `~/다운로드/dynamixel_spec_2026-11-21.xls`, 실제는 HTML 표, 73개 제품)

| 서보 | 스펙 전압 | 스톨 토크 | 무부하 속도 | 무게 | 기어비 | 입력 전압(최소/권장/최대) |
|---|---|---|---|---|---|---|
| XL430-W250-T | 12.0 V | 1.50 Nm (1.4 A) | 61 rpm | 57 g | 258.5:1 | 6.5 / 11.1 / 12.0 |
| XL330-M288-T | 5.0 V | 0.52 Nm (1.5 A) | 104 rpm | 18 g | 288.4:1 | 3.7 / 5.0 / 6.0 |
| XL330-M077-T | 5.0 V | 0.22 Nm (1.5 A) | 363 rpm | 18 g | 77.5:1 | 3.7 / 5.0 / 6.0 |

- 엑셀은 제품마다 한 전압 값만 있음. e-Manual 에는 XL430 11.1 V 1.4 Nm·57 rpm, 9 V 1.0 Nm·47 rpm 도 있음 (요약으로 읽음)
- 실험실/ROBOTIS MuJoCo 모델의 1.5 Nm = 12 V 값. 문서 탭 2 계산기 프리셋(XL430 1.4/57, M288 103 rpm, M077 0.215 Nm·383 rpm)은 엑셀과 다름
- "Continuous Operation" 칸은 이 세 서보 모두 '-' (연속 토크 공개 안 됨)

### 상황 1 (omx-lab/p01-torque, 브라우저에서 확인 완료)

뻗은 자세 = joint2 +80.2°, joint3 −80.2°. 실험: 0°(위로 세움)에서 1.5초 코사인 궤적으로 뻗고 4초 뒤 joint2가 목표 ±3° 안이면 "버팀".

| 항목 | 손계산 | MuJoCo (Node 확인) |
|---|---|---|
| g(q) joint2 | Σm·x = 0.0585 kg·m × 9.81 = 0.574 Nm | qfrc_bias 0.574 |
| 버티는 최소 토크, 마찰 끔 | 0.574 | 0.55 떨어짐 / 0.58 버팀 |
| 버티는 최소 토크, 마찰 켬 | 0.574 − 0.1 = 0.474 | 0.45 떨어짐 / 0.48 버팀 |
| 손끝 최대 물체 (1.5 Nm, 마찰 끔, x=0.401 m) | 235 g | 230 버팀 / 240 떨어짐 |
| 같은 조건 마찰 켬 | 261 g | 260 버팀 / 270 떨어짐 |

힘이 모자라면 팔이 앞으로 떨어져 손끝이 바닥에 닿음(joint2 약 89°). 받침대 같은 인위적 물체는 쓰지 않는다 (사용자가 싫어함).

페이지 5단계: 1 개념(g(q)=Σm·g·x) → 2 예측(링크 m, x 표 → g(q) 입력, ±5%) → 3 실험(joint2 최대 토크 슬라이더 0.14부터, 마찰 켬/끔, 경계 0.05 Nm 폭) → 4 확인(예측·g(q)·두 경계 비교 + 마찰 퀴즈) → 5 응용(1.5 Nm로 손끝 최대 물체 예측 → 물체 슬라이더 실험, 10 g 폭)

### 상황 2~10 (2026-11-21 구현, Node + 브라우저에서 확인)

공통: `common/lab.js` 에 모델 변형(`start({transform})`), 이름→번호(`lab.id/qadr/dadr`), 토크 모터(`lab.motor`), M(q)(`lab.fullM`, mj_fullM + DoubleBuffer.GetView),
접촉력(`lab.contactForce`), 시간 그래프(`OmxLab.Plot`), 숫자 표시(`lab.readouts`), 발산 감지(time 감소/NaN), 관절 이름표(3D 위, 켜고 끄기) 추가.
실행/초기화 때 opt(timestep, integrator, gravity), geom_size/friction/solref 도 원래 값으로 되돌림. 페이지 HTML 뼈대는 스크래치 gen.py로 한 번 생성(이후 직접 수정).

| 상황 | 실험 | 손계산 | 시뮬 |
|---|---|---|---|
| 2 떨림 | joint1 토크 PD 10° 스텝, 팔 뻗음, I 0.0206, b 0.2 | Kp4 Kd0 오버슈트 31.1% | 31.3% (Kd0.2: 4.7/4.7%), 지연 60 ms 계속 흔들림 |
| 3 처짐 | joint2 PD(+중력보상), Kp 10 | 3.29° | 3.27°, 보상 0°, 모델에 없는 100 g 2.25° |
| 4 미끄러짐 | 손가락 패드(pad6/7)+상자, 무중력에서 쥔 뒤 중력 | μ0.5 τ0.2 r0.045 → 227 g | 220 버팀 / 250 미끄러짐 |
| 5 넘어짐 | link0 freejoint, 베이스 바닥 x ±0.06 | 무게추 0.242 kg | 5초 0.23 넘어짐/0.25 버팀, 0.4초는 ~0.5 kg 필요 |
| 6 Sim2Real | 숨은 손끝 무게 40~100 g(localStorage), Kp10+보상 | m = Kp·e/(g·x) | 보정 후 처짐 ~0 |
| 7 발산 | joint1 한계 없는 스프링, Euler/RK4 | Kp200 dt 20.3 ms | 20 안정/25 발산, RK4 25 안정, Kp800 10/12 |
| 8 관통 | 판(y 0.25, 높이 0.1)+공 r 1 cm, 판 solref τ | τ4 ms, 0.3 m → 9.7 mm, 관통 h>0.72 | 10.5 mm, 1.0 m 관통, τ20 ms 0.3 m 관통 |
| 9 지연 | joint1 0→90° 코사인, 200 g, Kp20 Kd0.5 (+FF) | T최소 0.522 s | FF 0.54 따라감/0.50 늦음, FF 없이 ~1.0 s |
| 10 페이로드 | 위치제어 그대로, 최종 오차 >3° 무너짐 | 접은 자세 j4 398 g, 뻗은 자세 j2 235 g | 380 버팀/400 j4, 240 j2 무너짐 |

주의: MuJoCo 접촉은 soft라 단순 v·dt 터널링 식이 안 맞음 → 상황 8은 '파고듦 ≈ v·τ' (τ = 2·dt 일 때 잘 맞음).
그리퍼 메시 볼록껍질로 쥐면 쐐기처럼 밀려 식과 안 맞음 → 평행에 가까운 패드 사용. 테스트 Firefox 종료는 반드시 테스트 프로필 프로세스만 (사용자 브라우저 건드리지 말 것).

