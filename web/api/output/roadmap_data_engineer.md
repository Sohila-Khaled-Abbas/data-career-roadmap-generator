# Data Engineer Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### Python
**Why first:** Python is the lingua franca of data engineering. Every tool in your stack either uses Python or integrates with it. You need fluency here before touching specialized frameworks.

- Core syntax, data structures, functions
- File I/O and basic scripting
- Virtual environments and package management

### SQL
**Why alongside Python:** SQL is non-negotiable for data work. You'll query databases from day one. Learning it early prevents bad habits and makes everything downstream easier.

- SELECT, WHERE, JOIN operations
- Aggregations and GROUP BY
- Subqueries and CTEs
- Query optimization basics

### Pandas
**Why here:** Pandas is Python's data manipulation library. It's your first hands-on tool for working with structured data and bridges Python fundamentals to real data problems.

- DataFrames and Series
- Data cleaning and transformation
- Merging and reshaping
- Basic performance awareness

---

## Phase 2: Data Warehousing & Storage (Weeks 5-8)

### PostgreSQL
**Why first in this phase:** A solid relational database foundation. PostgreSQL is production-grade, open-source, and teaches you real database concepts without vendor lock-in. Master it before moving to cloud warehouses.

- Schema design and normalization
- Indexes and query performance
- Transactions and ACID properties
- Backup and replication basics

### Snowflake
**Why after PostgreSQL:** Snowflake is the modern cloud data warehouse. You now understand relational concepts and can focus on Snowflake's unique architecture: separation of compute/storage, time-travel, and semi-structured data handling.

- Architecture and cost model
- Data loading (COPY, Snowpipe)
- Performance tuning for cloud
- Role-based access control

### AWS (Core Services)
**Why here:** You need cloud infrastructure to run Snowflake and other tools. Focus on the data path: S3, IAM, EC2 basics, and networking.

- S3 (buckets, lifecycle policies, security)
- IAM (users, roles, policies)
- VPC and security groups
- EC2 fundamentals
- CloudWatch for monitoring

---

## Phase 3: Data Processing & Transformation (Weeks 9-14)

### Spark
**Why here:** Spark handles massive datasets that Pandas can't. You now have SQL knowledge and Python skills to learn distributed computing concepts. Spark is the industry standard for big data processing.

- RDDs and DataFrames
- Transformations and actions
- Partitioning and shuffling
- Performance tuning (memory, parallelism)
- Spark SQL

### dbt (Data Build Tool)
**Why after Spark:** dbt transforms raw data into analytics-ready tables using SQL and Python. You have SQL mastery and understand data warehouses. dbt enforces best practices in transformation logic.

- Project structure and profiles
- Models, tests, and documentation
- Incremental models
- Macros and Jinja templating
- Integration with Snowflake

### SQL Server
**Why here:** Some enterprises use SQL Server instead of PostgreSQL or Snowflake. Learn it as a variant, not a replacement. Your SQL fundamentals transfer; focus on T-SQL specifics and differences.

- T-SQL syntax and stored procedures
- Integration with Azure ecosystem
- Performance monitoring

---

## Phase 4: Orchestration & Workflow (Weeks 15-18)

### Airflow
**Why first in orchestration:** Airflow is the most widely adopted workflow orchestrator. It teaches you DAG-based thinking, dependency management, and scheduling—concepts that transfer to other tools.

- DAGs and operators
- Task dependencies and branching
- Sensors and triggers
- Monitoring and alerting
- Scaling with Celery/Kubernetes

### Dagster
**Why after Airflow:** Dagster is a modern alternative with stronger data lineage and asset-oriented design. You understand orchestration concepts; now learn a more opinionated, asset-centric approach.

- Assets and ops
- Sensors and dynamic orchestration
- Data lineage and observability
- Integration with dbt and Spark

### Kubernetes
**Why here:** Both Airflow and Dagster scale on Kubernetes. You now understand orchestration; learn the infrastructure layer that runs it.

- Pods, services, and deployments
- ConfigMaps and secrets
- Helm charts
- Resource management
- Logging and debugging

---

## Phase 5: Analytics & Visualization (Weeks 19-22)

### Power BI
**Why first:** Power BI is Microsoft's dominant BI tool. It's accessible and teaches dashboard design, data modeling, and business metrics without overwhelming complexity.

- Data modeling and relationships
- DAX formulas
- Dashboard design and interactivity
- Row-level security
- Integration with SQL Server and cloud data

### Tableau
**Why after Power BI:** Tableau is the premium alternative, stronger in exploratory analysis and complex visualizations. You understand BI fundamentals; focus on Tableau's unique strengths.

- Dimensions, measures, and calculated fields
- Advanced chart types
- Dashboards and storytelling
- Performance optimization
- Tableau Server administration

---

## Phase 6: Advanced ML & Specialized Tools (Weeks 23+)

### PyTorch
**Why last:** PyTorch is for machine learning pipelines. You now have Python mastery, data processing skills, and orchestration knowledge. PyTorch is the tool, not the foundation.

- Tensors and autograd
- Neural network basics
- Training loops and optimization
- Integration with data pipelines
- Model deployment considerations

---

## Learning Strategy

**Parallel tracks:** Phases 1-2 can overlap. Start AWS while learning PostgreSQL.

**Hands-on projects:** Build end-to-end pipelines at each phase:
- Phase 2: Load CSV → PostgreSQL → query
- Phase 3: Raw data → Spark processing → Snowflake via dbt
- Phase 4: Schedule Phase 3 pipeline with Airflow
- Phase 5: Visualize Snowflake data in Power BI
- Phase 6: Add ML predictions to your pipeline

**Time estimate:** 6 months of consistent, focused learning (20-30 hours/week).