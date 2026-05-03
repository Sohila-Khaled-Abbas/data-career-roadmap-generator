# Power BI Developer Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### SQL
**Why first:** SQL is the bedrock of data work. You cannot effectively use Power BI, Snowflake, or any data platform without querying data. Master this before touching anything else.

- Learn SELECT, WHERE, JOIN, GROUP BY, aggregations
- Practice with PostgreSQL locally
- Build comfort with subqueries and window functions

### Python Basics
**Why now:** Python is the lingua franca of data engineering and analytics. You'll need it for data manipulation, automation, and eventually pipeline orchestration.

- Variables, data types, control flow, functions
- Focus on practical scripting, not deep CS theory
- Set up a local environment (virtual environments, pip)

### PostgreSQL
**Why here:** A solid relational database to practice SQL deeply. It's production-grade and teaches you real database concepts without cloud complexity.

- Install locally, understand schemas and indexes
- Write and optimize queries
- Understand transactions and basic performance tuning

---

## Phase 2: Core Data Stack (Weeks 5-12)

### Pandas
**Why now:** The standard Python library for data manipulation. You'll use this constantly for ETL, data cleaning, and exploratory analysis before loading into Power BI.

- DataFrames, Series, indexing, groupby operations
- Merging, reshaping, and cleaning data
- Integration with SQL queries

### Power BI Fundamentals
**Why here:** You have SQL and Python basics. Now learn Power BI's core: data modeling, DAX, and visualization. This is your primary tool.

- Data import and transformation (Power Query)
- Data modeling (star schema, relationships)
- Basic DAX formulas and measures
- Dashboard and report design

### Snowflake
**Why now:** A modern cloud data warehouse. Learn it as your primary data source for Power BI. It's easier than on-prem SQL Server and more aligned with modern data stacks.

- Architecture and compute/storage separation
- Creating tables, loading data, querying at scale
- Understanding cost implications
- Integration with Power BI

### AWS Fundamentals
**Why here:** You need to understand where your data lives and how to access it. Start with S3, IAM, and basic networking.

- S3 for data storage
- IAM for access control
- EC2 basics (you'll need this for running tools)
- VPC and security groups

---

## Phase 3: Data Engineering & Orchestration (Weeks 13-20)

### SQL Server
**Why now:** Many enterprises still use SQL Server. Learn it as an alternative on-prem data source. Your SQL knowledge transfers; focus on T-SQL specifics and integration with Power BI.

- T-SQL syntax differences from PostgreSQL
- Stored procedures and performance tuning
- Integration with Power BI via native connectors

### dbt (Data Build Tool)
**Why here:** You have SQL, Snowflake, and Python. dbt lets you version-control, test, and document your data transformations. Essential for professional data engineering.

- Project structure and YAML configuration
- Writing and testing models
- Lineage and documentation
- Integration with Snowflake

### Airflow
**Why now:** You need to orchestrate data pipelines. Airflow is the industry standard for scheduling and monitoring ETL workflows.

- DAG concepts and task dependencies
- Operators and sensors
- Scheduling and monitoring
- Running locally and on AWS

### Dagster
**Why here:** A more modern alternative to Airflow with better data lineage and asset management. Learn it as a complement or alternative depending on your team's direction.

- Asset-oriented workflows
- Ops and graphs
- Sensors and dynamic orchestration
- Comparison with Airflow patterns

---

## Phase 4: Advanced Analytics & Scaling (Weeks 21-28)

### Spark
**Why now:** You have orchestration and SQL skills. Spark handles massive datasets that Pandas cannot. Learn PySpark for distributed data processing.

- RDDs, DataFrames, and SQL on Spark
- Transformations and actions
- Partitioning and performance tuning
- Integration with Airflow/Dagster pipelines

### Kubernetes
**Why here:** You're running Airflow, Spark, and other services at scale. Kubernetes manages containerized workloads in production.

- Pods, services, and deployments
- ConfigMaps and secrets
- Helm for package management
- Running Airflow and Spark on Kubernetes

### PyTorch
**Why now:** You have Python, Pandas, and Spark skills. PyTorch is for machine learning models that feed insights into Power BI dashboards.

- Tensors and autograd
- Building neural networks
- Training and evaluation
- Exporting models for inference

### Tableau (Optional Advanced)
**Why here:** You're expert in Power BI. Tableau is a complementary visualization tool. Learn it for competitive knowledge or if your organization uses both.

- Tableau's data model and calculations
- Advanced visualizations
- Comparison with Power BI approaches

---

## Phase 5: Integration & Mastery (Weeks 29+)

### End-to-End Pipelines
Combine everything: Python → dbt → Snowflake → Spark (if needed) → Power BI dashboards, orchestrated with Airflow/Dagster on Kubernetes.

### Specialization
- Choose depth: advanced DAX and Power BI optimization, or
- Advanced ML with PyTorch feeding Power BI, or
- Large-scale data engineering with Spark and Kubernetes

---

## Learning Principles

1. **Prerequisites matter:** Don't skip SQL or Python basics. Everything else depends on them.
2. **Practice with real data:** Use public datasets (Kaggle, AWS Open Data) throughout.
3. **Build projects:** Create an end-to-end pipeline from raw data to Power BI dashboard at each phase.
4. **Understand the "why":** Know why Snowflake beats PostgreSQL at scale, why dbt matters, why Kubernetes is necessary.
5. **Stay current:** This stack evolves. Follow data engineering blogs and communities.