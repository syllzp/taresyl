import permissionService from '../services/permissionService'

// 权限指令
const permissionDirective = {
  mounted(el, binding) {
    // 获取绑定的值（权限代码或权限代码数组）
    const permission = binding.value
    
    // 检查用户是否拥有该权限
    let hasPermission = true
    
    if (Array.isArray(permission)) {
      // 如果是数组，检查是否拥有任意一个权限
      hasPermission = permissionService.hasAnyPermission(permission)
    } else if (typeof permission === 'string' && permission) {
      // 如果是字符串，检查是否拥有该权限
      hasPermission = permissionService.hasPermission(permission)
    }
    
    // 如果用户没有权限，隐藏元素
    if (!hasPermission) {
      el.style.display = 'none'
    }
  },
  
  // 当指令所在组件更新时执行
  updated(el, binding) {
    // 重新检查权限
    const permission = binding.value
    
    let hasPermission = true
    
    if (Array.isArray(permission)) {
      hasPermission = permissionService.hasAnyPermission(permission)
    } else if (typeof permission === 'string' && permission) {
      hasPermission = permissionService.hasPermission(permission)
    }
    
    // 根据权限状态显示或隐藏元素
    if (hasPermission) {
      el.style.display = ''
    } else {
      el.style.display = 'none'
    }
  }
}

export default permissionDirective
