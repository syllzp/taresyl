import { mount } from '@vue/test-utils'
import { createStore } from 'vuex'
import ElementPlus from 'element-plus'
import RoleManagement from '@/components/permission/RoleManagement.vue'
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
      permissions: ['can_manage_roles']
    },
    getters: {
      currentUser: (state) => state.user,
      hasPermission: (state) => (permission) => {
        return state.permissions.includes(permission)
      }
    }
  })
}

describe('RoleManagement Component', () => {
  let wrapper
  let store

  beforeEach(() => {
    store = createMockStore()
    wrapper = mount(RoleManagement, {
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

  test('初始化时应该加载角色列表', async () => {
    const mockRoles = [
      { id: 1, name: 'Admin', description: 'Administrator role', is_built_in: true },
      { id: 2, name: 'User', description: 'Regular user role', is_built_in: true },
      { id: 3, name: 'CustomRole', description: 'Custom role', is_built_in: false }
    ]
    
    axios.get.mockResolvedValueOnce({ data: mockRoles })
    await wrapper.vm.loadRoles()
    
    expect(axios.get).toHaveBeenCalledWith('/api/roles/')
    expect(wrapper.vm.roles).toEqual(mockRoles)
  })

  test('应该能够创建新角色', async () => {
    const mockRole = { id: 4, name: 'NewRole', description: 'New role', is_built_in: false }
    
    axios.post.mockResolvedValueOnce({ data: mockRole })
    
    wrapper.vm.dialogVisible = true
    wrapper.vm.editingRole = {
      name: 'NewRole',
      description: 'New role'
    }
    
    await wrapper.vm.saveRole()
    
    expect(axios.post).toHaveBeenCalledWith('/api/roles/', wrapper.vm.editingRole)
    expect(wrapper.vm.dialogVisible).toBe(false)
  })

  test('应该能够更新角色', async () => {
    const mockRole = { id: 3, name: 'UpdatedRole', description: 'Updated role', is_built_in: false }
    
    axios.put.mockResolvedValueOnce({ data: mockRole })
    
    wrapper.vm.dialogVisible = true
    wrapper.vm.editingRole = {
      id: 3,
      name: 'UpdatedRole',
      description: 'Updated role'
    }
    
    await wrapper.vm.saveRole()
    
    expect(axios.put).toHaveBeenCalledWith('/api/roles/3/', wrapper.vm.editingRole)
    expect(wrapper.vm.dialogVisible).toBe(false)
  })

  test('应该能够删除角色', async () => {
    axios.delete.mockResolvedValueOnce({ status: 204 })
    
    await wrapper.vm.deleteRole(3, 'CustomRole')
    
    expect(axios.delete).toHaveBeenCalledWith('/api/roles/3/')
  })

  test('不应该能够删除内置角色', async () => {
    const deleteSpy = jest.spyOn(wrapper.vm, 'deleteRole')
    
    // 尝试删除内置角色
    await wrapper.vm.deleteRole(1, 'Admin')
    
    // 应该弹出提示，不调用删除API
    expect(axios.delete).not.toHaveBeenCalled()
  })

  test('应该能够打开编辑对话框', async () => {
    const mockRole = { id: 3, name: 'CustomRole', description: 'Custom role', is_built_in: false }
    
    await wrapper.vm.editRole(mockRole)
    
    expect(wrapper.vm.dialogVisible).toBe(true)
    expect(wrapper.vm.editingRole).toEqual(mockRole)
  })

  test('应该能够打开创建对话框', async () => {
    await wrapper.vm.createRole()
    
    expect(wrapper.vm.dialogVisible).toBe(true)
    expect(wrapper.vm.editingRole).toEqual({
      name: '',
      description: ''
    })
  })
})
