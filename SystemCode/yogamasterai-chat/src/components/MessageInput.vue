<template>
  <div class="input-container">
    <input
      type="text"
      v-model="message"
      placeholder="Type your message..."
      @keydown.enter="send"
    />

    <button @click="send">Send</button>
    <button @click="toggleCamera" class="camera-button">
      <i class="camera-icon"></i>
    </button>
    <button
      v-if="isCameraOn && !isCounting"
      @click="startCountdown"
      class="capture-button"
    >
      Capture in 10s
    </button>
    <button
      v-if="isCameraOn"
      @click="closeCamera"
      class="close-camera"
      style="margin-right: 10px"
    >
      Close Camera
    </button>
    <div v-if="isCounting" class="countdown-display">
      {{ countdown }} seconds remaining
    </div>
    <div
      @click="handleVoice"
      style="border-radius: 10px; margin-right: 10px; width: 54px"
    >
      <!-- {{ recognizing ? "close voice" : "send voice" }} -->
      <img class="voice-icon1" v-if="!recognizing" src="../assets/s2.png" />
      <img class="voice-icon2" v-else src="../assets/s1.png" />
    </div>
  </div>
</template>

<script>
export default {
  name: "MessageInput",
  data() {
    return {
      message: "",
      isCameraOn: false,
      isCounting: false,
      countdown: 10, // Countdown 10S
      recognizing: false,
      recognition: null,
      results: [],
    };
  },
  created() {
    this.recognition = new webkitSpeechRecognition() || new SpeechRecognition(); 
    this.recognition.continuous = true;
    this.recognition.onresult = this.handleResults;
  },
  methods: {
    send() {
      if (this.message.trim()) {
        this.$emit("sendMessage", this.message);
        this.message = "";
      }
    },
    handleVoice() {
      this.recognizing = !this.recognizing;
      if (this.recognizing) {
        try {
          this.recognition.start();
        } catch (error) {}
      } else {
        this.recognition.stop();
      }
    },

    handleResults(event) {
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        this.results.push(transcript);
      }
      if (this.results) {
        let res = "";
        for (const element of this.results) {
          res += element;
        }
        this.$emit("sendMessage", res);
        this.results = [];
      }
      this.recognizing = false;
    },
    toggleCamera() {
      this.isCameraOn = !this.isCameraOn;
      this.isCameraOn ? this.$emit("openCamera") : this.$emit("closeCamera");
    },
    startCountdown() {
      this.isCounting = true;
      this.countdown = 10; // Reset Countdown

      const countdownInterval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(countdownInterval);
          this.isCounting = false;
          this.$emit("capturePhoto");
        }
      }, 1000); 
    },
    closeCamera() {
      this.isCameraOn = false;
      this.isCounting = false;
      this.$emit("closeCamera");
    },
  },
};
</script>

<style scoped>
.input-container {
  position: relative;
  z-index: 10;
  display: flex;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 5px;
}

input {
  flex: 1;
  border: none;
  outline: none;
  padding: 10px;
  border-radius: 5px;
}

button {
  margin-left: 10px;
  background-color: #42a5f5;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
}

button:hover {
  background-color: #1e88e5;
}

.camera-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}
.voice-icon1 {
  display: inline-block;
  width: 100%;
  background-size: 100%;
  background-repeat: no-repeat;
}
.voice-icon2 {
  display: inline-block;
  width: 100%;
  background-repeat: no-repeat;
  background-size: 100%;
}
.voice-icon2:hover,
.voice-icon1:hover {
  border-radius: 5px;
  background-color: #a5d6a7;
}
.camera-icon {
  display: inline-block;
  background-image: url("../assets/camera-icon.png");
  width: 50px; /* Enlarge */
  height: 50px; /* Enlarge */
  background-size: cover;
}

.close-camera {
  background-color: #e57373;
  margin-left: 10px;
  padding: 10px;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

.close-camera:hover {
  background-color: #d32f2f;
}

.countdown-display {
  margin-left: 20px;
  font-size: 18px;
  color: red;
}
</style>
