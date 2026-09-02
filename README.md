# NBA Data Pipeline

An end-to-end AWS data pipeline that ingests, cleans, and queries public NBA team data on a daily schedule.

## Problem

I wanted hands-on practice building a production-style data pipeline (scheduled ingestion, cataloging, cleaning, and querying) rather than a one-off analysis notebook. NBA team data via the [balldontlie API](https://www.balldontlie.io/) was a simple, free, well-structured dataset to build against.

## Architecture

balldontlie API
│
▼
AWS Lambda (nba-pipeline-ingest)
triggered daily via EventBridge
│
▼
S3 (raw/teams/)
│
▼
Glue Crawler (nba-pipeline-crawler)
catalogs raw data → nba-pipeline-db
│
▼
Glue ETL Job (nba-pipeline-clean-teams)
flattens nested JSON
│
▼
S3 (processed/teams/) → teams_clean table
│
▼
Athena
SQL queries over the cleaned table


**Services used:** AWS Lambda, EventBridge, S3, Glue (Crawler + ETL), Athena, IAM

## What broke, and how I fixed it

After a week of daily runs, my "unique teams" count in Athena was inflated — 30 real NBA teams were showing up as ~210 rows. The Lambda function was re-ingesting the full team list on every scheduled run instead of only new records, so seven days of daily ingests meant seven duplicated copies of the same data landing in the raw S3 path.

Rather than rework the Glue ETL job immediately, I fixed it at the query layer first using `COUNT(DISTINCT id)` in Athena, so I could keep moving without blocking on a bigger pipeline change. The longer-term fix — deduplicating at ingestion or during the Glue ETL step — is a planned improvement (see below).

## Status / next steps

- [ ] Add unit tests for the Glue ETL transformation logic
- [ ] Add error handling and input validation to the Lambda ingest function (malformed API responses, retries)
- [ ] Move deduplication logic from the query layer into the Glue ETL job itself
- [ ] Document IAM role/permissions setup

This project is actively being built out — check commit history for the latest state.
