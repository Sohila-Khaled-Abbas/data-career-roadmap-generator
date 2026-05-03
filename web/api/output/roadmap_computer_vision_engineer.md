# Computer Vision Engineer Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### Python
**Why first:** Python is the lingua franca of computer vision and data engineering. Every tool downstream depends on it. You cannot meaningfully learn PyTorch, Spark, or any data pipeline without solid Python fundamentals.

**Focus areas:**
- Core syntax, data structures, OOP
- NumPy and basic array operations
- File I/O and working with libraries

---

## Phase 2: Data & SQL Fundamentals (Weeks 5-8)

### SQL
**Why now:** Before touching any data platform, you need to understand relational data and query logic. This is the bedrock of data retrieval across all platforms you'll use.

**Focus areas:**
- SELECT, JOIN, aggregations, subqueries
- Indexing and query optimization basics
- Transaction concepts

### Pandas
**Why after SQL:** Pandas is Python's in-memory SQL equivalent. Learning SQL first makes pandas intuitive—you already understand the mental model of filtering, grouping, and joining data.

**Focus areas:**
- DataFrames and Series
- Groupby, merge, pivot operations
- Data cleaning and transformation

### PostgreSQL
**Why here:** A concrete relational database to practice SQL and understand how databases actually work. PostgreSQL is production-grade and teaches you real constraints (ACID, indexes, query plans).

---

## Phase 3: Computer Vision Core (Weeks 9-14)

### PyTorch
**Why now:** You have Python fluency and understand data manipulation. PyTorch is the dominant framework for computer vision research and production. Learn it before distributed systems—you need to understand single-machine deep learning first.

**Focus areas:**
- Tensors and autograd
- Building neural networks from scratch
- Training loops, loss functions, optimization
- CNN architectures (ResNet, VGG, etc.)
- Transfer learning

---

## Phase 4: Scaling Data & Pipelines (Weeks 15-20)

### Spark
**Why now:** You understand Python, SQL, and single-machine data processing. Spark is the distributed version of pandas/SQL. Essential for processing the massive datasets computer vision projects generate.

**Focus areas:**
- RDDs and DataFrames
- Distributed SQL queries
- Partitioning and shuffling
- Performance tuning

### SQL Server & Snowflake
**Why after Spark:** You now understand distributed data concepts. These are enterprise data warehouses. SQL Server is on-premises; Snowflake is cloud-native. Learn both because they represent different deployment models you'll encounter.

**Focus areas:**
- Data warehouse architecture
- Query optimization at scale
- Cost management (especially Snowflake)
- Integration with cloud platforms

### dbt
**Why here:** dbt transforms raw data into analytics-ready tables. It sits between your data warehouse and analytics tools. Learn it after understanding Spark and SQL—you need to know what you're optimizing.

**Focus areas:**
- Data modeling (staging, intermediate, marts)
- Testing and documentation
- Lineage and dependencies

---

## Phase 5: Orchestration & Workflow (Weeks 21-26)

### Airflow
**Why now:** You have data pipelines (Spark jobs, dbt models). Airflow orchestrates them—scheduling, retries, monitoring, dependencies. Learn it before Dagster to understand the traditional approach.

**Focus areas:**
- DAGs and operators
- Task dependencies and scheduling
- Error handling and alerting
- Monitoring and logging

### Dagster
**Why after Airflow:** Dagster is a modern alternative with stronger data lineage and asset management. Learning Airflow first gives you context for why Dagster improves on it.

**Focus areas:**
- Assets and ops
- Data lineage and observability
- Testing pipelines
- Deployment patterns

---

## Phase 6: Cloud & Infrastructure (Weeks 27-32)

### AWS
**Why now:** You have workloads to deploy (PyTorch models, Spark jobs, data pipelines). AWS is the dominant cloud platform. Learn core services relevant to your stack.

**Focus areas:**
- EC2, S3, RDS
- SageMaker for model training and deployment
- Lambda for serverless compute
- IAM and security basics
- Cost monitoring

### Kubernetes
**Why after AWS:** Kubernetes orchestrates containerized workloads at scale. Learn it after understanding cloud infrastructure and having real services to deploy. It's the production standard for model serving and pipeline infrastructure.

**Focus areas:**
- Pods, deployments, services
- ConfigMaps and secrets
- Persistent volumes
- Helm for templating
- Monitoring and logging

---

## Phase 7: Analytics & Visualization (Weeks 33-36)

### Power BI & Tableau
**Why last:** These are consumption layers. You need data pipelines, warehouses, and models in place first. Learn both because they serve different organizational contexts—Power BI integrates with Microsoft ecosystems; Tableau is platform-agnostic.

**Focus areas:**
- Data source connections
- Dashboard design and interactivity
- Performance optimization
- Row-level security

---

## Learning Strategy

**Parallel tracks where applicable:**
- Phases 1-3 are strictly sequential
- In Phase 4, you can learn Spark and SQL Server/Snowflake in parallel
- In Phase 5, learn Airflow and Dagster in parallel after both are introduced
- Phase 6 can overlap with Phase 5 (deploy as you build)
- Phase 7 is independent; start once Phase 4 is solid

**Project-based validation:**
- After Phase 3: Build a computer vision model (image classification, object detection)
- After Phase 4: Ingest raw image metadata into a data warehouse, transform with dbt
- After Phase 5: Automate model retraining and data pipeline with Airflow
- After Phase 6: Deploy the model on Kubernetes, serve predictions via API
- After Phase 7: Build dashboards tracking model performance and data quality