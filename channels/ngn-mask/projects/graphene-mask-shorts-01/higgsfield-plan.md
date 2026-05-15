# 힉스필드(Higgsfield) 영상 생성 활용 가이드

> 작성일: 2026-05-10
> 잔액 확인: 1.1 크레딧 (Free 플랜) → **충전 후 실행 권장**

## 선택한 조합 (사용자 확정)
- **Hook**: Product Hit (`3d45fb46-254f-4c83-9685-8e3d28945a67`)
  - 컨셉: "오브젝트(전구)가 날아와 마스크에 부딪힘 → 짧은 반응 → 제품으로 피벗"
- **Preset**: Hyper Motion (`hyper_motion`)
  - 컨셉: 그래핀 분자구조·전구 시연·성분을 빠른 컷의 시각적 임팩트로 전개

## ⚠️ 호환성 제약
**Hyper Motion 프리셋은 Hook을 직접 지원하지 않는다.** Marketing Studio Hook은 UGC / Tutorial / Unboxing / Product Review / UGC Virtual Try On에서만 적용 가능.

→ 두 가지 실행 방법 중 선택해야 함.

---

## 실행 방법 1: 단일 영상 (Hyper Motion + Hook 컨셉을 prompt에 녹이기)
**장점**: 1번 호출, 크레딧 절약
**단점**: Hook 프리셋의 정형화된 효과는 적용 안됨

### 호출 예시
```python
# 1. 제품 등록 (이미 있는 마스크팩 박스 이미지 업로드)
mcp__claude_ai__show_marketing_studio(
    action="create",
    type="product",
    title="엔지엔 그래핀 에센셜 마스크팩",
    medias=[{"value": "<업로드한 마스크팩 이미지 URL>", "type": "media_input"}]
)

# 2. 영상 생성
mcp__claude_ai__generate_video(
    params={
        "model": "marketing_studio_video",
        "prompt": "[Product Hit 컨셉을 직접 명시한 prompt — 아래 참고]",
        "duration": 8,  # 또는 10
        "aspect_ratio": "9:16"
    }
)
```

### Prompt (한글+영문 혼용, 모델은 영문 권장)
```
A glowing light bulb suddenly flies into frame and gently touches an NGN GRAPHENE
ESSENTIAL MASK PACK held by an elegant Asian woman in her 30s. The bulb instantly
lights up on contact, with subtle blue electric currents flowing across the
graphene mask sheet. Quick cut to a hexagonal graphene molecular structure
animation, then to the mask sheet glowing with skincare ingredients absorbing
deeply into skin. Hyper-motion style, premium beauty product commercial,
clean white-to-blue gradient background, dramatic lighting, 9:16 vertical,
fast-paced cuts, K-beauty aesthetic.
```

---

## 실행 방법 2: 두 컷 분할 생성 후 편집 합성 (권장)
**장점**: Hook 프리셋의 정형화된 효과 활용 가능
**단점**: 2번 호출, 크레딧 2배, 후편집 필요

### 컷 A — 후킹부 (0~3초)
- **Preset**: Product Review (`product_review`) + **Hook**: Product Hit
- 호출 예시:
```python
mcp__claude_ai__generate_video(
    params={
        "model": "marketing_studio_video",
        "prompt": "A small glowing light bulb flies into frame and hits the NGN GRAPHENE ESSENTIAL MASK PACK held by an Asian woman in her 30s. Brief surprised reaction, then she calmly turns the product to the camera with a confident expression.",
        "duration": 5,
        "aspect_ratio": "9:16",
        "hook_id": "3d45fb46-254f-4c83-9685-8e3d28945a67"
    }
)
```

### 컷 B — 본편 (3~40초, Hyper Motion 단독)
- **Preset**: Hyper Motion (Hook 없음)
- 호출 예시:
```python
mcp__claude_ai__generate_video(
    params={
        "model": "marketing_studio_video",
        "prompt": "Premium K-beauty product commercial: hexagonal graphene molecular structure animation, mask sheet glowing with blue electric currents, copper coil vs graphene comparison split-screen showing 100x conductivity, ingredients absorbing deeply into skin cross-section, before/after skin tone transformation, NGN GRAPHENE ESSENTIAL MASK PACK product shot rotating, clean white-to-blue gradient background, hyper-motion style, fast-paced cuts, dramatic lighting, 9:16 vertical.",
        "duration": 8,
        "aspect_ratio": "9:16"
    }
)
```

### 후편집
- DaVinci Resolve / CapCut / Premiere에서 컷 A → 컷 B 컷 연결
- TTS 음성 (별도 생성) 오버레이
- 한글 자막 풀착장
- BGM 합성 (저작권 프리)

---

## 크레딧 견적 (대략)
- marketing_studio_video 1회: 약 5~15 크레딧 (모델 정확 견적은 호출 시 확인)
- 방법 1 = 약 5~15 크레딧
- 방법 2 = 약 10~30 크레딧
- **현재 잔액 1.1 → 모든 옵션 부족, 충전 필요**

## 제품 이미지 업로드 가이드
사용자가 제공한 상세페이지 이미지(jpg) 자체는 마스크팩 박스 + 모델 + 설명문이 섞여 있어 광고 영상 reference로 적합하지 않을 수 있음.

**권장 reference 이미지**:
1. 마스크팩 박스 단독 컷 (배경 화이트, 정면)
2. 마스크 시트 단독 컷 (펴진 상태, 그래핀 패턴 보임)
3. 모델이 마스크 들고 있는 크롭 컷

→ 사용자가 추가 자료 제공 시 image-to-video 흐름으로 더 정확한 영상 생성 가능.

---

## 실행 시 체크리스트
- [ ] 크레딧 5~30 수준으로 충전
- [ ] 마스크팩 단독 reference 이미지 1~3장 준비 (`media_upload`)
- [ ] `show_marketing_studio(action='create', type='product')`로 제품 등록
- [ ] 방법 1 또는 2 선택
- [ ] `generate_video` 호출 → `job_status` 폴링
- [ ] 결과물 다운로드
- [ ] TTS 대본(`script-v1.txt`) → 별도 TTS 서비스에서 음성 생성
- [ ] 영상 + 음성 + 자막 합성 (외부 편집툴)

## 호출 시 참조할 ID (불변)
- Product Hit hook: `3d45fb46-254f-4c83-9685-8e3d28945a67`
- Hyper Motion preset slug: `hyper_motion`
- Product Review preset slug: `product_review`
- 모델: `marketing_studio_video`
