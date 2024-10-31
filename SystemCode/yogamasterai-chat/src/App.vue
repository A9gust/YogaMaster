<template>
  <div id="app">
    <!-- <LoginIndex /> -->
    <router-view></router-view>
  </div>
</template>

<script>
import ChatPage from "./components/ChatPage.vue";
import TestRecord from "./components/TestRecord.vue";
import LoginIndex from "./components/LoginIndex.vue";

export default {
  name: "App",
  components: {
    ChatPage,
    TestRecord,
    LoginIndex,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background: #f0f4f8;
  height: 100vh;
  margin: 0;
  padding: 0;
}
body {
  margin: 0;
  padding: 0;
}
</style>
