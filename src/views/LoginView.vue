<template>
    <div class="Login-container">
      <h1 class="form-title">Login!</h1>
      <LoginForm />
    </div>
  </template>
  
  <script setup>
  import LoginForm from '../components/LoginForm.vue';
  </script>
  
  <style scoped>
  .Login-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .form-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 28px;
    color: #333;
  }
  </style>