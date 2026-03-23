# 🧪 NutriScanAI Test Suite with TestSprite

## Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Tests

**Run all tests once:**
```bash
npm run test:run
```

**Run tests in watch mode (auto-rerun on changes):**
```bash
npm run test:watch
```

**Run tests with UI dashboard:**
```bash
npm run test:ui
```

**Generate coverage report:**
```bash
npm run test:coverage
```

---

## 📋 Test Structure

### Test Files
- `tests/auth-recipe.test.js` - Authentication, authorization, recipe generation, PDF, toast notifications

### Test Categories

#### 1️⃣ Authentication Tests (Tests 1.1-1.9)
- ✅ Modal open/close functionality
- ✅ Input validation (email, password)
- ✅ Signup/Login flows
- ✅ Error handling

#### 2️⃣ Authorization Tests (Tests 2.1-2.7)
- ✅ Chef Pro restrictions
- ✅ Paywall blocking
- ✅ Interface updates based on auth state
- ✅ Header button changes

#### 3️⃣ Recipe Generation Tests (Tests 3.1-3.5)
- ✅ Recipe API calls
- ✅ Meal plan generation
- ✅ Error handling
- ✅ PRO-only features

#### 4️⃣ PDF Export Tests (Tests 4.1-4.2)
- ✅ PDF content validation
- ✅ Empty content handling

#### 5️⃣ Toast Notification Tests (Tests 5.1-5.3)
- ✅ Success toasts
- ✅ Error toasts
- ✅ Warning toasts

---

## 🎯 Test Results Expected

### ✅ All 19 Tests Should Pass:
```
✓ 1.1: Should open login modal
✓ 1.2: Should close login modal
✓ 1.6: Should show warning for empty fields
✓ 1.7: Should reject invalid email
✓ 1.8: Should reject short password
✓ 1.9: Should accept valid credentials
✓ 2.1: Should prevent Chef Pro if not logged in
✓ 2.2: Should show paywall if not PRO
✓ 2.3: Should allow Chef Pro if PRO
✓ 2.4: Should lock features for free user
✓ 2.5: Should unlock features for PRO user
✓ 2.6: Should show "SEJA PRO" when logged out
✓ 2.7: Should show logout button when logged in
✓ 3.1: Should generate recipe with valid API response
✓ 3.2: Should handle missing recipe content
✓ 3.5: Should block meal plan for non-PRO users
✓ 4.1: Should have content for PDF generation
✓ 4.2: Should handle empty content
✓ 5.1: Should create success toast
✓ 5.2: Should create error toast
✓ 5.3: Should create warning toast
```

---

## 🐛 Debugging Tips

If a test fails:

1. **Check the error message** - Shows which assertion failed
2. **Look at the test code** - Find the specific condition being tested
3. **Review the actual code** - Compare with implementation in `templates/index.html`
4. **Use verbose output** - Run with `npm run test:run` to see detailed logs

### Example Output:
```
FAIL  tests/auth-recipe.test.js > 🔐 Authentication Tests > 1.1
AssertionError: expected false to be true
  at test ("tests/auth-recipe.test.js:25:1")
```

---

## 📊 Next Steps

After running tests:

1. ✅ Run `npm run test:run` to verify all tests pass
2. 🔧 Fix any failing tests by updating code in `templates/index.html`
3. 📈 Generate coverage report: `npm run test:coverage`
4. 🚀 Add E2E tests if needed (for full user flows)
5. 🔄 Set up CI/CD testing (GitHub Actions)

---

## 🤖 TestSprite Integration

TestSprite can:
- 🧠 Generate test cases from code analysis
- 🎯 Identify untested code paths
- 📸 Run visual regression tests
- 🌐 Test in real browsers (E2E testing)

To use TestSprite for advanced testing:
```bash
# TestSprite is configured in .vscode/mcp.json
# Copilot will use TestSprite for smarter test generation
```

---

## 📝 Adding More Tests

To add new tests:

1. Create a new describe block:
```javascript
describe('New Feature', () => {
    it('should do something', () => {
        expect(true).toBe(true);
    });
});
```

2. Run tests: `npm run test:watch`
3. Tests auto-run on file save

---

## 🎓 Test Naming Convention

Tests follow this pattern:
- `[Test-Number]`: `[Description]`
- Example: `1.1: Should open login modal`
- Matches test plan in `tests/testplan.md`

---

## 💾 Files Created

```
NutriScanAI/
├── package.json              # Project dependencies
├── vitest.config.js          # Test configuration
├── tests/
│   ├── testplan.md          # Comprehensive test plan
│   └── auth-recipe.test.js  # 19 unit tests
```

---

Ready to run tests! 🚀
