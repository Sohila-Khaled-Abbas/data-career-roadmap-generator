# Data Analyst Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### SQL
**Why first:** SQL is the lingua franca of data work. You cannot analyze data without querying it. Every downstream tool depends on your ability to write efficient queries. Master this before touching any other tool.

- Relational database concepts
- SELECT, JOIN, aggregations, window functions
- Query optimization and indexing basics
- Practice on PostgreSQL and SQL Server

### Python Fundamentals
**Why concurrent with SQL:** Python is your primary programming language for data work. You need both query skills and scripting skills in parallel. Start with basics while building SQL muscle memory.

- Variables, data types, control flow
- Functions and modules
- File I/O and basic data manipulation
- NumPy and Pandas introduction

### PostgreSQL & SQL Server
**Why now:** Understand relational databases at a practical level. These are your data sources. Learn their specific dialects and quirks while SQL concepts are fresh.

---

## Phase 2: Core Data Skills (Weeks 5-12)

### Pandas
**Why here:** Now that you know SQL and Python basics, Pandas is your bridge to data manipulation in code. It's the standard library for exploratory data analysis and data cleaning—90% of daily work.

- DataFrames and Series
- Data cleaning and transformation
- Groupby and aggregations
- Merging and reshaping data

### Power BI & Tableau
**Why now:** You have data querying and manipulation skills. Now learn to communicate findings visually. These tools are industry standards for dashboarding and stakeholder communication. Start with one, then learn the other.

- Data modeling for visualization
- Dashboard design principles
- Interactive reports and filters
- Publishing and sharing

### AWS Fundamentals
**Why here:** Before diving into cloud-native tools, understand the cloud ecosystem. AWS is the market leader. Learn S3, EC2, and IAM basics—these underpin everything that follows.

- S3 (data storage)
- EC2 (compute instances)
- IAM (access control)
- Basic networking and VPCs

---

## Phase 3: Advanced Data Engineering (Weeks 13-24)

### Snowflake
**Why here:** You now understand SQL, databases, and cloud basics. Snowflake is a cloud data warehouse built for analytics. It's where modern data teams store and query data at scale.

- Architecture and compute separation
- Data loading and staging
- Performance tuning
- Cost optimization

### dbt (Data Build Tool)
**Why after Snowflake:** dbt transforms raw data into analytics-ready tables. It requires understanding your data warehouse (Snowflake) and SQL expertise. dbt is the modern standard for data transformation pipelines.

- Project structure and models
- Testing and documentation
- Incremental models
- Deployment and CI/CD

### Airflow
**Why here:** You now have transformation logic (dbt). Airflow orchestrates these workflows—scheduling, monitoring, and error handling. It's the industry standard for workflow automation.

- DAGs and task dependencies
- Operators and sensors
- Scheduling and backfilling
- Error handling and retries

### Spark
**Why here:** Airflow and dbt handle most workflows, but Spark handles massive-scale distributed processing. Learn it when you need to process data that doesn't fit in memory or requires complex transformations.

- RDD and DataFrame APIs
- Transformations and actions
- Partitioning and shuffling
- Performance tuning

---

## Phase 4: Specialized & Advanced (Weeks 25-36)

### Kubernetes
**Why here:** You've built data pipelines with Airflow and Spark. Kubernetes containerizes and orchestrates these at scale. Learn it when deploying production systems across teams.

- Pods, services, and deployments
- ConfigMaps and secrets
- Persistent volumes
- Helm charts for data tools

### Dagster
**Why here:** You know Airflow. Dagster is a modern alternative with stronger data lineage and asset management. Learn it as an alternative or complement to Airflow for more sophisticated orchestration needs.

- Assets and ops
- Sensors and resources
- Data lineage and observability
- Deployment strategies

### PyTorch
**Why last:** Machine learning is specialized. Only pursue this if your role requires predictive modeling or deep learning. It builds on Python and Pandas mastery but is orthogonal to core data analytics work.

- Tensors and autograd
- Neural network basics
- Training loops
- Model evaluation and deployment

---

## Learning Strategy

**Parallel tracks:** Phases 1-2 can overlap. Start SQL + Python together, then add Pandas while learning cloud basics.

**Project-based:** Build end-to-end projects at each phase:
- Phase 1: Query a database, export to CSV, analyze with Pandas
- Phase 2: Build a dashboard from a data warehouse
- Phase 3: Create a dbt project with Airflow orchestration
- Phase 4: Deploy a Spark job on Kubernetes

**Time investment:** 6-9 months to reach Phase 3 proficiency. Phases 4 are specialized—pursue based on job requirements.