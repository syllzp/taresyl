import { createApp } from 'vue'
import App from './App.vue'
import 'vform3-builds/dist/designer.style.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')