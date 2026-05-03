# AI Engineer Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### Python
**Why first:** Python is the lingua franca of AI/ML. Every tool in your stack either runs on Python or integrates with it. You cannot progress without fluency here.

- Core syntax, data structures, OOP principles
- Package management (pip, virtual environments)
- Essential libraries: NumPy basics, file I/O

### SQL Fundamentals
**Why alongside Python:** Data is your raw material. SQL is non-negotiable for querying databases and understanding data pipelines. Learn it early so you can work with real data immediately.

- SELECT, WHERE, JOIN operations
- Aggregations and GROUP BY
- Subqueries and basic optimization
- Apply to PostgreSQL (simplest relational DB to start with)

---

## Phase 2: Data Engineering Essentials (Weeks 5-8)

### PostgreSQL
**Why now:** You need a concrete relational database to practice SQL at scale. PostgreSQL is production-grade, open-source, and widely used in data pipelines.

- Schema design, indexing, query optimization
- Transactions and ACID properties
- Connection pooling and performance tuning

### Pandas
**Why after SQL:** Pandas bridges SQL and Python. You'll extract data via SQL, manipulate it with Pandas, and prepare it for ML. This is your daily workhorse.

- DataFrames and Series operations
- Groupby, merge, pivot operations
- Data cleaning and transformation patterns
- Integration with SQL queries

### SQL Server (Optional but Recommended)
**Why here:** Many enterprises use SQL Server. Learning it after PostgreSQL is easier—you already know relational concepts. The T-SQL dialect has unique features worth knowing.

- T-SQL syntax differences
- Window functions and CTEs
- Integration with enterprise tools

---

## Phase 3: Cloud & Data Warehousing (Weeks 9-12)

### AWS Fundamentals
**Why now:** Cloud is where modern data pipelines live. Start with AWS because it's the market leader and integrates with everything downstream.

- EC2, S3, IAM basics
- VPC and networking fundamentals
- Cost management and monitoring

### Snowflake
**Why after AWS basics:** Snowflake is a cloud-native data warehouse built for analytics. Understanding AWS first helps you grasp cloud architecture; Snowflake builds on those concepts.

- Architecture: compute vs. storage separation
- Data loading and unloading
- Query optimization and cost control
- Integration with Python and dbt

---

## Phase 4: Data Pipeline Orchestration (Weeks 13-16)

### Airflow
**Why first in orchestration:** Airflow is the industry standard for workflow orchestration. It's Python-native, so you already know the language. Master it before exploring alternatives.

- DAG design and task dependencies
- Operators and sensors
- Scheduling and monitoring
- Integration with Snowflake and AWS

### Dagster
**Why after Airflow:** Dagster is a modern alternative with stronger data lineage and asset management. Learning Airflow first gives you context for why Dagster's approach is different and better in certain scenarios.

- Asset-oriented workflows
- Data lineage and observability
- Comparison with Airflow patterns

### dbt (Data Build Tool)
**Why here:** dbt transforms raw data in your warehouse using SQL. It sits between your data pipeline (Airflow) and your warehouse (Snowflake). Learn it after orchestration so you understand the full flow.

- dbt projects and models
- Transformations in SQL
- Testing and documentation
- Integration with Snowflake and Airflow

---

## Phase 5: Big Data Processing (Weeks 17-20)

### Spark
**Why now:** Spark handles data at scale when Pandas and SQL hit limits. You've already learned Python, SQL, and cloud concepts—Spark combines all three.

- RDDs and DataFrames
- Transformations and actions
- Spark SQL
- Distributed computing principles
- Integration with AWS and Kubernetes

---

## Phase 6: Machine Learning & Deep Learning (Weeks 21-24)

### PyTorch
**Why here, not earlier:** You need data engineering skills first. PyTorch is for building and training models. Without clean data pipelines, you have nothing to train on.

- Tensors and autograd
- Neural network fundamentals
- Training loops and optimization
- GPU acceleration basics

---

## Phase 7: Containerization & Orchestration (Weeks 25-28)

### Kubernetes
**Why late in the sequence:** Kubernetes deploys containerized applications at scale. You need to understand what you're deploying (ML models, data pipelines) before learning the deployment layer.

- Pods, services, and deployments
- StatefulSets for data applications
- Helm for package management
- Integration with Spark and model serving

---

## Phase 8: Analytics & Visualization (Weeks 29-32)

### Power BI
**Why here:** By now, you have clean data in Snowflake. Power BI connects to it and creates dashboards. Learn it after your data is production-ready.

- Data modeling in Power BI
- DAX formulas
- Dashboard design
- Integration with Snowflake and SQL Server

### Tableau
**Why after Power BI:** Both are BI tools; learning one makes the other easier. Tableau is often preferred for exploratory analysis; Power BI for enterprise integration.

- Workbook and dashboard creation
- Calculated fields and LOD expressions
- Performance optimization
- Comparison with Power BI approaches

---

## Learning Strategy

**Parallel tracks:** Phases 1-2 can overlap. Start Python + SQL simultaneously.

**Project-based:** Build an end-to-end project at each phase:
- Phase 2: Extract data from PostgreSQL, clean with Pandas
- Phase 4: Orchestrate a pipeline with Airflow, transform with dbt
- Phase 6: Train a PyTorch model on cleaned data
- Phase 7: Deploy the pipeline on Kubernetes
- Phase 8: Visualize results in Power BI

**Time estimate:** 8 months of consistent, focused learning (20-30 hours/week).