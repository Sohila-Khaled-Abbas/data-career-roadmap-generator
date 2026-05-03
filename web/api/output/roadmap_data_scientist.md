# Data Scientist Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### Python
**Why first:** Python is the lingua franca of data science. Every tool, framework, and platform you'll use either runs on Python or integrates with it. You cannot progress without fluency here.

- Core syntax, data types, functions, OOP basics
- Libraries: NumPy, Pandas fundamentals
- Error handling and debugging

### SQL Fundamentals
**Why alongside Python:** SQL is how you access data. Before you can analyze anything, you need to retrieve it efficiently. This is non-negotiable and pairs naturally with Python basics.

- SELECT, WHERE, JOIN, GROUP BY, aggregations
- Subqueries and CTEs
- Query optimization basics
- Works with any database (PostgreSQL, SQL Server, Snowflake)

### Pandas
**Why now:** Once you can write SQL and Python, Pandas is your primary tool for data manipulation and exploration. It's the bridge between raw data and analysis.

- DataFrames and Series
- Filtering, grouping, merging
- Data cleaning and transformation
- Time series handling

---

## Phase 2: Data Infrastructure (Weeks 5-8)

### PostgreSQL
**Why here:** You need hands-on experience with a relational database. PostgreSQL is open-source, powerful, and teaches you real database concepts without vendor lock-in. It's your foundation for understanding all SQL databases.

- Schema design
- Indexing and query performance
- Transactions and ACID properties
- Local setup and administration basics

### SQL Server
**Why after PostgreSQL:** Many enterprises use SQL Server. Learning it after PostgreSQL is faster because you understand relational concepts; now you're just learning SQL Server-specific syntax and tools.

- T-SQL specifics
- SQL Server Management Studio
- Integration with enterprise environments

### Snowflake
**Why after SQL foundations:** Snowflake is a cloud data warehouse built on SQL. You need SQL mastery first. Snowflake's value is in scalability and cloud architecture, not in SQL itself.

- Cloud warehouse architecture
- Snowflake-specific SQL features
- Cost optimization and performance tuning
- Integration with Python and other tools

---

## Phase 3: Data Transformation & Orchestration (Weeks 9-12)

### dbt (Data Build Tool)
**Why here:** dbt transforms raw data into analytics-ready datasets using SQL. You need SQL expertise and a data warehouse (Snowflake) in place first. dbt is how professional data teams structure transformations.

- dbt project structure
- Models, tests, and documentation
- Lineage and dependency management
- Integration with Snowflake

### Airflow
**Why before Dagster:** Airflow is the industry standard for workflow orchestration. Learn it first to understand the core concepts (DAGs, tasks, scheduling, monitoring). It's more widely used and a prerequisite mindset for Dagster.

- DAG concepts and task dependencies
- Scheduling and backfilling
- Monitoring and alerting
- Operators and hooks

### Dagster
**Why after Airflow:** Dagster is a modern alternative with better data lineage and asset management. Learning Airflow first means you understand orchestration fundamentals; Dagster builds on these with a more sophisticated model.

- Asset-oriented workflows
- Data lineage and observability
- Comparison with Airflow patterns
- When to choose Dagster over Airflow

---

## Phase 4: Distributed Computing & Advanced Processing (Weeks 13-16)

### Spark
**Why here:** Spark processes massive datasets across clusters. You need orchestration experience (Airflow/Dagster) and SQL knowledge first. Spark is how you scale beyond single-machine processing.

- RDD, DataFrame, and SQL APIs
- Transformations and actions
- Partitioning and shuffling
- Performance tuning

### Kubernetes
**Why after Spark:** Kubernetes manages containerized applications at scale. You need to understand distributed systems (Spark) first. Kubernetes is how you deploy Spark clusters and orchestration tools in production.

- Container basics and Docker
- Pods, services, and deployments
- StatefulSets for data tools
- Helm for package management

---

## Phase 5: Machine Learning & Advanced Analytics (Weeks 17-20)

### PyTorch
**Why here:** PyTorch is for deep learning. You need Python mastery, data manipulation (Pandas), and distributed computing concepts (Spark) first. PyTorch is the tool, not the foundation.

- Tensors and autograd
- Neural network basics
- Training loops and optimization
- GPU acceleration

### Power BI & Tableau
**Why alongside PyTorch:** These are visualization and BI tools. Learn them after your data pipeline is solid. They consume clean data from dbt/Snowflake and present insights.

- **Power BI:** Microsoft ecosystem integration, DAX, Power Query
- **Tableau:** Visual analytics, dashboarding, storytelling
- Both require clean, well-structured data (from earlier phases)

---

## Phase 6: Cloud & Production (Weeks 21-24)

### AWS
**Why last:** AWS is the deployment platform. You need to understand all the tools first (Spark, Kubernetes, dbt, Airflow). AWS is where you run everything at scale.

- EC2, S3, RDS basics
- Lambda for serverless
- SageMaker for ML workflows
- IAM and security
- Cost management

---

## Learning Path Summary

```
Foundations → Infrastructure → Transformation → Distributed → ML/BI → Cloud
   (4 wks)      (4 wks)         (4 wks)        (4 wks)      (4 wks)   (4 wks)
```

**Key Principle:** Each phase builds on the previous. You cannot optimize Spark jobs without understanding SQL. You cannot deploy to Kubernetes without understanding Spark. You cannot use dbt without a data warehouse. This order respects dependencies and builds practical, production-ready skills.