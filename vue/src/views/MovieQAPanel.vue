<template>
    <div class="movie-qa-container">
      <div class="header">
        <h1>电影知识问答系统</h1>
        <p>基于知识图谱的智能问答</p>
      </div>
      
      <div class="chat-container">
        <div class="message-list" ref="messageList">
          <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.type]">
            <div class="avatar" v-if="msg.type === 'user'">
              <img src="@/assets/user.png" alt="用户头像">
            </div>
            <div class="message-content">
              <div>{{ msg.content }}</div>
              <div class="message-time">{{ msg.time }}</div>
            </div>
            <div class="avatar" v-if="msg.type === 'system'">
              <img src="@/assets/robot.png" alt="系统头像">
            </div>
          </div>
        </div>
        
        <div class="input-area">
          <input
            v-model="userInput"
            @keyup.enter="sendQuestion"
            placeholder="请输入关于电影的问题..."
          />
          <button @click="sendQuestion">发送</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import movieQARequest from '@/api/movieQA'
  
  export default {
    data() {
      return {
        userInput: '',
        messages: [],
        commonQuestions: []
      }
    },
    created() {
      this.loadCommonQuestions()
    },
    methods: {
      async loadCommonQuestions() {
        try {
          const response = await movieQARequest.getCommonQuestions()
          this.commonQuestions = response.data
        } catch (error) {
          console.error('获取常见问题失败:', error)
        }
      },
      
      async sendQuestion() {
          if (!this.userInput.trim()) return
          
          this.messages.push({
              type: 'user',
              content: this.userInput,
              time: new Date().toLocaleTimeString() // 添加时间戳
          })
          
          const question = this.userInput
          this.userInput = ''
          
          try {
              const answer = await movieQARequest.askMovieQuestion(question)
              
              this.messages.push({
                  type: 'system',
                  content: answer,
                  time: new Date().toLocaleTimeString() // 添加时间戳
              })
              
          } catch (error) {
              this.messages.push({
                  type: 'error',
                  content: '获取回答时出错: ' + (error.response?.error || error.message)
              })
              console.error('API请求错误:', error)
          }
          
          this.scrollToBottom()
      },
      scrollToBottom() {
        this.$nextTick(() => {
          const container = this.$refs.messageList
          container.scrollTop = container.scrollHeight
        })
      }
    }
  }
  </script>
  
  <style scoped>
  .movie-qa-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Arial', sans-serif;
  }
  
  .header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .chat-container {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }
  
  .message-list {
    height: 500px;
    overflow-y: auto;
    padding: 15px;
    background: #f9f9f9;
  }
  
  .message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 15px;
    padding: 10px 15px;
    border-radius: 18px;
    max-width: 80%;
  }
  
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 10px;
  }
  
  .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .message.user {
    margin-left: auto;
    background: #e3f2fd;
    border-bottom-right-radius: 5px;
    flex-direction: row-reverse;
  }
  
  .message.system {
    background: #f1f1f1;
    border-bottom-left-radius: 5px;
    margin-right: auto;
  }
  
  .message.cypher {
    background: #fff8e1;
    font-family: monospace;
    font-size: 14px;
    white-space: pre-wrap;
    border-bottom-left-radius: 5px;
  }
  
  .message.error {
    background: #ffebee;
    color: #c62828;
  }
  
  .input-area {
    display: flex;
    padding: 15px;
    background: #fff;
    border-top: 1px solid #eee;
  }
  
  .input-area input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 10px;
  }
  
  .input-area button {
    padding: 10px 20px;
    background: #2196f3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .input-area button:hover {
    background: #0d8bf2;
  }
  </style>