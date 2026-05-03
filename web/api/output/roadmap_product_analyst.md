# Product Analyst Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### SQL
**Why first:** SQL is the bedrock of data work. You cannot analyze data without querying it. Every downstream tool depends on your ability to write efficient queries. Master this before touching any analytics platform.

- Relational database concepts
- SELECT, JOIN, aggregations, window functions
- Query optimization basics
- Practice: 50+ queries on real datasets

### Python Fundamentals
**Why second:** Python is the lingua franca of data work. You'll use it for data manipulation, automation, and eventually machine learning. Learn it now so it becomes second nature.

- Variables, data types, control flow
- Functions and modules
- List comprehensions, dictionaries
- Error handling
- Practice: Build 5 small CLI tools

### Pandas
**Why third:** Once you know Python, immediately apply it to data manipulation. Pandas is how you'll wrangle data in 80% of your daily work. It bridges SQL and analysis.

- DataFrames and Series
- Filtering, grouping, merging
- Data cleaning and transformation
- Performance considerations
- Practice: Transform 10 messy datasets

---

## Phase 2: Data Infrastructure (Weeks 5-8)

### PostgreSQL
**Why here:** You need a production database to understand how data actually lives. PostgreSQL teaches you real-world database design, indexing, and constraints. It's also free and widely used.

- Schema design
- Indexes and query plans
- Transactions and ACID properties
- Basic administration
- Practice: Design and populate a 5-table schema

### AWS Fundamentals
**Why here:** Cloud is non-negotiable in modern data work. Start with AWS because it's the market leader. Learn compute (EC2), storage (S3), and basic networking.

- EC2 instances and security groups
- S3 buckets and object storage
- IAM roles and permissions
- VPC basics
- Practice: Deploy a simple application to EC2

### Snowflake
**Why here:** Now that you understand databases and cloud, learn the modern data warehouse. Snowflake is purpose-built for analytics and is industry standard for product analysts.

- Architecture (compute/storage separation)
- Data loading and staging
- Query performance and cost optimization
- Roles and access control
- Practice: Load data from S3, write 20+ analytical queries

---

## Phase 3: Data Pipeline & Orchestration (Weeks 9-12)

### dbt (Data Build Tool)
**Why here:** You now have data in Snowflake. dbt lets you transform it reliably and version-control your logic. It's the standard for analytics engineering.

- Project structure and models
- Transformations (staging, intermediate, marts)
- Testing and documentation
- Lineage and dependencies
- Practice: Build a 3-layer transformation pipeline

### Airflow
**Why here:** dbt handles transformations, but Airflow orchestrates everything. Learn to schedule, monitor, and retry data pipelines. It's the industry standard for workflow orchestration.

- DAGs and operators
- Task dependencies
- Scheduling and backfilling
- Error handling and alerting
- Practice: Build a 5-task pipeline with dependencies

### Dagster (Optional but Recommended)
**Why here:** Dagster is the modern alternative to Airflow with better observability. If your company uses it, learn it. Otherwise, master Airflow first—the concepts transfer.

- Assets and ops
- Sensors and triggers
- Observability and monitoring
- Practice: Migrate an Airflow DAG to Dagster

---

## Phase 4: Advanced Analytics & ML (Weeks 13-16)

### Spark
**Why here:** You've mastered small-scale data work. Spark handles massive datasets across clusters. Learn it for big data transformations and when Pandas/SQL hit limits.

- RDD and DataFrame APIs
- Transformations and actions
- Partitioning and shuffling
- Performance tuning
- Practice: Process a 10GB+ dataset

### PyTorch
**Why here:** You now have the infrastructure to run ML. PyTorch is the standard for deep learning in production. Learn it for recommendation systems, forecasting, and anomaly detection.

- Tensors and autograd
- Neural network basics
- Training loops and optimization
- Practice: Build a simple classification model

### Kubernetes
**Why here:** Once you're running ML models and complex pipelines, you need container orchestration. Kubernetes manages deployment, scaling, and reliability at scale.

- Pods, services, and deployments
- ConfigMaps and secrets
- Persistent volumes
- Practice: Deploy a containerized Python app

---

## Phase 5: Visualization & Reporting (Weeks 17-20)

### Power BI
**Why here:** You've built the data infrastructure. Now visualize it for stakeholders. Power BI is Microsoft's standard and integrates with enterprise systems.

- Data modeling and relationships
- DAX formulas
- Interactive dashboards
- Row-level security
- Practice: Build 3 executive dashboards

### Tableau
**Why here:** Tableau is the premium alternative for complex, exploratory analysis. Learn it for sophisticated visualizations and when Power BI isn't sufficient.

- Dimensions and measures
- Calculated fields and LOD expressions
- Dashboard interactivity
- Performance optimization
- Practice: Build 3 exploratory dashboards

### SQL Server
**Why here:** You've learned PostgreSQL and Snowflake. SQL Server is the enterprise alternative. Learn it if your company uses it, but the concepts are transferable.

- T-SQL specifics
- Stored procedures and functions
- Query optimization in SQL Server
- Integration with Power BI
- Practice: Migrate a PostgreSQL schema

---

## Learning Strategy

**Parallel tracks:** Phases 1-2 can overlap. Start AWS while finishing Pandas.

**Project-based:** Don't learn tools in isolation. Build an end-to-end project: ingest data → transform with dbt → orchestrate with Airflow → visualize in Power BI.

**Depth over breadth:** Master SQL and Python deeply before moving on. Shallow knowledge of many tools is worthless.

**Certification optional:** Focus on building portfolio projects, not certifications. Employers care about what you can do.

**Timeline:** 20 weeks of focused study, 2-3 hours daily. Adjust based on prior experience.