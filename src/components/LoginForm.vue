<template>
    <div class="login-form-container">
      <form id="loginForm" @submit.prevent="login" class="login-form">
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


        if (data.token) {
          localStorage.setItem('jwt_token', data.token);
        }

      
      if (data.user && data.user.id) {
        localStorage.setItem('user_id', data.user.id);
        }
        
        // Reset form fields after successful login
        username.value = '';
        password.value = '';
        
        // Optional: Redirect to dashboard or home page after successful login
        if (data.redirect) {
          window.location.href = data.redirect;
        } else {
          // Default redirect if not specified by the server
          window.location.href = '/';
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
  max-width: 500px; 
  margin: 0 auto;
  padding: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.form-label {
  color: white;
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
  text-align: left;
  font-size: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: none;
  font-size: 15px;
  background-color: white;
  color: black;
}

.btn-primary {
  background-color: #FFD700;
  color: black;
  font-weight: bold;
  padding: 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
}

.btn-primary:hover {
  background-color: #e6c200;
}

.alert {
  padding: 10px 15px;
  border-radius: 5px;
  margin-top: 15px;
  font-size: 14px;
  width: 100%;
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