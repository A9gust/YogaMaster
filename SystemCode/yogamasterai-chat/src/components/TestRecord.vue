<template>
  <div>
    <button @mousedown="startSpeech" @mouseout="stopSpeech">
      {{ recognizing ? "停止录音" : "开始录音" }}
    </button>
    <div v-if="recognizing">正在识别中...</div>
    <ul>
      <li v-for="(item, index) in results" :key="index">{{ item }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
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
    startSpeech() {
      this.recognition.start();
      this.recognizing = true;
    },
    stopSpeech() {
      this.recognition.stop();
      this.recognizing = false;
    },
    handleResults(event) {
      alert(2);
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        this.results.push(transcript);
      }
      this.recognizing = false;
    },
  },
};
</script>
