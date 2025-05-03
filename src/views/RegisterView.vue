<template>
    <div class="Register-container">
      <RegisterForm />
    </div>
  </template>
  
  <script setup>
import RegisterForm from '../components/RegisterForm.vue';
  </script>
  
  <style scoped>
  .Register-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
  }
  
  .form-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 28px;
    color: #333;
  }
  </style>