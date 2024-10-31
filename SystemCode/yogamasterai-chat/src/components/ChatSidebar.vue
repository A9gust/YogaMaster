<template>
  <div class="sidebar">
    <div class="logo-container">
      <img class="logo-img" src="@/assets/logo.png" alt="Yoga Master Logo" />
      <h1 class="project-title">Yoga Master AI</h1>
    </div>
    <div class="overlay">
      <div class="profile">
        <img class="profile-pic" src="@/assets/profile.jpeg" alt="User" />
        <h2>{{ yogaUser.username ? yogaUser.username : user.name }}</h2>
        <p>Yoga Level: {{ user.level }}</p>
      </div>
      <ul class="menu">
        <li class="menu-item" @click="startNewChat">New Chat</li>
        <li class="menu-item" @click="showUserInfo">User Info</li>
        <li class="menu-item" @click="showHistory">History</li>
        <li class="menu-item" @click="registerUser">Register VIP</li>
      </ul>
      <div class="auth-buttons">
        <button class="auth-button" @click="login">Login</button>
        <button class="auth-button logout" @click="logout">Logout</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatSidebar",
  data() {
    return {
      user: {
        name: "Li Qiuxian",
        level: "Intermediate",
      },
      yogaUser: {},
    };
  },
  mounted() {
    if (window.sessionStorage.getItem("yogaUser")) {
      this.yogaUser = JSON.parse(window.sessionStorage.getItem("yogaUser"));
    }
  },
  methods: {
    startNewChat() {
      console.log("Start a new chat");
      this.$emit("clearChat"); // Emit clearChat event
    },
    showUserInfo() {
      const userInfo = `User login information:\n\nName: ${this.user.name}\nYoga Level: ${this.user.level}`;
      alert(userInfo);
    },
    showHistory() {
      console.log("Show chat history");
    },
    registerUser() {
      this.$emit('openRegisterForm');
      console.log("Register user");
      const username = this.yogaUser.username || this.user.name;
      // axios.post("http://localhost:8000/api/register", { username: username })
      //   .then(response => {
      //     console.log("Username sent to the backend:", response.data);
      //   })
      //   .catch(error => {
      //     console.error("Error sending username to the backend:", error);
      //   });
    },
    login() {
      console.log("User logged in");
    },
    logout() {
      console.log("User logged out");
      window.sessionStorage.removeItem("yogaUser");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 300px;
  background: url("@/assets/logo3.jpeg") no-repeat center center;
  background-size: cover;
  position: relative;
  border-radius: 10px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Upper content */
  padding-top: 10px; /* Adjust padding  */
}

.logo-container {
  text-align: center;
  padding: 10px 0;
  background: rgba(255, 255, 255, 0.75);
  border-bottom: 1px solid #ddd;
}

.logo-img {
  width: 100px;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
}

.project-title {
  font-size: 18px;
  font-weight: bold;
  margin: 5px 0;
  color: #2c3e50;
}

.small-logout {
  margin-top: 5px;
  background-color: #e57373;
  color: white;
  border: none;
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.overlay {
  background-color: rgba(255, 255, 255, 0.65);
  padding: 10px; /* Adjust overlay padding  */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.profile {
  text-align: center;
  margin-bottom: 10px;
}

.profile-pic {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
  border: 2px solid #ffffff;
}

.menu {
  list-style: none;
  padding: 0;
}

.menu-item {
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.85);
  border-radius: 5px;
  margin-bottom: 5px; /* Minimum menu-item  */
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.menu-item:hover {
  /*background-color: rgba(255, 255, 255, 0.9);*/
  background-color: #a5d6a7;
  color: #fff;
}

.auth-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 10px; /* Reduce margin between buttons */
}

.auth-button {
  background-color: #42a5f5;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  width: 48%;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.auth-button.logout {
  background-color: #e57373;
}

.auth-button:hover {
  background-color: #2196f3;
}

.auth-button.logout:hover {
  background-color: #d32f2f;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
