[TOC]

## Spark Introduction

### What is Spark?

- Open-source distributed computing system for big data processing.
- Unified analytics engine for processing large-scale datasets.
- Offers high-speed, in memory processing capabilities
- Handles complex data processing tasks, data transformation, machine learning, graph processing, and real-time stream processing.

### Problems Spark Solves

- Traditional systems struggle with large volumes of data and perform computations in a timely manner.
- Spark overcomes this limitations by distributing the data across a cluster of machines and processing it in parallel. This distributed computing model allows Spark to process data much faster.
- Enables faster big data analytics and real-time processing.

### Why Spark is better?

- Fault tolerance and reliability by automatically recovering from failures, ensuring data integrity and job completion.
- In-memory processing for improved performance allows it to cache frequently accessed data, reducing disk I/O. This makes Spark well-suited for iterative algorithms and interactive data analysis.
- Seamless integration with various data sources and frameworks.
- Extensive libraries for machine learning, graph processing, and streaming analytics.
- Provides APIs for python, Java, Scala, and R.

## Spark Installation

Create a virtual env and install PySpark:

```bash
python -m venv .pyspark-env
source pyspark-env/bin/activate

pip install pyspark
```

Create a new jupyter notebook in Jupyterlab or vscode. See more details in the notebook.

## SparkContext vs SparkSession

SparkContext

- represents the connection to a Spark cluster
- coordinates task execution across the cluster
- entry point in earlier versions of Spark (1.x)

SparkSession

- Introduced in Spark 2.0
- Unified entry point for interacting with Spark
- Combines the functionalities of SparkContext, SQLContext, HiveContext, and StreamingContext
- support multiple programming languages (Scala, Java, Python, R)

Functionality Differences of them

- SparkContext
  - core functionality for low-level programming and cluster interaction
  - create RDDs (Resilient Distributed Datasets)
  - perform transformations and defines actions
- SparkSession
  - extend SparkContext functionality
  - higher-level abstractions like DataFrames and Datasets
  - support structured querying using SQL or DataFrame API
  - provide data source APIs, machine learning algorithms and streaming capabilities

Usage differences

- SparkContext
  - explicit creation to interact with Spark cluster
  - create RDDs, applies transformations, manages cluster resources
- SparkSession
  - recommended entry point since Spark 2.0
  - unified entry point that manages SparkContext internally
  - simplifies interaction with Spark
  - offer higher-level API for structured data processing using DataFrames and Datasets

Backward Compatibility

- SparkContext
  - fully supported for backward compatibility
  - use in specific scenarios or with libraries/APIs reliant on it
- SparkSession
  - recommended entry point since Spark 2.0
  - provides a higher-level API and better integration with latest Spark features

## Spark RDD Transformations and Actions

RDDs (Resilient Distributed Datasets)

- backbone of data processing in Spark
- distributed, fault-tolerant, and parallelizable data stucture
- efficiently processes large datasets across a cluster

RDD characteristics

- immutable: transformations create new RDDs, a RDD can not be modified once created
- distributed: data partitioned and processed in parallel across the nodes
- resilient: lineage tracks transformations for fault tolerance, recover lost data and continue computations in case of failures
- lazily evaluated: not executed immediately, execution plan optimized, transformations evaluated when necessary
- fault-tolerant operations: map, filter, reduce, collect, count, save, etc

RDD Operations

- Transformations
  - create new RDDs by applying computation/manipulation
  - lazy evaluation, lineage graph
  - exp: map, filter, flatMap, reduceByKey, sortBy, join

- Actions
  - return results or perform actions on RDD, triggering execution
  - eager evaluation, data movement/computation
  - exp: collect, count, first, take, save, foreach

## Spark DataFrame Intro

- DataFrame in Apache Spark: Powerful abstraction for distributed and structured data
- DataFrame Structure: Similar to a table in a relational database (rows and columns)
- schema information: enables query optimization and various optimizations

Advantages of DataFrames over RDDs

- Optimized Execution:
  - schema info enables query optimization and predicate pushdowns
  - faster and more efficient data processing
- ease of use:
  - high-level, SQL-like interface for data interaction
  - simplified compared to complex RDD transformations
- Integration with Echosystem:
  - seamless integration with Spark's ecosystem (Spark SQL, MLib, GraphX)
- Built-in Optimization:
  - leveraging Spark's catalyst optimizer for advanced optimizations
  - predicate pushdown, constant folding, loop unrolling
- Interoperability:
  - easily convert to/from other data formats (Pandas DataFrames)
  - seamless integration with other data processing tools

## Create Spark DataFrame

- DataFrame: User-friendly and optimized approach for structured data in Apache Spark

## Spark DataFrame Operations

See more details in the notebook.

## Spark SQL and SQL Operations

- Spark SQL is a module in Apache Spark
- query structured and semi-structured data using SQL commands
- extends Spark's capabilities to handle structured data effectively

Key Features of Spark SQL

- unified data processing: unified API for both batch and real-time data processing, simplifying end-to-end data pipeline development
- schema inference: automatically infers structured data source's schema, reducing the need for explicit schema definitions
- data source abstraction: support a wide range of data sources (Hive, Parquet, Avro, JSON, JDBC), enhancing versatility for working with various data formats
- integration with Hive: seamlessly integrates with Apache Hive, enabling Hive query execution and access to Hive UDFs within Spark SQL.
