<!-- Login.vue -->
<template>
  <div class="login-page">
    <div style="position: fixed; top: 30vh; right: 16vw">
      <h1>YOGA MASTER</h1>
      <div>
        <p style="text-align: left">usrrname:</p>
        <input v-model="username" placeholder="Enter your username" />
      </div>
      <div style="margin-bottom: 20px">
        <p style="text-align: left">password:</p>
        <input v-model="password" placeholder="Enter your password" />
      </div>
      <button @click="login">Login</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      loginImg: require("../assets/login.jpg"),
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      if (this.username.trim() == "") {
        alert("Username is required");
        return false;
      }
      if (!this.password) {
        alert("Password is required");
        return false;
      }
      try {
        const response = await axios.post("http://localhost:8000/api/login", {
          username: this.username,
          password: this.password,
        });
        if (response.data == "success") {
          window.sessionStorage.setItem(
            "yogaUser",
            JSON.stringify({
              username: this.username,
              password: this.password,
            })
          );
          this.$router.push("/ChatPage");
        } else {
          alert(response.data);
        }
      } catch (error) {
        alert(error);
      }
    },
  },
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
}
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: loginImg;
  background-color: #e3f2fd;

  overflow: hidden;
  background: url("../assets/login.jpg") no-repeat center center;
  background-size: cover;
}

input {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 350px;
}

button {
  width: 350px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
