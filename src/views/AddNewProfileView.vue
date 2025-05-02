<template>
    <div class="form-container">
      <h1 class="form-title">Add New Profile</h1>
      <form @submit.prevent="submit" class="form"> 
        <input v-model="profile.description" placeholder="Description" class="input" required/>
        <input v-model="profile.parish" placeholder="Parish" class="input" required/>
        <textarea v-model="profile.biography" placeholder="Biography" class="input" required></textarea>
        <input v-model="profile.sex" placeholder="Sex" class="input" required/>
        <input v-model="profile.race" placeholder="Race" class="input" required/>
        <input v-model.number="profile.birth_year" placeholder="Birth Year" class="input" required/>
        <input v-model.number="profile.height" placeholder="Height (inches)" class="input" required/>
        <input v-model="profile.fav_cuisine" placeholder="Favourite Cuisine" class="input"/>
        <input v-model="profile.fav_colour" placeholder="Favourite Colour" class="input"/>
        <input v-model="profile.fav_school_subject" placeholder="Favourite Subject" class="input"/>
        <label><input type="checkbox" v-model="profile.political"/>Political</label>
        <label><input type="checkbox" v-model="profile.religious"/>Religious</label>
        <label><input type="checkbox" v-model="profile.family_oriented"/>Family Oriented</label>
        <button class="button">Add New Profile</button>
      </form>
        
    </div>
</template>

<script>
import axios from 'axios';
export default {
  data(){
    return{
      profile: {
        description: '', parish: '', biography: '', sex: '', race: '', birth_year: '', height: '',
        fav_cuisine: '', fav_colour: '', fav_school_subject: '', political: false, religious: false, family_oriented: false
      },
      error: ''
    };
  },
  methods: {
    async submit() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.post('/api/profiles', this.profile, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.$router.push(`/profiles/${res.data.profile.id}`);
      } catch (err) {
        this.error = err.response.data.message || 'Error submitting profile';
      }
    }
  }
};
</script>
 
  
  <style>
  
  </style>