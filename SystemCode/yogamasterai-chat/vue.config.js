module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 后端服务器的地址和端口
        changeOrigin: true, // 支持跨域
        pathRewrite: {
          '^/api': '' // 将/api前缀移除（如果后端没有使用/api作为路由前缀）
        }
      }
    }
  }
};
