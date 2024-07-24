[TOC]

## Easy

### [175. Combine Two Tables](https://leetcode.com/problems/combine-two-tables/)

关键点：join两个表

```sql
SELECT p1.firstName, p1.lastName, a1.city, a1.state
FROM Person p1
LEFT JOIN Address a1
ON p1.personId = a1.personId;
```

### [181. Employees Earning More Than Their Managers](https://leetcode.com/problems/employees-earning-more-than-their-managers/)

关键点：inner join，注意命名使得代码语义更加清晰

```sql
SELECT e.name AS Employee
FROM Employee e
INNER JOIN Employee m
ON e.managerId = m.id
WHERE e.salary > m.salary;
```

### [182. Duplicate Emails](https://leetcode.com/problems/duplicate-emails/)

关键点：注意having和where的区别，group by后边使用having

```sql
SELECT email AS Email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

### [183. Customers Who Never Order](https://leetcode.com/problems/customers-who-never-order/)

关键点：not in后边应该跟select子查询，而不是具体的某一列

```sql
-- 第一种方法，使用not in
SELECT name AS Customers
FROM Customers
WHERE Customers.id NOT IN (SELECT customerId FROM Orders);
```

```sql
# 第二种方法，左连接，选择右侧为空的
SELECT c.name AS Customers 
FROM Customers c LEFT JOIN Orders o 
ON c.id=o.customerId 
WHERE o.customerId IS NULL;
```

### [196. Delete Duplicate Emails](https://leetcode.com/problems/delete-duplicate-emails/)

关键点：自连接的原理，delete语句的写法

```sql
# 第一种写法
DELETE p2
FROM Person p1
INNER JOIN Person p2
ON p1.email = p2.email
WHERE p2.id > p1.id;
```

```sql
# 第二种写法
DELETE p1 
FROM Person p1, Person p2
WHERE p1.Email = p2.Email AND p1.Id > p2.Id;
```

```sql
-- 可能只能在SQL中运行，MySQL不行
DELETE FROM Person
WHERE Person.email > (
    SELECT MIN(p2.id)
    FROM Person p2
    WHERE p2.email = Person.email
);
```

#### 如何理解SQL中的自连接？

自连接是两张表结构和数据内容完全相同的表，在做处理时，我们通常会给他们分别重命名来加以区分，然后进行关联。自连接实际上涉及的是同一张表的两个不同实例。

示例表内容：

有如下一张表Student，结构和数据如下：

![1](./images/1.png)

当我们进行自连接时，不加任何过滤条件，具体如下：

```sql
SELECT  
s1.Sname AS Sname1,
s2.Sname AS Sname2
FROM Student s2,Student s1
```

得到的结果是这样的，其实就是类似于数学上的排列：

![2](./images/2.png)

我们常见的自连接是有条件的，实际上是在上边的结果上进行过滤。

比如我们想得到一一对应的数据：

```sql
SELECT  
s1.Sname AS Sname1,
s2.Sname AS Sname2
FROM Student s2,Student s1
WHERE s1.Sname=s2.Sname
```

得到的结果就是两个自连接的表一一对应：

![3](./images/3.png)

这里就是自连接的精髓，张三自己和自己进行了关联。

但是在工作中，使用自连接的目的不是和自己关联，而是和表中的其他进行组合：

```sql
SELECT  
s1.Sname AS Sname1,
s2.Sname AS Sname2
FROM Student s2,Student s1
WHERE s1.Sname<>s2.Sname
```

![4](./images/4.png)

此外，如果我们想进一步除掉重复的数据行，比如（张三，李四）和（李四，张三）。

```sql
SELECT  
s1.Sname AS Sname1,
s2.Sname AS Sname2
FROM Student s2,Student s1
WHERE s1.Sname>s2.Sname
```

![5](./images/5.png)

现在我们删除如下表中重复的数据行，应该如何书写？

![6](./images/6.png)

我们可以发现这个表没有主键，因此我们可以使用自增长函数INDENTIFY()来生成一个类似于自增主键的ID，并将结果插入到Student_Tmp中：

```sql
SELECT 
IDENTITY(INT) ID,
Sname,
Score
INTO Student_Tmp
FROM Student
```

> Note: SELECT INTO是一种用于将查询的结果插入到新表中的语句
>
> ```sql
> SELECT column1, column2
> INTO new_table
> FROM existing_table
> WHERE condition;
> ```

我们使用自增长函数来生成了一个类似于自增主键的ID，并且将结果插入到Student_Tmp，其中具体内容如下：

![7](./images/7.png)

然后我们可以通过保留最大值或者最小值的方法来删除重复项。

```sql
DELETE FROM Student_Tmp
WHERE Student_Tmp.ID< (
            SELECT Max(s2.ID)
            FROM Student_Tmp s2
            WHERE Student_Tmp.Sname=s2.Sname
            AND Student_Tmp.Score=s2.Score
);
```

DELETE 语句有一个问题，因为 DELETE 语句不支持给表指定别名。要删除表中满足条件的行，你需要直接引用表名，而不是使用别名。

### [197. Rising Temperature](https://leetcode.com/problems/rising-temperature/)

关键点：自连接挑选，注意datediff(date1, date2)是date1-date2.

```sql
-- 第一种写法
SELECT w1.id
FROM Weather w1
JOIN Weather w2
ON DATEDIFF(w1.recordDate, w2.recordDate) = 1
WHERE w1.temperature > w2.temperature;
```

```sql
-- 自连接的特色写法
SELECT w1.id
FROM Weather w1, Weather w2
WHERE DATEDIFF(w1.recordDate, w2.recordDate) = 1 AND w1.temperature > w2.temperature;
```

### [511. Game Play Analysis I](https://leetcode.com/problems/game-play-analysis-i/)

```sql
SELECT player_id, MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id;
```

### [577. Employee Bonus](https://leetcode.com/problems/employee-bonus/)

关键点：没有注意审题，没有注意NULL的判断；使用了JOIN而不是LEFT JOIN，没有思考到有可能Bonus只存在部分雇员的bonus，所以还是审题问题。

```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b
ON e.empId = b.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```

### [584. Find Customer Referee](https://leetcode.com/problems/find-customer-referee/)

关键点：我们可以使用NOT IN代替!=来提高运行速度

```sql
SELECT name
FROM Customer
WHERE referee_id IS NULL OR referee_id != 2;
```

```sql
SELECT name
FROM Customer
WHERE referee_id IS NULL OR referee_id NOT IN (2);
```

### [586. Customer Placing the Largest Number of Orders](https://leetcode.com/problems/customer-placing-the-largest-number-of-orders/)

关键点：思路很重要，既然只有一个是订单最多的，那么直接排序选第一个即可，注意ORDER BY COUNT的思路。

```sql
SELECT o1.customer_number
FROM Orders o1
GROUP BY o1.customer_number
ORDER BY COUNT(*) DESC
LIMIT 1;
```

### [595. Big Countries](https://leetcode.com/problems/big-countries/)

```sql
SELECT name, population, area
FROM World
WHERE area >= 3000000 OR population >= 25000000;
```

### [596. Classes More Than 5 Students](https://leetcode.com/problems/classes-more-than-5-students/)

```sql
SELECT class
FROM Courses
GROUP BY class
HAVING COUNT(*) >= 5;
```

### [607. Sales Person](https://leetcode.com/problems/sales-person/)

关键点：子查询，NOT IN

```sql
SELECT s1.name
FROM SalesPerson s1
WHERE s1.sales_id NOT IN (
    SELECT o1.sales_id
    FROM Orders o1
    JOIN Company c1
    ON o1.com_id = c1.com_id
    WHERE name = 'RED'
);
```

### [610. Triangle Judgement](https://leetcode.com/problems/triangle-judgement/)

关键点：Yes和No记得加引号，三角形判断的条件是任意三条边之和大于第三边

```sql
-- 使用CASE WHEN
SELECT x, y, z, (CASE WHEN x+y>z AND y+z>x AND x+z>y THEN 'Yes' ELSE 'No' END) AS triangle
FROM Triangle;
```

>Note: IF(condition, value_if_true, value_if_false)

```sql
-- 使用IF
SELECT *, IF(x+y>z AND y+z>x AND z+x>y, "Yes", "No") AS triangle 
FROM Triangle;
```

### [619. Biggest Single Number](https://leetcode.com/problems/biggest-single-number/)

关键点：SQL的执行顺序

```sql
-- 错误的代码，从每个出现一次的分组中选出了最大值，而不是所有出现一次的数字的最大值
SELECT MAX(num) AS num
FROM MyNumbers
GROUP BY num
HAVING COUNT(*) = 1;
```

```sql
-- 正确的写法，利用子查询，先找出只出现一次的数字，再选出最大值
SELECT MAX(num) AS num
FROM (
    SELECT num
    FROM MyNumbers
    GROUP BY num
    HAVING COUNT(*) = 1
) AS unique_nums;
```

> 当 SQL 查询被执行时，通常会遵循以下步骤，这些步骤构成了查询的执行顺序：
>
> 1. **FROM**：首先，执行 FROM 子句，该子句指定要从中检索数据的表或子查询。数据库引擎从这些表或子查询中获取所有的行和列。
> 2. **WHERE**：接下来，执行 WHERE 子句，该子句用于筛选在 FROM 子句中检索的数据。只有满足 WHERE 子句中条件的行才会被包含在结果中。
> 3. **GROUP BY**：如果查询包含 GROUP BY 子句，则根据 GROUP BY 子句中指定的列对数据进行分组。
> 4. **HAVING**：如果查询包含 HAVING 子句，则根据 HAVING 子句中指定的条件对分组进行筛选。只有满足 HAVING 子句中条件的分组才会被包含在结果中。
> 5. **SELECT**：执行 SELECT 子句，该子句用于选择要返回的列，计算新的列，或者对数据进行聚合操作。
> 6. **ORDER BY**：如果查询包含 ORDER BY 子句，则根据 ORDER BY 子句中指定的列对结果进行排序。
> 7. **LIMIT/OFFSET**：最后，如果查询包含 LIMIT 或 OFFSET 子句，则根据这些子句来限制返回的行数或跳过指定数量的行。

此处还有一个需要注意的点就是，为什么不能使用limit 1来取最大值。题目的要求是“如果没有只出现一次的数字，就输出null”，也就是说，当我们查询的结果为空时，我们需要输出null。这里我们总结了一个表格（以下内容参考链接：https://leetcode.cn/problems/biggest-single-number/solutions/683252/dang-biao-ge-wei-kong-shi-ru-he-fan-hui-6qpzg）

![8](./images/8.png)

此处需要强调的是，空表示表格没有任何输出，null表示输出为null。我们可以理解为表格中一行都没有（空）和表格中有记录但是值都是null。

我们使用如下的数据集：

```sql
CREATE TABLE IF NOT EXISTS my_numbers (num INT);
TRUNCATE TABLE my_numbers
INSERT INTO my_numbers (num) VALUES ('8');
INSERT INTO my_numbers (num) VALUES ('8');
INSERT INTO my_numbers (num) VALUES ('3');
INSERT INTO my_numbers (num) VALUES ('3');
INSERT INTO my_numbers (num) VALUES ('4');
INSERT INTO my_numbers (num) VALUES ('4');
INSERT INTO my_numbers (num) VALUES ('5');
INSERT INTO my_numbers (num) VALUES ('5');
```

![9](./images/9.png)

1. 使用聚合函数对空值进行处理时，SUM/AVG/MAX/MIN都会返回null值。首先我们根据题意，给出一个无法输出null的代码：

   ```sql
   #代码1.1
       select num
       from my_numbers 
       group by num
       having count(num)=1
       order by num desc
       limit 0,1
   ```

   返回的表格为空

   这时我们在外层加一个select尝试聚合函数：

   ```sql
   SELECT SUM(num) sum_num, AVG(num) avg_num, MAX(num) max_num,MIN(num) min_num
   FROM (
   	SELECT num
   	FROM my_numbers 
   	GROUP BY num
   	HAVING COUNT(num)=1
   	ORDER BY num DESC
   	LIMIT 0,1
   ) t1
   ```

   得到的结果可以返回null值，也就是说，只要表格为空，加入任何聚合函数，我们都可以得到null的结果。：

   ![10](./images/10.png)

2. 使用ifnull对空值进行处理，实际上不是ifnull起作用。

   ```sql
   #代码2.1
   select ifnull((select max(num)
   from my_numbers
   group by num
   having count(*) = 1
   Order by num DESC
   limit 1), null) num
   ```

   实际上我们不建议使用ifnull来处理并输出null值，原因如下：

   - ifnull函数定位：用于判断第一个表达式是否为null，如果为null就返回第二个参数的值，如果不为null就返回第一个参数的值。

     ```sql
     IFNULL(expression, alt_value)
     ```

     这就意味着，如果expression为null，才会返回alt_value的值。按照ifnull函数的运行逻辑，要使得代码能够输出alt_value，其实expression本身就应该为null值，然而根据上边的代码，我们知道ifnull的第一个参数实际上为空，函数ifnull其实没有起到任何作用。那么我们可能会有疑问，是否ifnull的第一个参数为空时，仍然可以输出第二个参数的值？

     ```sql
     #代码2.2
     SELECT IFNULL(t1.num,NULL) ifnull_num
     FROM(
     	SELECT num
     	FROM my_numbers 
     	GROUP BY num
     	HAVING COUNT(num)=1
     	ORDER BY num DESC
     	LIMIT 0,1
     ) t1
     ```

     此时输出的结果仍然为空：

     ![11](./images/11.png)

     那么为什么代码2.1和2.2输出的结果不同？其实差别在select语句上。

     3. 使用select对空值进行处理，观察代码2.1可以发现，代码1.1的结构被放在了select语句中，而不是from语句中，这样的放置会导致最后的结果不同。

        ```sql
        #代码3.1 将代码1.1放置在from后，再从虚拟表中选择num
        SELECT num
        FROM(
        	SELECT num
        	FROM my_numbers 
        	GROUP BY num
        	HAVING COUNT(num)=1
        	ORDER BY num DESC
        	LIMIT 0,1
        ) t1
        ```

        ![12](./images/12.png)

        可以发现，如果这样排列我们的代码，我们得到的值仍然为空，但是如果我们将整块代码写在select中：

        ```sql
        #代码3.2 将代码1.1直接放置在select中
        SELECT(
        	SELECT num
        	FROM my_numbers 
        	GROUP BY num
        	HAVING COUNT(num)=1
        	ORDER BY num DESC
        	LIMIT 0,1
        ) select_num
        ```

        ![13](./images/13.png)

        我们得到了null值，因此如果我们在select语句中写入空值，直接运行select语句，我们将会得到null值。

        总结：

        - select 空 param1 -> param1：null
        - select param1 from 空 —> param1：空

     4. limit语句不会输出新的null值，除非表格中本身就存在null值，因为limit语句对表格只是进行截取，如我们的代码1.1所示，输出值为空，也印证了这一点。

     5. where语句所带来的限制条件并不会输出新的null值，除非表格中本身就存在null，同理having也一样。这里我们可以测试一下：

        ```sql
        #代码5.1
        SELECT num
        FROM my_numbers 
        WHERE num IS NULL
        ```

        从我们的测试集中，我们知道数据是不包含null值的，那么在这样的条件下，我们的输出依旧为空。

        ![14](./images/14.png)

        也就是说，当数据库中无法匹配当前条件时，输出的数据行是空而非null的。

     总结：

     - 可以使用聚合函数进行空值null值的转换，具体的聚合函数包括SUM/AVG/MAX/MIN
     - 可以使用select语句进行转换，但空值应直接写在select中而非from中
     - limit语句无法出现新的null值
     - where和having同样无法出现新的null值

### [620. Not Boring Movies](https://leetcode.com/problems/not-boring-movies/)

```sql
SELECT *
FROM Cinema
WHERE id % 2 = 1 AND description != "boring"
ORDER BY rating DESC;
```

```sql
SELECT *
FROM Cinema
WHERE MOD(id, 2) = 1 AND description != "boring"
ORDER BY rating DESC;
```

> Note: is not 和!=的区别在于， !=用于两个非null值不相等时返回true , is not 通常用于特殊比较is not null ； is not true。
> 例如：
> select true is not true #会返回0
> select false is not true #会返回1 

### [627. Swap Salary](https://leetcode.com/problems/swap-salary/)

关键点：UPDATE，CASE WHEN, IF

> CASE
>     WHEN condition1 THEN value1
>     WHEN condition2 THEN value2
>     ...
>     ELSE default_value
> END

```sql
UPDATE Salary
SET sex = (CASE WHEN sex='f' THEN 'm' ELSE 'f' END);
```

> UPDATE table_name
> SET column1 = value1, column2 = value2, ...
> WHERE condition;

```sql
UPDATE Salary
SET sex = IF(sex='f', 'm', 'f');
```

> IF(condition, value_if_true, value_if_false)

### [1050. Actors and Directors Who Cooperated At Least Three Times](https://leetcode.com/problems/actors-and-directors-who-cooperated-at-least-three-times/)

```sql
SELECT actor_id, director_id
FROM ActorDirector
GROUP BY actor_id, director_id
HAVING COUNT(*) >= 3;
```

### [1068. Product Sales Analysis I](https://leetcode.com/problems/product-sales-analysis-i/)

```sql
SELECT s.year, s.price, p.product_name
FROM Sales s
LEFT JOIN Product p
ON s.product_id = p.product_id;
```

### [1075. Project Employees I](https://leetcode.com/problems/project-employees-i/)

```sql
SELECT p.project_id, ROUND(AVG(e.experience_years), 2) AS average_years
FROM Project p
LEFT JOIN Employee e
ON p.employee_id = e.employee_id
GROUP BY p.project_id;
```

### [1084. Sales Analysis III](https://leetcode.com/problems/sales-analysis-iii/)

关键点：需要所有的订单都是在时间范围内的

```sql
SELECT p.product_id, p.product_name
FROM Product p
JOIN Sales s
ON p.product_id = s.product_id
GROUP BY p.product_id
HAVING MIN(s.sale_date) >= '2019-01-01' AND MAX(s.sale_date) <= '2019-03-31';
```

### [1141. User Activity for the Past 30 Days I](https://leetcode.com/problems/user-activity-for-the-past-30-days-i/)

关键点：DISTINCT，查阅30天活跃用户数量。注意边界值的设定，假如说规定一天，那就是>=0, <1，因为只有7-27当天；同理，<30 AND >= 0。

```sql
SELECT activity_date AS day, COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE DATEDIFF('2019-07-27', activity_date) < 30 
			AND DATEDIFF('2019-07-27', activity_date) >= 0
GROUP BY activity_date;
```

### [1148. Article Views I](https://leetcode.com/problems/article-views-i/)

```sql
SELECT DISTINCT author_id AS id
FROM Views
WHERE author_id = viewer_id
ORDER BY id ASC;
```

### [1179. Reformat Department Table](https://leetcode.com/problems/reformat-department-table/)

关键点：行转列写法，CASE WHEN/IF函数的用法，聚合函数

```sql
SELECT id, 
SUM(CASE WHEN month='Jan' THEN revenue END) AS Jan_Revenue,
SUM(CASE WHEN month='Feb' THEN revenue END) AS Feb_Revenue,
SUM(CASE WHEN month='Mar' THEN revenue END) AS Mar_Revenue,
SUM(CASE WHEN month='Apr' THEN revenue END) AS Apr_Revenue,
SUM(CASE WHEN month='May' THEN revenue END) AS May_Revenue,
SUM(CASE WHEN month='Jun' THEN revenue END) AS Jun_Revenue,
SUM(CASE WHEN month='Jul' THEN revenue END) AS Jul_Revenue,
SUM(CASE WHEN month='Aug' THEN revenue END) AS Aug_Revenue,
SUM(CASE WHEN month='Sep' THEN revenue END) AS Sep_Revenue,
SUM(CASE WHEN month='Oct' THEN revenue END) AS Oct_Revenue,
SUM(CASE WHEN month='Nov' THEN revenue END) AS Nov_Revenue,
SUM(CASE WHEN month='Dec' THEN revenue END) AS Dec_Revenue
FROM department
GROUP BY id
ORDER BY id;
```

```sql
SELECT id,
    MAX(IF(`month`='Jan',revenue,NULL)) Jan_Revenue,
    MAX(IF(`month`='Feb',revenue,NULL)) Feb_Revenue,
    MAX(IF(`month`='Mar',revenue,NULL)) Mar_Revenue,
    MAX(IF(`month`='Apr',revenue,NULL)) Apr_Revenue,
    MAX(IF(`month`='May',revenue,NULL)) May_Revenue,
    MAX(IF(`month`='Jun',revenue,NULL)) Jun_Revenue,
    MAX(IF(`month`='Jul',revenue,NULL)) Jul_Revenue,
    MAX(IF(`month`='Aug',revenue,NULL)) Aug_Revenue,
    MAX(IF(`month`='Sep',revenue,NULL)) Sep_Revenue,
    MAX(IF(`month`='Oct',revenue,NULL)) Oct_Revenue,
    MAX(IF(`month`='Nov',revenue,NULL)) Nov_Revenue,
    MAX(IF(`month`='Dec',revenue,NULL)) Dec_Revenue
FROM Department 
GROUP BY id;
```

重写部门表格，部门id和每个月的收入。部门id可以通过GROUP BY方法，根据部门id来统计收入时，中间需要有这样一步，SQL每次执行查询，除了统计该月份有的数据，还会统计其他月份，它们都是NULL。所以最后还需要一个聚合函数（SUM/MAX）来把每次查询的数据按照id汇总，这才是月收入。

此处我们举个例子了解一下SQL语句查询的执行步骤：

```sql
SELECT col_1, col_2, COUNT(*) as num                  #顺序5
FROM table_1 JOIN table_2 ON table_1.id = table_2.id  #顺序1
WHERE col_3 > 2.90                                    #顺序2
GROUP BY table_1.id                                   #顺序3
HAVING num > 2                                        #顺序4
ORDER BY num DESC                                     #顺序6
LIMIT 2                                               #顺序7
```

![row](./images/row.png)

如果不使用聚合函数，我们看到的就是步骤2这样的表，但是这显然不符合分组要求，就会报错。所以最后要使用sum或者MAX来聚合。

那么现在来到另一个问题，如何理解GROUP BY和聚合函数。

我们不能写成select * from Table group by id，为什么不能用*而是一定要用某个列的聚合函数呢。这是因为，在分组之后，单元格中会存在多个值，关系数据库是基于关系的，单元格中不允许存在多个值，因此会报错。

### [1211. Queries Quality and Percentage](https://leetcode.com/problems/queries-quality-and-percentage/)

关键点：SUM和COUNT还是分不清，query_name可能存在NULL

```sql
-- 规范写法，使用CASE WHEN或者IF
SELECT query_name, ROUND(AVG(rating/position), 2) AS quality, ROUND(SUM(IF(rating<3, 1, 0))*100/COUNT(*), 2) AS poor_query_percentage
FROM Queries
WHERE query_name IS NOT NULL
GROUP BY query_name;
```

```sql
-- 简略写法
SELECT query_name, ROUND(AVG(rating/position), 2) AS quality, ROUND(SUM(rating<3)*100/COUNT(*), 2) AS poor_query_percentage
FROM Queries
WHERE query_name IS NOT NULL
GROUP BY query_name;
```

```sql
-- 使用AVG
SELECT query_name, ROUND(AVG(rating/position), 2) AS quality, ROUND(AVG(rating < 3) * 100, 2) AS poor_query_percentage
FROM Queries
WHERE query_name IS NOT NULL
GROUP BY query_name;
```

不能直接COUNT(rating<3)，因为rating<3返回的结果为true或者false，不能直接计数

### [1484. Group Sold Products By The Date](https://leetcode.com/problems/group-sold-products-by-the-date/)

关键点：使用GROUP_CONCAT()进行字符串拼接，注意两个distinct

```sql
SELECT 
    sell_date,
    COUNT(DISTINCT product) AS num_sold,
    GROUP_CONCAT(DISTINCT product ORDER BY product SEPARATOR ',') AS products
FROM 
    Activities
GROUP BY 
    sell_date;
```

> Note: GROUP_CONCAT(expression [ORDER BY expression] [SEPARATOR separator])

此处我们对product进行拼接，并按照product的字典序排序。

### [1251. Average Selling Price](https://leetcode.com/problems/average-selling-price/)

关键点：LEFT JOIN，IFNULL添加的位置不正确，一开始添加在了SUM的内层

```sql
SELECT p.product_id, IFNULL(ROUND(SUM(p.price*u.units)/SUM(u.units), 2), 0) AS average_price
FROM Prices p
LEFT JOIN UnitsSold u
ON p.product_id = u.product_id AND u.purchase_date >= p.start_date AND u.purchase_date <= p.end_date
GROUP BY p.product_id;
```

### [1280. Students and Examinations](https://leetcode.com/problems/students-and-examinations/)

关键点：JOIN最好写全称笛卡尔积CROSS JOIN，而且，用错了聚合函数！我对id进行了sum，这显然是大错特错，应该返回的是行数之和！而且count对NULL行不计数。

```sql
-- 第一种写法，先全连接再左连接
SELECT stu.student_id, stu.student_name, sub.subject_name, COUNT(exam.student_id) AS attended_exams
FROM Students stu
JOIN Subjects sub
LEFT JOIN Examinations exam
ON stu.student_id = exam.student_id AND sub.subject_name = exam.subject_name
GROUP BY stu.student_id, sub.subject_name
ORDER BY stu.student_id, sub.subject_name;
```

```sql
-- 第二种写法，
SELECT s.student_id, s.student_name, sub.subject_name, COALESCE(e.attended_exams, 0) AS attended_exams
FROM Students s
CROSS JOIN Subjects sub
LEFT JOIN (
    SELECT student_id, subject_name, COUNT(*) AS attended_exams
    FROM Examinations
    GROUP BY student_id, subject_name
) e ON s.student_id = e.student_id AND sub.subject_name = e.subject_name
ORDER BY s.student_id, sub.subject_name;
```

> Note: COALESCE 是 SQL 中的一个函数，用于处理 NULL 值。它接受多个参数，并返回参数列表中的第一个非 NULL 值。如果所有参数都是 NULL，则返回 NULL。
>
> ```sql
> COALESCE(value1, value2, ...)
> ```

首先从Examinations表分组算出每个人参加每个考试的次数，再进行JOIN。

### [1327. List the Products Ordered in a Period](https://leetcode.com/problems/list-the-products-ordered-in-a-period/)

关键点：闰年是能被4整除但不能被100整除，或者能被400整除。

```sql
SELECT p.product_name, SUM(o.unit) AS unit
FROM Products p
JOIN Orders o
ON p.product_id = o.product_id
WHERE o.order_date BETWEEN '2020-02-01' AND '2020-02-29'
GROUP BY p.product_id
HAVING SUM(o.unit) >= 100;
```

### [1378. Replace Employee ID With The Unique Identifier](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/)

```sql
SELECT e2.unique_id, e1.name
FROM Employees e1
LEFT JOIN EmployeeUNI e2
ON e1.id = e2.id;
```

### [1407. Top Travellers](https://leetcode.com/problems/top-travellers/)

```sql
SELECT u.name, SUM(IFNULL(r.distance, 0)) AS travelled_distance
FROM Users u
LEFT JOIN Rides r
ON u.id = r.user_id
GROUP BY r.user_id
ORDER BY travelled_distance DESC, u.name ASC;
```

此处我们在SUM中使用IFNULL判断是否为空，如果为空则设为0.

### [1517. Find Users With Valid E-Mails](https://leetcode.com/problems/find-users-with-valid-e-mails/)

```sql
SELECT product_id
FROM Products
WHERE low_fats = 'Y' AND recyclable = 'Y';
```

### [1587. Bank Account Summary II](https://leetcode.com/problems/bank-account-summary-ii/)

```sql
SELECT u.name, SUM(amount) AS balance
FROM Users u
LEFT JOIN Transactions t
ON u.account = t.account
GROUP BY u.account
HAVING SUM(t.amount) > 10000;
```

这里实际上HAVING已经进行筛选了，并且如果一列中存在NULL值，SUM直接不对该行进行加和，也就是说，SUM能够很好地处理NULL值的情况，所以这里可以不使用IFNULL。

### [1633. Percentage of Users Attended a Contest](https://leetcode.com/problems/percentage-of-users-attended-a-contest/)

```sql
SELECT contest_id, ROUND(COUNT(user_id) * 100 / (SELECT COUNT(*) FROM Users), 2) AS percentage
FROM Register
GROUP BY contest_id
ORDER BY percentage DESC, contest_id ASC;
```

### [1661. Average Time of Process per Machine](https://leetcode.com/problems/average-time-of-process-per-machine/)

```sql
SELECT machine_id, 
    ROUND(SUM(CASE WHEN activity_type = 'start' THEN (-1)*timestamp ELSE timestamp END) * 2 / COUNT(*), 3) AS processing_time
FROM Activity
GROUP BY machine_id;
```

我感觉我的方法比自连接好捏～

### [1517. Find Users With Valid E-Mails](https://leetcode.com/problems/find-users-with-valid-e-mails/)

关键点：正则表达式，转义字符在mysql中是两个斜杠

`REGEXP`是正则表达式的意思：

- ^表示以后边的字符为开头
- []表示括号内任意字符
  - [0-9]表示一个字符范围，匹配从0到9的任何字符
  - [^a-z]：这个变量匹配不在a到z范围内的任何字符，^用来否定字符范围，它在方括号内的含义与方括号外表示开始的含义不同
- -表示连续
- *表示重复前边任意字符任意次数
  - [a-z]*表示一个字符范围，匹配从a到z的任何字符0次或多次
  - [a-z]+表示一个字符范围，匹配从a到z的任何字符1次或多次
- .匹配任何一个字符
- \用来转义后面的特殊字符
- $表示以前面的字符结尾

```sql
SELECT *
FROM users
WHERE mail REGEXP '^[a-zA-Z][a-zA-Z0-9\\_\\.\\-]*\\@leetcode\\.com$'
```

此处我们也转义了'@'字符，因为它们在正则表达式中具有特殊意义。正则需要前面加\，mysql需要加两个\，一个正则要的，一个mysql要的。

### [1527. Patients With a Condition](https://leetcode.com/problems/patients-with-a-condition/)

关键点：正则表达式

```sql
SELECT *
FROM PATIENTS
WHERE CONDITIONS REGEXP '^DIAB1|\\sDIAB1';
```

而前缀存在分为2种：

I 类糖尿病位于第一个时: 以DIAB1开始，即CONDITIONS REGEXP '^DIAB1'
I 类糖尿病不是第一个时: 含有空格DIAB1，即CONDITIONS REGEXP '\sDIAB1'
所以答案很明显了

用正则表达式来匹配这2种情况就行

位于第一个时，用 ^ 匹配输入字符串的开始位置，即^DIAB1
不是第一个时，又符合前缀所以它属于代码后段的首位，即前面有空格与代码首段隔开，用 \s 匹配一个被视为白空格的空格或字符；
但要注意的是：多数正则表达式实现使用单个反斜杠转义特殊字符，一遍能使用这些字符本身，但是MySQL要求两个反斜杠（MySQL自己解释一个，正则表达式库解释另一个），所以是\sDIAB1

然后这2种情况只要满足一种即可，所以用 |
| 管道符号用于指定匹配字符串时要使用的替代模式；在由竖线分隔的一行模式中，竖线被解释为OR，匹配过程从最左侧的模式开始，在找到第一个匹配项时停止

参考链接：https://leetcode.cn/problems/patients-with-a-condition/solutions/2166550/mysqlzheng-ze-biao-da-shi-jian-dan-yun-y-pfwq/
### [1667. Fix Names in a Table](https://leetcode.com/problems/fix-names-in-a-table/)

关键点：字符串函数

考察字符串函数的用法：

- `CONCAT(str1, str2) :` 拼接字符串
- `UPPER(str) :` 字符串变成大写
- `LOWER(str) :` 字符串变成小写
- `LENGTH(str) :` 获取字符串的长度
- `LEFT(str,len) :` 获取字符串左边 len 个字符
- `RIGHT(str,len) :` 获取字符串右边 len 个字符
- `SUBSTR(str,start,len) :` 获取 str 中从 start 开始的 len 个字符

```sql
SELECT user_id, CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTR(name, 2))) as name
FROM Users
ORDER BY user_id;
```

### [1581. Customer Who Visited but Did Not Make Any Transactions](https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/)

```sql
SELECT v.customer_id, COUNT(*) AS count_no_trans
FROM Visits v
WHERE visit_id NOT IN (SELECT visit_id FROM Transactions)
GROUP BY v.customer_id;
```

### [1683. Invalid Tweets](https://leetcode.com/problems/invalid-tweets/)

关键点：字符串长度，用char_length()也行

```sql
SELECT tweet_id
FROM Tweets
WHERE LENGTH(content) > 15;
```

### [1693. Daily Leads and Partners](https://leetcode.com/problems/daily-leads-and-partners/)

```sql
SELECT date_id, make_name, COUNT(DISTINCT lead_id) AS unique_leads, COUNT(DISTINCT partner_id) AS unique_partners
FROM DailySales
GROUP BY date_id, make_name;
```

### [1729. Find Followers Count](https://leetcode.com/problems/find-followers-count/)

```sql
SELECT user_id, COUNT(*) AS followers_count
FROM Followers
GROUP BY user_id
ORDER BY user_id;
```

### [1731. The Number of Employees Which Report to Each Employee](https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/)

```sql
SELECT e2.employee_id, e2.name, COUNT(e1.employee_id) AS reports_count, ROUND(AVG(e1.age)) AS average_age
FROM Employees e1, Employees e2
WHERE e1.reports_to = e2.employee_id
GROUP BY e2.employee_id
ORDER BY e2.employee_id;
```

### [1741. Find Total Time Spent by Each Employee](https://leetcode.com/problems/find-total-time-spent-by-each-employee/)

```sql
SELECT event_day as day, emp_id, SUM(out_time - in_time) AS total_time
FROM Employees
GROUP BY event_day, emp_id;
```

### [2356. Number of Unique Subjects Taught by Each Teacher](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/)

```sql
SELECT teacher_id, COUNT(DISTINCT subject_id) AS cnt
FROM Teacher
GROUP BY teacher_id;
```

### [1789. Primary Department for Each Employee](https://leetcode.com/problems/primary-department-for-each-employee/)

关键点：使用UNION，当两种情况不好一起筛选时，或者使用subquery

```sql
SELECT employee_id, department_id
FROM Employee
WHERE primary_flag = 'Y'
UNION
SELECT employee_id, department_id
FROM Employee
GROUP BY employee_id
HAVING COUNT(*) = 1
```

```sql
SELECT DISTINCT employee_id, department_id
FROM Employee
WHERE employee_id IN (
    SELECT employee_id
    FROM Employee
    GROUP BY employee_id
    HAVING COUNT(*) = 1
  )
  OR primary_flag = 'Y'
ORDER BY employee_id;
```

### [1795. Rearrange Products Table](https://leetcode.com/problems/rearrange-products-table/)

关键点：行列互相转换，行转列使用SUM等聚合函数，列转行使用UNION。

1. 列转行

```sql
SELECT product_id, 'store1' AS store, store1 AS price FROM products WHERE store1 IS NOT NULL
UNION
SELECT product_id, 'store2' AS store, store2 AS price FROM products WHERE store2 IS NOT NULL
UNION
SELECT product_id, 'store3' AS store, store3 AS price FROM products WHERE store3 IS NOT NULL;
```

2. 列转行

```sql
SELECT 
  product_id,
  SUM(IF(store = 'store1', price, NULL)) 'store1',
  SUM(IF(store = 'store2', price, NULL)) 'store2',
  SUM(IF(store = 'store3', price, NULL)) 'store3' 
FROM
  Products1 
GROUP BY product_id ;
```

![15](./images/15.png)

![16](./images/16.png)

还有一点需要注意：group by 有一个原则,就是 select 后面的所有列中,没有使用聚合函数的列,必须出现在 group by 后面。

### [1873. Calculate Special Bonus](https://leetcode.com/problems/calculate-special-bonus/)

关键点：正则函数或者NOT LIKE

```sql
SELECT employee_id, (CASE WHEN name NOT REGEXP '^M' AND employee_id % 2 = 1 THEN salary ELSE 0 END) AS bonus
FROM Employees
ORDER BY employee_id;
```

或者使用`NOT LIKE "M%"`, CASE WHEN也可以换成IF，除此之外，还可以使用UNION，但是这里我觉得没有必要。

salary * ( employee_id%2 ) * ( name not like 'M%') as bonus 看到别人这个感觉挺巧妙，在 SQL 中，布尔表达式的结果通常是 1（表示True）或 0（表示False）。这是因为 SQL 使用整数来表示布尔值，其中 1 通常表示True，而 0 表示False。但是在日常工作逻辑中这种可能会不方便他人理解。

### [1890. The Latest Login in 2020](https://leetcode.com/problems/the-latest-login-in-2020/)

```sql
SELECT user_id, MAX(time_stamp) AS last_stamp
FROM Logins
WHERE YEAR(time_stamp) = 2020
GROUP BY user_id;
```

### [1965. Employees With Missing Information](https://leetcode.com/problems/employees-with-missing-information/)

关键点：UNION

```sql
SELECT employee_id FROM Employees WHERE employee_id NOT IN (SELECT employee_id FROM Salaries)
UNION 
SELECT employee_id FROM Salaries WHERE employee_id NOT IN (SELECT employee_id FROM Employees)
ORDER BY employee_id ASC
```

### [1978. Employees Whose Manager Left the Company](https://leetcode.com/problems/employees-whose-manager-left-the-company/)

```sql
SELECT employee_id
FROM Employees
WHERE salary < 30000 AND manager_id NOT IN (SELECT employee_id FROM Employees)
ORDER BY 1;
```

世纪难题，到底是NOT IN的子查询快，还是JOIN快

## Medium

### [176. Second Highest Salary](https://leetcode.com/problems/second-highest-salary/)

关键点：第二高的薪水

```sql
-- 这种写法只适用于这种情况
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```

```sql
-- 使用limit offset，适用情况较多
SELECT 
(SELECT DISTINCT salary
FROM Employee ORDER BY salary DESC
LIMIT 1 OFFSET 1)
AS SecondHighestSalary;
```

> Note: `LIMIT number_of_rows OFFSET offset_value`
>
> - `number_of_rows`是要返回的行数。
> - `offset_value`是要跳过的行数。

### [177. Nth Highest Salary](https://leetcode.com/problems/nth-highest-salary/)

关键点：使用UDF

```
CREATE FUNCTION functionName(param1 INT, param2 INT)
RETURNS INT
BEGIN
    DECLARE result INT;
    
    -- 函数逻辑
    SET result = param1 + param2;
    
    RETURN result;
END;
```

用户定义函数是一段预先定义好的SQL代码，可以接受参数并返回结果。这样的函数可以在SQL查询中像内置函数一样使用，使得重复的逻辑可以封装在函数中，提高代码的可维护性和可重用性。

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
SET N = N-1;
  RETURN (
      SELECT DISTINCT(salary) from Employee order by salary DESC
      LIMIT 1 OFFSET N    
  );
END
```

在MySQL中，你不能在`OFFSET`后直接使用算术表达式，例如`OFFSET N-1`。相反，你需要先计算出偏移量的值，然后将其传递给`OFFSET`。修正这个问题的方法是在`OFFSET`之前计算`N-1`，然后将结果传递给`OFFSET`。**limit后面只能够跟明确的数字，不能跟表达式。**

`LIMIT`用于限制返回结果集的行数，而`OFFSET`用于指定结果集的起始位置。

### [178. Rank Scores](https://leetcode.com/problems/rank-scores/)

关键点：窗口函数，从高到低排序，相等的分数排名相同，并且排名的数字不间断

参考这个写的很详细：

https://help.aliyun.com/zh/sls/user-guide/window-functions

https://juejin.cn/post/7007055860560216071

```
Input: 
Scores table:
+----+-------+
| id | score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+
Output: 
+-------+------+
| score | rank |
+-------+------+
| 4.00  | 1    |
| 4.00  | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.50  | 4    |
+-------+------+
```

*rank函数*：例子中显示5、5、5、8。即**当出现有并列名次的行，会占用下一个名次的位置**。比如正常排名是1，2，3，4，但如果前三名是并列的话，结果会是1，1，1，4。

*dense_rank函数*：例子中显示5、5、5、6。即**当出现有并列名次的行，不占用下一名次的位置**。比如正常排名是1，2，3，4，如果前3名是并列的话，结果会是1，1，1，2。

*row_number函数*：这个例子中是5、6、7、8。也就是**不考虑并列名次的情况**。如果前3名是并列的话，排名是正常的1，2，3，4。

所以按照题意这里应该选择dense_rank函数。

```sql
SELECT 
    score, 
    dense_rank() over (order by score DESC) AS 'rank'
FROM Scores
ORDER BY 'rank' DESC;
```

```sql
-- 语法
dense_rank() over (
    [partition by partition_expression]
    [order by order_expression]
)
```

| **参数**                            | **说明**                                               |
| ----------------------------------- | ------------------------------------------------------ |
| partition by *partition_expression* | 窗口分区，根据分区表达式将数据划分成不同的分区。       |
| order by *order_expression*         | 窗口排序，根据排序表达式对各个分区内的每一行进行排序。 |

### [180. Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/)

关键点：寻找连续出现至少三次的数字

参考链接：https://leetcode.cn/problems/consecutive-numbers/solutions/21537/sql-server-jie-fa-by-neilsons

```sql
SELECT DISTINCT num AS ConsecutiveNums
FROM(
SELECT id, num, 
    ROW_NUMBER() OVER(order by id) -
    ROW_NUMBER() OVER(partition by num order by id) AS SerialNumbersSubGroup
FROM Logs) AS Sub
GROUP BY num, SerialNumbersSubGroup
HAVING COUNT(1) >= 3
```

这种解法在官方更新测试用例之后不能通过，但是可以借鉴其思想。

首先我们先来读读题，题目中id是一个自增列，也就是说id是连续增加的，有可能会出现以下情况，这种情况中，id不连续，即使num是连续的也视为num没有“连续出现”：

<img src="./images/18.png" alt="18" style="zoom:50%;" />

那么我们可能会想，是不是把第一个数字改成id就可以了？也就是这种：

```sql
SELECT DISTINCT num AS ConsecutiveNums
FROM(
SELECT id, num, 
    id - ROW_NUMBER() OVER(partition by num order by id) AS SerialNumbersSubGroup
FROM Logs) AS Sub
-- 注意这里先使用num分组，再按照差值分组，因为只按照差值分组的时候可能会出现相等的巧合，如下图所示
GROUP BY num, SerialNumbersSubGroup
HAVING COUNT(1) >= 3
```

![5.png](./images/1616483373-sBYtbs-5.png)

结果出现了新的错误：

<img src="./images/19.png" alt="19" style="zoom: 50%;" />

这个报错是因为：现在使用的是BIGINT UNSIGNED，而结果中会出现负数，这超出了目前可处理的范围。

为了使问题更直观，我们在postgresql中进行试验。

```sql
CREATE TABLE Logs (
    id SERIAL PRIMARY KEY,
    num INT
);

INSERT INTO Logs (id, num) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 2),
(5, 1),
(6, 2),
(7, 2);

SELECT * FROM Logs;
```

```sql
SELECT *, ROW_NUMBER() OVER(partition by num order by id) AS SubGroup
FROM Logs;
```

<img src="./images/23.png" alt="截屏2024-05-09 23.00.31" style="zoom:50%;" />

可以看到，首先按照num分组，相同的分到一组，然后在组内分配row_number。

然后用id与subgroup相减：

```sql
SELECT *, id - SubGroup AS IdSubGroup
FROM (SELECT *, ROW_NUMBER() OVER(partition by num order by id) AS SubGroup
FROM Logs) sub
```



<img src="./images/24.png" alt="24" style="zoom:50%;" />

可以看到我们连续出现数字对应得到的差是相等的，也就回到了我们上边的答案，那么为什么会出现BIGINT超时的情况呢？我们用上边出错的例子进行试验：

<img src="./images/25.png" alt="25" style="zoom:50%;" />

我们可以看到，row_number是从1开始计数的，而id是从0开始的，则会出现差值为负数的情况，leetcode默认使用BIGINT UNSIGNED，则会出现报错。正确的方法就是添加一个CAST转换为SIGNED类型。

```sql
SELECT DISTINCT num AS ConsecutiveNums
FROM(
SELECT id, num, 
    id - CAST(ROW_NUMBER() OVER(partition by num order by id) AS SIGNED) AS SerialIdSubGroup
FROM Logs) AS Sub
GROUP BY num, SerialIdSubGroup
HAVING COUNT(1) >= 3
```

> Note: CAST函数进行类型转换，`CAST(expression AS data_type)`

对于整数值之间的减法，如果其中一个是 UNSIGNED 类型，而结果是负数，那么根据 MySQL 的规则，结果会被强制转换为无符号整数类型，并且被解释为最大整数值。所以会出现out of range的情况。**RANK(), DENSE_RANK(), ROW_NUMBER()函数返回的值类型是UNSIGNED INT(无符号的数值)。**UNSIGNED INT与UNSIGNED INT之间运算，结果的默认类型也是UNSIGNED。但是在此情景中，差值会出现负值(SIGNED INT)，因此会报错。需要先使用CAST()函数，转化成SIGNED INT再做减法。

> Note: **int默认为signed int**，它与unsigned int运算时，结果被转换为unsigned int

***发现一个宝藏：https://zhuanlan.zhihu.com/p/569793964***

### [184. Department Highest Salary](https://leetcode.com/problems/department-highest-salary/)

关键点：注意命名，rank是关键字，会导致错误，日常命名要避免这些。

```sql
SELECT Department, Employee, Salary
FROM (
    SELECT 
  		d.name AS Department, 
  		e.name AS Employee, e.salary AS Salary, 
  		DENSE_RANK() OVER(PARTITION BY d.id ORDER BY e.salary DESC) AS rk
    FROM Employee e
    JOIN Department d
    ON e.departmentId = d.id
) sub_rank
WHERE rk = 1;
```

```sql
select new.department,new.employee,new.salary
from(select d.name as department, e.name as employee, e.salary as salary, Max(e.salary) over (partition by d.id) as max_salary
from employee e join department d on e.departmentId = d.id
)as new
where new.salary = new.max_salary
```

所有的聚合函数都可以在窗口函数中使用，此处我们使用的是在每个窗口内寻找MAX。

```sql
sum() over (
    [partition by partition_expression]
    [order by order_expression]
    [frame]
)
```

| **参数**                            | **说明**                                                     |
| ----------------------------------- | ------------------------------------------------------------ |
| partition by *partition_expression* | 窗口分区，根据分区表达式将数据划分成不同的分区。             |
| order by *order_expression*         | 窗口排序，根据排序表达式对各个分区内的每一行进行排序。       |
| *frame*                             | 窗口框架，例如`range between unbounded preceding and unbounded following`。 |

### [550. Game Play Analysis IV](https://leetcode.com/problems/game-play-analysis-iv/)

关键点：没有理解题目的意思！

```sql
-- 一开始的错误解法
SELECT ROUND(COUNT(DISTINCT a1.player_id) / (SELECT COUNT(DISTINCT player_id) FROM Activity), 2) AS fraction
FROM Activity a1, Activity a2
WHERE a1.player_id = a2.player_id AND DATEDIFF(a2.event_date, a1.event_date) = 1;
```

题目的意思是，Write a solution to report the **fraction** of players that logged in again on the day after the day they **first logged in**. You need to count the number of players that logged in for at least two consecutive days starting from their **first login date**, then divide that number by the total number of players.

显然我们的做法只考虑了连续两天出现，而没有考虑只是在初次log in的第二天再次登录。也就是说，我们需要首先找到每个用户的首次登录时间。

```sql
-- 第一种做法，不使用窗口函数
SELECT ROUND(COUNT(DISTINCT a.player_id) / (SELECT COUNT(DISTINCT player_id) FROM Activity), 2) AS fraction
FROM Activity a
JOIN (SELECT player_id, MIN(event_date) AS first_login_date FROM Activity GROUP BY player_id) AS first_login
WHERE a.player_id = first_login.player_id AND DATEDIFF(a.event_date, first_login.first_login_date) = 1;
```

```sql
-- 第二种方法，使用窗口函数
SELECT ROUND(COUNT(new.player_id) / (SELECT COUNT(DISTINCT player_id) FROM activity), 2) AS fraction 
FROM (
    SELECT player_id, event_date, DENSE_RANK() OVER (PARTITION BY player_id ORDER BY event_date ASC) AS first_log
    FROM activity
) AS new 
JOIN activity AS a ON DATE_ADD(new.event_date, INTERVAL 1 DAY) = a.event_date
WHERE new.first_log = 1 AND new.player_id = a.player_id;
```

> Note：这里有一个需要注意的点，就是COUNT等聚合函数会导致返回结果只有一行，所以注意聚合函数的位置会不会影响其他列返回的结果。

### [570. Managers with at Least 5 Direct Reports](https://leetcode.com/problems/managers-with-at-least-5-direct-reports/)

```sql
SELECT e1.name
FROM Employee e1, Employee e2
WHERE e1.id = e2.managerId
GROUP BY e1.id
HAVING COUNT(*) >= 5;
```

### [585. Investments in 2016](https://leetcode.com/problems/investments-in-2016/)

关键点：子查询，IN，聚合函数不一定非要group by之后才能使用

```sql
SELECT ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM Insurance
WHERE tiv_2015 IN
(SELECT tiv_2015
FROM Insurance
GROUP BY tiv_2015
HAVING COUNT(*) > 1)
-- 注意这里的写法
AND (lat, lon) IN 
(SELECT lat, lon
FROM Insurance
GROUP BY lat, lon
HAVING COUNT(*) = 1)
```

### [602. Friend Requests II: Who Has the Most Friends](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/)

关键点：union all

参考链接：https://developer.aliyun.com/article/885871

当你想要合并两个查询的结果集时，`UNION ALL` 是一个很有用的操作符。它将两个查询的结果集堆叠在一起，形成一个包含所有结果的单一结果集。这个操作符和 `UNION` 的区别在于，`UNION` 会自动去重，而 `UNION ALL` 不会。

```sql
SELECT id, COUNT(*) AS num
FROM (
    SELECT requester_id AS id FROM RequestAccepted 
    UNION ALL
    SELECT accepter_id AS id FROM RequestAccepted
) AS t1
GROUP BY id
ORDER BY num DESC
LIMIT 1;
```

想计算两列分别出现的数值次数，union all是一个很好的选择

### [608. Tree Node](https://leetcode.com/problems/tree-node/)

关键点：写复杂了，其实不用这么复杂，还是要理解题意

```sql
-- 一开始的写法，其实不用写CTE，我好蠢
WITH p_help AS (
    SELECT DISTINCT p_id
    FROM Tree
    WHERE p_id IS NOT NULL
)
SELECT id, (CASE WHEN p_id IS NULL THEN 'Root' 
            WHEN id NOT IN (SELECT p_id FROM p_help) THEN 'Leaf'
            ELSE 'Inner'
            END) AS type
FROM Tree;
```

```sql
SELECT id, 
    CASE
        WHEN p_id IS NULL THEN 'Root'
        WHEN id IN (
            SELECT p_id FROM Tree
        ) THEN 'Inner'
        ELSE 'Leaf' END AS type
FROM Tree
```

但是我在这里遇到一个很有意思的问题

```sql
SELECT * FROM Tree WHERE id IN (SELECT p_id FROM Tree)
```

使用IN可以正常返回结果，但是使用下边的NOT IN不能正常返回结果。这是为什么呢？

参考：https://stackoverflow.com/questions/129077/null-values-inside-not-in-clause

```sql
A: select 'true' where 3 in (1, 2, 3, null)
B: select 'true' where 3 not in (1, 2, null)
```

查询 A 与以下内容相同：

```sql
select 'true' where 3 = 1 or 3 = 2 or 3 = 3 or 3 = null
```

既然`3 = 3`是真的，你就会得到一个结果。

查询 B 与以下相同：

```sql
select 'true' where 3 <> 1 and 3 <> 2 and 3 <> null
```

`NOT IN` 的实现原理是 对每一个a表的指定字段和每一个b表的指定字段进行不相等比较(!=). 而SQL中 `任意!=null`的运算结果都是false. 所以B表中存在一个 `null `,`NOT IN`的查询永远都会返回false,即查询结果为空. 当你在一个可以为NULL的列上使用 `IN`或者 `NOT IN` 子查询时，可以好好想想使用 `EXISTS`或 `NOT EXISTS`代替 .因为 `nulls`是 `NOT IN`慢的如蜗牛的罪魁祸首!

参考链接：https://www.jianshu.com/p/ebfec61bcf6a

将值与 null 进行比较不会返回`false`；它返回`unknown`。并且`unknown`有自己的逻辑：

```sql
unknown  AND  false  = false 
unknown  AND  true   = unknown
unknown  OR   true   = true
unknown  OR   false  = unknown
```

这是如何实现的一个例子：

```sql
where 1 not in (2, null)
--> where 1 <> 2 and 1 <> null
--> where true and unknown
--> where unknown
```

#### MySQL中NOT IN和NOT EXISTS存在区别

如果想对两个表进行差集操作，可以配合子查询，使用`NOT IN`或者`NOT EXISTS`。`NOT IN`更加显得清晰、简单。如今的数据库系统都会将这两种查询方式优化成相同的执行计划获得类似的结果，处理外部和内部查询相关性。

有个很重要的区别是，如果在子查询的结果里返回了NULL，`NOT IN` 子句会执行失败，因为NULL和任何值都不相等。除了这个，`NOT IN` 和`NOT EXISTS` 应该就没什么区别了

接下来就要来说说`NOT IN` 慢得如蜗牛的一个例子了，nulls是罪魁祸首。

> Note: 可以在查询前边加`EXPLAIN`关键字来查看查询的查询计划。
>
> 例如：`EXPLAIN SELECT * FROM Tree WHERE id NOT IN (SELECT p_id FROM Tree);`

原博客有更详细的解释，包括二者具体查询计划的区别。

参考链接：https://explainextended.com/2009/09/18/not-in-vs-not-exists-vs-left-join-is-null-mysql/

这个文章有全面的比较，值得认真阅读

维基百科三值逻辑：https://en.wikipedia.org/wiki/Null_%28SQL%29

<img src="./images/26.png" alt="26" style="zoom:50%;" />

MySQL官方文档：https://dev.mysql.com/doc/refman/8.0/en/working-with-null.html

不能使用算术比较运算符，如=、&lt;或&lt;&gt;来测试是否为NULL。为了演示这一点，请尝试以下查询：

<img src="./images/27.png" alt="27" style="zoom:50%;" />

因为与NULL的任何算术比较的结果也是NULL，所以您无法从这种比较中获得任何有意义的结果。两个NULL值在GROUP BY中被认为是相等的。When doing an `ORDER BY`, `NULL` values are presented first if you do `ORDER BY ... ASC` and last if you do `ORDER BY ... DESC`.

### [626. Exchange Seats](https://leetcode.com/problems/exchange-seats/)

关键点：思路，分类讨论

```sql
SELECT 
    CASE WHEN id%2=0 THEN id-1 WHEN id%2=1 AND id!=(SELECT MAX(id) FROM Seat) THEN id+1 ELSE id END AS id,
    student
FROM Seat
ORDER BY id ASC;
```

### [1045. Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/)

```sql
SELECT customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product)
```

#### Foreign key

foreign key请看这个博客，讲解很详细：

https://blog.csdn.net/qq_42534026/article/details/106158803

### [1070. Product Sales Analysis III](https://leetcode.com/problems/product-sales-analysis-iii/)

关键点：不能对group by使用limit，但是我们可以使用窗口函数实现类似的功能

```sql
SELECT product_id, year AS first_year, quantity, price
FROM (SELECT *, DENSE_RANK() OVER(PARTITION BY product_id ORDER BY year ASC) AS rk FROM Sales) sub
WHERE rk = 1
```

第二种解法可以使用IN，重点是选择IN的项

```sql
select product_id, year as first_year, quantity, price
from Sales
where (product_id, year) in (select product_id, min(year) from Sales group by product_id)
```

### [1158. Market Analysis I](https://leetcode.com/problems/market-analysis-i/)

关键点：COUNT对于null的处理

1.count(1)与count(*)得到的结果一致，包含null值。
2.count(字段)不计算null值
3.count(null)结果恒为0

```sql
SELECT Users.user_id AS buyer_id, Users.join_date, COUNT(order_id) AS orders_in_2019
FROM
(SELECT * FROM Orders WHERE YEAR(order_date) = '2019'
) sub
RIGHT JOIN Users
ON Users.user_id = sub.buyer_id
GROUP BY Users.user_id
```

这里的count可以不用ifnull，因为count对null的处理是0.

### [1164. Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date/)

关键点：使用CTE和UNION

```sql
WITH price_help AS (
    SELECT *, DENSE_RANK() OVER(PARTITION BY product_id ORDER BY change_date DESC) AS rk
    FROM Products
    WHERE change_date <= '2019-08-16'
)
SELECT product_id, new_price AS price
FROM price_help
WHERE rk = 1
UNION
SELECT product_id, 10 AS price
FROM Products
WHERE product_id NOT IN (SELECT product_id FROM price_help)
```

### [1174. Immediate Food Delivery II](https://leetcode.com/problems/immediate-food-delivery-ii/)

```sql
SELECT ROUND(AVG(order_date = customer_pref_delivery_date)*100, 2) AS immediate_percentage
FROM (
    SELECT *, DENSE_RANK() OVER(PARTITION BY customer_id ORDER BY order_date ASC) AS rk_date
    FROM Delivery
    ) sub
WHERE rk_date = 1
```

`AVG(order_date = customer_pref_delivery_date)`：这一部分计算满足条件的记录的比例。由于条件返回的是布尔值（1 或 0），因此它实际上计算了满足条件的记录的比例。如果记录的订单日期等于客户首选的交付日期，则条件为真，否则为假。

### [1193. Monthly Transactions I](https://leetcode.com/problems/monthly-transactions-i/)

关键点：DATE_FORMAT函数，区分SUM和COUNT的使用

```sql
SELECT DATE_FORMAT(trans_date, '%Y-%m') AS month, 
       country,
       COUNT(*) AS trans_count,
       SUM(IF(state='approved', 1, 0)) AS approved_count,
       SUM(amount) AS trans_total_amount,
       SUM(IF(state='approved', amount, 0)) AS approved_total_amount
FROM Transactions
GROUP BY country, YEAR(trans_date), MONTH(trans_date)
```

在 MySQL 中，使用 `DATE_FORMAT` 函数可以将日期格式化为指定的字符串格式。具体用法是：

```sql
DATE_FORMAT(date_column, format)
```

这里需要注意COUNT和SUM的区别，COUNT(0) = 1，COUNT(NULL) = 0。`type = '1'` 实际上是一个条件表达式，它会返回布尔值（1 或 0），所以应该使用SUM，因为使用COUNT它对0和1都会计数为1.

聚合函数中都可以加过滤条件来进行计算，例如第一个SUM其实可以简写为：`SUM(state='approved') AS approved_count`.但是第二个SUM不可以这样操作，大家可以想想为什么。

### [1204. Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/)

关键点：思路，聚合函数的窗口函数，使用SUM窗口函数求累计和

```sql
SELECT person_name
FROM (SELECT *, SUM(weight) OVER(ORDER BY turn ASC) AS total_weight
    FROM Queue) total_weight
WHERE total_weight <= 1000
ORDER BY turn DESC
LIMIT 1;
```

### [1321. Restaurant Growth](https://leetcode.com/problems/restaurant-growth/)

关键点：窗口函数，滑动窗口

参考链接：https://leetcode.cn/problems/restaurant-growth/solutions/1047332/jiang-jie-bing-gai-jin-ping-lun-qu-da-la-34xv

首先理解题意，计算七天窗口内消费者付的平均金额。

<img src="./images/28.png" alt="28" style="zoom:50%;" />

了解一下窗口函数，之前我们一直没有用到窗口滑动的数据范围。

```sql
[你要的操作] OVER ( PARTITION BY  <用于分组的列名>
                    ORDER BY <按序叠加的列名> 
                    ROWS <窗口滑动的数据范围> )
```

**<窗口滑动的数据范围> 用来限定[ 你要的操作] 所运用的数据的范围，具体有如下这些：**

```sql
当前行 - current row
之前的行 - preceding
之后的行 - following
无界限 - unbounded
表示从前面的起点 - unbounded preceding
表示到后面的终点 - unbounded following
```

举个例子：

```sql
取当前行和前五行：ROWS between 5 preceding and current row --共6行
取当前行和后五行：ROWS between current row and 5 following --共6行
取前五行和后五行：ROWS between 5 preceding and 5 folowing --共11行
```

本题中，要按照日期累计金额，从当天算起一共7天。

可以理解成操作是累计金额，按序叠加的列是日期，窗口内的函数要取当前行和前6行。

需要注意的是：

- 即使前边的数据不够，窗口函数也会将范围内的数据框住并计算，因此需要最后手动地只要能够完整框住7天的情况。
- 另外比较阴损的是，本题的数据中存在着某一日有多个消费的情况，这样一来即使窗口照旧向前取6天就无法覆盖被挤出去的数据了，因此，需要构建一个小表格用来存放每天的金额总量 【绊子2】

```sql
SELECT DISTINCT visited_on,
       sum_amount AS amount, 
       ROUND(sum_amount/7, 2) AS average_amount
-- 以上是破解【绊子1】并计算平均值，少用一次窗口函数提高运行速度
FROM (
    SELECT visited_on, 
       SUM(amount) OVER ( ORDER BY visited_on ROWS 6 PRECEDING ) AS sum_amount
    -- 以下是计算每天的金额总量，破解【绊子2】
    FROM (
        SELECT visited_on, 
            SUM(amount) AS amount
        FROM Customer
        GROUP BY visited_on
         ) TT
     ) LL
-- 最后手动只要覆盖完整7天的数据，破解【绊子1】
WHERE DATEDIFF(visited_on, (SELECT MIN(visited_on) FROM Customer)) >= 6
```

- 首先计算每天的金额总量，存储在一个子查询表格中
- 利用滑动窗口，计算每七天的金额总量
- 最后利用where过滤能够覆盖完整7天的数据

这里我们少使用了窗口函数来提高运行速度，可以直接除以7。

### [1341. Movie Rating](https://leetcode.com/problems/movie-rating/)

关键点：UNION会去重！！！如果人名和电影名字重复则会导致错误，所以要使用UNION ALL

```sql
(SELECT u.name AS results
FROM Users u
JOIN MovieRating m1
ON u.user_id = m1.user_id
GROUP BY m1.user_id
ORDER BY COUNT(rating) DESC, u.name ASC
LIMIT 1)

UNION ALL

(SELECT m2.title AS results
FROM Movies m2
JOIN MovieRating m3
ON m2.movie_id = m3.movie_id
WHERE YEAR(created_at) = '2020' AND MONTH(created_at) = '02'
GROUP BY m3.movie_id
ORDER BY AVG(rating) DESC, m2.title ASC
LIMIT 1)
```

或者使用left(created_at, 7)也行。

> Note: LEFT(string, number_of_characters)，包括空格

### [1393. Capital Gain/Loss](https://leetcode.com/problems/capital-gainloss/)

```sql
SELECT stock_name, SUM(CASE WHEN operation = 'Sell' THEN price ELSE price*(-1) END) AS capital_gain_loss
FROM Stocks
GROUP BY stock_name
```

### [1907. Count Salary Categories](https://leetcode.com/problems/count-salary-categories/)

关键点：当有一种情况缺失，不好表达且没有另外的表可以JOIN时，考虑使用UNION。

```sql
SELECT 'Low Salary' AS category, SUM(income<20000) AS accounts_count
FROM Accounts
UNION
SELECT 'Average Salary' AS category, SUM(income>=20000 AND income<=50000) AS accounts_count
FROM Accounts
UNION
SELECT 'High Salary' AS category, SUM(income>50000) AS accounts_count
FROM Accounts
```

### [1934. Confirmation Rate](https://leetcode.com/problems/confirmation-rate/)

```sql
SELECT s.user_id, ROUND(IFNULL(AVG(action='confirmed'), 0), 2) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c
ON s.user_id = c.user_id
GROUP BY s.user_id
```

 ## Hard

### [185. Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/)

关键点：这里不用使用LEFT JOIN，因为当部门不存在要求的高收入结果时，可以不返回结果，还要注意几种rank的区别

<img src="./images/29.png" alt="29" style="zoom:50%;" />

```sql
SELECT d_name AS Department, e_name AS Employee, salary AS Salary
FROM (
    SELECT d.id, d.name AS d_name, e.name AS e_name, e.salary, DENSE_RANK() OVER(PARTITION BY d.id ORDER BY e.salary DESC) AS s_rank
    FROM Department d
    JOIN Employee e
    ON d.id = e.departmentId
) sub
WHERE s_rank <= 3
```

### [262. Trips and Users](https://leetcode.com/problems/trips-and-users/)

关键点：其实JOIN的时候可以利用ON来进行过滤

```sql
-- 注意这里有空格的列名需要加引号
SELECT t.request_at AS Day, ROUND(AVG(status!='completed'), 2) AS 'Cancellation Rate'
FROM Trips t
JOIN Users u1
JOIN Users u2
ON t.client_id = u1.users_id AND t.driver_id = u2.users_id
WHERE request_at BETWEEN '2013-10-01' AND '2013-10-03' AND u1.banned = 'No' AND u2.banned = 'No'
GROUP BY t.request_at;
```

```sql
SELECT
    request_at as 'Day', round(avg(Status!='completed'), 2) as 'Cancellation Rate'
FROM 
-- 在这里其实就可以直接定义u1.banned了
    trips t JOIN users u1 ON (t.client_id = u1.users_id AND u1.banned = 'No')
    JOIN users u2 ON (t.driver_id = u2.users_id AND u2.banned = 'No')
WHERE	
    request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY 
    request_at
```

```sql
-- 不使用JOIN的方法，妙啊！
select request_at 'Day',
round(count(if(status!='completed',status,null))/count(*),2) 'Cancellation Rate'
from Trips
where request_at between '2013-10-01' and '2013-10-03'
and client_id not in (select users_id from Users where banned='Yes') 
and driver_id not in (select users_id from Users where banned='Yes')
group by request_at;
```

### [601. Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/)

```sql
WITH help1 AS (
    SELECT id, visit_date, people, (id - ROW_NUMBER() OVER(ORDER BY id)) AS diff
    FROM Stadium
    WHERE people >= 100
),
help2 AS(
    SELECT diff
    FROM help1 
    GROUP BY diff
    HAVING COUNT(*) >= 3
)
SELECT id, visit_date, people 
FROM help1
WHERE diff IN (SELECT diff FROM help2)
ORDER BY visit_date ASC;
```

### [534. 游戏玩法分析 III](https://leetcode.cn/problems/game-play-analysis-iii/)

```sql
SELECT 
    player_id, 
    event_date, 
    SUM(games_played) OVER(PARTITION BY player_id ORDER BY event_date) AS games_played_so_far
FROM Activity
```

### [574. 当选者](https://leetcode.cn/problems/winning-candidate/)

关键点：**使用JOIN而不是子查询**，子查询可能会对性能有影响，特别是在数据量较大的情况下。使用JOIN可以更直观地理解查询意图。

一开始我的答案是这样的：

```sql
SELECT name
FROM Candidate
WHERE id IN (
    SELECT candidateId
    FROM Vote
    GROUP BY candidateId
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
```

但是报错了，为什么呢，明明看起来没有问题？

```
This version of MySQL doesn't yet support 'LIMIT & IN/ALL/ANY/SOME subquery'
```

这个错误通常是由于MySQL版本太旧导致的。在旧版本的MySQL中，无法在子查询中使用LIMIT和IN / ALL / ANY / SOME子查询。您需要升级到MySQL的较新版本，以解决这个问题。或者，您可以尝试使用其他方法来编写查询，而不是使用子查询和LIMIT。（无语死了）

回归最传统的写法：

```sql
SELECT name
FROM Candidate c
JOIN Vote v
ON c.id = v.candidateId
GROUP BY candidateId
ORDER BY COUNT(*) DESC
LIMIT 1;
```

或者把子查询的方法改写成JOIN：

```sql
SELECT name
FROM Candidate a
JOIN (
    SELECT candidateid, COUNT(id) AS vote_count
    FROM Vote
    GROUP BY candidateid
    ORDER BY vote_count DESC
    LIMIT 1
) b
ON a.id = b.candidateid;
```

### [578. 查询回答率最高的问题](https://leetcode.cn/problems/get-highest-answer-rate-question/)

```sql
SELECT question_id AS survey_log
FROM (
    SELECT question_id, SUM(action='answer')/SUM(action='show') AS as_rate
    FROM SurveyLog
    GROUP BY question_id
    ORDER BY as_rate DESC, question_id ASC
    LIMIT 1
) sub
```

上边是我最初的解法，但是我学到ORDER BY中其实可以直接使用SUM来排序！

```sql
SELECT question_id AS survey_log
FROM survey_log
GROUP BY question_id
ORDER BY SUM(if(action = "answer", 1, 0)) / SUM(if(action = "show", 1, 0)) DESC
LIMIT 1
```

### [580. 统计各专业学生人数](https://leetcode.cn/problems/count-student-number-in-departments/)

```sql
SELECT dept_name, COUNT(Student_id) AS student_number
FROM Department d
LEFT JOIN Student s
ON d.dept_id = s.dept_id
GROUP BY d.dept_id
ORDER BY student_number DESC, dept_name ASC;
```

```sql
SELECT dept_name, IFNULL(student_number, 0) AS student_number
FROM Department d
LEFT JOIN (
    SELECT *, COUNT(*) AS student_number
    FROM Student
    GROUP BY dept_id
) sub
ON d.dept_id = sub.dept_id
ORDER BY student_number DESC, dept_name ASC;
```

### [612. 平面上的最近距离](https://leetcode.cn/problems/shortest-distance-in-a-plane/)

关键点：记得剔除自己和自己连接的行

```sql
SELECT ROUND(SQRT((p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y)), 2) AS shortest
FROM Point2D p1, Point2D p2
WHERE p1.x != p2.x OR p1.y != p2.y
ORDER BY shortest ASC
LIMIT 1;
```

为了提高效率，可以通过限定连接条件减少一半计算

```sql
-- 可以用MIN，我怎么没想到
SELECT ROUND(MIN(SQRT(POWER(p1.x - p2.x, 2) + POWER(p1.y - p2.y, 2))), 2) AS shortest
FROM point2D p1
JOIN point2D p2 
-- 筛选掉重复的行
ON p1.x < p2.x OR p1.y < p2.y;
```

```sql
POWER(base, exponent)
```

- `base`：要计算其指定次幂的基数。
- `exponent`：指定的幂。

### [614. 二级关注者](https://leetcode.cn/problems/second-degree-follower/)

```sql
SELECT followee AS follower, COUNT(*) AS num
FROM Follow
GROUP BY followee
HAVING followee IN (SELECT follower FROM Follow)
ORDER BY follower;
```

### [1077. 项目员工 III](https://leetcode.cn/problems/project-employees-iii/)

```sql
SELECT project_id, employee_id
FROM (SELECT p.project_id, p.employee_id, RANK() OVER(PARTITION BY p.project_id ORDER BY e.experience_years DESC) AS rk
    FROM Project p
    JOIN Employee e
    ON p.employee_id = e.employee_id) sub
WHERE rk = 1;
```

### [1098. 小众书籍](https://leetcode.cn/problems/unpopular-books/)

关键点：ON和WHERE的区别

```sql
SELECT sub1.book_id, sub1.name
FROM (
    SELECT *
    FROM Books
    WHERE DATEDIFF('2019-06-23', available_from) >= 30
) sub1
LEFT JOIN (
    SELECT *, SUM(quantity) AS orders_num
    FROM Orders
    WHERE dispatch_date >= '2018-06-23'
    GROUP BY book_id
) sub2
ON sub1.book_id = sub2.book_id
WHERE orders_num < 10 OR orders_num IS NULL;
```

```sql
-- 网友的解法，把条件限制放在ON后边
select b.book_id, name
from books b left join orders o
on b.book_id = o.book_id and dispatch_date >= '2018-06-23'
where available_from < '2019-05-23'
group by b.book_id
having ifnull(sum(quantity), 0) < 10
```

考察的知识点主要是left join的使用以及on和where的辨析
注意两个条件的区别：

- 过去一年内订单总量少于10本：因为有的书根本没有订单，所以该条件应该让left join对应的on去筛选，没有订单的至少返回null，后续可以通过ifnull()把null转换成0
- 不考虑上架不满一个月的书：应该直接通过where筛除，不符合条件的连null都不应该有，否则会混入结果中导致错误
- 本题的时间边界条件比较模糊，“一个月”、“一年”都没有比较清楚的描述，用例也没那么强，大致对即可通过
- 链接：https://leetcode.cn/problems/unpopular-books/solutions/182606/mysql-1098-xiao-zhong-shu-ji-on-he-where-de-bian-x/。

### [1107. 每日新用户统计](https://leetcode.cn/problems/new-users-daily-count/)

关键点：DISTINCT，因为用户可能一天多次登陆！

```sql
SELECT activity_date AS login_date, COUNT(DISTINCT user_id) AS user_count
FROM (
    SELECT *, RANK() OVER(PARTITION BY user_id ORDER BY activity_date) AS rk
    FROM Traffic
    WHERE activity = 'login'
) sub
WHERE DATEDIFF('2019-06-30', activity_date) <= 90 AND rk = 1
GROUP BY activity_date;
```

```sql
-- 网友的写法，首先选出每个user登陆的最早日期，这种方法不需要distinct
SELECT 
    login_date,
    count(user_id) user_count 
FROM (  
    SELECT 
        min(activity_date) AS login_date, 
        user_id
    FROM Traffic
    WHERE activity= 'login'
    GROUP BY user_id
) t
WHERE DATEDIFF('2019-6-30', login_date) <= 90
GROUP BY login_date;
```

很巧妙啊，首先利用group by分组，然后选出每个组中最小的日期，这种写法我很少写。还有就是注意“90天内”这个条件，是小于等于！

### [1112. 每位学生的最高成绩](https://leetcode.cn/problems/highest-grade-for-each-student/)

```sql
SELECT student_id, course_id, grade
FROM (
    SELECT *, RANK() OVER(PARTITION BY student_id ORDER BY grade DESC, course_id ASC) AS rk
    FROM Enrollments
) sub
WHERE rk = 1
ORDER BY student_id ASC;
```

### [1126. 查询活跃业务](https://leetcode.cn/problems/active-businesses/)

```sql
SELECT e.business_id
FROM Events e
RIGHT JOIN (
    SELECT event_type, AVG(occurrences) AS avg_occur
    FROM Events
    GROUP BY event_type
) sub
ON e.event_type = sub.event_type AND e.occurrences > sub.avg_occur
GROUP BY e.business_id
HAVING COUNT(e.event_type) > 1
```

```sql
-- 使用窗口函数，很妙！
select business_id
from (select *,if(occurrences > avg(occurrences) over(partition by event_type),1,0) as act
    from Events) a
group by business_id
having sum(act) > 1
```

### [1132. 报告的记录 II](https://leetcode.cn/problems/reported-posts-ii/)

关键点：可能会存在重复的行

```sql
SELECT ROUND(AVG(average_daily_percent), 2) AS average_daily_percent
FROM (
    SELECT COUNT(DISTINCT r.post_id)*100/COUNT(DISTINCT a.post_id)  AS average_daily_percent
    FROM Actions a
    LEFT JOIN Removals r
    ON a.post_id = r.post_id
    WHERE extra = 'spam'
    GROUP BY a.action_date
) sub
```

因为表中可能存在重复的行，所以有可能同一天有相同的 `post_id`，但是只需要统计一次，所以要用 `DISTINCT` 去重。

### [1149. 文章浏览 II](https://leetcode.cn/problems/article-views-ii/)

关键点：又忘记加distinct了，同一个用户可能在不同的日期读了两篇文章以上！

```sql
SELECT DISTINCT viewer_id AS id
FROM Views
GROUP BY view_date, viewer_id
HAVING COUNT(DISTINCT article_id) >= 2
ORDER BY id ASC;
```

### [1205. 每月交易 II](https://leetcode.cn/problems/monthly-transactions-ii/)

关键点：理解题意！

```sql
SELECT 
    t.month,
    t.country,
    SUM(approved_count) AS approved_count,
    SUM(approved_amount) AS approved_amount,
    SUM(chargeback_count) AS chargeback_count,
    SUM(chargeback_amount) AS chargeback_amount
FROM (
    SELECT 
        SUBSTR(trans_date, 1, 7) AS month,
        country,
        COUNT(1) AS approved_count,
        SUM(amount) AS approved_amount,
        0 AS chargeback_count,
        0 AS chargeback_amount
    FROM Transactions
    WHERE state = 'approved'
    GROUP BY SUBSTR(trans_date, 1, 7), country

    UNION ALL

    SELECT 
        SUBSTR(b.trans_date, 1, 7) AS month,
        a.country,
        0 AS approved_count,
        0 AS approved_amount,
        COUNT(1) AS chargeback_count,
        SUM(a.amount) AS chargeback_amount
    FROM Transactions a
    INNER JOIN Chargebacks b ON a.id = b.trans_id
    GROUP BY SUBSTR(b.trans_date, 1, 7), a.country
) t
GROUP BY t.month, t.country;
```

### [1212. 查询球队积分](https://leetcode.cn/problems/team-scores-in-football-tournament/)

关键点：UNION和UNION ALL

```sql
WITH help AS (
    SELECT *,
        CASE WHEN host_goals > guest_goals THEN 3 WHEN host_goals < guest_goals THEN 0 ELSE 1 END AS host_points,
        CASE WHEN host_goals < guest_goals THEN 3 WHEN host_goals > guest_goals THEN 0 ELSE 1 END AS guest_points
    FROM Matches)
SELECT t.team_id, t.team_name, IFNULL(SUM(sub.num_points), 0) AS num_points
FROM Teams t
LEFT JOIN (
    SELECT host_team AS team_id, SUM(host_points) AS num_points
    FROM help
    GROUP BY host_team
    UNION ALL
    SELECT guest_team AS team_id, SUM(guest_points) AS num_points
    FROM help
    GROUP BY guest_team
) sub
ON t.team_id = sub.team_id
GROUP BY t.team_id
ORDER BY num_points DESC, team_id ASC;
```

- `UNION`：合并两个查询结果集，并去除重复的行。
- `UNION ALL`：合并两个查询结果集，但不会去除重复的行。

这里存在隐患就是因为我们UNION的列名相同，因此如果guest和host得分一样就会被消除！

### [1264. 页面推荐](https://leetcode.cn/problems/page-recommendations/)

```sql
(SELECT DISTINCT l.page_id AS recommended_page
FROM Friendship f
JOIN Likes l
ON f.user2_id = l.user_id
WHERE f.user1_id = 1 AND l.page_id NOT IN (SELECT page_id FROM Likes WHERE user_id = 1))
UNION
(SELECT DISTINCT l.page_id AS recommended_page
FROM Friendship f
JOIN Likes l
ON f.user1_id = l.user_id
WHERE f.user2_id = 1 AND l.page_id NOT IN (SELECT page_id FROM Likes WHERE user_id = 1))
```

```sql
WITH help AS (
    SELECT user2_id AS user_id FROM Friendship WHERE user1_id = 1
    UNION
    SELECT user1_id AS user_id FROM Friendship WHERE user2_id = 1)
SELECT DISTINCT page_id AS recommended_page
FROM Likes l
JOIN help h
ON l.user_id = h.user_id
WHERE l.page_id NOT IN (SELECT page_id FROM Likes WHERE user_id = 1);
```

下边是一个很妙的解法：

```sql
SELECT DISTINCT page_id AS recommended_page
FROM Likes
WHERE user_id IN (
    SELECT (CASE WHEN user1_id = 1 THEN user2_id WHEN user2_id = 1 THEN user1_id END) AS user_id
    FROM Friendship
    WHERE user1_id = 1 OR user2_id = 1
) AND page_id NOT IN (SELECT page_id FROM Likes WHERE user_id = 1)
```

使用CASE WHEN！

### [1270. 向公司 CEO 汇报工作的所有人](https://leetcode.cn/problems/all-people-report-to-the-given-manager/)

```sql
WITH help1 AS (
    SELECT employee_id
    FROM Employees
    WHERE manager_id = 1 and employee_id != 1),
help2 AS (
    SELECT employee_id
    FROM Employees
    WHERE manager_id IN (SELECT * FROM help1)),
help3 AS (
    SELECT employee_id
    FROM Employees
    WHERE manager_id IN (SELECT * FROM help2)
)
SELECT * FROM help1
UNION 
SELECT * FROM help2
UNION
SELECT * FROM help3
```

### [1285. 找到连续区间的开始和结束数字](https://leetcode.cn/problems/find-the-start-and-end-number-of-continuous-ranges/)

```sql
SELECT MIN(log_id) AS start_id, MAX(log_id) AS end_id
FROM (
    SELECT *, log_id - ROW_NUMBER() OVER(ORDER BY log_id ASC) AS diff
    FROM Logs
) sub
GROUP BY diff
ORDER BY start_id;
```

### [1308. 不同性别每日分数总计](https://leetcode.cn/problems/running-total-for-different-genders/)

```sql
(SELECT 'F' AS gender, day, SUM(score_points) OVER(ORDER by day ASC) AS total
FROM Scores
WHERE gender = 'F'
ORDER BY day ASC)
UNION 
(SELECT 'M' AS gender, day, SUM(score_points) OVER(ORDER by day ASC) AS total
FROM Scores
WHERE gender = 'M'
ORDER BY day ASC)
```

其实有更简便的写法：

```sql
SELECT gender, day, SUM(score_points) OVER(PARTITION BY gender ORDER by day ASC) AS total
FROM Scores
ORDER BY gender, day;
```

直接按照gender分区就好啦！

### [1355. 活动参与者](https://leetcode.cn/problems/activity-participants/)

```sql
WITH help AS (
    SELECT activity, COUNT(*) AS cnt
    FROM Friends
    GROUP BY activity
)
SELECT activity
FROM help
WHERE cnt != (SELECT MAX(cnt) FROM help) AND cnt != (SELECT MIN(cnt) FROM help)
```

```sql
select activity as ACTIVITY
from friends
group by activity
having count(*)>any(
    select count(*) from friends group by activity
) and count(*)<any(
    select count(*) from friends group by activity
)
```

使用ANY很巧妙！`ANY` 操作符在 MySQL 中主要用于比较某个值与子查询返回的多个值中的任意一个。

### [1364. 顾客的可信联系人数量](https://leetcode.cn/problems/number-of-trusted-contacts-of-a-customer/)

```sql
SELECT i.invoice_id, c1.customer_name, i.price, COUNT(c2.contact_name) AS contacts_cnt,
    SUM(IF(c2.contact_email IN (SELECT email FROM Customers), 1, 0)) AS trusted_contacts_cnt
FROM Invoices i
LEFT JOIN Customers c1
ON i.user_id = c1.customer_id
LEFT JOIN Contacts c2
ON c1.customer_id = c2.user_id
GROUP BY i.invoice_id
ORDER BY i.invoice_id;
```

### [1398. 购买了产品 A 和产品 B 却没有购买产品 C 的顾客](https://leetcode.cn/problems/customers-who-bought-products-a-and-b-but-not-c/)

关键点：注意distinct

```sql
SELECT c.customer_id, c.customer_name
FROM Orders o
JOIN Customers c
ON o.customer_id = c.customer_id
WHERE o.product_name = 'A' OR o.product_name = 'B'
GROUP BY o.customer_id
HAVING COUNT(DISTINCT o.product_name) = 2 AND o.customer_id NOT IN (SELECT customer_id FROM Orders WHERE product_name = 'C')
ORDER BY c.customer_id;
```

```sql
-- 利用sum+条件过滤计算数量
SELECT
    c.customer_id, c.customer_name
FROM
    Orders o LEFT JOIN Customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id
HAVING
    SUM(product_name = 'A') * SUM(product_name = 'B') > 0
    AND SUM(product_name = 'C') = 0
ORDER BY c.customer_id
```

### [1440. 计算布尔表达式的值](https://leetcode.cn/problems/evaluate-boolean-expression/)

```sql
SELECT e.left_operand, e.operator, e.right_operand,
    CASE WHEN e.operator = '=' THEN IF(v1.value = v2.value, 'true', 'false')
    WHEN e.operator = '>' THEN IF(v1.value > v2.value, 'true', 'false')
    WHEN e.operator = '<' THEN IF(v1.value < v2.value, 'true', 'false') END AS value
FROM Expressions e
JOIN Variables v1
ON e.left_operand = v1.name
JOIN Variables v2
ON e.right_operand = v2.name;
```

```sql
SELECT e.left_operand, e.operator, e.right_operand,
    CASE 
        WHEN e.operator = '=' AND v.value = v1.value THEN 'true'
        WHEN e.operator = '>' AND v.value > v1.value THEN 'true'
        WHEN e.operator = '<' AND v.value < v1.value THEN 'true'
        ELSE 'false'
    END AS value 
FROM Expressions AS e 
JOIN Variables AS v ON e.left_operand = v.name 
JOIN Variables AS v1 ON e.right_operand = v1.name;
```

### [1445. 苹果和桔子](https://leetcode.cn/problems/apples-oranges/)

```sql
SELECT sale_date, SUM(IF(fruit = 'apples', sold_num, (-1)*sold_num)) AS diff
FROM Sales
GROUP BY sale_date
ORDER BY sale_date;
```

### [1454. 活跃用户](https://leetcode.cn/problems/active-users/)

关键点：注意distinct，内侧和外侧都要distinct

```sql
SELECT DISTINCT id, name
FROM (
    SELECT DISTINCT a.id, a.name, l.login_date, 
        DATE_SUB(login_date, INTERVAL (DENSE_RANK() OVER(PARTITION BY l.id ORDER BY l.login_date)) DAY) AS rk
    FROM Logins l
    JOIN Accounts a
    ON l.id = a.id
) sub
GROUP BY rk, id
HAVING COUNT(*) >= 5
ORDER BY id;
```

### [1459. 矩形面积](https://leetcode.cn/problems/rectangles-area/)

```sql
SELECT p1.id AS p1, p2.id AS p2, ABS(p1.x_value-p2.x_value) * ABS(p1.y_value-p2.y_value) AS area
FROM Points p1, Points p2
WHERE p1.id < p2.id AND p1.x_value != p2.x_value AND p1.y_value != p2.y_value
ORDER BY area DESC, p1 ASC, p2 ASC;
```

### [1468. 计算税后工资](https://leetcode.cn/problems/calculate-salaries/)

```sql
SELECT company_id, employee_id, employee_name,
    ROUND(CASE WHEN highest_salary < 1000 THEN salary
        WHEN highest_salary > 10000 THEN 0.51*salary
        ELSE 0.76*salary END) AS salary
FROM (
    SELECT *, MAX(salary) OVER(PARTITION BY company_id) AS highest_salary
    FROM Salaries
) sub;
```

### [1501. 可以放心投资的国家](https://leetcode.cn/problems/countries-you-can-safely-invest-in/)

```sql
WITH help AS (
    SELECT caller_id AS id, duration
    FROM Calls
    UNION ALL
    SELECT callee_id AS id, duration
    FROM Calls
)
SELECT c.name AS country
FROM help h
JOIN Person p
ON h.id = p.id
JOIN Country c
ON LEFT(p.phone_number, 3) = c.country_code
GROUP BY c.name
HAVING AVG(h.duration) > (SELECT AVG(duration) FROM help);
```

### [1532. 最近的三笔订单](https://leetcode.cn/problems/the-most-recent-three-orders/)

```sql
SELECT c.name AS customer_name, c.customer_id, sub.order_id, sub.order_date
FROM (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC) rk
    FROM Orders
) sub
JOIN Customers c
ON sub.customer_id = c.customer_id
WHERE sub.rk <= 3
ORDER BY c.name ASC, c.customer_id ASC, sub.order_date DESC;
```

### [1549. 每件商品的最新订单](https://leetcode.cn/problems/the-most-recent-orders-for-each-product/)

```sql
SELECT p.product_name, p.product_id, sub.order_id, sub.order_date
FROM (
    SELECT *, RANK() OVER(PARTITION BY product_id ORDER BY order_date DESC) AS rk
    FROM Orders) sub
JOIN Products p
ON sub.product_id = p.product_id
WHERE rk = 1
ORDER BY p.product_name ASC, p.product_id ASC, sub.order_id ASC;
```

### [1555. 银行账户概要](https://leetcode.cn/problems/bank-account-summary/)

关键点：

- Mysql中 null与所有数字相加都是null
- 例如 select null+1+2 ；结果是null
- 记得使用UNION ALL，因为不同的transaction可能导致相同的行

```sql
WITH help AS (SELECT u.user_id, u.user_name, u.credit, (-1)*amount AS amount
    FROM Users u
    LEFT JOIN Transactions t
    ON u.user_id = t.paid_by
    UNION ALL
    SELECT u.user_id, u.user_name, u.credit, amount AS amount
    FROM Users u
    LEFT JOIN Transactions t
    ON u.user_id = t.paid_to)
SELECT user_id, user_name, credit+IFNULL(SUM(amount), 0) AS credit,
    IF(credit+SUM(amount)<0, 'Yes', 'No') AS credit_limit_breached
FROM help
GROUP BY user_id;
```

### [1596. 每位顾客最经常订购的商品](https://leetcode.cn/problems/the-most-frequently-ordered-products-for-each-customer/)

```sql
WITH help1 AS(SELECT *, COUNT(product_id) OVER(PARTITION BY customer_id, product_id) AS ct
    FROM Orders),
help2 AS (
    SELECT *, RANK() OVER(PARTITION BY customer_id ORDER BY ct DESC) AS rk
    FROM help1
)
SELECT DISTINCT h.customer_id, h.product_id, p.product_name
FROM help2 h
JOIN Products p
ON h.product_id = p.product_id
WHERE h.rk = 1;
```

从评论区学到一种更好的解法，以前从来没用过！

```sql
SELECT customer_id, T.product_id, product_name 
FROM(
    SELECT customer_id, product_id,
    RANK() OVER(PARTITION BY customer_id ORDER BY COUNT(*) DESC ) AS RK
    FROM Orders o
    GROUP BY customer_id, product_id
) T
LEFT JOIN Products p on p.product_id = t.product_id 
WHERE RK=1
```

首先按照customer_id, product_id分组，然后应用窗口函数，按照count排序。

### [1613. 找到遗失的ID](https://leetcode.cn/problems/find-the-missing-ids/)

关键点：递归写法！第一次学，好激动

```sql
WITH recursive a AS (
    SELECT MAX(customer_id) AS n FROM Customers
    UNION
    SELECT n-1 FROM a WHERE n > 1
)
SELECT n AS ids
FROM a
WHERE n NOT IN (SELECT customer_id FROM Customers)
ORDER BY ids ASC;
```

注意这里其实存在一个优化，就是首先寻找最大，然后只生成1-max的序列，而不是生成1-100的序列，效率更高。

参考链接：https://blog.csdn.net/w13966597931/article/details/133221384

```sql
WITH RECURSIVE cte_name (column_list) AS (
    SELECT initial_query_result
    UNION [ALL]
    SELECT recursive_query
    FROM cte_name
    WHERE condition
)
SELECT * FROM cte_name;
```

### [1699. 两人之间的通话次数](https://leetcode.cn/problems/number-of-calls-between-two-persons/)

```sql
SELECT from_id AS person1, to_id AS person2, COUNT(*) AS call_count, SUM(duration) AS total_duration
FROM (
    SELECT 
    CASE WHEN from_id > to_id THEN to_id ELSE from_id END AS from_id,
    CASE WHEN from_id > to_id THEN from_id ELSE to_id END AS to_id,
    duration
    FROM Calls
) sub
GROUP BY from_id, to_id;
```

### [1709. 访问日期之间最大的空档期](https://leetcode.cn/problems/biggest-window-between-visits/)

关键点：新知识LEAD函数

参考链接：https://leetcode.cn/problems/biggest-window-between-visits/solutions/1202409/mysql-leadchuang-kou-han-shu-group-bymia-esnc

`LAG` 和 `LEAD` 是SQL中的窗口函数，用于在查询结果中访问当前行相对于某一行的前一行或后一行的值。对于一张表的一行数据而言，在其之上的是Lag, 在其之下的是Lead。

```
+---------+------------+
        LAG()
------------------------
      current_row
------------------------
        LEAD()
+-----------------------+
```

所以我们第一个想到就是用`LEAD()`函数。我们按照时间排序把下一行的时间找到，然后就可以算window差了.

```sql
LEAD(col, offset, default)

col - 指你要操作的那一列
offset - 偏移几行，如果是1就是下1行，以此类推
default - 如果下一行不存在，用什么值填充
```

在这道题中，我们刚好要算最后一个时间点和`2021-01-01`的windows_diff，所以直接填上即可.

```sql
SELECT user_id, MAX(DATEDIFF(date_next, visit_date)) AS biggest_window
FROM (
    SELECT user_id, visit_date,
    LEAD(visit_date, 1, '2021-1-1') OVER(PARTITION BY user_id ORDER BY visit_date ASC) AS date_next
    FROM UserVisits
) sub
GROUP BY user_id
ORDER BY user_id;
```

### [1715. 苹果和橘子的个数](https://leetcode.cn/problems/count-apples-and-oranges/)

关键点：`SUM` 函数用于对一组行的值进行聚合！不是a+b这种使用sum。在 SQL 中，任何数值与 `NULL` 相加都会返回 `NULL`。`COALESCE` 函数用于返回其参数列表中的第一个非 `NULL` 值。

```sql
SELECT SUM(a_count) AS apple_count, SUM(o_count) AS orange_count
FROM (
    SELECT b.apple_count+COALESCE(c.apple_count, 0) AS a_count, b.orange_count+COALESCE(c.orange_count, 0) AS o_count
    FROM Boxes b
    LEFT JOIN Chests c
    ON b.chest_id = c.chest_id
) sub;
```

或者简单一些写：

```sql
SELECT 
    SUM(b.apple_count+COALESCE(c.apple_count, 0)) AS apple_count,
    SUM(b.orange_count+COALESCE(c.orange_count, 0)) AS orange_count
FROM Boxes b
LEFT JOIN Chests c
ON b.chest_id = c.chest_id;
```

### [1747. 应该被禁止的 Leetflex 账户](https://leetcode.cn/problems/leetflex-banned-accounts/)

```sql
SELECT DISTINCT l1.account_id AS account_id 
FROM LogInfo l1, LogInfo l2
WHERE l1.account_id = l2.account_id -- 某个用户
    AND l1.ip_address != l2.ip_address -- 异地登陆
    AND l1.login <= l2.login -- 其中一个还没下线，另一个就登录了
    AND l2.login <= l1.logout;
```

### [1783. 大满贯数量](https://leetcode.cn/problems/grand-slam-titles/)

```sql
WITH help AS (SELECT Wimbledon AS player_id
FROM Championships
UNION ALL
SELECT Fr_open AS player_id
FROM Championships
UNION ALL
SELECT US_open AS player_id
FROM Championships
UNION ALL
SELECT Au_open AS player_id
FROM Championships)

SELECT h.player_id, p.player_name, COUNT(*) AS grand_slams_count
FROM help h
JOIN Players p
ON h.player_id = p.player_id
GROUP BY player_id
```

### [1811. 寻找面试候选人](https://leetcode.cn/problems/find-interview-candidates/)

