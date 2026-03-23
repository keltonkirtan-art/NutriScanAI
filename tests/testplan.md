# 🧪 NutriScanAI Test Plan - Critical Path

## Test Suite Overview
- **Project**: NutriScanAI PWA (Recipe + Meal Planning)
- **Framework**: TestSprite (AI-powered)
- **Focus**: Authentication & Recipe Generation (Critical Path)
- **Scope**: Unit tests for core functions

---

## 1️⃣ AUTHENTICATION TESTS

### Test 1.1: Modal Login Opens Correctly
```
Function: abrirModalLogin()
Expected: #modal-login element class 'hidden' is removed
Test: Check if modal-login is visible after function call
```

### Test 1.2: Modal Login Closes Correctly  
```
Function: fecharModalLogin()
Expected: #modal-login element class 'hidden' is added
Test: Check if modal-login is hidden after function call
```

### Test 1.3: Session Verification - Logged In User
```
Function: verificarSessao()
Expected: usuarioLogado is set to session.user
Expected: atualizarInterface() is called
Condition: Session exists in Supabase
```

### Test 1.4: Session Verification - No Session
```
Function: verificarSessao()
Expected: usuarioLogado = null
Expected: window.usuarioIsPro = false
Expected: atualizarInterface() is called
Condition: No active session
```

### Test 1.5: Logout Flow
```
Function: fazerLogout()
Expected: User is signed out from Supabase
Expected: usuarioLogado = null
Expected: page reloads for PWA cleanup
Expected: Modal closes
```

### Test 1.6: Login Input Validation - Empty Fields
```
Function: fazerLogin()
Expected: Toast warning "📧 Digite e-mail e senha!"
Condition: Email or password empty
```

### Test 1.7: Login Input Validation - Invalid Email
```
Function: fazerLogin()
Expected: Toast warning "📧 E-mail inválido!"
Condition: Email without @ or .
```

### Test 1.8: Login Input Validation - Short Password
```
Function: fazerLogin()
Expected: Toast warning "🔐 Senha deve ter 6+ caracteres"
Condition: Password < 6 characters
```

### Test 1.9: Signup Input Validation - Valid
```
Function: fazerCadastro()
Expected: Toast success "✅ Conta criada! Faça login agora."
Condition: Valid email + password (6+ chars)
```

---

## 2️⃣ AUTHORIZATION & PAYWALL TESTS

### Test 2.1: Chef Pro Guard - Not Logged In
```
Function: verificarChefPro(event)
Expected: event.preventDefault() called
Expected: Modal login opens (abrirModalLogin())
Expected: radio-rapido remains checked
Condition: usuarioLogado = null
```

### Test 2.2: Chef Pro Guard - Logged In But Not PRO
```
Function: verificarChefPro(event)
Expected: event.preventDefault() called
Expected: Paywall modal opens (abrirModalPaywall())
Expected: radio-rapido remains checked
Condition: usuarioLogado exists, window.usuarioIsPro = false
```

### Test 2.3: Chef Pro Guard - PRO User
```
Function: verificarChefPro(event)
Expected: event.preventDefault() NOT called
Expected: No modals open
Expected: radio-elaborado can be selected
Condition: window.usuarioIsPro = true
```

### Test 2.4: Interface Update - Free User
```
Function: atualizarInterface()
Expected: paywall-overlay visible
Expected: painel-clinico has opacity-30, pointer-events-none
Expected: btn-semanal disabled (gray)
Condition: window.usuarioIsPro = false
```

### Test 2.5: Interface Update - PRO User
```
Function: atualizarInterface()
Expected: paywall-overlay hidden
Expected: painel-clinico normal (no opacity/pointer-events)
Expected: btn-semanal enabled (red)
Condition: window.usuarioIsPro = true
```

### Test 2.6: Interface Update - Header Button (Logged Out)
```
Function: atualizarInterface()
Expected: btn-login-header text = "SEJA PRO"
Expected: onclick = "abrirModalLogin()"
Condition: usuarioLogado = null
```

### Test 2.7: Interface Update - Header Button (Logged In)
```
Function: atualizarInterface()
Expected: btn-login-header text includes "SAIR"
Expected: onclick = "fazerLogout()"
Condition: usuarioLogado exists
```

---

## 3️⃣ RECIPE GENERATION TESTS

### Test 3.1: Recipe Generation - Valid Input
```
Function: gerarReceita()
Expected: #conteudo-receita contains recipe HTML
Expected: Toast success "✅ Receita gerada!"
Condition: All required fields filled
```

### Test 3.2: Recipe Generation - Missing Fields
```
Function: gerarReceita()
Expected: Toast warning about missing field
Expected: No API call made
Condition: Any required field is empty
```

### Test 3.3: Recipe Generation - API Error
```
Function: gerarReceita()
Expected: Toast error "❌ Erro ao gerar receita"
Expected: Button re-enabled
Condition: API returns error
```

### Test 3.4: Meal Plan Generation - Valid Input
```
Function: gerarPlanoSemanal()
Expected: #conteudo-receita contains 7-day meal plan
Expected: Toast success "✅ Plano semanal pronto!"
Condition: All fields valid, user is PRO
```

### Test 3.5: Meal Plan Generation - Non-PRO User
```
Function: gerarPlanoSemanal()
Expected: Paywall modal opens
Expected: No API call made
Condition: window.usuarioIsPro = false
```

---

## 4️⃣ PDF Export TESTS

### Test 4.1: PDF Generation - Valid Content
```
Function: baixarPDF()
Expected: Toast success "✅ PDF gerado com sucesso!"
Expected: PDF file downloaded
Condition: #conteudo-receita has content
```

### Test 4.2: PDF Generation - Missing Content
```
Function: baixarPDF()
Expected: Toast error "❌ Erro ao gerar PDF"
Expected: Button re-enabled
Condition: #conteudo-receita is empty
```

---

## 5️⃣ TOAST NOTIFICATION TESTS

### Test 5.1: Toast Display - Success
```
Function: mostrarToast("Test message", "sucesso")
Expected: Toast appears with green styling
Expected: Auto-hides after 3000ms
```

### Test 5.2: Toast Display - Error
```
Function: mostrarToast("Error", "erro")
Expected: Toast appears with red styling
Expected: Auto-hides after 3000ms
```

### Test 5.3: Toast Display - Warning
```
Function: mostrarToast("Warning", "aviso")
Expected: Toast appears with yellow styling
Expected: Animation slideInRight plays
```

---

## 📊 Test Execution Summary

**Total Tests**: 27 test cases
**Critical Tests**: 15 (Auth + Recipe Gen)
**Priority Order**:
1. Authentication Tests (1.1-1.9) ✅
2. Authorization Tests (2.1-2.7) ✅
3. Recipe Generation (3.1-3.5) ✅
4. PDF Export (4.1-4.2) ⚠️
5. Toast Notifications (5.1-5.3) ⚠️

---

## 🚀 Next Steps
1. Run TestSprite to generate test code
2. Validate all critical path tests pass
3. Fix any failing tests
4. Add frontend E2E tests
5. Test Supabase integration
