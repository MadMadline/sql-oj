
---

# SQL 判题服务 API 文档

## 1. 服务概述

SQL 判题服务是一个独立的微服务，负责安全执行学生提交的 SQL 语句，与预期输出进行比对，并返回判题结果。  
服务基于 FastAPI 开发，使用 Docker 动态创建临时的 PostgreSQL 容器作为沙箱环境，执行完毕后自动销毁容器。  
技术栈：FastAPI + Docker + PostgreSQL  
默认端口：8080  
通信协议：HTTP + JSON

---

## 2. 启动服务

### 2.1 环境要求

Python 3.10 或更高版本  
Docker Desktop（或 Docker Engine）已安装并运行  
端口 8080 未被占用

### 2.2 安装依赖

```bash
pip install -r requirements_judge.txt
```

`requirements_judge.txt` 内容：

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
docker==7.1.0
psycopg2-binary==2.9.10
pydantic==2.9.0
requests==2.32.3
```

### 2.3 启动命令

```bash
python judge_service.py
```

或使用提供的批处理文件（Windows）：

```bash
start_judge.bat
```

启动成功输出示例：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

---

## 3. API 端点

### 3.1 健康检查

**GET** `/health`

用于检查服务是否正常运行。

**响应示例**：

```json
{
  "status": "ok"
}
```

---

### 3.2 判题接口

**POST** `/judge`

执行学生提交的 SQL，并与预期输出比对。

#### 请求头

| 参数名 | 值 |
|--------|-----|
| Content-Type | application/json |

#### 请求体 (JSON)

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `submitted_sql` | string | 是 | 学生提交的 SQL 语句（如 `SELECT name, age FROM students;`） |
| `test_cases` | array | 是 | 测试用例列表，至少包含一个用例 |
| `test_cases[].expected_output` | string | 是 | 预期输出字符串，格式见下文“输出格式说明” |
| `test_cases[].test_input` | string | 否 | 该用例的测试数据准备语句（多条语句可用分号分隔） |
| `create_table_sql` | string | 否 | 建表语句（多条语句可用分号分隔），所有测试用例共享 |
| `timeout` | integer | 否 | SQL 执行超时时间（秒），默认 30 秒 |

#### 请求示例

```json
{
  "submitted_sql": "SELECT name, age FROM students WHERE age > 18 ORDER BY age;",
  "create_table_sql": "CREATE TABLE students (id INT, name VARCHAR(50), age INT);",
  "test_cases": [
    {
      "test_input": "INSERT INTO students VALUES (1, 'Alice', 20), (2, 'Bob', 17), (3, 'Charlie', 22);",
      "expected_output": "name|age\nAlice|20\nCharlie|22"
    },
    {
      "test_input": "INSERT INTO students VALUES (1, 'David', 19), (2, 'Eve', 16);",
      "expected_output": "name|age\nDavid|19"
    }
  ],
  "timeout": 30
}
```

#### 响应体 (JSON)

| 字段 | 类型 | 描述 |
|------|------|------|
| `passed` | boolean | 所有测试用例是否全部通过 |
| `execution_status` | string | 判题状态：`ACCEPTED` / `WRONG_ANSWER` / `TIMEOUT` / `ERROR` |
| `score` | integer | 得分（0-100），等于通过用例数 / 总用例数 × 100 |
| `details` | array | 每个测试用例的详细结果 |

**`details` 数组元素**：

| 字段 | 类型 | 描述 |
|------|------|------|
| `test_case_id` | integer | 测试用例序号（从 0 开始） |
| `passed` | boolean | 该用例是否通过 |
| `actual_output` | string | 学生 SQL 在该用例下的实际输出 |
| `error_message` | string | 若发生异常，返回错误信息（正常时为 `null`） |

#### 响应示例（全部通过）

```json
{
  "passed": true,
  "execution_status": "ACCEPTED",
  "score": 100,
  "details": [
    {
      "test_case_id": 0,
      "passed": true,
      "actual_output": "name|age\nAlice|20\nCharlie|22",
      "error_message": null
    },
    {
      "test_case_id": 1,
      "passed": true,
      "actual_output": "name|age\nDavid|19",
      "error_message": null
    }
  ]
}
```

#### 响应示例（部分未通过）

```json
{
  "passed": false,
  "execution_status": "WRONG_ANSWER",
  "score": 50,
  "details": [
    {
      "test_case_id": 0,
      "passed": true,
      "actual_output": "name|age\nAlice|20\nCharlie|22",
      "error_message": null
    },
    {
      "test_case_id": 1,
      "passed": false,
      "actual_output": "",
      "error_message": "syntax error at or near \"SELEC\""
    }
  ]
}
```

#### 响应示例（超时）

```json
{
  "passed": false,
  "execution_status": "TIMEOUT",
  "score": 0,
  "details": []
}
```

---

## 4. 输出格式说明

### 4.1 预期输出 (`expected_output`) 格式

- 第一行为**列名**，用竖线 `|` 分隔（例如 `name|age`）。
- 后续每行为**一行数据**，同样用 `|` 分隔。
- 行与行之间用换行符 `\n` 分隔。
- 示例：

```
name|age
Alice|20
Charlie|22
```

**注意**：
- 列名顺序必须与学生 SQL 返回的列名顺序一致。
- 系统会忽略每行首尾的空格，以及行尾空格，但列值内部的空格会保留。

### 4.2 实际输出 (`actual_output`) 格式

判题服务会将学生 SQL 执行的结果集自动转换为与 `expected_output` 相同的格式，规则如下：

- 列名从数据库返回的字段名直接读取（转为字符串）。
- 每行数据按查询返回的顺序输出（未排序时可能与预期顺序不同，由比对逻辑处理）。
- 若 SQL 不返回结果集（如 `INSERT`、`UPDATE`），则 `actual_output` 为空字符串 `""`。

---

## 5. 错误状态说明

| `execution_status` | 含义 |
|--------------------|------|
| `ACCEPTED` | 所有测试用例通过 |
| `WRONG_ANSWER` | 至少有一个测试用例未通过（结果不匹配或执行错误） |
| `TIMEOUT` | 容器启动超时或 SQL 执行超过设定时间 |
| `ERROR` | 服务内部异常（如 Docker 未运行、网络问题等） |

---

## 6. 安全机制

1. **容器隔离**：每次判题启动一个全新的 PostgreSQL 临时容器，判题结束后立即销毁。
2. **资源限制**：每个容器内存限制 `512MB`，CPU 配额限制（避免无限循环）。
3. **只读文件系统（部分）**：通过 `tmpfs` 挂载可写目录，根文件系统不可写（移除 `read_only` 后仍保留关键限制）。
4. **能力裁剪**：容器只保留必要的 Linux Capabilities，丢弃 `SYS_ADMIN`、`NET_RAW` 等高危权限。
5. **SQL 超时**：通过 PostgreSQL 的 `statement_timeout` 参数强制中断长时间运行的查询。
6. **事务回滚**：每个测试用例在独立的数据库会话中执行，结束后回滚，确保用例间数据隔离。

---

## 7. 注意事项

- **判题服务必须与 Docker 运行在同一主机上**，因为代码通过 Docker SDK 创建容器。
- 判题服务**本身不需要数据库**，它动态创建临时数据库实例。
- 如果业务后端与判题服务不在同一台机器，需修改 `judge.py` 中的 `JUDGE_SERVICE_URL` 为实际地址（默认 `http://localhost:8080/judge`）。
- 由于每次判题都会启动一个新容器，**并发判题时可能有一定延迟**（约 2~3 秒/次），建议业务层控制并发量或使用容器池优化。
- 多条 SQL 语句用分号 `;` 分隔，但**不支持 SQL 字符串内部包含分号**（极少数情况），如有需要请将复杂语句合并为单条或使用存储过程。

---

## 8. 集成到业务后端

业务后端（Django）只需调用 `judge.py` 中的 `judge_submission` 函数即可：

```python
from apps.submissions.judge import judge_submission

result = judge_submission(
    submitted_sql="SELECT name FROM users;",
    test_cases=[
        {"expected_output": "name\nAlice", "test_input": "INSERT INTO users ..."}
    ],
    create_table_sql="CREATE TABLE users ..."
)
```

该函数会同步等待判题结果，并返回与上述 API 响应一致的字典。

---

## 9. 常见问题

**Q：判题服务启动后提示 `docker.errors.DockerException`？**  
A：请确保 Docker Desktop 已启动，且当前用户有权限访问 Docker 守护进程。

**Q：判题超时如何调整？**  
A：在请求体中传递 `timeout` 字段（单位秒），或修改 `SQL_TIMEOUT` 常量后重启服务。

**Q：如何支持多个标准答案（多种正确写法）？**  
A：当前设计不支持。教师应在 `test_cases` 中配置多组不同的预期输出（每组对应一种正确答案），只要学生 SQL 输出与其中一组完全匹配，即可判为正确。
