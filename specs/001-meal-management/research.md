# Research: Meal Management Feature

**Feature**: 001-meal-management
**Date**: 2025-10-25
**Purpose**: Resolve technical unknowns and document technology decisions for implementation

## Research Questions

This document addresses the "NEEDS CLARIFICATION" items identified in the Technical Context:

1. Should users be able to log meals offline?
2. What OCR/CV library should be used for nutrition label parsing?
3. What LLM API should be used for meal planning, and what rate limiting strategy?

---

## 1. Offline Capability for Meal Logging

### Decision
**Implement offline-first architecture with background sync**

### Rationale
- **User context**: Users log meals throughout the day, often in environments with poor connectivity (restaurants, cafeterias, kitchens)
- **Core use case**: Meal logging (FR-003) is a high-frequency action (3-10 meals/day per user)
- **User experience**: Requiring internet connectivity for every meal log would create significant friction
- **Data safety**: Meal logs are user-generated, immutable records - perfect for optimistic offline writes
- **Performance**: Success criteria SC-002 requires meal logging in <60 seconds; network latency would make this impossible

### Implementation Approach
- **Mobile**: Use React Native AsyncStorage or SQLite for local persistence
- **Sync strategy**: Queue offline writes, sync to backend when connectivity restored
- **Conflict resolution**: Last-write-wins for user's own data (no multi-device conflicts in MVP)
- **Scope limitation**: Only meal logging needs full offline support; pantry management, planning, and insights can require connectivity

### Alternatives Considered
- **Online-only**: Rejected due to poor UX and failure to meet performance criteria
- **Full offline mode**: Rejected as too complex for MVP; LLM planning requires backend anyway
- **Hybrid (selected)**: Offline meal logging + online for other features balances UX and complexity

---

## 2. OCR/CV Library for Nutrition Label Parsing

### Decision
**Use open-source computer vision: MediaPipe + Tesseract OCR (or PaddleOCR) for on-device processing**

### Rationale
- **Zero API costs**: Eliminates recurring per-image costs entirely (critical for MVP budget)
- **User privacy**: All image processing happens on-device; no nutrition data sent to third parties
- **Offline capability**: Works without internet connection, aligns with offline-first strategy
- **Modern OSS quality**: MediaPipe (Google) and PaddleOCR have significantly improved accuracy in recent years
- **MVP timeline**: Good-enough accuracy (70-80%) with user confirmation is acceptable; perfect OCR not required
- **Scalability**: No cost increase as user base grows

### Implementation Approach
1. **Image preprocessing** (mobile-side):
   - Use MediaPipe for image orientation detection and correction
   - Crop to nutrition label region using edge detection (OpenCV or MediaPipe)
   - Enhance contrast and denoise (OpenCV filters)

2. **Text extraction** (mobile or backend):
   - **Option A (Mobile)**: React Native integration with Tesseract.js or react-native-text-recognition
   - **Option B (Backend)**: Upload preprocessed image to FastAPI, use PaddleOCR or Tesseract Python
   - Extract text blocks with bounding boxes

3. **Structured parsing** (backend service):
   - Regex patterns for "Calories", "Total Fat X g", "Protein X g", etc.
   - Fuzzy matching for label variations ("Total Carbohydrate" vs "Total Carbs")
   - Extract numeric values with units

4. **Validation UI**:
   - Display parsed fields in nutrition label layout
   - Highlight low-confidence fields for user correction
   - Allow manual override of any field

5. **Fallback**: If OCR quality score < 60%, skip OCR and show manual entry form directly

### Technology Choice
**Primary Stack**:
- **MediaPipe** (Google): Image preprocessing, text detection regions
- **PaddleOCR** (Baidu, open-source): Superior to Tesseract for complex layouts, supports 80+ languages
- **OpenCV**: Image enhancement and preprocessing utilities

**Alternative**: Tesseract OCR if PaddleOCR integration proves difficult (more mature mobile libraries)

### Implementation Location
**Backend processing (recommended)**:
- Mobile sends captured image to `/api/food-items/parse-label`
- Backend uses PaddleOCR + custom parsing logic
- Returns structured JSON with confidence scores
- Pros: Better accuracy (full Python ML stack), easier to iterate on parsing logic
- Cons: Requires internet, ~5-10 second processing time

**On-device processing (optional enhancement)**:
- React Native integration via native modules
- Pros: Instant feedback, works offline
- Cons: Larger app size, lower accuracy, harder to maintain

### Alternatives Considered
- **Google Cloud Vision API**: $1.50/1000 images = $45/month at 30% adoption. Rejected: unnecessary cost for MVP
- **AWS Textract**: Similar pricing to Cloud Vision. Rejected: same reason
- **Tesseract only**: Lower accuracy (~60-70%). Rejected: PaddleOCR offers better accuracy (~80-90%) for similar effort
- **Mobile ML Kit (on-device)**: Limited structured output, requires native integration. Rejected: backend approach simpler for MVP

---

## 3. LLM API Selection & Rate Limiting

### Decision
**Use Google Gemini 2.5 Flash for meal planning with user-level rate limiting**

### Rationale

#### LLM Selection: Gemini 2.5 Flash
- **Cost**: **FREE tier** - 15 requests/minute, 1500 requests/day, 1M requests/month
  - At 10k users × 1 plan/week = ~1,430 plans/week = **$0/month** (well within free limits)
  - Paid tier (if needed later): $0.075/$0.30 per 1M tokens (half the cost of GPT-4o-mini)
- **Performance**: Fast inference (<5 seconds typical), meets <20 second target easily
- **Context window**: 1M tokens - massive capacity for pantry inventory + recipes + user constraints
- **Structured output**: Supports JSON mode via response_schema parameter
- **Quality**: Gemini 2.5 Flash competitive with GPT-4o-mini for structured generation tasks
- **Prompt example**:
  - Pantry (50 items × 50 tokens) = 2,500 tokens
  - User constraints + system prompt = 1,000 tokens
  - Output (7-day plan, 3 meals/day, 200 tokens each) = 4,200 tokens
  - **Total**: ~3,500 input + 4,200 output = **FREE** (within daily limits)

#### Free Tier Capacity Analysis
- **Daily limit**: 1,500 requests/day
- **Expected usage**: 10k users × 2 plans/week ÷ 7 days = ~2,857 plans/day at full adoption
- **Reality**: Gradual user growth + not all users generate plans weekly = likely <1,000 plans/day for first 6-12 months
- **Conclusion**: Free tier sufficient for MVP and early growth; upgrade to paid when approaching limits

#### Rate Limiting Strategy
1. **User-level limits**:
   - Free tier: 2 meal plans per week (covers normal usage)
   - Cooldown: 12 hours between plan generations
   - Burst: Allow 1 extra plan/week for re-generation after feedback

2. **System-level protection**:
   - Respect Gemini API rate limits: 15 requests/minute (enforced by exponential backoff)
   - Queue system: If rate limit hit, queue requests and process when capacity available
   - Monitor daily usage: Alert at 80% of 1,500 daily limit
   - Failover: If free tier exhausted, gracefully degrade or switch to paid tier

3. **Optimization techniques**:
   - Cache common meal suggestions by dietary pattern (vegetarian, high-protein, etc.)
   - Incremental updates: If user modifies plan, only regenerate affected days
   - Batch processing: Group multiple user requests during off-peak hours
   - Smart retry: Use exponential backoff for rate limit errors (429)

### Implementation Approach
```python
# Pseudocode for rate limiting with Gemini
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

genai.configure(api_key=GEMINI_API_KEY)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
@rate_limit(user_limit="2/week", system_limit="15/minute")
async def generate_meal_plan(user_id, constraints):
    # Check user quota
    if not check_user_quota(user_id):
        raise QuotaExceededError("You've reached your weekly plan limit")

    # Build prompt with pantry + constraints
    prompt = build_meal_plan_prompt(user_id, constraints)

    # Configure Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Call Gemini with JSON schema for structured output
    response = await model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=MealPlanSchema  # Pydantic schema
        )
    )

    # Parse and validate response
    plan = parse_meal_plan(response.text)

    # Increment user quota
    increment_user_quota(user_id)

    return plan
```

### Alternatives Considered

| Option | Cost (10k users, 1 plan/week) | Pros | Cons | Decision |
|--------|-------------------------------|------|------|----------|
| **Gemini 2.5 Flash** | **FREE** (up to 1.5k/day) | Zero cost, fast, large context, structured output | Rate limits may constrain growth | ✅ **Selected** |
| GPT-4o-mini | ~$120/month | Reliable, proven structured output | Unnecessary cost for MVP | ❌ Not needed with free Gemini |
| GPT-4o | ~$400/month | Best reasoning, fastest | 40x more expensive than Gemini paid tier | ❌ Overkill and expensive |
| Claude 3.5 Sonnet | ~$150/month | High quality, good reasoning | 10x more expensive than Gemini paid tier | ❌ Unnecessary cost |
| Llama 3 (self-hosted) | ~$200/month (compute) | No per-token cost, data privacy | Requires ML ops, slower, less reliable | ❌ Too complex for MVP |
| Gemini 2.5 Pro | ~$250/month | Better reasoning than Flash | More expensive, Flash sufficient for meal planning | ❌ Overkill for task |

---

## Best Practices & Patterns

### React Native Development
- **State management**: Use React Context API for MVP, migrate to Redux if state complexity grows
- **Navigation**: React Navigation v6 (industry standard)
- **UI components**: React Native Paper or NativeBase for consistent Material Design/iOS styling
- **Image handling**: react-native-image-picker for camera/gallery access
- **Charts**: react-native-chart-kit or Victory Native for insights visualizations
- **Offline storage**: @react-native-async-storage/async-storage for simple key-value, expo-sqlite for structured data

### FastAPI Best Practices
- **Project structure**: Layered architecture (routes → services → models)
- **Dependency injection**: Use FastAPI's Depends() for database sessions, auth
- **Validation**: Pydantic schemas for all request/response validation
- **Error handling**: Custom exception handlers with consistent error format
- **Database migrations**: Alembic for SQLAlchemy migrations
- **Testing**: pytest with TestClient for API tests, factories for test data
- **Authentication**: JWT tokens with httpOnly cookies for mobile
- **CORS**: Configure for React Native development (localhost + production domains)

### PostgreSQL Schema Design
- **Normalization**: Normalize to 3NF for FoodItem (template) vs PantryItem (instance) separation
- **Indexing**: Index foreign keys, user_id, and date fields for query performance
- **Timestamps**: created_at, updated_at on all tables for auditing
- **Soft deletes**: Consider deleted_at for user data recovery
- **Constraints**: Use CHECK constraints for valid ranges (e.g., quantity >= 0, rating 1-5)

### Testing Strategy
- **Backend**:
  - Unit tests: 80%+ coverage for services layer
  - Integration tests: API contract tests for all endpoints
  - Fixtures: Reusable test data factories (pytest-factory-boy)

- **Mobile**:
  - Component tests: Jest + React Testing Library for UI components
  - Snapshot tests: For UI consistency
  - E2E tests: (Optional) Detox for critical user flows

---

## Technology Stack Summary

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| **Backend** | Python | 3.11+ | Business plan decision, ML ecosystem |
| **Backend Framework** | FastAPI | 0.104+ | High performance, async, OpenAPI docs |
| **Database** | PostgreSQL | 15+ | Relational, reliable, business plan decision |
| **ORM** | SQLAlchemy | 2.0+ | Industry standard, type-safe |
| **Migrations** | Alembic | 1.12+ | SQLAlchemy integration |
| **Mobile** | React Native | 0.72+ | Cross-platform, business plan decision |
| **Mobile Language** | TypeScript | 5.0+ | Type safety, better DX |
| **Mobile Navigation** | React Navigation | 6.x | Industry standard |
| **Mobile UI** | React Native Paper | 5.x | Material Design components |
| **Mobile Storage** | AsyncStorage + expo-sqlite | Latest | Hybrid offline strategy |
| **Charts** | react-native-chart-kit | Latest | Simple, sufficient for MVP |
| **OCR** | PaddleOCR + MediaPipe | Latest | Open-source, zero cost, good accuracy |
| **Image Processing** | OpenCV (cv2) | 4.8+ | Preprocessing, enhancement |
| **LLM** | Google Gemini 2.5 Flash | Latest | FREE tier (1.5k requests/day), structured output |
| **Backend Testing** | pytest | 7.4+ | Python standard |
| **Mobile Testing** | Jest | 29+ | React standard |
| **Cloud** | AWS | N/A | Business plan decision |

---

## Open Questions for Future Phases

These questions are deferred to later features or post-MVP:

1. **Multi-device sync**: How to handle conflicts when user logs meals on multiple devices?
2. **Image storage**: Where to store nutrition label photos long-term? S3? User device only?
3. **LLM fine-tuning**: Should we fine-tune a model on user feedback data for better personalization?
4. **Nutritional database**: When to introduce external food database integration (post-MVP)?
5. **Advanced offline**: Should pantry management also work offline?
6. **Analytics**: What user behavior metrics to track for product improvement?

---

## References

- [React Native Best Practices 2024](https://reactnative.dev/docs/best-practices)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Gemini API Free Tier Limits](https://ai.google.dev/pricing)
- [PaddleOCR Documentation](https://github.com/PaddlePaddle/PaddleOCR)
- [MediaPipe Solutions](https://developers.google.com/mediapipe)
- [OpenCV Python Documentation](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
