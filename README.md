# Train delay data project
train_delay_data_project ingests live (or near-real-time) UK train data, processes it into useful features, trains a model to predict delays, serves the predictions through a simple dashboard or API
## Project overview
### Goal - build a small but realistic system that
* Ingests live (or near-real-time) UK train data
* Processes it into useful features
* Trains a model to predict delays
* Serves the predictions through a simple dashboard or API
* Aim to phase in real-time streaming
### Data sources you can use
* National Rail data feeds – they provide APIs and XML feeds via their developer platform and the Rail Data Marketplace, including real-time information from systems like Darwin and performance-related data
* Network Rail open data feeds – they offer public operational feeds such as realtime performance, schedules, and movement data once you create an account
* Third-party APIs – services like UK Train API or Realtime Trains offer live and schedule data for British rail, sometimes in simpler formats for developers.
* You can start with static or historical data from these sources (or even CSV exports) and only later wire in “live” ingestion.
### Recommended tech stack
* Ingestion & storage
  * Python scripts for pulling data
  * PostgreSQL or DuckDB for storage (local is fine)
* Transformation & modelling
  * dbt for data modelling and tests
  * Python/scikit-learn for the prediction model
* Orchestration
  * Airflow or Prefect to schedule and chain pipelines
* Serving / UI
  * Streamlit web app for visualising predictions and current delays
* Streaming
  * Kafka (or even just scheduled frequent pulls) to simulate real-time ingestion
  * Spark Structured Streaming if you want to go big, but this can be a “Phase 2” thing
### Architecture at a high level
#### 1. Raw layer
* What: Raw train movements, timetables, and delay info from an API or feed
* Where: Stored in a raw_* schema/table in Postgres/DuckDB
#### 2. Modelled layer (dbt):
*	What: Cleaned tables like trains, stops, journeys, delays
*	Features
  *	Planned vs actual arrival times
  * Station, operator, route, time of day, day of week
  * Historical average delay per route/station/time slot
#### 3.	Prediction layer:
*	What: A model that predicts “likelihood and size of delay for a given upcoming service”
*	How: Batch training daily; scoring upcoming services every few minutes
#### 4.	Serving layer:
* What: A small app where you select a station/route and see
* Upcoming services
  * Predicted delay (e.g. “On time”, “Low risk”, “High risk”)
  * Confidence or probability
## Get and explore the data
1.	Register / choose data source:
o	Option A: Use National Rail / Network Rail feeds and pull performance/timetable data.
o	Option B: Use a third-party API like UK Train API or Realtime Trains if they’re easier to integrate.
2.	Write a simple ingestion script (Python):
o	Hit the API periodically or download a historical dump
o	Store responses as JSON or into raw_trains / raw_movements tables
3.	Goal for this phase
o	You can query: “For this train, what time was it supposed to arrive, and when did it actually arrive?”
4.	Do an exploratory notebook to inspect
o	Distribution of delays
o	Difference by time of day or station
o	Missing or messy fields
o	This will also help you design your features.
### Build a proper data model with dbt
* Set up dbt project
  * Connect it to your Postgres/DuckDB
  * Create models like
    * stg_trains (cleaned raw train data)
    * stg_movements
    * fct_journey_delays (fact table with delay as a metric)
* Create features for the model: 
  * planned_arrival_time, actual_arrival_time, delay_minutes
  * hour_of_day, day_of_week, is_peak
  * route_id, origin_station, destination_station
  * Historical average delay for route_id at hour_of_day
* Add tests:
  * Use dbt tests to ensure: 
    * No duplicate primary keys
    * Non-null fields where needed
    * Reasonable ranges for delay_minutes
### Train and serve a delay prediction model
#### Model training (offline)
* Load your fct_journey_delays into a notebook
  * Frame it as either
    * Classification: Will delay > 5 minutes? (yes/no)
    * Regression: Predict delay_minutes
    * Logistic regression / Random Forest / XGBoost
* Track metrics (accuracy / ROC-AUC for classification, MAE for regression)
  * Plot feature importance
  * Save the trained model (e.g. using joblib)
* Batch scoring
  * Create a Python script that fetches upcoming services (next 30–60 minutes)
  * Generates features with dbt models
  * Loads the saved model and writes predictions into a predicted_delays table
* Orchestrate with Airflow/Prefect
  * DAG flow
    * Task 1: Ingest new data
    * Task 2: Run dbt models
    * Task 3: Run batch predictions
### Build a small but effective UI
* Use Streamlit (fast and simple)
  * Filter: Station / route / timeframe
  * Table: Upcoming trains with planned time, predicted delay, risk label
  * Plot: Historical average delay for that station over the day
## Applicable technologies
This project demonstrates the following skills and technologies:
* Modern data stack: dbt, Airflow/Prefect, Streamlit, cloud-like patterns
* Real-time / near-real-time thinking: Even if it’s scheduled batch, you can describe how you’d make it fully streaming with Kafka or a cloud pub/sub later
* End-to-end ownership: From raw data ingestion to model deployment and user-facing app
* Data quality and monitoring: Through tests and possibly basic metrics
