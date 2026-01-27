import { createRouter, createWebHistory } from 'vue-router'
import FormList from '../views/FormList.vue'
import FormDesign from '../views/FormDesign.vue'
import SystemLog from '../views/SystemLog.vue'
import UserList from '../views/UserList.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import PermissionManagement from '../views/PermissionManagement.vue'
import MainLayout from '../components/MainLayout.vue'
import permissionService from '../services/permissionService'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    component: MainLayout,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'Home',
        component: FormList
      },
      {
        path: 'form/design',
        name: 'FormDesign',
        component: FormDesign
      },
      {
        path: 'form/design/:id',
        name: 'FormEdit',
        component: FormDesign
      },
      {
        path: 'form/data',
        name: 'FormData',
        component: () => import('../views/FormData.vue')
      },
      {
        path: 'system/logs',
        name: 'SystemLog',
        component: SystemLog
      },
      {
        path: 'system/users',
        name: 'UserList',
        component: UserList
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: () => import('../views/UserProfile.vue')
      },
      {
        path: 'system/permissions',
        name: 'PermissionManagement',
        component: PermissionManagement,
        meta: {
          requiresAuth: true,
          requiredPermission: 'permission_manage'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫，检查登录状态和权限
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // 检查用户是否登录（通过本地存储的token判断）
  const isLoggedIn = !!localStorage.getItem('token')
  
  if (requiresAuth && !isLoggedIn) {
    // 如果需要认证但未登录，重定向到登录页面
    next('/login')
  } else if (to.path === '/login' && isLoggedIn) {
    // 如果已登录但访问登录页面，重定向到首页
    next('/')
  } else {
    // 检查路由是否需要特定权限
    const requiredPermission = to.matched.some(record => record.meta.requiredPermission)
    
    if (requiredPermission) {
      // 获取路由需要的权限
      const permission = to.matched.find(record => record.meta.requiredPermission)?.meta.requiredPermission
      
      // 检查用户是否拥有该权限
      if (permission && !permissionService.hasPermission(permission)) {
        // 如果用户没有该权限，重定向到首页
        next('/')
        // 可以在这里添加一个提示，告诉用户没有权限访问该页面
      } else {
        // 用户拥有该权限，正常访问
        next()
      }
    } else {
      // 路由不需要特定权限，正常访问
      next()
    }
  }
})

export default router
