<template>
  <div class="chat-window">
    <h2>Chat Window</h2>
    <div class="messages">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'message',
          message.type === 'sent' ? 'user-message' : 'ai-message',
        ]"
      >
        <div class="message-bubble" v-if="!message.photo">
          {{ message.text }}
        </div>
        <img
          v-if="message.photo"
          :src="message.photo"
          alt="Captured photo"
          class="captured-photo"
        />
      </div>
    </div>
    <video ref="video" v-if="isCameraOn" autoplay class="camera-view"></video>
    <MessageInput
      @sendMessage="sendMessage"
      @openCamera="handleOpenCamera"
      @closeCamera="handleCloseCamera"
      @capturePhoto="handleCapturePhoto"
    />
  </div>
</template>

<script>
import axios from 'axios';
import MessageInput from './MessageInput.vue';

axios.defaults.baseURL = 'http://localhost:8000';

export default {
  name: 'ChatWindow',
  components: {
    MessageInput,
  },
  data() {
    return {
      messages: [
        { id: 1, text: "Hello! How can I assist you today?", type: "received" },
        {
          id: 2,
          text: "I need a yoga recommendation for relaxation.",
          type: "sent",
        },
      ],
      isCameraOn: false,
      videoStream: null,
    };
  },
  methods: {
    clearMessages() {
      this.messages = [
        { id: 1, text: "Hello! How can I assist you today?", type: "received" },
        // {
        //   id: 2,
        //   text: "I need a yoga recommendation for relaxation.",
        //   type: "sent",
        // },
      ]; // Clear chat messages
    },
    async sendMessage(text) {
  console.log("sendMessage function called with:", text);  // Record

  if (!text || text.trim() === '' || text.startsWith('System:')) {
    console.log("Invalid message detected, skipping.");
    return;
  }

  this.messages.push({ id: Date.now(), text, type: 'sent' });

  try {
    const response = await axios.post('http://localhost:8000/api/chat', { message: text });
    const { reply, recommended_pose } = response.data || {};

    if (reply) {
      console.log("Received reply from backend:", reply);
      this.messages.push({ id: Date.now(), text: reply, type: 'received' });
    }

    if (recommended_pose && recommended_pose.image_path) {
      const fullImagePath = `http://localhost:8000${recommended_pose.image_path}`;
      //const fullImagePath = `http://localhost:8000/static/images/Chair_Pose.jpg`;
      console.log("Received pose recommendation:", recommended_pose);
      this.messages.push({
        id: Date.now(),
        text: `Recommended Pose: ${recommended_pose.name}`,
        type: 'received',
        photo: fullImagePath
      });
    }
  } catch (error) {
    console.error('Error sending message:', error);
    this.messages.push({ id: Date.now(), text: 'Sorry, I couldn\'t process your message.', type: 'received' });

    return;
  }
},

handleOpenCamera() {
      this.isCameraOn = true;
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          this.videoStream = stream;
          this.$refs.video.srcObject = stream;
        })
        .catch((error) => {
          console.error("Error accessing camera:", error);
          this.isCameraOn = false;
          alert("Unable to access the camera. Please check your permissions.");
        });
    },
    handleCloseCamera() {
      this.isCameraOn = false;
      if (this.videoStream) {
        this.videoStream.getTracks().forEach((track) => track.stop());
        this.videoStream = null;
        this.$refs.video.srcObject = null;
      }
    },
    async handleCapturePhoto() {
      if (this.$refs.video) {
        const canvas = document.createElement("canvas");
        canvas.width = this.$refs.video.videoWidth;
        canvas.height = this.$refs.video.videoHeight;
        const context = canvas.getContext("2d");
        context.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);

        // Convert to blob objec
        canvas.toBlob(async (blob) => {
          const formData = new FormData();
          formData.append("photo", blob, "photo.png"); // Add blob to dataframe

          // View photos
          this.messages.push({
            id: Date.now(),
            text: "Photo captured",
            type: "sent",
            photo: URL.createObjectURL(blob), 
          });

          // Auto reply message
          this.messages.push({
            id: Date.now(),
            text: "Receive Your Photo, Feedback is generating....",
            type: "received",
          });

          try {
            // Axios to send dataframe
            const response = await axios.post(
              "http://localhost:8000/api/upload",
              formData,
              {
                headers: {
                  "Content-Type": "multipart/form-data", // Set request
                },
              }
            );

            // Process feedback
            const { reply } = response.data;
            this.messages.push({
              id: Date.now(),
              text: reply,
              type: "received",
            });
          } catch (error) {
            console.error("Error uploading photo:", error);

            // Upload failed
            this.messages.push({
              id: Date.now(),
              text: "抱歉，无法处理这张照片。",
              type: "received",
            });
          } finally {
            // Close camera
            this.handleCloseCamera();
          }
        });
      } else {
        console.error("No video element found for capturing photo.");
      }
    },
  },
};
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  background: url("../assets/logo2.jpg") no-repeat center center; /* Add background */
  background-size: cover;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  z-index: 1;
}

.message {
  margin-bottom: 10px;
  display: flex;
}

.user-message {
  justify-content: flex-end;
}

.ai-message {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 60%;
  padding: 10px;
  border-radius: 15px;
  position: relative;
  z-index: 1;
  background-color: #e3f2fd;
}

.user-message .message-bubble {
  background-color: #a5d6a7;
  color: #ffffff;
  border-bottom-right-radius: 0;
}

.ai-message .message-bubble {
  background-color: #90caf9;
  color: #ffffff;
  border-bottom-left-radius: 0;
}

.captured-photo {
  max-width: 200px;
  border-radius: 10px;
  margin-top: 10px;
}

.camera-view {
  width: 100%;
  max-height: 500px;
  margin-top: 10px;
  border-radius: 10px;
}
</style>
