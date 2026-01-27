import permissionDirective from './permission'

// 注册所有指令
const registerDirectives = (app) => {
  // 注册权限指令
  app.directive('permission', permissionDirective)
}

export default registerDirectives
