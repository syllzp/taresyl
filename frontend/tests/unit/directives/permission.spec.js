import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import permissionDirective from '@/directives/permission'
import permissionService from '@/services/permissionService'

// 模拟权限服务
jest.mock('@/services/permissionService', () => ({
  hasPermission: jest.fn(),
  hasAnyPermission: jest.fn(),
  userPermissions: []
}))

describe('Permission Directive', () => {
  let app

  beforeEach(() => {
    app = createApp({})
    app.use(ElementPlus)
    
    // 重置模拟函数
    jest.clearAllMocks()
  })

  afterEach(() => {
    app = null
  })

  test('应该正确注册权限指令', () => {
    // 注册指令
    app.directive('permission', permissionDirective)
    
    // 验证指令是否注册成功
    const directives = app._context.directives
    expect(directives.permission).toBeDefined()
  })

  test('当用户有权限时，元素应该显示', () => {
    // 模拟权限服务返回 true
    permissionService.hasPermission.mockReturnValue(true)
    
    // 创建一个测试元素
    const element = document.createElement('div')
    document.body.appendChild(element)
    
    // 模拟指令绑定
    const binding = {
      value: 'can_manage_users'
    }
    
    // 模拟 vnode
    const vnode = {
      el: element
    }
    
    // 调用指令的 mounted 钩子
    permissionDirective.mounted(element, binding, vnode)
    
    // 验证元素是否显示
    expect(element.style.display).not.toBe('none')
    
    // 清理
    document.body.removeChild(element)
  })

  test('当用户没有权限时，元素应该隐藏', () => {
    // 模拟权限服务返回 false
    permissionService.hasPermission.mockReturnValue(false)
    
    // 创建一个测试元素
    const element = document.createElement('div')
    document.body.appendChild(element)
    
    // 模拟指令绑定
    const binding = {
      value: 'can_manage_users'
    }
    
    // 模拟 vnode
    const vnode = {
      el: element
    }
    
    // 调用指令的 mounted 钩子
    permissionDirective.mounted(element, binding, vnode)
    
    // 验证元素是否隐藏
    expect(element.style.display).toBe('none')
    
    // 清理
    document.body.removeChild(element)
  })

  test('当绑定值是数组且用户拥有任意一个权限时，元素应该显示', () => {
    // 模拟权限服务返回 true
    permissionService.hasAnyPermission.mockReturnValue(true)
    
    // 创建一个测试元素
    const element = document.createElement('div')
    document.body.appendChild(element)
    
    // 模拟指令绑定
    const binding = {
      value: ['can_manage_users', 'can_manage_roles']
    }
    
    // 模拟 vnode
    const vnode = {
      el: element
    }
    
    // 调用指令的 mounted 钩子
    permissionDirective.mounted(element, binding, vnode)
    
    // 验证元素是否显示
    expect(element.style.display).not.toBe('none')
    
    // 清理
    document.body.removeChild(element)
  })

  test('当绑定值是数组且用户没有任何权限时，元素应该隐藏', () => {
    // 模拟权限服务返回 false
    permissionService.hasAnyPermission.mockReturnValue(false)
    
    // 创建一个测试元素
    const element = document.createElement('div')
    document.body.appendChild(element)
    
    // 模拟指令绑定
    const binding = {
      value: ['can_manage_users', 'can_manage_roles']
    }
    
    // 模拟 vnode
    const vnode = {
      el: element
    }
    
    // 调用指令的 mounted 钩子
    permissionDirective.mounted(element, binding, vnode)
    
    // 验证元素是否隐藏
    expect(element.style.display).toBe('none')
    
    // 清理
    document.body.removeChild(element)
  })

  test('当绑定值为空时，元素应该显示', () => {
    // 创建一个测试元素
    const element = document.createElement('div')
    document.body.appendChild(element)
    
    // 模拟指令绑定
    const binding = {
      value: ''
    }
    
    // 模拟 vnode
    const vnode = {
      el: element
    }
    
    // 调用指令的 mounted 钩子
    permissionDirective.mounted(element, binding, vnode)
    
    // 验证元素是否显示
    expect(element.style.display).not.toBe('none')
    
    // 清理
    document.body.removeChild(element)
  })

  test('当绑定值为 null 时，元素应该显示', () => {
    // 创建一个测试元素
    const element = document.createElement('div')
    document.body.appendChild(element)
    
    // 模拟指令绑定
    const binding = {
      value: null
    }
    
    // 模拟 vnode
    const vnode = {
      el: element
    }
    
    // 调用指令的 mounted 钩子
    permissionDirective.mounted(element, binding, vnode)
    
    // 验证元素是否显示
    expect(element.style.display).not.toBe('none')
    
    // 清理
    document.body.removeChild(element)
  })
})

