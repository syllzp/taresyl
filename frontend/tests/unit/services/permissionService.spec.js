import permissionService from '@/services/permissionService'
import axios from 'axios'

// 模拟 axios
jest.mock('axios', () => {
  const mockAxios = {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
    create: jest.fn(() => mockAxios),
    interceptors: {
      request: {
        use: jest.fn((config) => config)
      },
      response: {
        use: jest.fn((response) => response)
      }
    }
  }
  return mockAxios
})

describe('Permission Service', () => {
  beforeEach(() => {
    // 重置权限服务的用户权限
    permissionService.userPermissions = []
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  test('应该正确获取用户权限', async () => {
    const mockPermissions = [
      { codename: 'can_manage_users' },
      { codename: 'can_manage_roles' }
    ]
    
    axios.get.mockResolvedValueOnce({ data: mockPermissions })
    
    const result = await permissionService.getPermissions()
    
    expect(axios.get).toHaveBeenCalledWith('/api/auth/user-permissions/')
    expect(result).toEqual(mockPermissions)
  })

  test('应该正确检查用户是否有权限', () => {
    // 设置用户权限
    permissionService.userPermissions = [
      { codename: 'can_manage_users' },
      { codename: 'can_manage_roles' }
    ]
    
    // 测试用户拥有的权限
    expect(permissionService.hasPermission('can_manage_users')).toBe(true)
    expect(permissionService.hasPermission('can_manage_roles')).toBe(true)
    
    // 测试用户没有的权限
    expect(permissionService.hasPermission('can_manage_permissions')).toBe(false)
  })

  test('当没有权限时，应该返回 false', () => {
    permissionService.userPermissions = []
    
    expect(permissionService.hasPermission('can_manage_users')).toBe(false)
  })

  test('应该正确检查用户是否拥有多个权限中的任意一个', () => {
    // 设置用户权限
    permissionService.userPermissions = [
      { codename: 'can_manage_users' }
    ]
    
    // 测试用户拥有的权限
    expect(permissionService.hasAnyPermission(['can_manage_users', 'can_manage_roles'])).toBe(true)
    expect(permissionService.hasAnyPermission(['can_manage_roles', 'can_manage_permissions'])).toBe(false)
  })

  test('应该正确检查用户是否拥有所有指定权限', () => {
    // 设置用户权限
    permissionService.userPermissions = [
      { codename: 'can_manage_users' },
      { codename: 'can_manage_roles' }
    ]
    
    // 测试用户拥有所有权限
    expect(permissionService.hasAllPermissions(['can_manage_users', 'can_manage_roles'])).toBe(true)
    expect(permissionService.hasAllPermissions(['can_manage_users', 'can_manage_permissions'])).toBe(false)
  })

  test('应该正确刷新用户权限', async () => {
    const mockPermissions = [
      { codename: 'can_manage_users' },
      { codename: 'can_manage_roles' }
    ]
    
    axios.get.mockResolvedValueOnce({ data: mockPermissions })
    
    const result = await permissionService.refreshPermissions()
    
    expect(axios.get).toHaveBeenCalledWith('/api/auth/user-permissions/')
    expect(result).toEqual(mockPermissions)
  })

  test('当获取权限失败时，应该返回空数组', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'))
    
    const result = await permissionService.getPermissions()
    
    expect(axios.get).toHaveBeenCalledWith('/api/auth/user-permissions/')
    expect(result).toEqual([])
  })
})

