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
      this.$router.push(`/profiles/${profileId}`);
    }
  }
};
</script>

<style scoped>
.form-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}
</style>