# 피지컬AI 실험실 1단계: 번호 재정리 + 사이드바 레이아웃 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 페이지(기초 + 상황 10개 + 도구 2개)를 새 번호·이름 기반 주소·단원 구성으로 옮기고, 위쪽 탭 대신 왼쪽 사이드바 레이아웃(로고, 피지컬AI 실험실 이름, 제작자 표시)을 모든 페이지에 적용한다. 새 상황 11개는 "준비 중"으로 목록에만 나온다.

**Architecture:** 번호·단원·제목은 `common/lab.js` 의 `PROBLEMS`/`TOOLS` 한 곳에만 둔다. 각 페이지 HTML 에는 번호를 쓰지 않고, `lab.js` 가 페이지를 사이드바 틀로 감싸며(`OmxLab.shell`) 제목 번호, 경로, 단계 진행줄, 이전·다음, 다른 상황 참조 글자(`data-ref`)를 채운다. 이렇게 하면 다음에 문제를 끼워 넣을 때 `PROBLEMS` 만 고치면 된다.

**Tech Stack:** 정적 HTML/CSS/JS (빌드 없음), MuJoCo 3.17.0 WASM, three.js r128. 검사: Python 3 스크립트, Docker ruby:3.1 + html-proofer 3.19.4, headless Firefox.

**Spec:** `/home/langpeu/isaac/omx_isaac_lab/omx_lab/docs/2026-11-21-kinematics-dynamics-expansion-design.md` (5·6장). 레이아웃 시안: https://claude.ai/artifact/Rm6VGDm9LGiR11N1EnNK9G (소스 `$SCRATCH/omx-layout-mockup.html`)

작업 폴더: `~/isaac/omx_isaac_lab/omx-lab/` (git 아님). 배포 클론: `~/isaac/omx_isaac_lab/langpeu.github.io/omx-lab/` (rsync).

## Global Constraints

- 사이트 이름 "피지컬AI 실험실", 부제 "OMX-AI로 배우는 기구학·동역학". 주소 폴더 `omx-lab/` 는 그대로.
- 로고: `~/바탕화면/channels4_profile.jpg` → `common/logo.jpg` (alt "랑프 두잇 로고").
- 제작자 카드: "제작 Langpeu", 링크 `https://www.youtube.com/@langpeudoit` (새 탭, `rel="noopener"`). 그 아래 "비공식 학습 자료 · ROBOTIS와 관계없음".
- 단원(순서, 이름 · 설명): 기초 · 식, 기호, 단위 / 기구학 · 위치와 각도 / 정역학 · 멈춰서 버티는 힘 / 동역학 · 움직일 때의 관성 / 제어 · 목표를 따라가게 하기 / 액추에이터 · 모터·서보 특성 / 시뮬레이션 · 시뮬레이터의 한계 / 도구 · 계산기.
- 번호·폴더 대응 (설계 문서 5장 표 그대로):

  | n | id (폴더) | 제목 | 단원 | 이전 폴더 |
  |---|---|---|---|---|
  | 0 | basics | 기초 개념 | 기초 | p00-basics |
  | 1 | fk | FK: 손끝은 어디에? | 기구학 | (준비 중) |
  | 2 | ik | IK: 공을 잡으려면 몇 도? | 기구학 | (준비 중) |
  | 3 | singularity | 손끝 속도와 특이점 | 기구학 | (준비 중) |
  | 4 | torque | 명령을 보내도 안 움직임 | 정역학 | p01-torque |
  | 5 | payload | 물체를 들면 동작 이상 | 정역학 | p10-payload |
  | 6 | push | 어느 방향으로 밀 때 제일 셀까 | 정역학 | (준비 중) |
  | 7 | slip | 미끄러짐 | 정역학 | p04-slip |
  | 8 | tipping | 넘어짐 | 정역학 | p05-tipping |
  | 9 | inertia | 뻗은 팔은 왜 느리게 돌까 | 동역학 | (준비 중) |
  | 10 | pendulum | 힘 빠진 팔 흔들기 | 동역학 | (준비 중) |
  | 11 | coupling | 어깨를 돌리면 팔꿈치가 끌려간다 | 동역학 | (준비 중) |
  | 12 | centrifugal | 원심력은 무시해도 될까 | 동역학 | (준비 중) |
  | 13 | vibration | 떨림·진동 | 제어 | p02-vibration |
  | 14 | sag | 목표까지 못 감·처짐 | 제어 | p03-sag |
  | 15 | pid | 처짐을 I항으로 없애기 | 제어 | (준비 중) |
  | 16 | lag | 너무 느림·궤적 지연 | 제어 | p09-lag |
  | 17 | speed-torque | 빠를수록 힘이 약해진다 | 액추에이터 | (준비 중) |
  | 18 | current | 서보가 뜨거워지는 이유 | 액추에이터 | (준비 중) |
  | 19 | diverge | 시뮬 폭발·발산 | 시뮬레이션 | p07-diverge |
  | 20 | contact | 관통·튕김 | 시뮬레이션 | p08-contact |
  | 21 | sim2real | Sim-to-Real 갭 | 시뮬레이션 | p06-sim2real |
  | 도구 | tool-servo, tool-estimate | (그대로), tool-kinematics "FK·IK 계산기" 준비 중 | 도구 | 그대로 |

- 브라우저 저장 키: `omx-lab-<id>` (예 `omx-lab-torque`). 진행 기록 `omx-lab-progress`, 사이드바 폭 `omx-lab-side-w`, 단원 접힘 `omx-lab-units`, 계산기 `omx-lab-calc`. 기존 키는 옮기지 않는다. 모든 localStorage 접근은 try/catch.
- 사이드바 폭 220~520 px, 기본 288 px, 두 번 클릭 기본값, ←/→ 16 px. 820 px 이하 서랍(☰, 바깥/ Esc 로 닫기). 1080 px 이하 시뮬 창과 카드 위아래.
- 색·글꼴 토큰은 지금 `lab.css` 그대로 (파랑=모터, 주황=중력), 다크 모드 유지. 모든 숫자 열은 tabular-nums.
- 페이지 HTML·JS 안에 "상황 [0-9]" 숫자를 직접 쓰지 않는다. 코드 주석도 번호 대신 id 를 쓴다.
- htmlproofer 3.19.4 `--disable-external --check-html --allow-hash-href` 통과.
- 받침대 같은 인위적 물체 추가 금지, 실험 내용·수치는 바꾸지 않는다.

## Review Focus

1. **실험이 그대로 도는지**: 폴더·id 를 바꾼 뒤에도 각 상황의 시뮬레이션이 로드되고 실행된다 (모델·lib 상대 경로 `../model`, `../lib` 유지). → Task 6 에서 torque·sag·contact 를 실제로 실행해 확인.
2. **옛 주소로 들어온 사람**: `p01-torque/` 등 11개 옛 주소가 새 주소로 바로 이동하고, 앵커(`#c5`)가 있으면 유지된다. → Task 5 검사 스크립트.
3. **localStorage 가 막힌 브라우저**(사생활 보호 창): 사이드바·진행 표시·폭 조절이 오류 없이 기본값으로 동작. → Task 3 에서 `localStorage` 를 throw 하도록 바꾼 페이지로 확인.
4. **검색 결과가 없을 때 / 단원 전부 접었을 때**: 빈 목록 대신 "‘…’와 맞는 문제가 없습니다" 문구, 접힌 단원도 현재 문제는 보이게(현재 문제 단원은 자동으로 펼침). → Task 3.
5. **휴대폰 폭**: 서랍이 열린 동안 본문 스크롤 막힘, 문제를 누르면 서랍 닫힘, 가로 스크롤 없음. → Task 6 스크린샷 390 px.

---

### Task 1: 목록 데이터와 검사 스크립트

**Files:**
- Modify: `common/lab.js` (PROBLEMS, TOOLS, 새 도우미, export)
- Create: `tools/check_site.py`

**Interfaces:**
- Produces (window.OmxLab):
  - `UNITS: Array<{key, name, sub}>` — key: `"basics"|"kin"|"statics"|"dyn"|"control"|"actuator"|"sim"|"tools"`
  - `PROBLEMS: Array<{n:number, id:string, title:string, concept:string, unit:string, ready:boolean, minutes?:number}>` — 위 표 순서, `ready` 는 폴더가 있는 것만 true
  - `TOOLS: Array<{id, title, desc, ready}>`
  - `find(id) -> {n, title, unit, ...}|null` (PROBLEMS·TOOLS 둘 다)
  - `label(id) -> string` — 상황: `"상황 4"`, 기초: `"0 · 기초 개념"`, 도구: `"도구 · 서보 스펙 계산기"`
  - `refLinks(root=document)` — `a[data-ref]` 의 글자 안 `{n}` 을 번호로, `{t}` 를 제목으로 바꾸고 `href` 가 비었으면 `ROOT + id + "/"` 로 채움
- `tools/check_site.py`: 인자 없이 실행, 위반마다 한 줄 출력 후 종료 코드 1, 통과면 `OK n pages` 출력.

- [ ] **Step 1: `tools/check_site.py` 작성 (먼저 실패해야 함)**
  검사 항목: (a) `lab.js` 의 PROBLEMS/TOOLS 를 정규식으로 읽어 `ready:true` 인 id 마다 `<id>/index.html` 이 있음, (b) `ready:false` 인 id 폴더는 없음, (c) `lib/`·`model/`·`tools/` 를 뺀 모든 `.html`/`.js` 에 정규식 `상황 ?\d` 가 없음, (d) `href="../pNN-…"` 같은 옛 폴더 링크가 새 페이지에 없음, (e) 각 `ready` 페이지에 `<script src="../common/lab.js">` 와 `<h1>` 이 하나, (f) 사이트 이름 "OMX 동역학 실험실" 문자열이 없음, (g) 옛 주소 11개 폴더에 redirect 페이지가 있음(Task 5 전에는 실패해도 됨 — `--skip-redirect` 옵션).
- [ ] **Step 2: 실행해서 실패 확인** — `python3 tools/check_site.py --skip-redirect` → 여러 위반 출력, 종료 코드 1.
- [ ] **Step 3: `lab.js` 에 UNITS·새 PROBLEMS·TOOLS·`find`·`label`·`refLinks` 구현, export 추가.** 기존 `renderList`/`renderTools` 는 Task 3 에서 대체하므로 이 단계에서는 그대로 둔다.
- [ ] **Step 4: `node` 가 없으므로 문법 확인은 Firefox 로드로 대신**(Task 3), 여기서는 `python3 tools/check_site.py --skip-redirect` 가 (a)(b) 관련 위반만 남는지 확인 (폴더 이동 전이라 (a) 실패는 정상).

### Task 2: 폴더 이동과 페이지에서 번호 빼기

**Files:**
- Move: `p00-basics/`→`basics/`, `p01-torque/`→`torque/`, `p02-vibration/`→`vibration/`, `p03-sag/`→`sag/`, `p04-slip/`→`slip/`, `p05-tipping/`→`tipping/`, `p06-sim2real/`→`sim2real/`, `p07-diverge/`→`diverge/`, `p08-contact/`→`contact/`, `p09-lag/`→`lag/`, `p10-payload/`→`payload/`. 각 폴더의 `pNN.js` → `<id>.js` (basics 는 `basics.js`).
- Modify: 위 11개 폴더의 `index.html`·`<id>.js`, `tool-servo/index.html`, `tool-estimate/index.html`, `index.html`

**Interfaces:**
- Consumes: `OmxLab.label`, `OmxLab.refLinks`, `OmxLab.find` (Task 1)
- Produces: 각 페이지 JS 는 `OmxLab.renderNav($("nav"), "<id>")` 대신 `OmxLab.shell("<id>")` 를 부른다. `shell` 은 Task 3 에서 만들므로, 브라우저 확인은 Task 3 이 끝난 뒤 함께 한다 (Task 2 의 확인은 검사 스크립트만).

- [ ] **Step 1: 폴더·파일 이름 바꾸기** (`mv`), `index.html` 의 `<script src="pNN.js">` 를 새 이름으로.
- [ ] **Step 2: 각 페이지 머리말 정리**: `<title>` = `<제목> | 피지컬AI 실험실` (번호 없음), `<span class="crumb">…</span>` 과 `<nav class="tabs" id="nav" …>` 삭제, `<h1>` 의 `상황 N · ` 접두어 삭제(뒤 문장은 그대로, 예 `<h1>명령을 보내도 팔이 안 움직임</h1>`), meta description 의 사이트 이름 교체.
- [ ] **Step 3: 다른 상황을 가리키는 글자를 `data-ref` 로**: HTML 은 `<a data-ref="sag" href="../sag/">상황 {n}</a>` 형태, 링크가 아니던 문장(예 p06 "상황 3에서 본 식")도 링크로 바꾼다. JS 문자열은 `` `${OmxLab.label("sag")}처럼` `` 식으로. 대상: 위 grep 결과의 줄 전부 (`p03.js:81,95`, `p06.js` 주석·`index.html:46,64`, `p10 index.html:71` "뻗은 자세 (상황 1)", basics 의 `상황 1~10`/`상황 8`/`상황 6`/버튼 2개, tool-servo `:74`, tool-estimate `:35,49,70`). 기초 개념 표의 `.go` 숫자 링크는 `<a data-ref="torque" href="../torque/">{n}</a>`.
- [ ] **Step 4: 각 JS 첫 줄 주석의 `상황 N ·` 를 id 로**(예 `/* torque · 아예 안 움직임 — … */`), `OmxLab.store("omx-lab-N")` → `OmxLab.store("omx-lab-<id>")`, `OmxLab.renderNav($("nav"), "pNN-…")` → `OmxLab.shell("<id>")`.
- [ ] **Step 5: 상황 카드 안 `basics-link` 의 `href="../p00-basics/#…"` → `../basics/#…`, 도구 링크 그대로.**
- [ ] **Step 6: `python3 tools/check_site.py --skip-redirect`** → (a)~(f) 통과, `OK`.

### Task 3: 사이드바 틀 (`OmxLab.shell`)

**Files:**
- Modify: `common/lab.js` (shell, 진행 기록, 기존 renderNav/renderList/renderTools 제거), `common/lab.css` (사이드바·진행줄·이전/다음·서랍·폭 조절, `.tabs`/`.tab*`/`.tabsep`/`.crumb`/`.plist` 규칙 정리)
- Create: `common/logo.jpg`

**Interfaces:**
- Consumes: `UNITS`, `PROBLEMS`, `TOOLS`, `find`, `refLinks`, `store`
- Produces: `OmxLab.shell(currentId: string|null)` — `null` 은 첫 화면. 하는 일: body 의 기존 내용(`.wrap` + `footer#foot`)을 `<div class="app"><aside class="side">…</aside><div class="resizer">…</div><div class="scrim"></div><main class="main">[topbar][기존 내용][pager]</main></div>` 로 옮김; 현재 페이지가 상황이면 `<h1>` 앞에 `<span class="n">{n}</span>`, h1 위에 단원 칩 + 개념; 카드(`article.card[id^="c"]`)가 2개 이상이면 단계 진행줄(카드 h2 의 `:` 앞 글자, 숫자 대신 ✓ 는 `.card.done`); `refLinks()` 호출.
- 진행 기록: `MutationObserver` 로 카드 `done` 클래스 변화를 보고 `omx-lab-progress[id] = "part"`(done 1개 이상) / `"done"`(모든 카드). 목록의 원·진행 막대(완료 수 / ready 문제 수)를 갱신.

- [ ] **Step 1: 로고 복사** `cp ~/바탕화면/channels4_profile.jpg common/logo.jpg`.
- [ ] **Step 2: CSS 이식**: 시안의 `.app/.side/.brand/.search/.progress/.unit/.item/.resizer/.scrim/.menu-btn/.topbar/.stepper/.pager/.maker` 규칙을 `lab.css` 토큰 이름(`--panel`, `--line`, `--soft`, `--accent` …)에 맞춰 옮김. 새 토큰 `--side`, `--accent-soft` 를 세 테마 블록 모두에 추가(값은 시안 것). 옛 `.tabs`, `.tab`, `.tabsep`, `.crumb`, `h2.sect`, `.sectnote` 규칙 삭제. `.wrap` 은 `max-width: 1240px` 유지하되 좌우 padding 은 `.main` 이 가짐.
- [ ] **Step 3: `shell` 구현** (시안 스크립트의 목록 그리기·검색·접기·서랍·폭 조절을 옮김). 추가 규칙: 검색어가 있으면 접힌 단원도 펼쳐 보임, 현재 문제의 단원은 항상 펼침, 준비 중 항목은 링크 아님(`<div class="item soon">`), 이전/다음은 `ready` 인 것만 건너뛰며 PROBLEMS 순서(도구 제외), 서랍 열림 중 `body{overflow:hidden}`. 첫 화면(`null`)은 topbar 경로 없음.
- [ ] **Step 4: 페이지 로드 확인 스크립트로 검증**: 스크래치에 `shot.sh` (http.server 8765 + `firefox --headless --profile ~/snap/firefox/common/omxtest/prof --screenshot`), torque·basics·tool-servo 1280 폭 캡처 → 사이드바·번호 4·단계줄·이전(3 준비 중이라 건너뛰고 `0 · 기초 개념`)·다음(5) 확인.
- [ ] **Step 5: localStorage 막힘 확인**: 스크래치 테스트 페이지에서 iframe 안 `Storage.prototype.getItem/setItem` 을 throw 로 바꾼 뒤 torque 로드 → 캡처가 정상(오류로 빈 화면 아님).
- [ ] **Step 6: 검색 "없는말" 입력, 모든 단원 접기 상태를 테스트 페이지(iframe 조작)로 캡처** → 안내 문구, 현재 단원 펼침 확인.

### Task 3b: 떠 있는 계산기 (`common/calc.js`)

시안의 계산기를 그대로 옮긴다 (시안 소스 `$SCRATCH/omx-layout-mockup.html` 의 "떠 있는 계산기" CSS·HTML·JS).

**Files:**
- Create: `common/calc.js` (DOM 을 스스로 만들어 `body` 끝에 붙임, 전역 `OmxCalc`)
- Modify: `common/lab.css` (`.calc-fab`, `.calc*`, `.tape`, `.keys` 규칙), 모든 페이지 `index.html` 에 `<script src="../common/calc.js"></script>` (첫 화면은 `common/calc.js`)

**Interfaces:**
- Produces: `OmxCalc.evaluate(src: string, opts?: {deg?: boolean, ans?: number}) -> number` (실패 시 한국어 메시지의 Error throw), `OmxCalc.open()`, `OmxCalc.close()`
- 저장 키 `omx-lab-calc` = `{hist: [{ex, rs}] (최근 50개), deg, ans}`

동작 (시안과 같음): 오른쪽 아래 "계산기 \" 버튼 또는 `\` 키(입력칸 밖에서)로 열고 닫기, Esc 닫기 · 기록 테이프에 `식 = 결과`가 차례로 쌓임, 식을 누르면 입력칸으로 다시, 결과를 누르면 입력칸에 끼워 넣기 · 입력하는 동안 미리보기 `= …`, 틀린 식은 이유 표시(괄호 빠짐, 모르는 이름, 0으로 나눔) · 키: C ( ) ⌫ ÷ / sin 7 8 9 × / cos 4 5 6 − / √ 1 2 3 + / x² 0 . π = / g ans xʸ tan · DEG/RAD 전환(기본 DEG) · 상수 g = 9.81, π, ans · 곱셈 생략(2π, 2(3)) · "답 넣기" = 마지막으로 누른 페이지의 숫자 입력칸에 결과를 넣고 `input` 이벤트 발생 · 넓은 화면은 머리줄 끌어 옮기기, 820 px 이하는 아래쪽 시트 · 계산은 `eval` 없이 직접 해석.

- [ ] **Step 1: 계산 테스트 페이지 작성** `tools/calc_test.html` (배포 제외 목록에 추가, 블로그로 rsync 할 때 `--exclude tools/`). 검사식과 기대값:
  `0.0232÷9.81÷0.401×1000` → 5.897590377 · `1.5÷(9.81×0.401)` → 0.3813097226 · `2π(3+1)²−√16` → 96.53096491 · `sin(30)` (DEG) → 0.5 · `sin(π/6)` (RAD) → 0.5 · `-2^2` → -4 · `2^3^2` → 512 · `50%×g` → 4.905 · `1.5e-3×1000` → 1.5 · 오류: `(1+2` → "괄호", `foo(2)` → "모르는 이름", `1÷0` → "무한대". 결과를 표로 보여 주고 모두 맞으면 제목에 `PASS`.
- [ ] **Step 2: 테스트 페이지를 Firefox 로 열어 FAIL 확인** (calc.js 없음).
- [ ] **Step 3: `common/calc.js` 구현, CSS 이식, 페이지에 script 추가.**
- [ ] **Step 4: 테스트 페이지 PASS 캡처, torque 페이지에서 계산기 열기·답 넣기(실험 슬라이더 옆 숫자칸이 아니라 예측 입력칸 `pred-g`)를 iframe 조작으로 확인.**

### Task 4: 첫 화면, 기초 개념, 도구, 문서 파일

**Files:**
- Modify: `index.html`, `basics/index.html`, `tool-servo/index.html`, `tool-estimate/index.html`, `README.md`, `NOTICE`, `common/lab.js`(renderFoot 문구)

**Interfaces:**
- Consumes: `OmxLab.shell(null)`, `UNITS`, `PROBLEMS`, `TOOLS`

- [ ] **Step 1: 첫 화면**: 제목 "피지컬AI 실험실", 부제·소개 문장(예측 → 실험 → 비교, 설치 없음, OMX-AI 팔로워 팔), "처음이면 0 · 기초 개념부터" 버튼, 단원별 카드 묶음(단원 이름 · 설명, 카드에 번호·제목·개념, 준비 중 흐리게) — `OmxLab.renderHome(el)` 로 그림. 스크립트는 `OmxLab.shell(null); OmxLab.renderHome(...)`.
- [ ] **Step 2: 기초 개념**: `상황 1~10` 문장을 "모든 상황" 으로, τ 경고의 상황 번호를 `data-ref="contact"` 로(Task 2 에서 했으면 확인만). 기구학 용어 추가는 2단계 범위라 하지 않음.
- [ ] **Step 3: README/NOTICE/꼬리말**: 사이트 이름 교체, README 구조 절을 새 폴더 이름·`PROBLEMS` 설명으로, 꼬리말에 "제작 Langpeu" 링크는 넣지 않음(사이드바에 있음).
- [ ] **Step 4: `python3 tools/check_site.py --skip-redirect`** → OK.

### Task 5: 옛 주소 이동 페이지

**Files:**
- Create: `p00-basics/index.html` … `p10-payload/index.html` (11개, 같은 틀)

- [ ] **Step 1: 틀**: `<!doctype html>`, charset, `<title>이동: <새 제목> | 피지컬AI 실험실</title>`, `<meta http-equiv="refresh" content="0; url=../<id>/">`, `<link rel="canonical" href="../<id>/">`, 본문에 새 주소 링크 한 줄, 해시 유지 스크립트 `location.replace("../<id>/" + location.hash)`. `tools/check_site.py` 가 이 폴더들은 (c)~(f) 검사에서 뺌.
- [ ] **Step 2: `python3 tools/check_site.py`** (옵션 없이) → OK.
- [ ] **Step 3: `p01-torque/#c5` 를 Firefox 로 열어 캡처** → torque 페이지 응용 카드 위치.

### Task 6: 전체 확인과 배포

**Files:** 없음 (확인), 작업 노트 `omx_lab/CLAUDE.md`

- [ ] **Step 1: htmlproofer**: 스크래치 `site/omx-lab` 로 rsync 후 Docker ruby:3.1 + html-proofer 3.19.4 → `HTML-Proofer finished successfully`.
- [ ] **Step 2: 화면 캡처**: 첫 화면·basics·torque·sim2real·tool-servo 를 1280 폭, torque 를 390 폭(서랍 닫힘·열림), 다크(`prefers-color-scheme` 는 headless 에서 `ui.systemUsesDarkTheme` 설정 프로필로) → 가로 스크롤 없음, 글자 겹침 없음.
- [ ] **Step 3: 실험 실행**: Marionette(또는 iframe 테스트 페이지)로 torque 에서 1.0 Nm 실행 → "버팀", sag 기본 실행, contact 기본 실행 → 결과 표시 확인. 상황 1 경계(마찰 끔 0.55 떨어짐/0.58 버팀) 한 번 재확인.
- [ ] **Step 4: 작업 노트 갱신**: 새 번호표, 폴더, `shell`/`refLinks` 규칙, 옛 주소 이동, 검사 스크립트 사용법.
- [ ] **Step 5: 사용자에게 결과 보고 후 승인받고** 블로그 클론에 rsync → `git pull --rebase` → 커밋 → push. 배포 실행은 사용자가 함.
