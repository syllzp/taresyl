import { createApp } from 'vue'
import App from './App.vue'
import VForm from 'vform3-builds'
import 'vform3-builds/dist/designer.style.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.use(VForm)
app.mount('#app')