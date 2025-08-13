# 梦幻筑界 · ID_2META 实名验证系统 开发文档

## 1. 系统概述
该系统由静态前端页面和 FastAPI 后端接口组成，用于调用 **阿里云 CloudAuth Intl 身份实名验证 API**，实现 **姓名 + 身份证号** 的实名认证。

- **前端（`index.html`）**：用户输入 → 本地预校验 → 调用 `/api/verify`
- **后端（`api/verify.py`）**：调用阿里云接口 → 返回结果给前端
- **部署**：Vercel 无服务器架构（前端静态托管 + 后端函数）

---

## 2. 项目结构
/
├── index.html # 前端页面
├── api/
│ └── verify.py # 后端 API（FastAPI）
├── requirements.txt # Python 依赖
└── vercel.json # Vercel 部署配置


---

## 3. 前端说明（`index.html`）

**技术栈：**
- Bootstrap 5 + Bootstrap Icons
- 原生 JavaScript

**主要功能：**
- 身份证严格预校验（格式、地址码、顺序码、出生日期、校验位）
- 输入过滤（仅数字和末位 X，自动转大写）
- 提交按钮加载状态
- 结果卡片渲染（状态映射：一致、不一致、无记录、未知）
- 原始响应折叠查看与复制

**调用方式：**
```javascript
fetch("/api/verify", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "张三", idNumber: "11010519900101001X" })
})

4. 后端说明（api/verify.py）
技术栈：

FastAPI

阿里云 CloudAuth Intl SDK

接口路径：
POST /api/verify

请求参数（JSON）：
{ "name": "张三", "idNumber": "11010519900101001X" }

响应字段（主要）：
| 字段名         | 说明                     |
| ----------- | ---------------------- |
| `code`      | API 返回码（Success/Error） |
| `message`   | 消息文本                   |
| `requestId` | 请求 ID                  |
| `bizCode`   | 业务码（1=一致，2=不一致，3=无记录）  |
| `raw`       | 原始响应（调试用，生产可去掉或脱敏）     |


5. 环境变量设置

必需变量：

| 变量名                               | 说明                  | 示例               |
| --------------------------------- | ------------------- | ---------------- |
| `ALIBABA_CLOUD_ACCESS_KEY_ID`     | 阿里云 AccessKeyId     | `LTAI5txxxxxxxx` |
| `ALIBABA_CLOUD_ACCESS_KEY_SECRET` | 阿里云 AccessKeySecret | `abcd1234xxxx`   |

选填变量（增强安全性）：

| 变量名         | 说明                | 示例                           |
| ----------- | ----------------- | ---------------------------- |
| `API_TOKEN` | 接口访问 Bearer Token | `7a3c8baf9d234678accc112233` |

API_TOKEN变量请注意在前端代码的320行填写为自己的变量值，需要与Vercel填写的一直，否则会无法调用

6. 部署说明
本项目可直接在 Vercel 部署，实现前后端一体化的无服务器运行。

https://vercel.com
