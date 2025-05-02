<template>
    <div class="login-form-container">
      <form id="loginForm" @submit.prevent="login" class="login-form">
        <h2 class="form-title">Login</h2>
        
        <div class="form-group mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" id="username" v-model="username" class="form-control" required />
        </div>
        
        <div class="form-group mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" id="password" v-model="password" class="form-control" required />
        </div>
        
        <button type="submit" class="btn btn-primary">Login</button>
        
        <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>
        <div v-if="errors.length" class="alert alert-danger mt-3">
          <ul>
            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
          </ul>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const username = ref('');
  const password = ref('');
  const message = ref('');
  const errors = ref([]);
  const csrf_token = ref('');
  
  function getCsrfToken() {
    fetch('/api/v1/csrf-token')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
      })
      .catch(error => {
        console.error('Error fetching CSRF token:', error);
      });
  }
  
  onMounted(() => {
    getCsrfToken();
  });
  
  const login = async () => {
    // Clear previous messages/errors
    message.value = '';
    errors.value = [];
    
    // Form validation
    let isValid = true;
    
    if (!username.value.trim()) {
      errors.value.push('Username is required');
      isValid = false;
    }
    
    if (!password.value) {
      errors.value.push('Password is required');
      isValid = false;
    }
    
    if (!isValid) return;
    
    // Prepare form data for submission
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);
    
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': csrf_token.value
        }
      });
      
      const data = await response.json();
      
      if (response.ok) {
        message.value = data.message || 'Login successful!';
        errors.value = [];
        
        // Reset form fields after successful login
        username.value = '';
        password.value = '';
        
        // Optional: Redirect to dashboard or home page after successful login
        if (data.redirect) {
          window.location.href = data.redirect;
        } else {
          // Default redirect if not specified by the server
          window.location.href = '/Users';
        }
      } else {
        errors.value = data.errors || ['Login failed. Please check your credentials and try again.'];
      }
    } catch (error) {
      console.error('Error:', error);
      errors.value = ['An error occurred during login. Please try again later.'];
    }
  };
  </script>
  
  <style scoped>
  .login-form-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .form-title {
    margin-bottom: 20px;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
  }
  
  .form-control {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ced4da;
    border-radius: 4px;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
  }
  
  .btn-primary:hover {
    background-color: #0069d9;
  }
  
  .alert {
    padding: 10px 15px;
    border-radius: 4px;
    margin-top: 15px;
  }
  
  .alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }
  
  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }
  </style>