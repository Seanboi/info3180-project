<template>
  <div class="profile-card">
    <p><strong>Description:</strong> {{ profile.description }}</p>
    <p><strong>Parish:</strong> {{ profile.parish }}</p>
    <p><strong>Biography:</strong> {{ profile.biography }}</p>
    <p><strong>Sex:</strong> {{ profile.sex }}</p>
    <p><strong>Race:</strong> {{ profile.race }}</p>
    <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
    <p><strong>Height:</strong> {{ profile.height }} inches</p>
    <p><strong>Favorite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
    <p><strong>Favorite Color:</strong> {{ profile.fav_colour }}</p>
    <p><strong>Favorite School Subject:</strong> {{ profile.fav_school_subject }}</p>
    <p><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
    <p><strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
    <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
  </div>
</template>

<script>
export default {
  name: 'ProfileCard',
  props: {
    profile: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.profile-card {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #3498db;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.profile-card p {
  margin: 10px 0;
}
</style>
