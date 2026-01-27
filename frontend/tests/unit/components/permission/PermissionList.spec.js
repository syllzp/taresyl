import { mount } from '@vue/test-utils'
import { createStore } from 'vuex'
import ElementPlus from 'element-plus'
import PermissionList from '@/components/permission/PermissionList.vue'
import axios from 'axios'
import { createApp } from 'vue'

// 模拟 axios
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn()
}))

// 模拟路由
const mockRouter = {
  push: jest.fn()
}

// 模拟存储
const createMockStore = () => {
  return createStore({
    state: {
      user: {
        id: 1,
        username: 'admin'
      },
      permissions: ['can_manage_permissions']
    },
    getters: {
      currentUser: (state) => state.user,
      hasPermission: (state) => (permission) => {
        return state.permissions.includes(permission)
      }
    }
  })
}

describe('PermissionList Component', () => {
  let wrapper
  let store

  beforeEach(() => {
    store = createMockStore()
    wrapper = mount(PermissionList, {
      global: {
        plugins: [ElementPlus, store],
        mocks: {
          $router: mockRouter,
          $axios: axios
        }
      }
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  test('组件应该正常挂载', () => {
    expect(wrapper.exists()).toBe(true)
  })

  test('初始化时应该加载权限列表', async () => {
    const mockPermissions = [
      { id: 1, codename: 'can_manage_users', name: 'Can manage users', description: 'Permission to manage users' },
      { id: 2, codename: 'can_manage_roles', name: 'Can manage roles', description: 'Permission to manage roles' },
      { id: 3, codename: 'can_manage_permissions', name: 'Can manage permissions', description: 'Permission to manage permissions' }
    ]
    
    axios.get.mockResolvedValueOnce({ data: mockPermissions })
    await wrapper.vm.loadPermissions()
    
    expect(axios.get).toHaveBeenCalledWith('/api/permissions/')
    expect(wrapper.vm.permissions).toEqual(mockPermissions)
  })

  test('应该能够创建新权限', async () => {
    const mockPermission = { id: 4, codename: 'can_view_dashboard', name: 'Can view dashboard', description: 'Permission to view dashboard' }
    
    axios.post.mockResolvedValueOnce({ data: mockPermission })
    
    wrapper.vm.dialogVisible = true
    wrapper.vm.editingPermission = {
      codename: 'can_view_dashboard',
      name: 'Can view dashboard',
      description: 'Permission to view dashboard'
    }
    
    await wrapper.vm.savePermission()
    
    expect(axios.post).toHaveBeenCalledWith('/api/permissions/', wrapper.vm.editingPermission)
    expect(wrapper.vm.dialogVisible).toBe(false)
  })

  test('应该能够更新权限', async () => {
    const mockPermission = { id: 3, codename: 'can_manage_permissions', name: 'Can manage permissions', description: 'Updated permission description' }
    
    axios.put.mockResolvedValueOnce({ data: mockPermission })
    
    wrapper.vm.dialogVisible = true
    wrapper.vm.editingPermission = {
      id: 3,
      codename: 'can_manage_permissions',
      name: 'Can manage permissions',
      description: 'Updated permission description'
    }
    
    await wrapper.vm.savePermission()
    
    expect(axios.put).toHaveBeenCalledWith('/api/permissions/3/', wrapper.vm.editingPermission)
    expect(wrapper.vm.dialogVisible).toBe(false)
  })

  test('应该能够删除权限', async () => {
    axios.delete.mockResolvedValueOnce({ status: 204 })
    
    await wrapper.vm.deletePermission(3, 'Can manage permissions')
    
    expect(axios.delete).toHaveBeenCalledWith('/api/permissions/3/')
  })

  test('应该能够打开编辑对话框', async () => {
    const mockPermission = { id: 3, codename: 'can_manage_permissions', name: 'Can manage permissions', description: 'Permission to manage permissions' }
    
    await wrapper.vm.editPermission(mockPermission)
    
    expect(wrapper.vm.dialogVisible).toBe(true)
    expect(wrapper.vm.editingPermission).toEqual(mockPermission)
  })

  test('应该能够打开创建对话框', async () => {
    await wrapper.vm.createPermission()
    
    expect(wrapper.vm.dialogVisible).toBe(true)
    expect(wrapper.vm.editingPermission).toEqual({
      codename: '',
      name: '',
      description: ''
    })
  })
})
