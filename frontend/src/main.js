import { createApp } from 'vue'
import App from './App.vue'
import VForm from 'vform3-builds'
import 'vform3-builds/dist/designer.style.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router/index.js'
import registerDirectives from './directives/index.js'
import permissionService from './services/permissionService'

const app = createApp(App)
app.use(ElementPlus)
app.use(VForm)
app.use(router)

// 注册指令
registerDirectives(app)

// 应用启动时获取用户权限
if (localStorage.getItem('token')) {
  permissionService.getPermissions().catch(error => {
    console.error('获取用户权限失败', error)
  })
}

app.mount('#app')