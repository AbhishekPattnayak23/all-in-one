class SecureLogin {
  constructor() {
    this.form = document.getElementById('loginForm');
    this.init();
  }

  init() {
    this.form.addEventListener('submit', this.handleSubmit.bind(this));
    this.addInputValidation();
  }

  addInputValidation() {
    const inputs = this.form.querySelectorAll('input');
    inputs.forEach(input => {
      input.addEventListener('blur', this.validateField.bind(this));
      input.addEventListener('input', this.clearError.bind(this));
    });
  }

  validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    const errorSpan = document.getElementById(`${field.name}-error`);
    
    let error = '';
    
    if (!value) {
      error = `${field.name.charAt(0).toUpperCase() + field.name.slice(1)} is required`;
    } else if (field.name === 'username' && !/^[a-zA-Z0-9_]+$/.test(value)) {
      error = 'Username can only contain letters, numbers, and underscores';
    } else if (field.name === 'password' && value.length < 8) {
      error = 'Password must be at least 8 characters';
    }
    
    errorSpan.textContent = error;
    field.setAttribute('aria-invalid', error ? 'true' : 'false');
    
    return !error;
  }

  clearError(event) {
    const field = event.target;
    const errorSpan = document.getElementById(`${field.name}-error`);
    errorSpan.textContent = '';
    field.setAttribute('aria-invalid', 'false');
  }

  async handleSubmit(event) {
    event.preventDefault();
    
    // Clear previous errors
    const errorSpans = this.form.querySelectorAll('.error');
    errorSpans.forEach(span => span.textContent = '');
    
    // Validate all fields
    const inputs = this.form.querySelectorAll('input');
    let isValid = true;
    
    inputs.forEach(input => {
      if (!this.validateField({ target: input })) {
        isValid = false;
      }
    });
    
    if (!isValid) return;
    
    // Get form data
    const formData = new FormData(this.form);
    const data = Object.fromEntries(formData);
    
    try {
      // Disable submit button during request
      const submitBtn = this.form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify(data)
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        // Redirect on success
        window.location.href = result.redirectUrl;
      } else {
        // Display error
        const errorDiv = document.getElementById('general-error');
        errorDiv.textContent = result.error || 'Login failed';
        submitBtn.disabled = false;
      }
    } catch (error) {
      console.error('Login error:', error);
      const errorDiv = document.getElementById('general-error');
      errorDiv.textContent = 'An error occurred. Please try again.';
      this.form.querySelector('button[type="submit"]').disabled = false;
    }
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => new SecureLogin());
