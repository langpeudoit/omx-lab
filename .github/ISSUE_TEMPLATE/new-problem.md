---
name: 새 문제 추가
about: 새 문제(상황) 하나를 만들 때
title: "[새 문제] N 이름 (id)"
labels: ["새 문제"]
---

## 개요
- 번호 / id / 단원:
- 제목:
- 개념 한 줄:

## 손계산 ↔ 시뮬 확인
- [ ] 손계산 식과 값
- [ ] 브라우저 MuJoCo(`tools/probe.html`)로 시뮬 값 확인
- [ ] 허용오차와 실험 조건을 정해 사용자에게 수치 보고

## 구현
- [ ] `site/<id>/` 페이지 (개념 → 예측 → 실험 → 확인 → 응용)
- [ ] 실험은 `OmxLab.check3` 방식 (예측 ×0.9 / 그대로 / ×1.1)
- [ ] 정답 예측을 넣으면 실제로 "맞음"이 나오는지 확인
- [ ] `common/lab.js` 에서 `ready: true`
- [ ] `python3 site/tools/check_site.py` 통과
- [ ] 브라우저 `tools/test.html`, `tools/calc_test.html` 통과

## 참고
- 설계 문서 `docs/2026-11-21-kinematics-dynamics-expansion-design.md` 7장 해당 절
