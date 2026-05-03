# BI Developer Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### SQL
**Why first:** SQL is the lingua franca of data work. Every tool downstream depends on your ability to query, transform, and understand data at the source. You cannot effectively use Snowflake, dbt, or any analytics platform without SQL fluency.

- Master SELECT, JOINs, aggregations, window functions
- Understand query optimization and execution plans
- Practice with PostgreSQL (lightweight, free, industry-standard)

### Python Basics
**Why concurrent with SQL:** Python is your primary programming language for BI automation, data manipulation, and scripting. Start here so you can automate tasks and build tools throughout your career.

- Core syntax, data structures, functions
- File I/O and basic scripting
- Package management (pip, virtual environments)

---

## Phase 2: Core Data Skills (Weeks 5-12)

### Pandas
**Why now:** Pandas is Python's data manipulation library. It bridges SQL and advanced analytics. You'll use it constantly for ETL, data cleaning, and exploratory analysis before moving to distributed systems.

- DataFrames and Series operations
- Groupby, merge, pivot operations
- Data cleaning and transformation patterns

### PostgreSQL (Deep Dive)
**Why deepen here:** PostgreSQL is a production-grade relational database. Understanding it deeply teaches you database design, indexing, and performance tuning—skills that transfer to Snowflake and SQL Server.

- Schema design and normalization
- Indexing strategies
- Transaction management and ACID properties

### Power BI & Tableau
**Why together:** Both are visualization and BI platforms. Learn one deeply, then the other becomes easier. Start with Power BI (Microsoft ecosystem dominance) or Tableau (industry standard)—choose based on your target companies.

- Data modeling for BI tools
- DAX (Power BI) or Tableau Calculations
- Dashboard design and performance optimization
- Connecting to databases and data sources

---

## Phase 3: Cloud & Scalable Data (Weeks 13-20)

### AWS Fundamentals
**Why before Snowflake:** AWS is the infrastructure layer. Understanding EC2, S3, IAM, and networking gives you context for why Snowflake runs on cloud and how data pipelines are architected at scale.

- S3 (object storage)
- EC2 (compute)
- IAM (access control)
- VPC and networking basics
- CloudWatch (monitoring)

### Snowflake
**Why after AWS:** Snowflake is a cloud data warehouse built on AWS/Azure/GCP. You now understand the cloud infrastructure it runs on. Snowflake is where BI developers spend most of their time—querying, modeling, and optimizing data.

- Architecture (compute, storage separation)
- Data loading and unloading
- Performance tuning and cost optimization
- Role-based access control
- Time travel and zero-copy cloning

### SQL Server
**Why here:** SQL Server is common in enterprise BI environments. You already know SQL deeply; this teaches you SQL Server-specific features (T-SQL, stored procedures, SSIS) and how it differs from PostgreSQL and Snowflake.

- T-SQL syntax and stored procedures
- Integration Services (SSIS) for ETL
- SQL Server Agent for scheduling
- Differences from standard SQL

---

## Phase 4: Data Engineering & Orchestration (Weeks 21-28)

### dbt (Data Build Tool)
**Why now:** dbt transforms raw data into analytics-ready tables using SQL and YAML. It's the modern standard for data transformation in BI. You have SQL mastery and cloud warehouse experience—dbt is the natural next step.

- Project structure and best practices
- Models, tests, and documentation
- Incremental models and snapshots
- Integration with Snowflake and data warehouses

### Airflow
**Why after dbt:** Airflow orchestrates data pipelines—scheduling dbt runs, SQL queries, and Python scripts. You now have transformations (dbt) and need to schedule and monitor them reliably.

- DAGs (Directed Acyclic Graphs)
- Operators and sensors
- Task dependencies and error handling
- Monitoring and alerting

### Dagster
**Why after Airflow:** Dagster is a modern orchestration alternative with stronger data lineage and asset management. Learning Airflow first gives you context for why Dagster improves upon it. Choose Airflow or Dagster based on your company's stack.

- Assets and asset graphs
- Ops and graphs
- Sensors and dynamic orchestration
- Data lineage and observability

---

## Phase 5: Advanced Analytics & Distributed Computing (Weeks 29-36)

### Spark
**Why here:** Spark processes massive datasets across clusters. You have BI fundamentals, cloud experience, and orchestration knowledge. Spark is for when data exceeds single-machine or warehouse capacity.

- RDDs, DataFrames, and SQL
- Transformations and actions
- Partitioning and shuffling
- Integration with Snowflake and cloud storage

### PyTorch
**Why last:** PyTorch is for machine learning and deep learning. BI developers rarely need this, but it's valuable for predictive analytics, anomaly detection, and advanced modeling. Learn it only if your role requires ML.

- Tensors and autograd
- Neural networks and training loops
- Integration with data pipelines
- Model deployment considerations

### Kubernetes
**Why last:** Kubernetes orchestrates containerized applications. It's infrastructure-heavy and most relevant if you're deploying Airflow, Spark, or custom services at scale. Many BI developers use managed services instead.

- Pods, services, and deployments
- ConfigMaps and secrets
- Helm for package management
- Running data tools on Kubernetes

---

## Learning Strategy

**Parallel tracks:** Phases 2 and 3 can overlap. Start AWS while finishing Pandas.

**Project-based:** Build an end-to-end pipeline: extract data from PostgreSQL → transform with Pandas/dbt → load to Snowflake → visualize in Power BI → orchestrate with Airflow.

**Depth over breadth:** Master SQL and Python deeply before spreading across tools. Tools change; fundamentals don't.

**Company-specific:** Adjust based on your target company's stack. Finance firms favor SQL Server; startups favor Snowflake + dbt + Airflow.