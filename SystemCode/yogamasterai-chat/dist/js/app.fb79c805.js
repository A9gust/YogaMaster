(function(){"use strict";var e={2976:function(e,t,n){var a=n(5130),s=n(6768);const o={id:"app"};function r(e,t,n,a,r,i){const c=(0,s.g2)("ChatInterface");return(0,s.uX)(),(0,s.CE)("div",o,[(0,s.bF)(c)])}var i=n(4232),c="data:image/png;base64,";const u={class:"chat-container"},d={class:"chat-box"},l={key:0,class:"message-text"},p=["src"],h={class:"input-container"};function g(e,t,n,o,r,g){return(0,s.uX)(),(0,s.CE)("div",u,[t[6]||(t[6]=(0,s.Lk)("img",{src:c,alt:"Yoga Master Logo",class:"logo"},null,-1)),t[7]||(t[7]=(0,s.Lk)("h2",{class:"chat-header"},"YOGA MASTER",-1)),(0,s.Lk)("div",d,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(r.messages,(e=>((0,s.uX)(),(0,s.CE)("div",{key:e.id,class:(0,i.C4)(["message",e.sender])},[e.image?(0,s.Q3)("",!0):((0,s.uX)(),(0,s.CE)("p",l,(0,i.v_)(e.text),1)),e.image?((0,s.uX)(),(0,s.CE)("img",{key:1,src:e.image,alt:"User uploaded image",class:"uploaded-image"},null,8,p)):(0,s.Q3)("",!0)],2)))),128))]),(0,s.Lk)("div",h,[(0,s.bo)((0,s.Lk)("input",{"onUpdate:modelValue":t[0]||(t[0]=e=>r.userInput=e),onKeyup:t[1]||(t[1]=(0,a.jR)(((...e)=>g.sendMessage&&g.sendMessage(...e)),["enter"])),placeholder:"Send a message",class:"chat-input"},null,544),[[a.Jo,r.userInput]]),(0,s.Lk)("button",{onClick:t[2]||(t[2]=(...e)=>g.sendMessage&&g.sendMessage(...e)),class:"send-button"},t[5]||(t[5]=[(0,s.Lk)("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor",width:"18",height:"18"},[(0,s.Lk)("path",{d:"M2 21l21-9L2 3v7l15 2-15 2z"})],-1)])),(0,s.Lk)("input",{type:"file",onChange:t[3]||(t[3]=(...e)=>g.handleFileUpload&&g.handleFileUpload(...e)),accept:"image/*",class:"upload-button"},null,32),(0,s.Lk)("button",{onClick:t[4]||(t[4]=(...e)=>g.capturePhoto&&g.capturePhoto(...e)),class:"camera-button"},"📷")])])}n(4114),n(4603),n(7566),n(8721);var f={data(){return{userInput:"",messages:[{id:1,sender:"AI",text:"Welcome to AI Yoga! Let's find the perfect pose for you today."}],uploadedImage:null}},methods:{async sendMessage(){if(this.userInput.trim()){this.messages.push({id:Date.now(),sender:"User",text:this.userInput});try{const e=await fetch("http://localhost:5000/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:this.userInput})}),t=await e.json();this.messages.push({id:Date.now()+1,sender:"AI",text:t.response})}catch(e){this.messages.push({id:Date.now()+1,sender:"AI",text:"Sorry, I am unable to process your request right now. Please try again later."})}this.userInput=""}},handleFileUpload(e){const t=e.target.files[0];t&&(this.uploadedImage=URL.createObjectURL(t),this.messages.push({id:Date.now(),sender:"User",text:"Uploaded an image",image:this.uploadedImage}))},async capturePhoto(){try{const e=await navigator.mediaDevices.getUserMedia({video:!0}),t=document.createElement("video");t.srcObject=e,t.play();const n=document.createElement("canvas");n.width=640,n.height=480,t.addEventListener("loadedmetadata",(()=>{n.getContext("2d").drawImage(t,0,0,n.width,n.height);const e=n.toDataURL("image/png");this.messages.push({id:Date.now(),sender:"User",text:"Captured a photo",image:e}),t.srcObject.getTracks().forEach((e=>e.stop()))}))}catch(e){console.error("Camera access denied:",e)}}}},m=n(1241);const v=(0,m.A)(f,[["render",g]]);var y=v,b={components:{ChatInterface:y}};const w=(0,m.A)(b,[["render",r]]);var k=w;(0,a.Ef)(k).mount("#app")}},t={};function n(a){var s=t[a];if(void 0!==s)return s.exports;var o=t[a]={exports:{}};return e[a].call(o.exports,o,o.exports,n),o.exports}n.m=e,function(){var e=[];n.O=function(t,a,s,o){if(!a){var r=1/0;for(d=0;d<e.length;d++){a=e[d][0],s=e[d][1],o=e[d][2];for(var i=!0,c=0;c<a.length;c++)(!1&o||r>=o)&&Object.keys(n.O).every((function(e){return n.O[e](a[c])}))?a.splice(c--,1):(i=!1,o<r&&(r=o));if(i){e.splice(d--,1);var u=s();void 0!==u&&(t=u)}}return t}o=o||0;for(var d=e.length;d>0&&e[d-1][2]>o;d--)e[d]=e[d-1];e[d]=[a,s,o]}}(),function(){n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,{a:t}),t}}(),function(){n.d=function(e,t){for(var a in t)n.o(t,a)&&!n.o(e,a)&&Object.defineProperty(e,a,{enumerable:!0,get:t[a]})}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={524:0};n.O.j=function(t){return 0===e[t]};var t=function(t,a){var s,o,r=a[0],i=a[1],c=a[2],u=0;if(r.some((function(t){return 0!==e[t]}))){for(s in i)n.o(i,s)&&(n.m[s]=i[s]);if(c)var d=c(n)}for(t&&t(a);u<r.length;u++)o=r[u],n.o(e,o)&&e[o]&&e[o][0](),e[o]=0;return n.O(d)},a=self["webpackChunkyogamasterai_chat"]=self["webpackChunkyogamasterai_chat"]||[];a.forEach(t.bind(null,0)),a.push=t.bind(null,a.push.bind(a))}();var a=n.O(void 0,[504],(function(){return n(2976)}));a=n.O(a)})();
//# sourceMappingURL=app.fb79c805.js.map