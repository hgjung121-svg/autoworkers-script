# 팩트체크 — ep07-part3 (배당 재투자 정밀 시뮬편)

> 프로젝트: etf-ep07-part3 (보충편, 재투자 3트랙 정밀 시뮬)
> 검증일: 2026-05-10
> 대상: ep07-part3 보강 데이터 (base는 ep07/ep07-part2 factcheck.md.base 참조)
> 검증 원칙: 1차 출처(공식 운용사·감독당국·언론사 1면) 우선, 정밀 시뮬편이므로 ★★★ 데이터만 영상 단정 인용

---

## A. 배당 재투자 3트랙 시뮬 (영상 보정 포인트 #2 — 핵심)

| 데이터 | 출처 검증 | 검증 | 실제값 | 출처 |
|---|---|---|---|---|
| JEPI 6년 누적 총수익 (DRIP) | Total Real Returns | ✅ 검증됨 | +89.65% (2020.05.21~2026.05.01) | totalrealreturns.com/n/JEPI,SPY |
| JEPI 6년 연환산 총수익 (DRIP) | Total Real Returns | ✅ 검증됨 | +11.37%/yr | totalrealreturns.com |
| SPY 6년 누적 총수익 (DRIP) | Total Real Returns | ✅ 검증됨 | +165.86% | totalrealreturns.com/n/JEPI,SPY |
| SPY 6년 연환산 총수익 (DRIP) | Total Real Returns | ✅ 검증됨 | +17.88%/yr | totalrealreturns.com |
| JEPI vs SPY 누적 격차 | 계산 | ✅ 검증됨 | 76.21%p (SPY 우세) | 위 두 항목 차이 |
| $10,000 → JEPI 6년 후 | Total Real Returns | ✅ 검증됨 | $18,965 | totalrealreturns.com |
| $10,000 → SPY 6년 후 | Total Real Returns | ✅ 검증됨 | $26,586 | totalrealreturns.com |
| JEPQ 4년 누적 총수익 (DRIP) | Total Real Returns | ✅ 검증됨 | +79.46% (2022.05~2026.05) | totalrealreturns.com/n/JEPQ,QQQ |
| JEPQ 4년 연환산 (DRIP) | Total Real Returns | ✅ 검증됨 | +15.78%/yr | totalrealreturns.com |
| QQQ 4년 누적 (DRIP) | Total Real Returns | ✅ 검증됨 | +109.75% | totalrealreturns.com |
| QQQ 4년 연환산 (DRIP) | Total Real Returns | ✅ 검증됨 | +20.39%/yr | totalrealreturns.com |
| QYLD 12.4년 누적 (DRIP) | Total Real Returns | ✅ 검증됨 | +178.83% (2013.12~2026.05) | totalrealreturns.com/n/QYLD,QQQ |
| QYLD 12.4년 연환산 (DRIP) | Total Real Returns | ✅ 검증됨 | +8.63%/yr | totalrealreturns.com |
| QQQ 12.4년 누적 (DRIP) | Total Real Returns | ✅ 검증됨 | +780.10% | totalrealreturns.com |
| QQQ 12.4년 연환산 (DRIP) | Total Real Returns | ✅ 검증됨 | +19.20%/yr | totalrealreturns.com |
| QYLD vs QQQ 누적 격차 | 계산 | ✅ 검증됨 | 601.27%p (4.4배) | 위 항목 차이 |
| $10,000 → QYLD 12.4년 (DRIP) | Total Real Returns | ✅ 검증됨 | $27,883 | totalrealreturns.com |
| $10,000 → QQQ 12.4년 (DRIP) | Total Real Returns | ✅ 검증됨 | $88,010 | totalrealreturns.com |
| QYLD 상장가→2026.05 NAV | Optimized Portfolio | ✅ 검증됨 | $25.00 → 약 $18 (NAV -28%) | optimizedportfolio.com QYLD 2026 |
| QYLD 연 NAV 잠식률 | Optimized Portfolio | ✅ 검증됨 | 약 3.72%/yr | optimizedportfolio.com |
| JEPI 5년 연환산 (2020-2025) | stockanalysis | ✅ 검증됨 | +8.04%/yr | stockanalysis.com / financecharts.com |
| SP500 5년 연환산 (2021-2025) | macrotrends | ✅ 검증됨 | 약 +14.4%/yr | macrotrends.net SP500 historical |
| JEPI vs SP500 5년 격차 | 계산 | ✅ 검증됨 | 약 6.36%p/yr | 위 항목 차이 |

## B. 분배율 20% 가상 시뮬 (Base 데이터 재검증)

| 데이터 | 레퍼 | 검증 | 실제값 | 출처 |
|---|---|---|---|---|
| 분배율 20% → 1만원 → 3,357원 (15년) | base | ✅ 검증됨 | 3,357원 (2010~2024.12.31, 1만원 시작) | 한국경제 2025.01.20 |
| 분배율 15% → 7,186원 | base | ✅ 검증됨 | 7,186원 | 한국경제 2025.01.20 |
| 분배율 10% → 1만5,334원 | base | ✅ 검증됨 | 1만5,334원 (오히려 +53%) | 한국경제 2025.01.20 |
| 시뮬 주체 | base | ⚠️ 한정사항 | "운용업계 관계자" (특정 기관 비공개) | 한국경제 2025.01.20 |
| 시뮬 가정 | base | ⚠️ 한정사항 | "옵션 매도 효과 미반영, 분배율 = 기초자산 직접 차감" 단순 모델 명시 | 한국경제 2025.01.20 |
| 기초자산 | base | ✅ 검증됨 | 미 S&P500 토털리턴(TR) 지수 | 한국경제 2025.01.20 |
| 영상 표현 보정 권장 | - | 추가 | "분배율이 기초자산 성장률을 초과하면 NAV는 깎인다" 조건문 권장 | - |

## C. 샤프 비율 / 변동성 / MDD (영상 보정 포인트 #3)

| 데이터 | 출처 검증 | 검증 | 실제값 | 출처 |
|---|---|---|---|---|
| QQQ 5년 샤프 비율 | PortfoliosLab | ✅ 검증됨 | 약 0.49 | portfolioslab.com/symbol/QQQ |
| QQQ 3년 샤프 비율 | PortfoliosLab | ✅ 검증됨 | 약 1.17 | portfolioslab.com |
| QQQ 1년 샤프 비율 | PortfoliosLab | ✅ 검증됨 | 약 2.74 | portfolioslab.com |
| VOO 12개월 샤프 | PortfoliosLab | ✅ 검증됨 | 약 2.32 | portfolioslab.com |
| SCHD 12개월 샤프 | PortfoliosLab | ✅ 검증됨 | 약 2.48 | portfolioslab.com (SCHD vs JEPI) |
| JEPI 12개월 샤프 | PortfoliosLab | ✅ 검증됨 | 1.50~1.74 (시점별) | portfolioslab.com |
| JEPI 변동성 | PortfoliosLab | ✅ 검증됨 | 약 2.67~4.03% (저변동성) | portfolioslab.com |
| VOO 변동성 | PortfoliosLab | ✅ 검증됨 | 약 5.58% | portfolioslab.com |
| SCHD 5년 표준편차 (연환산) | YCharts/Morningstar | ✅ 검증됨 | 약 10.55~15.6% | ycharts SCHD 5Y, lazyportfolio |
| QQQ 변동성 | Unusual Whales | ✅ 검증됨 | 약 16.29% | unusualwhales.com QQQ |
| JEPI 최대낙폭 (상장 후) | PortfoliosLab | ✅ 검증됨 | -13.71% | portfolioslab.com |
| SPY 최대낙폭 (장기) | PortfoliosLab | ✅ 검증됨 | -55.19% (장기 누적) | portfolioslab.com |
| SCHD 최대낙폭 (상장 후) | YCharts | ✅ 검증됨 | -33.4% (2011-2025) | ycharts SCHD MDD |
| QQQ 최대낙폭 (장기) | PortfoliosLab | ✅ 검증됨 | -82.97% (2002.10.09 닷컴) | portfolioslab.com |
| QQQ 회복 기간 (닷컴) | base 재검 | ✅ 검증됨 | 3,112 거래일 (약 14년) | portfolioslab.com |
| QQQ 5년 연환산 (DRIP) | stockanalysis | ✅ 검증됨 | +17.01%/yr | stockanalysis.com |
| QQQ 10년 연환산 (DRIP) | stockanalysis | ✅ 검증됨 | +21.90%/yr | stockanalysis.com |
| VOO 5년 연환산 (DRIP) | stockanalysis | ✅ 검증됨 | +13.42%/yr | stockanalysis.com |
| VOO 10년 연환산 (DRIP) | stockanalysis | ✅ 검증됨 | +15.57%/yr | stockanalysis.com |
| SCHD 5년 연환산 (DRIP) | stockanalysis | ✅ 검증됨 | +7.92%/yr | stockanalysis.com |
| SCHD 10년 연환산 (DRIP) | stockanalysis | ✅ 검증됨 | +12.69%/yr | stockanalysis.com |

## D. 한국 시장 ETF 2026년 5월 분배율

| 데이터 | 출처 검증 | 검증 | 실제값 | 출처 |
|---|---|---|---|---|
| SOL 팔란티어커버드콜OTM채권혼합 분배율 1위 | 신한자산운용 | ✅ 검증됨 | 26.24% (2026.01) / 연환산 24.78% (3월) | econsis.kr 2026.01 / 신한자산운용 |
| PLUS 고배당주위클리커버드콜 분배율 | PLUS ETF | ✅ 검증됨 | **20.86%** (2026.01) — base의 19.5% 대비 상향 | econsis.kr 2026.01 |
| SOL 팔란티어미국채커버드콜혼합 | 신한자산운용 | ✅ 검증됨 | 19.75% | econsis.kr 2026.01 |
| RISE 미국테크100데일리고정커버드콜 | KB자산운용 | ✅ 검증됨 | 19.54% | econsis.kr 2026.01 |
| KODEX 미국나스닥100데일리커버드콜OTM | 삼성자산 | ✅ 검증됨 | 19.10% | econsis.kr 2026.01 |
| KODEX 200타겟위클리커버드콜 | 삼성자산 | ✅ 검증됨 | 코스피 200 타겟 15% 위클리 CC 지수 추적 | samsungfund.com |
| 일반 월배당 ETF 1위 SOL 코리아고배당 | 신한자산운용 | ✅ 검증됨 | 8.73% | econsis.kr 2026.01 |
| 미래에셋 "반토막 분배율" 7% 적정 발언 | 한국경제 | ✅ 검증됨 | 김남기 본부장 2025.09.18 발언 | hankyung.com 2025.09.18 |
| 금감원 2024.07 소비자 경보 | base | ✅ 검증됨 | 변동분배율 강조 | 한국경제 2024.07 |
| 2026 금감원 전수조사 진행 | 금감원 | ✅ 검증됨 | 진행 중 (구체 결과 미공개) | 한국경제 2026 |
| 종목명 "분배율" "프리미엄" 규제 | base | ✅ 검증됨 | 유지 | 한국경제 2024.07 |
| ISA 납입한도 4,000만원 상향 (입법) | 한국금융신문 | ⚠️ 입법 진행 | 2024 세법개정안 반영, 2026.04 기준 시행 미완 | hankyung 2024.07.25, 뉴시스 2024.07 |
| ISA 비과세 한도 200→500만원 (서민형 1,000만원) | 한국금융신문 | ⚠️ 입법 진행 | 입법 진행 중 | 뉴시스 2024.07 |
| 슈퍼 ISA / 생산적 금융 ISA 출시 | 정부 | ✅ 검증됨 | 2026.06 출시 목표 (세법 통과 시점 변동) | 캐시코드 2026 |
| 자본시장법 시행령 개정안 | 금융위 | ✅ 검증됨 | 단일종목 레버리지 ETF, 완전 액티브 ETF, 커버드콜 기반 확대 | 금융위 2026 |

## E. 학술 / 1차 연구 자료

| 데이터 | 출처 검증 | 검증 | 실제값 | 출처 |
|---|---|---|---|---|
| Whaley 2002 BXM 논문 | Cboe | ✅ 검증됨 | "Return and risk of CBOE buy write monthly index", Journal of Derivatives 10, 35-42 (2002) | Cboe 공식 / Whaley 1988.06~2001.12 데이터 |
| BXM 10년 = SP500 1/3 | Cboe | ✅ 검증됨 | 최근 10년 BXM 총수익이 SP500의 1/3 | Cboe 공식, ProShares 2026 |
| BXM skewness -1.11 vs SP500 -0.81 | Cboe | ✅ 검증됨 | 부정적 왜곡도 BXM이 더 큼 | CBOE 데이터 |
| JEPI ELN 구조 ordinary income 과세 (미국) | Mezzi | ✅ 검증됨 | 옵션 프리미엄도 이자소득으로 분류, 최고 37% | mezzi.com 2026 |
| JEPI 세전 10% → 세후 6.8% (32% 세율 구간) | Mezzi | ✅ 검증됨 | 미국 거주자 기준 | mezzi.com 2026 |
| QYLD ROC 2021/0%, 2022/81.5%, 2023/100%, 2024/0% | Optimized Portfolio | ✅ 검증됨 | ROC 분류 변동 극심 | optimizedportfolio.com |

## F. 본편 데이터 보정 / 재검증

| 데이터 | base | 검증 | 실제값 | 출처 |
|---|---|---|---|---|
| JEPI 6년 NAV +15% | base | ✅ 검증됨 | NAV +15% (정확) | base |
| JEPI 6년 총수익(DRIP) | base 누락 | 추가 | +89.65% | totalrealreturns.com |
| 본편 표현 ("거의 그대로") | base | ⚠️ 보정 필요 | 보정형: "NAV +15%, 총수익(DRIP) +89.65%, SP500 TR +165.86% — 결론은 같지만 프레이밍 통일 필요" | - |
| PLUS 분배율 19.5% | base | ⚠️ 갱신 | 2026.01 기준 20.86%로 상향 | econsis.kr 2026.01 |
| 1만원 → 3,357원 시뮬 | base | ✅ 검증됨 + ⚠️ 한정 | 한국경제 2025.01.20 / 옵션 매도 효과 미반영 가정 명시 필요 | hankyung 2025.01.20 |
| KODEX 미국 S&P500 배당귀족 커버드콜 6.2% | base | ❓ 미확인 | 정확한 상품코드 여전히 확인 불가 — 영상 인용 시 제거 권장 | - |
| SCHD 최대 비중 종목 (브로드컴) | base | ⚠️ 시점 한정 | 2024년 시점 기준, 2026.05 시점 별도 확인 필요 | - |

---

## 검증 요약

| 구분 | 건수 |
|---|---|
| ✅ 검증됨 | 64 |
| ⚠️ 한정사항/입법 진행 | 6 |
| ❓ 미확인 | 2 |
| ❌ 불일치 | 0 |

### 핵심 발견

1. **본편 비대칭 프레이밍 정량 확인**: JEPI 6년 NAV +15%만 인용 → 실제 DRIP 총수익은 +89.65%, SPY DRIP는 +165.86%. 결론(SP500 TR > JEPI TR)은 동일하지만 76%p 격차를 직접 제시해야 정확.

2. **QYLD 12.4년 데이터가 가장 강력한 회수 증거**: $10,000 → QYLD $27,883 vs QQQ $88,010 (3.16배 격차). DRIP 시나리오 자체가 답이 아님을 입증.

3. **base 시뮬 (1만원 → 3,357원) 출처는 한국경제 2025.01.20 (서울경제 아님)**: ep07/ep07-part2 verified-data.md에서 "서울경제 2025"로 표기되어 있으나 1차 출처는 한국경제 (서울경제도 동일 시뮬 인용 보도). 본편 옵션 매도 효과 미반영 가정 명시 필요.

4. **PLUS 분배율 갱신**: 본편 19.5% → 2026.01 기준 20.86%. 영상 시점 데이터 갱신 필수.

5. **샤프 비율 데이터로 양방향 방어 가능**:
   - QQQ 5년 샤프 0.49 → "QQQ 만능" 프레임 막을 수 있음
   - JEPI 12개월 샤프 1.50~1.74 → SCHD/VOO 대비 우세하지 않음
   - 결국 샤프로 보면 JEPI/QQQ 둘 다 절대 우위 없음 → 시청자 판단 영역으로 넘김

6. **금감원 2026 전수조사 결과 미공개**: 진행 중 사실은 ✅ 검증, 구체 결과·제재 발표는 미확인. 영상에서 "결과는 시청 시점에 따라 다를 수 있다" 자막 권장.

7. **ISA 4,000만원 상향은 입법 진행 중 (2026.04 기준 시행 미완)**: 영상에서 "추진 중"으로 표현 필수.

### 영상 단정 인용 가능 데이터 (★★★ 1차 출처)

- Total Real Returns 6년/4년/12.4년 누적 수익 모든 수치
- 한국경제 2025.01.20 분배율별 1만원 시뮬 3개 결과값
- econsis.kr 2026.01 한국 ETF 분배율 TOP 10
- Whaley 2002 BXM 논문 (학술 권위)
- Cboe BXM 10년 = SP500 1/3 데이터

### 영상 인용 시 한정사항 명시 필수

- 분배율 20% 시뮬: "옵션 매도 효과 미반영 가정 하" 명시
- ISA 4,000만원 상향: "입법 진행 중, 시행 시점 미확정" 명시
- 금감원 전수조사: "진행 중" 명시
- JEPI 분배율 8%대: "변동분배율, 2026.04 기준" 명시
- 한국 ETF 분배율 TOP 10: "2026.01 기준, 변동 가능" 명시
