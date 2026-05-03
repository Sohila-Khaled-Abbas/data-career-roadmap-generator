# Analytics Engineer Learning Roadmap

## Phase 1: Foundations (Weeks 1-4)

### SQL
**Why first:** SQL is the lingua franca of data work. You cannot be effective in analytics without fluent SQL. Every downstream tool depends on your ability to query, transform, and understand data at the source. Master this before touching any framework.

- Relational database concepts
- SELECT, JOIN, GROUP BY, window functions
- Query optimization and execution plans
- Subqueries and CTEs

### Python Basics
**Why concurrent with SQL:** Python is your primary programming language for analytics. Start fundamentals in parallel with SQL so you can begin combining them immediately.

- Variables, data types, control flow
- Functions and modules
- File I/O and basic scripting
- Virtual environments and package management

### Postgres
**Why here:** A solid relational database to practice SQL against. Postgres is production-grade, widely used, and teaches you real database concepts without cloud complexity.

- Installation and basic administration
- Creating tables and schemas
- Writing and testing queries
- Understanding indexes and query plans

---

## Phase 2: Core Data Stack (Weeks 5-12)

### Pandas
**Why now:** Bridge between SQL and Python. Pandas lets you manipulate data programmatically and is essential for data exploration, cleaning, and transformation before it reaches production pipelines.

- DataFrames and Series
- Filtering, grouping, and aggregation
- Merging and reshaping data
- Performance considerations with large datasets

### AWS Fundamentals
**Why here:** Cloud infrastructure is non-negotiable in modern analytics. Start with AWS basics to understand compute, storage, and networking before building on it.

- EC2, S3, IAM basics
- VPCs and security groups
- CloudWatch and basic monitoring
- Cost awareness

### Snowflake
**Why after AWS basics:** Snowflake is a cloud-native data warehouse built on AWS (and other clouds). Understanding cloud fundamentals first makes Snowflake architecture click. It's the industry standard for analytics workloads.

- Architecture: compute, storage, metadata
- Creating warehouses, databases, schemas
- Data loading and unloading
- Query performance and cost optimization
- Snowflake-specific SQL features

### dbt (Data Build Tool)
**Why here:** dbt transforms raw data into analytics-ready tables using SQL and Python. It's the standard for analytics engineering and sits naturally after Snowflake. dbt enforces best practices: version control, testing, documentation, and lineage.

- Project structure and configuration
- Models, sources, and tests
- Incremental models and snapshots
- Jinja templating for DRY SQL
- Documentation and lineage

---

## Phase 3: Orchestration & Pipelines (Weeks 13-18)

### Airflow
**Why first in orchestration:** Airflow is the most widely adopted workflow orchestrator. It teaches you DAG-based thinking, error handling, and scheduling—concepts that transfer to other tools.

- DAGs and operators
- Task dependencies and branching
- Sensors and triggers
- Monitoring and alerting
- XComs for task communication

### Dagster
**Why after Airflow:** Dagster is a modern alternative with stronger data lineage, asset-based thinking, and better testing. Learning Airflow first gives you orchestration fundamentals; Dagster shows you the evolution of the space.

- Assets and asset graphs
- Ops and graphs
- Sensors and dynamic orchestration
- Testing and local development
- Comparison with Airflow patterns

---

## Phase 4: Advanced Processing (Weeks 19-24)

### Spark
**Why here:** Spark handles massive datasets that Pandas and single-machine SQL cannot. Learn it after orchestration because production pipelines often use Spark for heavy lifting.

- RDDs, DataFrames, and Datasets
- Transformations and actions
- Partitioning and shuffling
- Performance tuning
- Spark SQL and integration with Snowflake

### Kubernetes
**Why after Spark:** Kubernetes orchestrates containerized workloads at scale. After learning Spark, you'll understand why Kubernetes matters for distributed systems. It's essential for production deployments.

- Pods, services, and deployments
- ConfigMaps and secrets
- Persistent volumes
- Helm charts
- Running Spark on Kubernetes

---

## Phase 5: Machine Learning & Visualization (Weeks 25-30)

### PyTorch
**Why here:** PyTorch is for building machine learning models. Learn it after core data engineering because you need clean, reliable data pipelines before experimenting with ML.

- Tensors and autograd
- Building neural networks
- Training loops and optimization
- Common architectures
- Integration with production pipelines

### Power BI & Tableau
**Why together, at the end:** These are visualization and BI tools. Learn them after your data is clean and accessible. Both serve similar purposes; learn one deeply, then the other is straightforward.

- Data modeling and relationships
- Creating dashboards and reports
- Interactivity and drill-down
- Performance optimization
- Publishing and sharing

**Power BI first** if your organization uses Microsoft stack; **Tableau first** if you need broader market relevance.

### SQL Server
**Why last:** SQL Server is a relational database like Postgres, but enterprise-focused. If your organization uses it, learn it after Postgres. The SQL fundamentals transfer; you're learning platform-specific features.

- T-SQL syntax and differences from standard SQL
- Stored procedures and functions
- Indexing and query optimization
- Integration with Azure ecosystem
- Administration basics

---

## Learning Strategy

**Parallel tracks:** Phases 1-2 can overlap. Start SQL and Python together, then add Pandas and AWS in parallel.

**Project-based:** Build an end-to-end pipeline: extract data from Postgres → transform with dbt in Snowflake → orchestrate with Airflow → visualize in Power BI.

**Depth over breadth:** Master SQL and Python deeply before moving to frameworks. A weak foundation breaks everything downstream.

**Revisit constantly:** You'll return to SQL and Python throughout your career. Each new tool teaches you something that makes you better at the basics.