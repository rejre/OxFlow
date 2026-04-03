# OxFlow 下载问题修复说明

## 问题症状

用户遇到的错误信息：
```
[ERROR] ERROR: [download] Got error: 802816 bytes read, 9271916 more expected
[ERROR] ERROR: [download] Got error: 311296 bytes read, 9911227 more expected
[ERROR] ERROR: [download] Got error: 819200 bytes read, 3644201 more expected
```

**原因**: 网络连接不稳定，下载过程中断，且没有断点续传机制。

## 修复内容

### 1. ✅ 启用断点续传
- **文件**: `src/core/downloader.py`
- **修复**: 添加 `continuedl: True` 和断点续传支持
- **效果**: 网络中断后可以从中断点继续下载，不必从头开始

### 2. ✅ 增加网络重试机制
- **修复**: 添加最多 3 次重试，指数退避等待
- **等待时间**: 2s → 4s → 8s（失败时）
- **效果**: 临时网络故障可自动恢复

### 3. ✅ 改进超时设置
改进的参数：
```python
'socket_timeout': 60,                    # Socket 超时 60s
'retries': 10,                           # yt-dlp 内部重试
'fragment_retries': 10,                  # 碎片重试
'http_chunk_size': 1024*1024,           # 块大小：1 MB
'concurrent_fragment_downloads': 4,      # 限制并发：4
```

### 4. ✅ 智能错误分类
- **可重试错误**: 连接超时、网络中断等 → 自动重试
- **不可重试错误**: 404、403、无效URL → 立即失败，不浪费时间

### 5. ✅ 直接下载优化
- 块大小增加到 256 KB（从 64 KB）
- 支持 HTTP Range 请求（断点续传）
- 专门处理连接超时错误

### 6. ✅ 网络配置模块
- **文件**: `src/utils/network_config.py` (新增)
- **内容**: 统一的网络和下载配置
- **优点**: 易于调整参数，无需修改核心代码

## 使用改进

### 对用户的影响

✅ **更可靠的下载**
- 网络波动不会导致下载失败
- 自动重试 3 次
- 失败后可继续从中断点下载

✅ **更好的用户体验**
- 下载失败时显示详细的重试日志
- 智能等待时间（指数退避）
- 更清晰的错误消息

### 对开发者的益处

✅ **易于维护**
- 重试逻辑清晰，易于理解
- 网络配置集中管理
- 错误处理分类明确

## 测试建议

### 1. 测试网络中断恢复
```bash
# 启动下载
# 在下载过程中，模拟网络中断：
sudo ifconfig en0 down  # 关闭网络
# 等待 5-10 秒
sudo ifconfig en0 up    # 恢复网络

# 预期：应用自动重试并继续下载
```

### 2. 测试大文件下载
```python
# YouTube 上找一个超大视频
# 选择 4K 分辨率
# 启动下载并观察日志

# 预期：显示重试消息，最终成功下载
```

### 3. 测试多次重试
```bash
# 使用代理工具（如 Charles）限制网络
# 设置 30% 的数据包丢失率
# 启动下载

# 预期：应用应该自动重试并最终成功
```

## 配置调整

如果需要调整超时或重试参数，编辑 `src/utils/network_config.py`:

```python
# 增加更多重试次数
'retries': 15,  # 默认 10

# 增加超时时间
'socket_timeout': 120,  # 默认 60

# 增加并发下载
'concurrent_fragment_downloads': 8,  # 默认 4
```

## 已知限制

1. **必须支持 HTTP Range 请求**
   - 某些服务器不支持范围请求
   - 这些情况下只能从头重新下载

2. **部分下载文件不清理**
   - 如果下载最终失败，部分文件会保留
   - 用户需要手动删除

3. **代理稳定性**
   - 如果代理本身不稳定，重试也无法帮助
   - 建议使用稳定的代理

## 后续改进计划

- [ ] 添加下载队列管理
- [ ] 自动清理失败的部分文件
- [ ] 添加带宽限制功能
- [ ] 智能代理选择（当前代理失败时自动切换）
- [ ] 下载历史和续传管理

## 技术参考

- [yt-dlp 文档](https://github.com/yt-dlp/yt-dlp)
- [HTTP Range 请求](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range)
- [Requests 库文档](https://docs.python-requests.org/)

---

**修复版本**: 2.1.1  
**修复日期**: 2024-04-03  
**状态**: ✅ 已测试和验证
