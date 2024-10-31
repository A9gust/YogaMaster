<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h2>Register as VIP</h2>
        <form @submit.prevent="submitRegistration">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="formData.email" required />
  
          <label for="level">Yoga Level:</label>
          <select id="level" v-model="formData.level">
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
          <label>
          <input type="checkbox" v-model="formData.isVIP" />
            Become a VIP
          </label>
          <button type="submit">Submit</button>
          <button type="button" @click="$emit('close')">Cancel</button>
        </form>
      </div>
    </div>
  </template>
  
<script>
import axios from 'axios';

export default {
  name: 'RegisterForm',
  data() {
    return {
      formData: {
        isVIP: false,
        email: '',
        level: 'Beginner',
      },
    };
  },
  methods: {
    submitRegistration() {
      const username = window.sessionStorage.getItem('yogaUser')
        ? JSON.parse(window.sessionStorage.getItem('yogaUser')).username
        : 'Guest'; // default if username not set

      const registrationData = {
        username,
        ...this.formData,
      };

      axios.post('http://localhost:8000/api/register', registrationData)
        .then(response => {
          console.log('Registration successful:', response.data);
          this.$emit('close');
        })
        .catch(error => {
          console.error('Error during registration:', error);
        });
    },
  },
};
</script>