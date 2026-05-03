# Data Architect Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### 1. **Python**
**Why first:** Python is the lingua franca of data work. Every tool in your stack either uses Python or integrates with it. You need fluency here before touching specialized frameworks.
- Core concepts: variables, functions, OOP, error handling
- Libraries: built-in modules, package management (pip)

### 2. **SQL**
**Why immediately after Python:** SQL is non-negotiable for data work. You'll query databases constantly, and this skill is independent of Python but equally fundamental. Learn it in parallel or right after Python.
- Query fundamentals: SELECT, WHERE, JOINs, aggregations
- Schema design basics
- Indexing and query optimization concepts

### 3. **Postgres**
**Why here:** Start with a single relational database to understand ACID principles, transactions, and how databases actually work. Postgres is open-source, widely used, and teaches you real database concepts without vendor lock-in.
- Installation and basic administration
- Creating tables, constraints, relationships
- Writing and optimizing queries

---

## Phase 2: Core Data Stack (Weeks 5-10)

### 4. **Pandas**
**Why now:** You have Python and SQL foundations. Pandas is the bridge between raw data and analysis. It's essential for data manipulation, cleaning, and exploration before moving to distributed systems.
- DataFrames and Series
- Data cleaning and transformation
- Groupby, merge, pivot operations
- Performance considerations

### 5. **SQL Server**
**Why after Postgres:** You understand relational databases now. SQL Server teaches you enterprise database concepts, T-SQL specifics, and how different databases handle similar problems differently. This prepares you for cloud data warehouses.
- T-SQL syntax and differences from standard SQL
- Stored procedures and functions
- Query execution plans

### 6. **Snowflake**
**Why here:** You have SQL mastery and understand databases. Snowflake is a cloud-native data warehouse built for the modern data stack. It's where you'll actually work as a data architect.
- Architecture: compute, storage, and scaling
- Data loading and unloading
- Performance tuning and cost optimization
- Snowflake-specific SQL features

### 7. **AWS**
**Why now:** Snowflake lives in the cloud. AWS is the dominant cloud platform for data work. Learn core services: S3, EC2, IAM, RDS, and how they interconnect. This is infrastructure thinking.
- Core services: compute, storage, networking
- Identity and access management
- Cost and resource management
- Integration with data tools

---

## Phase 3: Data Engineering & Orchestration (Weeks 11-16)

### 8. **dbt (Data Build Tool)**
**Why here:** You have Snowflake and SQL mastery. dbt transforms raw data into analytics-ready tables using SQL and version control. It's the modern standard for data transformation and sits between your warehouse and analytics.
- Project structure and best practices
- Models, tests, and documentation
- Incremental models and performance
- Integration with Snowflake

### 9. **Airflow**
**Why now:** You understand data pipelines conceptually (dbt). Airflow orchestrates them—scheduling, monitoring, and managing dependencies. Learn how to build reliable, production-grade workflows.
- DAGs and task dependencies
- Operators and sensors
- Scheduling and backfilling
- Error handling and retries

### 10. **Dagster**
**Why after Airflow:** You understand orchestration concepts. Dagster is a modern alternative with stronger data lineage, asset management, and type safety. Compare and contrast with Airflow; understand when to use each.
- Assets and ops
- Sensors and dynamic orchestration
- Data lineage and observability
- Advantages over Airflow for complex pipelines

---

## Phase 4: Distributed Computing & Advanced Processing (Weeks 17-22)

### 11. **Spark**
**Why here:** You have orchestration and SQL skills. Spark handles massive datasets across clusters. Essential for processing data too large for single machines. Learn PySpark to leverage your Python knowledge.
- RDDs, DataFrames, and Datasets
- Transformations and actions
- Partitioning and shuffling
- Performance tuning and cluster management

### 12. **Kubernetes**
**Why now:** You're running distributed systems (Spark, Airflow). Kubernetes manages containerized workloads at scale. Learn how to deploy and manage data applications in production.
- Pods, services, and deployments
- ConfigMaps and secrets
- Resource management and scaling
- Helm for package management

---

## Phase 5: Machine Learning & Advanced Analytics (Weeks 23-28)

### 13. **PyTorch**
**Why here:** You have Python mastery, Spark for distributed computing, and Kubernetes for deployment. PyTorch is for building and training neural networks. Learn it for ML pipelines and advanced analytics.
- Tensors and autograd
- Building neural networks
- Training loops and optimization
- Integration with data pipelines

---

## Phase 6: Analytics & Visualization (Weeks 29-32)

### 14. **Power BI**
**Why here:** You've built the data infrastructure. Power BI is for business intelligence and dashboarding. Learn DAX, data modeling, and how to surface insights to stakeholders.
- Data modeling and relationships
- DAX formulas and calculations
- Dashboard design and interactivity
- Integration with Snowflake and other sources

### 15. **Tableau**
**Why last:** You understand BI concepts from Power BI. Tableau is an alternative with different strengths. Learn it to understand the BI landscape and choose the right tool for different scenarios.
- Connecting to data sources
- Building visualizations and dashboards
- Calculated fields and parameters
- Performance and best practices

---

## Learning Strategy

**Parallel tracks:** Phases 1-2 can have some overlap (Python + SQL + Postgres simultaneously). Phases 3-4 can overlap (dbt + Airflow, Spark + Kubernetes).

**Hands-on projects:** Build end-to-end pipelines at each phase:
- Phase 2: Load data into Snowflake, write SQL queries
- Phase 3: Build a dbt project with Airflow orchestration
- Phase 4: Process large datasets with Spark on Kubernetes
- Phase 5: Train a model with PyTorch in a pipeline
- Phase 6: Visualize results in Power BI and Tableau

**Time estimate:** 6-8 months of focused learning with consistent practice.