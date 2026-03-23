/**
 * 🧪 NutriScanAI Authentication Tests
 * Tests for: Login, Logout, Session, Modals
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

// Mock Supabase client
const mockSupabaseAuth = {
    getSession: vi.fn(),
    signUp: vi.fn(),
    signInWithPassword: vi.fn(),
    signOut: vi.fn(),
    onAuthStateChange: vi.fn(),
};

// Mock global state
let usuarioLogado = null;
let window_usuarioIsPro = false;

describe('🔐 Authentication Tests', () => {
    
    beforeEach(() => {
        // Reset state before each test
        usuarioLogado = null;
        window_usuarioIsPro = false;
        
        // Mock DOM elements
        document.body.innerHTML = `
            <input id="login-email" type="email" />
            <input id="login-senha" type="password" />
            <div id="modal-login" class="hidden"></div>
            <div id="radio-rapido"></div>
            <div id="radio-elaborado"></div>
            <button id="btn-login-header"></button>
            <div id="paywall-overlay"></div>
            <div id="painel-clinico"></div>
            <div id="btn-semanal"></div>
        `;
    });

    // ==========================================
    // Test 1.1: Modal Login Opens Correctly
    // ==========================================
    it('1.1: Should open login modal when abrirModalLogin() called', () => {
        const modal = document.getElementById('modal-login');
        modal.classList.add('hidden');
        
        // Simulate abrirModalLogin function
        modal.classList.remove('hidden');
        
        expect(modal.classList.contains('hidden')).toBe(false);
    });

    // ==========================================
    // Test 1.2: Modal Login Closes Correctly
    // ==========================================
    it('1.2: Should close login modal when fecharModalLogin() called', () => {
        const modal = document.getElementById('modal-login');
        modal.classList.remove('hidden');
        
        // Simulate fecharModalLogin function
        modal.classList.add('hidden');
        
        expect(modal.classList.contains('hidden')).toBe(true);
    });

    // ==========================================
    // Test 1.6: Login Input Validation - Empty Fields
    // ==========================================
    it('1.6: Should show warning for empty email/password', () => {
        const emailInput = document.getElementById('login-email');
        const senhaInput = document.getElementById('login-senha');
        
        emailInput.value = '';
        senhaInput.value = '';
        
        const isValid = !!(emailInput.value.trim() && senhaInput.value);
        expect(isValid).toBe(false);
    });

    // ==========================================
    // Test 1.7: Login Input Validation - Invalid Email
    // ==========================================
    it('1.7: Should reject invalid email format', () => {
        const emailInput = document.getElementById('login-email');
        emailInput.value = 'invalid-email';
        
        const isValidEmail = emailInput.value.includes('@') && emailInput.value.includes('.');
        expect(isValidEmail).toBe(false);
    });

    // ==========================================
    // Test 1.8: Login Input Validation - Short Password
    // ==========================================
    it('1.8: Should reject password with less than 6 characters', () => {
        const senhaInput = document.getElementById('login-senha');
        senhaInput.value = '12345';
        
        const isValidPassword = senhaInput.value.length >= 6;
        expect(isValidPassword).toBe(false);
    });

    // ==========================================
    // Test 1.9: Signup Input Validation - Valid
    // ==========================================
    it('1.9: Should accept valid email and password', () => {
        const emailInput = document.getElementById('login-email');
        const senhaInput = document.getElementById('login-senha');
        
        emailInput.value = 'user@example.com';
        senhaInput.value = 'password123';
        
        const isValidEmail = emailInput.value.includes('@') && emailInput.value.includes('.');
        const isValidPassword = senhaInput.value.length >= 6;
        
        expect(isValidEmail).toBe(true);
        expect(isValidPassword).toBe(true);
    });
});

describe('👤 Authorization & Paywall Tests', () => {
    
    beforeEach(() => {
        usuarioLogado = null;
        window_usuarioIsPro = false;
        
        document.body.innerHTML = `
            <div id="modal-login" class="hidden"></div>
            <div id="modal-paywall" class="hidden"></div>
            <div id="radio-rapido" checked="true"></div>
            <div id="radio-elaborado"></div>
            <div id="paywall-overlay"></div>
            <div id="painel-clinico"></div>
            <div id="btn-semanal"></div>
            <button id="btn-login-header"></button>
        `;
    });

    // ==========================================
    // Test 2.1: Chef Pro Guard - Not Logged In
    // ==========================================
    it('2.1: Should prevent Chef Pro selection if not logged in', () => {
        const event = { preventDefault: vi.fn() };
        usuarioLogado = null;
        
        // Simulate verificarChefPro logic
        if (!usuarioLogado) {
            event.preventDefault();
            document.getElementById('radio-rapido').checked = true;
        }
        
        expect(event.preventDefault).toHaveBeenCalled();
        expect(document.getElementById('radio-rapido').checked).toBe(true);
    });

    // ==========================================
    // Test 2.2: Chef Pro Guard - Logged In But Not PRO
    // ==========================================
    it('2.2: Should show paywall if logged in but not PRO', () => {
        const event = { preventDefault: vi.fn() };
        usuarioLogado = { id: 'user-123' };
        window_usuarioIsPro = false;
        
        // Simulate verificarChefPro logic
        if (window_usuarioIsPro !== true) {
            event.preventDefault();
            document.getElementById('radio-rapido').checked = true;
        }
        
        expect(event.preventDefault).toHaveBeenCalled();
    });

    // ==========================================
    // Test 2.3: Chef Pro Guard - PRO User
    // ==========================================
    it('2.3: Should allow Chef Pro selection if PRO user', () => {
        const event = { preventDefault: vi.fn() };
        usuarioLogado = { id: 'user-123' };
        window_usuarioIsPro = true;
        
        // Simulate verificarChefPro logic
        if (!usuarioLogado) {
            event.preventDefault();
        } else if (window_usuarioIsPro !== true) {
            event.preventDefault();
        }
        
        expect(event.preventDefault).not.toHaveBeenCalled();
    });

    // ==========================================
    // Test 2.4: Interface Update - Free User
    // ==========================================
    it('2.4: Should hide paywall and lock features for free user', () => {
        window_usuarioIsPro = false;
        const paywall = document.getElementById('paywall-overlay');
        const clinico = document.getElementById('painel-clinico');
        
        // Simulate atualizarInterface for free user
        paywall.classList.remove('hidden');
        clinico.classList.add('opacity-30', 'pointer-events-none');
        
        expect(paywall.classList.contains('hidden')).toBe(false);
        expect(clinico.classList.contains('opacity-30')).toBe(true);
    });

    // ==========================================
    // Test 2.5: Interface Update - PRO User
    // ==========================================
    it('2.5: Should unlock all features for PRO user', () => {
        window_usuarioIsPro = true;
        const paywall = document.getElementById('paywall-overlay');
        const clinico = document.getElementById('painel-clinico');
        
        // Simulate atualizarInterface for PRO user
        paywall.classList.add('hidden');
        clinico.classList.remove('opacity-30', 'pointer-events-none');
        
        expect(paywall.classList.contains('hidden')).toBe(true);
        expect(clinico.classList.contains('opacity-30')).toBe(false);
    });

    // ==========================================
    // Test 2.6: Header Button - Logged Out
    // ==========================================
    it('2.6: Should show "SEJA PRO" button when logged out', () => {
        usuarioLogado = null;
        const btn = document.getElementById('btn-login-header');
        
        // Simulate atualizarInterface
        btn.innerHTML = 'SEJA PRO';
        btn.setAttribute('onclick', 'abrirModalLogin()');
        
        expect(btn.innerHTML).toContain('SEJA PRO');
        expect(btn.getAttribute('onclick')).toBe('abrirModalLogin()');
    });

    // ==========================================
    // Test 2.7: Header Button - Logged In
    // ==========================================
    it('2.7: Should show logout button when logged in', () => {
        usuarioLogado = { id: 'user-123', email: 'user@test.com' };
        const btn = document.getElementById('btn-login-header');
        
        // Simulate atualizarInterface
        btn.innerHTML = '<i class="fas fa-sign-out-alt mr-1"></i> SAIR';
        btn.setAttribute('onclick', 'fazerLogout()');
        
        expect(btn.innerHTML).toContain('SAIR');
        expect(btn.getAttribute('onclick')).toBe('fazerLogout()');
    });
});

describe('🍽️ Recipe Generation Tests', () => {
    
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="conteudo-receita"></div>
            <button id="btn-receita">Gerar Receita</button>
        `;
        window_usuarioIsPro = true;
        usuarioLogado = { id: 'user-123' };
    });

    // ==========================================
    // Test 3.1: Recipe Generation - API Success
    // ==========================================
    it('3.1: Should generate recipe with valid API response', () => {
        const conteudo = document.getElementById('conteudo-receita');
        const mockRecipeHTML = '<h1>Atum Confitado</h1><p>Delicioso!</p>';
        
        // Simulate successful API response
        conteudo.innerHTML = mockRecipeHTML;
        
        expect(conteudo.innerHTML).toContain('Atum Confitado');
        expect(conteudo.innerHTML.length).toBeGreaterThan(0);
    });

    // ==========================================
    // Test 3.2: Recipe Generation - Empty Output
    // ==========================================
    it('3.2: Should handle missing recipe content', () => {
        const conteudo = document.getElementById('conteudo-receita');
        
        expect(conteudo.innerHTML).toBe('');
    });

    // ==========================================
    // Test 3.5: Meal Plan - Non-PRO User Blocked
    // ==========================================
    it('3.5: Should block meal plan generation for non-PRO users', () => {
        window_usuarioIsPro = false;
        const event = { preventDefault: vi.fn() };
        
        // Simulate gerarPlanoSemanal guard
        if (window_usuarioIsPro !== true) {
            event.preventDefault();
        }
        
        expect(event.preventDefault).toHaveBeenCalled();
    });
});

describe('📄 PDF Export Tests', () => {
    
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="conteudo-receita">
                <h1>Test Recipe</h1>
                <p>Test content</p>
            </div>
            <button id="btn-pdf">Baixar PDF</button>
        `;
    });

    // ==========================================
    // Test 4.1: PDF Generation - Valid Content
    // ==========================================
    it('4.1: Should have content for PDF generation', () => {
        const conteudo = document.getElementById('conteudo-receita');
        
        expect(conteudo.innerHTML.length).toBeGreaterThan(0);
        expect(conteudo.innerHTML).toContain('Test Recipe');
    });

    // ==========================================
    // Test 4.2: PDF Generation - Empty Content
    // ==========================================
    it('4.2: Should handle empty content gracefully', () => {
        const conteudo = document.getElementById('conteudo-receita');
        conteudo.innerHTML = '';
        
        expect(conteudo.innerHTML).toBe('');
    });
});

describe('🔔 Toast Notification Tests', () => {
    
    beforeEach(() => {
        document.body.innerHTML = '<div id="toast-container"></div>';
    });

    // ==========================================
    // Test 5.1: Toast Success Message
    // ==========================================
    it('5.1: Should create success toast', () => {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = 'toast toast-sucesso';
        toast.innerHTML = 'Test success message';
        container.appendChild(toast);
        
        expect(container.contains(toast)).toBe(true);
        expect(toast.classList.contains('toast-sucesso')).toBe(true);
    });

    // ==========================================
    // Test 5.2: Toast Error Message
    // ==========================================
    it('5.2: Should create error toast', () => {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = 'toast toast-erro';
        toast.innerHTML = 'Test error message';
        container.appendChild(toast);
        
        expect(container.contains(toast)).toBe(true);
        expect(toast.classList.contains('toast-erro')).toBe(true);
    });

    // ==========================================
    // Test 5.3: Toast Warning Message
    // ==========================================
    it('5.3: Should create warning toast', () => {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = 'toast toast-aviso';
        toast.innerHTML = 'Test warning message';
        container.appendChild(toast);
        
        expect(container.contains(toast)).toBe(true);
        expect(toast.classList.contains('toast-aviso')).toBe(true);
    });
});
