# Spotify-Data-Pipeline-Spark-Powered-Transformation-and-Snowflake-Storage

This project demonstrates the process of building a scalable and automated data pipeline on AWS. The pipeline extracts data from the Spotify API, processes it using AWS Glue and Lambda, and loads the transformed data into an S3 bucket, from where it can be analyzed and visualized using tools like Power BI.

![Screenshot 2024-08-23 002926](https://github.com/user-attachments/assets/fe16e767-4b8f-4cee-b4fc-ece607e176fc)

## Technology Used

- **AWS Lambda**: For extracting data from the Spotify API.
- **Amazon S3**: Used as both raw data storage and transformed data storage.
- **AWS Glue**: For data transformation using Spark.
- **AWS EventBridge**: For triggering the Lambda function.
- **Snowflake**: For loading and storing transformed data.
- **Power BI**: For data visualization and reporting.

## Pipeline Overview

The data pipeline consists of the following stages:

1. **Extract**:
   - Data is extracted from the Spotify API using AWS Lambda. 
   - The Lambda function is triggered by AWS EventBridge on a daily schedule.
   - The extracted raw data is stored in Amazon S3.

2. **Transform**:
   - AWS Glue processes the raw data stored in S3.
   - The transformation logic is written in PySpark and includes functions to process albums, artists, and songs.
   - The transformed data is saved back to Amazon S3 in CSV format.

3. **Load**:
   - The transformed data is then loaded into Snowflake using Snowpipe.
   - Power BI is used to create visual dashboards based on the data stored in Snowflake.

## Project Execution Flow

The following diagram provides a high-level overview of the project execution flow:

1. **AWS CloudWatch** triggers the Lambda function daily.
2. **AWS Lambda** extracts data from the Spotify API and stores it in S3.
3. **AWS Glue** processes the data stored in S3.
4. The transformed data is saved back to S3.
5. The transformed data is loaded into Snowflake using Snowpipe.
6. **Power BI** consumes the data from Snowflake for visualization.


## Project Visuals

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/08e4e6eb-94d5-4344-a82f-eefd0d2b31c5" alt="Image 1" width="300"/></td>
    <td><img src="https://github.com/user-attachments/assets/71dc4393-96fa-4f3f-af3f-b4e73c36df9b" alt="Image 2" width="300"/></td>
    <td><img src="https://github.com/user-attachments/assets/eaa85155-05aa-4e62-aa95-267d3ab5d121" alt="Image 3" width="300"/></td>
  </tr>
</table>


## Project Tree Structure

The following tree structure represents the project's organization:

```
spotify-data-pipeline/
├── lambda/
│   └── lambda_function.py       # Extracts data from Spotify API
├── glue/
│   └── glue_transformation.py   # Spark script for data transformation
├── s3/
│   ├── raw_data/                # S3 bucket for raw data storage
│   └── transformed_data/        # S3 bucket for transformed data
├── snowflake/
│   ├── snowpipe_config.sql      # Snowpipe configuration for data loading
├── dashboards/
│   ├── powerbi/                 # Power BI dashboard files
├── eventbridge/
│   └── event_rule.json          # EventBridge rule to trigger Lambda
├── README.md                    # Project README file
└── requirements.txt             # Python dependencies file

```

## Conclusion
This project serves as an excellent example of building an end-to-end data pipeline using AWS services. The integration of AWS Lambda, Glue, S3, and Snowflake provides a robust and scalable solution for processing and analyzing data from external APIs. The final output is visualized using Power BI, allowing for detailed analysis and insights into the Spotify dataset.
