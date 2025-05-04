<template>
  <div class="form-container">
    <h1 class="form-title">Add New Profile</h1>
    <ProfileForm @submit-success="handleSubmitSuccess" />
  </div>
</template>

<script>
import ProfileForm from '../components/ProfileForm.vue';

export default {
  name: 'AddProfileView',
  components: {
    ProfileForm
  },
  methods: {
    handleSubmitSuccess(profileId) {
      // Handle successful submission, e.g., redirect to profile page
      console.log("Profile Submitted Successfully!");
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.profile-form-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #0B6623; 
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
  color: white;
}

.form-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 1rem;
  font-weight: bold;
  color: #FFD700;
}

.form-label {
  font-weight: 500;
  color: #ffffff;
}

.form-control {
  border: none;
  border-radius: 6px;
  padding: 10px;
}

.form-text {
  font-size: 0.85rem;
  color: #eee;
}

.btn-primary {
  background-color: #FFD700;
  color: #0B6623;
  border: none;
  font-weight: bold;
  padding: 12px;
  border-radius: 6px;
  margin-top: 10px;
}

.btn-primary:hover {
  background-color: #e6c200;
  color: #0B6623;
}

.alert-success,
.alert-danger {
  margin-top: 1rem;
}
</style>