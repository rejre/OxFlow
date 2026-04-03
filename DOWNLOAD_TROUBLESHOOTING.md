# OxFlow 下载故障排查指南

## 🔴 常见错误和解决方案

### 错误 1: 下载中途停止 (bytes read error)

**症状**:
```
[ERROR] Got error: 802816 bytes read, 9271916 more expected
```

**原因**: 网络连接中断

**解决方案** ✅:
1. **自动重试** - 应用会自动重试 3 次
2. **等待片刻** - 第一次重试等待 2 秒，第二次 4 秒，第三次 8 秒
3. **检查网络** - 确保网络连接正常
4. **重试下载** - 如果仍然失败，请再次尝试

**代码版本**: v2.1.1+ 包含自动重试

---

### 错误 2: 连接超时

**症状**:
```
[ERROR] Connection timeout
```

**原因**: 
- 网络太慢
- 目标服务器响应慢
- 防火墙阻止

**解决方案**:
1. ✅ 检查网络连接速度
   ```bash
   ping 8.8.8.8
   ```

2. ✅ 尝试其他网络
   - 切换到其他 WiFi
   - 改用有线网络

3. ✅ 使用代理
   - 在 OxFlow 设置中添加代理
   - 示例: `http://127.0.0.1:7890`

4. ✅ 选择更低的分辨率
   - 360p 或 480p 比 4K 更容易成功

---

### 错误 3: 403 Forbidden / 404 Not Found

**症状**:
```
[ERROR] HTTP 403 / HTTP 404
```

**原因**:
- 视频已删除或私密
- 地区限制
- 防爬虫措施

**解决方案**:
1. ✅ 检查视频是否仍存在
   - 在浏览器中打开链接

2. ✅ 使用浏览器 Cookie
   - 在 OxFlow 设置中选择你常用的浏览器
   - 这可以绕过一些限制

3. ✅ 使用代理突破地区限制
   - 添加代理服务器地址

4. ✅ 更新 yt-dlp
   ```bash
   pip install --upgrade yt-dlp
   ```

---

### 错误 4: 无法转码/合并视频

**症状**:
```
[ERROR] ffmpeg not found
```

**原因**: 未安装 FFmpeg

**解决方案**:
1. ✅ 安装 FFmpeg
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # Windows
   # 从 https://ffmpeg.org/download.html 下载
   ```

2. ✅ 在 OxFlow 中配置 FFmpeg 路径
   - 打开设置
   - 找到 "FFmpeg 路径"
   - 通常为: `/usr/local/bin` 或 `/opt/homebrew/bin`

3. ✅ 验证安装
   ```bash
   ffmpeg -version
   ```

---

## 📋 检查清单

下载前检查：

- [ ] 网络连接良好
  ```bash
  ping 8.8.8.8  # 应该看到 < 100ms 的响应时间
  ```

- [ ] YouTube/Bilibili 等网站可访问
  ```bash
  curl -I https://www.youtube.com  # 应该返回 200
  ```

- [ ] OxFlow 已安装最新版本
  ```bash
  # 检查版本
  ```

- [ ] 下载目录有足够空间
  ```bash
  # 检查剩余空间
  df -h
  ```

- [ ] 如果需要 FFmpeg，已安装
  ```bash
  ffmpeg -version
  ```

---

## 💡 最佳实践

### 1. 选择合适的分辨率

| 分辨率 | 文件大小 | 下载时间 | 失败率 | 建议场景 |
|--------|---------|---------|--------|---------|
| 360p | 50-200 MB | 快 | 低 | ✅ 不稳定网络 |
| 480p | 100-300 MB | 中等 | 中等 | ✅ 普通使用 |
| 720p | 200-500 MB | 慢 | 中等 | ✅ 好的网络 |
| 1080p | 500-1500 MB | 很慢 | 较高 | ✅ 需要高质量 |
| 2160p | 1-5 GB | 非常慢 | 高 | ⚠️ 很少使用 |

**建议**: 大多数情况下选择 **720p** 或 **1080p**

### 2. 选择合适的时间下载

- ❌ 避免: 晚上 8-11 点（网络拥堵）
- ✅ 最佳: 工作时间（9:00-17:00）
- ✅ 备选: 凌晨 2-6 点（网络最快）

### 3. 使用代理加速

如果直接下载速度慢：
```
代理示例: http://127.0.0.1:7890
（Clash, V2Ray 等代理工具）
```

### 4. 大文件下载建议

对于超过 1 GB 的文件：
1. 使用稳定的网络
2. 在后台进行（不要关闭应用）
3. 选择低分辨率或音频格式
4. 监控进度（查看日志）

---

## 🔧 高级调试

### 查看详细日志

**macOS/Linux**:
```bash
# 日志位置
~/.oxflow/logs/oxflow.log

# 实时查看
tail -f ~/.oxflow/logs/oxflow.log
```

**Windows**:
```
C:\Users\<username>\AppData\Roaming\OxFlow\logs\oxflow.log
```

### 增加超时时间

编辑 `~/.oxflow/config.json`:
```json
{
  "socket_timeout": 120,
  "max_retries": 15
}
```

### 使用代理调试

```bash
# 使用 Shadowsocks/V2Ray
# 或 Clash for macOS/Windows
```

---

## 🚀 性能优化

### 提高下载速度

1. ✅ 使用有线网络
2. ✅ 关闭其他应用的网络使用
3. ✅ 选择较低分辨率
4. ✅ 使用代理（如果有高速代理）

### 降低 CPU 使用

在 OxFlow 设置中：
- ✅ 启用"低功耗模式"
- ✅ 减少"并发片段下载数"

---

## 📞 获取帮助

如果问题仍未解决：

1. **收集信息**:
   - 错误消息（完整内容）
   - 日志文件
   - 操作系统和版本
   - 尝试下载的 URL

2. **提交 Issue**:
   - GitHub: https://github.com/rejre/OxFlow/issues
   - 包含上述所有信息

3. **提供更多细节**:
   - "不工作" 不够详细
   - "下载 YouTube 视频时，在 50% 处停止，显示 'bytes read' 错误" 更好

---

**最后更新**: 2024-04-03  
**版本**: OxFlow 2.1.1+  
**状态**: ✅ 已修复断点续传和重试机制
