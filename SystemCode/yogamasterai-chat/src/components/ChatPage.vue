<template>
  <div class="chat-page">
    <ChatSidebar @clearChat="handleClearChat" @openRegisterForm="showForm = true" />
    <div class="chat-content">
      <ChatWindow ref="chatWindow"/>
      <RegisterForm v-if="showForm" @close="showForm = false" />
    </div>
  </div>
</template>

<script>
import ChatSidebar from './ChatSidebar.vue';
import ChatWindow from './ChatWindow.vue';
import RegisterForm from './RegisterForm.vue';

export default {
  name: 'ChatPage',
  components: {
    ChatSidebar,
    ChatWindow,
    RegisterForm,
  },
  data() {
    return {
      showForm: false,
    };
  },
  methods: {
    handleClearChat() {
      this.$refs.chatWindow.clearMessages(); // Call clearMessages on ChatWindow component
    }
  }
};
</script>

<style scoped>
.chat-page {
  display: flex;
  width: 100%;
  height: 100vh;
  background: linear-gradient(to right, #f0f4f8, #ffffff);
  padding: 10px;
  box-sizing: border-box;
}

.chat-content {
  flex: 1;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-left: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>
