# 💻 Landing Kit 프로토타입 & PayPal 결제 연동 — 개발 로드맵 초안

## 🎯 목표: 1인 기업용 랜딩 페이지 MVP (Next.js + Supabase + PayPal)

### 1. 스택 설정 및 초기 구조화 (Day 0-1)
```bash
# Next.js + Tailwind CSS 기반 템플릿 생성
npx create-next-app@latest landing-kit --typescript --tailwind --eslint
cd landing-kit
npm install @supabase/supabase-js next-auth

# PayPal SDK 준비 (Next.js 서버 렌더링 환경 고려)
npm install @paypal/react-paypal-js # 또는 PayPal Commerce Platform SDK
```
- **기능 요구사항 정의:**
  - Hero 섹션: 가치 제안 + 강력한 CTA
  - Features: 3~4 가지 핵심 기능 (Supabase 데이터로 동적 로딩 가능)
  - Testimonials: Supabase 테이블에서 리뷰/추천 문구 불러오기
  - Pricing: 기본/프로페셔널/기업용 3 단계 가격 책정 (PayPal 결제와 연동된 버튼 생성 필요)
  - FAQ: Accordion 컴포넌트
  - Footer: 연락처, SNS 링크

### 2. PayPal 결제 연동 기술적 검토 및 병목 지점 분석 🛠️

#### ✅ 구현 가능성
- **프론트엔드 (Next.js):** `@paypal/react-paypal-js` 라이브러리를 사용하거나, PayPal Commerce Platform에서 제공하는 `<PayPalButton>` 컴포넌트를 서버 렌더링 환경에 맞게 `dynamic import` 로 처리.
- **백엔드 (Supabase + Next.js API Routes):** 결제 요청을 Supabase 테이블 (orders) 에 기록하고, PayPal 사인온 URL 을 동적으로 생성하는 API Route (`/api/paypal/orders`) 구현 가능.
- **보안:** PayPal Client ID 및 Secret 은 `.env.local` 에 저장하고 `.gitignore` 로 관리. Next.js 환경 변수로 노출되지 않도록 주의.

#### ⚠️ 병목 지점 및 해결책
1. **Supabase 인증 및 데이터 연동 속도**  
   - 병목: Supabase 실시간 구독 (Realtime) 을 Hero 섹션의 동적 콘텐츠에 적용할 경우, 클라이언트에서 초기 데이터 로딩이 지연될 수 있음.  
   - 해결: `prefetch` 전략으로 데이터 미리 로드하거나, `loading` 컴포넌트를 사용.
   
2. **PayPal SDK 서버 렌더링 (SSR) 환경에서의 호환성**  
   - 병목: PayPal SDK 는 클라이언트 측 JS 가 필수적이므로, Next.js `getServerSideProps` 나 API Route 에서 직접 초기화되지 않을 수 있음.  
   - 해결: Next.js 13+ 의 `<ClientProvider>` 패턴을 따르거나, `useEffect` 로 클라이언트 초기화. PayPal SDK 를 `dynamic import()` 로 지연 로드하여 번들 크기 감소.

3. **결제 후 리디렉션 및 주문 상태 확인**  
   - 병목: PayPal 웹훅 (Webhook) 이 정상적으로 처리되지 않으면, 주문 상태를 업데이트하지 못해 환불이나 재결제가 어려움.  
   - 해결: PayPal API 를 통해 결제 결과를 직접 확인하고, Supabase orders 테이블에 `status` 컬럼을 추가하여 외부 검증 로직 구현.

### 3. 개발 로드맵 (총 14 일 예상)

#### Phase 1: 프로토타입 구축 및 기본 기능 구현 (Day 1-5)
| 구분 | 작업 내용 | 담당자 | 완료 기준 |
|------|----------|--------|-----------|
| Day 1 | Next.js + Tailwind 템플릿 생성, Supabase 초기 설정 (테이블: orders, testimonials) | 코다리 | 프로젝트 루트 생성 및 Supabase 연결 확인 |
| Day 2 | Hero 섹션 및 Features 컴포넌트 개발 (Supabase 데이터 연동) | 코다리 | 로컬 환경에서 데이터 로딩 테스트 완료 |
| Day 3 | Testimonials 섹션 구축 + Accordion FAQ 구현 | 코다리 | UI 와 동적 데이터 연동 검증 |
| Day 4 | Pricing 섹션 디자인 및 PayPal 버튼 배치 (클라이언트 측 `dynamic import`) | 현빈 (디자인), 코다리 (개발) | 버튼 클릭 시 모달/페이지 전환 로직 구현 |
| Day 5 | Footer 및 네비게이션 컴포넌트 완성, 전체 레이아웃 검토 | Designer (현빈) | 시각적 일관성 확인 |

#### Phase 2: PayPal 결제 연동 및 백엔드 API 구축 (Day 6-10)
| 구분 | 작업 내용 | 담당자 | 완료 기준 |
|------|----------|--------|-----------|
| Day 6 | PayPal SDK 초기화 및 환경 변수 (.env) 관리 설정 | 코다리 | `.gitignore` 에 API 키 포함 안됨 확인 |
| Day 7 | Next.js API Route (`/api/paypal/orders`) 구현: 결제 요청 처리, Supabase orders 저장 | 코다리 | Postman 등으로 API 테스트 통과 |
| Day 8 | PayPal 사인온 URL 생성 로직 및 프론트엔드 `<PayPalButton>` 컴포넌트 개발 | 현빈 (UX), 코다리 (개발) | 버튼 클릭 시 올바른 주문 ID 생성됨 확인 |
| Day 9 | 결제 완료 페이지 구현 + PayPal 웹훅 처리 로직 (Webhook endpoint 설정) | 현빈, 코다리 | 웹훅 테스트 환경에서 주문 상태 업데이트 확인 |
| Day 10 | Supabase `orders` 테이블 스키마 최적화 및 인덱스 추가 | 코다리 | 쿼리 성능 테스트 통과 |

#### Phase 3: 통합 테스트 및 배포 준비 (Day 11-14)
| 구분 | 작업 내용 | 담당자 | 완료 기준 |
|------|----------|--------|-----------|
| Day 11 | 전체 페이지 흐름 테스트 (Hero → Features → Pricing → Checkout) | 코다리 | 브라우저 개발자 도구에서 네트워크 요청 확인 |
| Day 12 | PayPal 결제 시뮬레이션 (샌드백 환경) 및 환불 로직 구현 | 현빈, 코다리 | 테스트 완료 보고 |
| Day 13 | 성능 최적화: Next.js `images` 컴포넌트 사용, Tailwind JIT 설정, Lighthouse 점수 90+ 목표 | 코다리 | Lighthouse 결과 확인 |
| Day 14 | GitHub에 프로토타입 저장소 생성 및 CI/CD 파이프라인 (Vercel) 연결 | 현빈 | 배포 자동화 테스트 완료 |

### 4. 기술적 결정 사항 (Tech Decisions)
- **프론트엔드:** Next.js 14 + App Router + Tailwind CSS  
- **백엔드:** Supabase (PostgreSQL) — 인증 없이도 데이터만 사용하는 경우 `anon` 역할 사용  
- **결제:** PayPal Commerce Platform API v2 — 보안 및 PCI DSS 준수 고려  
- **배포:** Vercel (Next.js 호환성 최적) + GitHub Actions 자동 배포  

### 5. 예상 리스크 및 대비책
| 리스크 | 영향도 | 해결책 |
|--------|--------|--------|
| PayPal 샌드백 환경에서 결제 흐름이 실제와 다름 | 중 | 결제 완료 시뮬레이션 도구를 적극 활용하고, 웹훅 테스트 키를 별도로 관리 |
| Supabase 데이터 접근 지연 (초기 로딩) | 낮 | `prefetch` 전략 + 클라이언트 측 캐싱 |
| Next.js 서버 사이드 렌더링 환경에서 PayPal SDK 호환성 문제 | 중 | `dynamic import()` 로 SDK 지연 로드, `useEffect` 로 초기화 |

---  
**다음 단계:** Phase 1 Day 1 작업 시작 — Next.js 프로젝트 생성 및 Supabase 초기 설정. 💻