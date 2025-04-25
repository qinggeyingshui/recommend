<template>
    <div class="enter-container">
      <div id="world"></div>
      <div class="text-overlay">
        <div class="text-line" style="bottom: 85%;left: 670px;">💞欢迎来跟猫猫玩💞</div>
        <div class="text-line" style="bottom: 80%;left: 700px;">不愧是我！！！</div>
        <div class="text-line" style="bottom: 70%;left: 640px;"></div>
        <div class="button-container">
          <el-button 
            @click="handleClick"
            :loading="loading"
            class="enter-button"
          >
            欢迎探索，旅行者！
          </el-button>
        </div>
        <div class="credit-text">Syclover @ cl4y</div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Enter',
    data() {
      return {
        loading: false
      }
    },
    mounted() {
      this.loadScripts();
      window.addEventListener('load', this.checkResources);
    },
    beforeDestroy() {
      window.removeEventListener('load', this.checkResources);
    },
    methods: {
    reload() {
      this.loading = true;  // 开始加载
      // 模拟一些异步操作，然后跳转
      setTimeout(() => {
        location.href = '/';  // 跳转到登录页面
      }, 1000);  // 这里模拟1秒后跳转
    },
      handleClick() {
        console.log('按钮被点击');
        this.reload();
      },
      loadScripts() {
        const scripts = [
          './three.min.js',
          './TweenMax.min.js',
          './OrbitControls.js',
          './Cat.js',
          './index.js'
        ];
        
        scripts.forEach(src => {
          const script = document.createElement('script');
          script.src = src;
          document.body.appendChild(script);
        });
      },
      checkResources() {
        if(!window.THREE) console.error('Three.js未加载');
        if(!window.TWEEN) console.error('TweenMax未加载');
        if(!window.Cat) console.error('Cat.js未加载');
        if(!document.getElementById('world')) console.error('找不到world容器');
      }
    }
  }
  </script>
  
  <style scoped>
  .enter-container {
    position: relative;
    width: 100%;
    height: 100vh;
    background-color: #6ecccc;
    overflow: hidden;
  }
  
  #world {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 1;
  }
  
  .text-overlay {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 10;
    pointer-events: none; /* 默认穿透点击事件 */
  }
  
  .text-line {
    position: absolute;
    text-shadow: 0px 0px 5px;
    font-family: KaiTi, arial;
    color: black;
    font-size: 20px;
    white-space: nowrap;
  }
  
  .credit-text {
    position: absolute;
    bottom: 5%;
    width: 100%;
    text-align: center;
    font: italic 15px Georgia, serif;
    color: white;
  }
  
  .button-container {
    position: absolute;
    bottom: 20%;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;
    pointer-events: auto; /* 允许按钮接收点击事件 */
  }
  
  .enter-button {
    padding: 15px 30px;
    font-size: 18px;
    border-radius: 25px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    pointer-events: auto;
    height: 50px;
    border-radius: 20px;
    backdrop-filter: blur(1px);
    background-color: rgba(255, 255, 255, 0.5);
    font-family: 'Dancing Script', cursive;
    font-size: 24px;
  }
  
  .enter-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
  }
  </style>