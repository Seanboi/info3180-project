<template>
    <div class="register-form-container">
      <form id="registerForm" @submit.prevent="register" class="register-form">  
      <h1 class="form-title">Register!</h1>
      <p class="subtitle">Join us at Jam Date Today!</p>
      
        <div class="form-group mb-3">
          <label for="fullname" class="form-label">Full Name</label>
          <input type="text" id="fullname" name="name" v-model="name" class="form-control" required />
        </div>
        
        <div class="form-group mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" id="username" name="username" v-model="username" class="form-control" required />
        </div>
        
        <div class="form-group mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" id="password" name="password" v-model="password" class="form-control" required />
        </div>
        
        <div class="form-group mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" id="email" name="email" v-model="email" class="form-control" required />
        </div>
        
        <div class="form-group mb-3">
          <label for="photo" class="form-label">Account Photo</label>
          <input type="file" id="photo" name="photo" @change="onFileChange" class="form-control" required />
        </div>
        
        <button type="submit" class="btn btn-primary">Register</button>
        
        <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>
        <div v-if="errors.length" class="alert alert-danger mt-3">
          <ul>
            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
          </ul>
        </div>
        
        <div v-if="csrfStatus" class="alert alert-info mt-3">
          CSRF Status: {{ csrfStatus }}
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const name = ref('');
  const username = ref('');
  const password = ref('');
  const email = ref('');
  const photo = ref(null);
  const message = ref('');
  const errors = ref([]);
  const csrf_token = ref('');
  const csrfStatus = ref('');
  const router = useRouter();
  
  function getCsrfToken() {
    fetch('/api/v1/csrf-token')
      .then((response) => {
        if (!response.ok) {
          csrfStatus.value = `Error: Server returned ${response.status}`;
          throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('CSRF token received:', data);
        csrf_token.value = data.csrf_token;
        csrfStatus.value = 'CSRF token received successfully';
      })
      .catch(error => {
        console.error('Error fetching CSRF token:', error);
        csrfStatus.value = `Error: ${error.message}`;
      });
  }
  
  onMounted(() => {
    getCsrfToken();
  });
  
  const onFileChange = (event) => {
    photo.value = event.target.files[0];
    
    // Optional: Validate file type
    const allowedTypes = ['image/jpeg', 'image/png'];
    if (photo.value && !allowedTypes.includes(photo.value.type)) {
      errors.value = ['Only JPG and PNG images are allowed'];
      event.target.value = ''; // Reset the file input
      photo.value = null;
    } else {
      // Clear any previous error when a valid file is selected
      errors.value = errors.value.filter(err => !err.includes('images are allowed'));
    }
  };
  
  const register = async () => {
    // Clear previous messages/errors
    message.value = '';
    errors.value = [];
    
    // Form validation
    let isValid = true;
    if (!name.value.trim()) {
      errors.value.push('Full name is required');
      isValid = false;
    }
    
    if (!username.value.trim()) {
      errors.value.push('Username is required');
      isValid = false;
    }
    
    if (!password.value) {
      errors.value.push('Password is required');
      isValid = false;
    }
    
    if (!email.value.trim()) {
      errors.value.push('Email is required');
      isValid = false;
    } else if (!/^\S+@\S+\.\S+$/.test(email.value)) {
      errors.value.push('Please enter a valid email address');
      isValid = false;
    }
    
    if (!photo.value) {
      errors.value.push('Profile photo is required');
      isValid = false;
    }
    
    if (!isValid) return;
    
    // Prepare form data for submission
    let form_data = new FormData();
    form_data.append('name', name.value);
    form_data.append('username', username.value);
    form_data.append('password', password.value);
    form_data.append('email', email.value);
    form_data.append('photo', photo.value);
    
    try {
      message.value = 'Submitting registration...';
      console.log('CSRF Token used:', csrf_token.value);
      
      const response = await fetch('/api/register', {
        method: 'POST',
        body: form_data,
        headers: {
          'X-CSRFToken': csrf_token.value
        }
      });
      
      const data = await response.json();
      console.log('Registration response:', data);
      
      if (response.ok) {
        message.value = data.message || 'Registration successful!';
        errors.value = [];
        
        // Reset form fields after successful registration
        name.value = '';
        username.value = '';
        password.value = '';
        email.value = '';
        photo.value = null;
        
        setTimeout(() => {
        router.push('/login');
      }, 2000);
       } else {
         errors.value = data.errors || [data.message || 'Registration failed. Please try again.'];
      }
    } catch (error) {
      console.error('Error:', error);
      errors.value = ['An error occurred during registration. Please try again later.'];
    }
  };
  </script>
  
  <style scoped>
  .register-form-container {
  background-color: #FFD700;
  border-radius: 12px;
  padding: 2rem 2rem;
  max-width: 500px;
  margin: 3rem auto;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.form-title {
  font-size: 32px;
  font-weight: bold;
  color: #0B6623;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  margin-bottom: 1.5rem;
  color: black;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-label {
  font-size: 14px;
  font-weight: bold;
  color: black;
  margin-bottom: 6px;
  display: block;
}

.form-control {
  width: 100%;
  padding: 10px;
  font-size: 15px;
  border-radius: 6px;
  border: none;
  background-color: white;
  color: black;
}

.btn-primary {
  background-color: #0B6623;
  color: white;
  font-weight: bold;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
}

.btn-primary:hover {
  background-color: #09541c;
}

.alert {
  margin-top: 15px;
  padding: 10px;
  border-radius: 6px;
  font-size: 14px;
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

.alert-info {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}
  </style>