SQL开窗函数是一种强大的数据分析工具，它允许在**保留原始行数据**的前提下，对一组相关行（称为"窗口"）进行聚合、排名或分析计算。与普通聚合函数（如SUM、AVG）不同，开窗函数不会将多行合并为一行，而是为每行添加一个计算结果列。


### 一、基本语法
开窗函数的核心结构是：
```sql
函数名(列名) OVER (
  [PARTITION BY 分组列]  -- 可选：将数据分成多个窗口（类似GROUP BY，但不合并行）
  [ORDER BY 排序列]      -- 可选：窗口内的行排序
  [ROWS/RANGE 窗口框架]  -- 可选：定义窗口内参与计算的行范围
)
```
其中，`OVER()`是开窗函数的标志，括号内的部分称为**窗口子句**。


### 二、窗口子句详解
#### 1. PARTITION BY（分组）
将数据按指定列分成多个独立窗口，每个窗口内单独计算。  
**示例**：按地区分组，计算每个地区的总销售额（保留原始行）：
```sql
SELECT region, month, amount,
       SUM(amount) OVER (PARTITION BY region) AS total_region_sales
FROM sales;
```

#### 2. ORDER BY（排序）
对窗口内的行排序，通常配合累计计算或排名。  
**默认行为**：排序后，窗口框架自动设为`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`（累计到当前行）。  
**示例**：按地区分组、月份排序，计算累计销售额：
```sql
SELECT region, month, amount,
       SUM(amount) OVER (PARTITION BY region ORDER BY month) AS cumulative_sales
FROM sales;
```

#### 3. ROWS/RANGE（窗口框架）
定义窗口内参与计算的行范围（仅在ORDER BY后生效）：
- **ROWS**：按物理行数范围（如前N行、后N行）  
  例：`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`（当前行+前2行）
- **RANGE**：按值范围（如日期前后N天）  
  例：`RANGE BETWEEN INTERVAL '1' DAY PRECEDING AND CURRENT ROW`

**常见简写**：
- `ORDER BY ...` → 默认累计到当前行
- `PARTITION BY ...` → 默认整个分组为窗口


### 三、常见开窗函数分类
#### 1. 聚合类开窗函数
复用普通聚合函数，在窗口内计算：  
`SUM()`、`AVG()`、`COUNT()`、`MAX()`、`MIN()`

**示例**：计算每个地区的平均销售额：
```sql
SELECT region, month, amount,
       AVG(amount) OVER (PARTITION BY region) AS avg_region_sales
FROM sales;
```

#### 2. 排名类开窗函数
专门用于生成排名，无普通聚合版本：
- **ROW_NUMBER()**：窗口内分配唯一连续序号（无并列）
- **RANK()**：允许并列，并列后序号跳空（如1,1,3）
- **DENSE_RANK()**：允许并列，并列后序号不跳空（如1,1,2）
- **NTILE(n)**：将窗口内的行分成n个桶，每个桶行数尽量相等

**示例**：学生成绩排名（按科目分组）：
```sql
SELECT subject, student, score,
       ROW_NUMBER() OVER (PARTITION BY subject ORDER BY score DESC) AS rn,
       RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS rk,
       DENSE_RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS drk
FROM scores;
```

#### 3. 分析类开窗函数
用于获取窗口内其他行的数据：
- **LAG(col, n, default)**：获取当前行前n行的col值（无则用default）
- **LEAD(col, n, default)**：获取当前行后n行的col值
- **FIRST_VALUE(col)**：窗口内第一行的col值
- **LAST_VALUE(col)**：窗口内最后一行的col值（需指定完整框架）

**示例**：计算销售额环比（上月对比）：
```sql
SELECT region, month, amount,
       LAG(amount,1,0) OVER (PARTITION BY region ORDER BY month) AS prev_month,
       (amount - LAG(amount,1,0))/LAG(amount,1,1) AS mom_growth -- 环比增长率
FROM sales;
```


### 四、典型应用场景
1. **累计求和/平均**：如用户消费累计、月度业绩累计。
2. **Top N问题**：如每个地区销售额前3的商品（用ROW_NUMBER+子查询过滤）。
3. **移动统计**：如最近7天的平均气温（用ROWS框架）。
4. **同比环比**：用LAG/LEAD获取历史数据对比。
5. **排名**：如考试成绩排名、员工绩效排名。


### 五、注意事项
- **执行顺序**：开窗函数在`WHERE/GROUP BY/HAVING`之后、`ORDER BY`之前执行，因此无法直接在`WHERE`中使用结果（需用子查询/CTE过滤）。
- **数据库支持**：MySQL 8.0+/PostgreSQL/Oracle/SQL Server均支持，老版本MySQL（5.x）无此功能。
- **窗口框架**：使用`LAST_VALUE`时需显式指定完整框架（如`ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`），否则默认仅计算到当前行。


通过开窗函数，你可以高效地完成复杂的数据分析任务，避免繁琐的自连接或变量操作。掌握它能大幅提升SQL
@所有人