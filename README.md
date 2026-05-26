

# Data Preparation and User-Level Aggregation Pipeline

## Project Context

This repository contains the data engineering and data cleaning pipeline developed for the IF29 project *“Comparison of Two Classification Methods for Detecting Atypical X (Twitter) Profiles”*.

The goal of this pipeline is to transform raw Twitter World Cup tweets stored in MongoDB into a **user-level aggregated dataset**, where each row corresponds to one Twitter profile and contains behavioral, social, and content-based features suitable for Machine Learning models.

This step provides the **input data** for both supervised and unsupervised classification approaches.

---

## Dataset Description

### Input Data

* Source: `Tweet_Worldcup` dataset
* Format: JSON documents
* Storage: MongoDB collection `tweets`
* Granularity: one document per tweet

Each tweet document follows the native Twitter JSON structure and may contain:

* tweet metadata
* embedded retweeted content (`retweeted_status`)
* user profile information (`user`)

### Key Assumption

For profile analysis, the pipeline focuses on the **author of the tweet** (`user`) and not on the original author of a retweeted status (`retweeted_status.user`).

---

## Pipeline Overview

The data preparation pipeline is fully implemented using a **MongoDB aggregation pipeline executed via mongosh**.

### Main Steps

1. Feature extraction at tweet level
2. Identification of retweets
3. Grouping tweets by user ID
4. Computation of aggregated behavioral indicators
5. Preservation of static user profile attributes
6. Output to a new MongoDB collection
7. Export to CSV and JSON formats

---

## MongoDB Aggregation Pipeline

### Tweet-Level Feature Engineering

For each tweet, the following features are computed:

* `is_retweet_flag`: binary indicator (1 if retweet, 0 otherwise)
* `tweet_length`: number of characters in the tweet text
* `hashtags_count`: number of hashtags
* `urls_count`: number of URLs
* `mentions_count`: number of user mentions
* `tweet_date`: tweet creation date converted to ISODate

---

### User-Level Aggregation

Tweets are grouped by `user.id`. For each user, the pipeline computes:

#### Activity Metrics

* Total number of tweets
* Number of retweets
* Retweet ratio

#### Content Metrics

* Average tweet length
* Average number of hashtags per tweet
* Average number of URLs per tweet
* Average number of mentions per tweet

#### Engagement Metrics

* Average number of favorites received
* Average number of retweets received

#### Temporal Metrics

* First tweet date
* Last tweet date
* Number of active days
* Average tweet frequency (tweets per day)

#### Social Profile Metrics

* Number of followers
* Number of friends (followings)
* Followers-to-friends ratio
* Verified account indicator
* Default profile image indicator
* Profile language

Static user profile attributes are preserved using the `$first` operator.

---

## Output Collection

The aggregation pipeline outputs the results into a new MongoDB collection:

```
users_aggregated
```

Each document in this collection represents a single Twitter user enriched with aggregated features derived from all their tweets.

---

## Exported Files

The final dataset is exported in two formats:

### JSON Export

```
users_aggregated.json
```

* Preserves all numeric and boolean fields
* Suitable for reuse in MongoDB or further processing

### CSV Export

```
users_aggregated.csv
```

* Flat, tabular format
* Compatible with pandas, scikit-learn, and visualization tools

---

## CSV Column Description

| Column Name               | Description                               |
| ------------------------- | ----------------------------------------- |
| `screen_name`             | Twitter username                          |
| `verified`                | Whether the account is verified           |
| `followers_count`         | Number of followers                       |
| `friends_count`           | Number of followed accounts               |
| `followers_friends_ratio` | followers_count / friends_count           |
| `nb_tweets`               | Total number of tweets in dataset         |
| `nb_retweets`             | Number of retweets                        |
| `retweet_ratio`           | nb_retweets / nb_tweets                   |
| `avg_tweet_length`        | Average tweet length                      |
| `avg_hashtags`            | Average number of hashtags per tweet      |
| `avg_urls`                | Average number of URLs per tweet          |
| `avg_mentions`            | Average number of user mentions per tweet |
| `avg_favorites`           | Average number of favorites received      |
| `avg_retweet_count`       | Average number of retweets received       |
| `tweet_frequency`         | Average tweets per day                    |
| `default_profile_image`   | Whether default profile image is used     |
| `profile_lang`            | Declared profile language                 |

---

## Intended Usage

The aggregated dataset is designed to be used as:

* Input for unsupervised learning (clustering, anomaly detection)
* Input for supervised learning (bot / atypical profile classification)
* Basis for exploratory data analysis and visualization

All features are numerical or boolean, enabling straightforward normalization and dimensionality reduction.

---

## Reproducibility

The aggregation pipeline is deterministic and can be re-executed at any time on the raw tweet collection to regenerate the dataset.

Dependencies:

* MongoDB
* mongosh
* mongoexport (for CSV and JSON export)

---

## Author and Role

**Housseni YABRE – Data Engineer / Data Cleaner**

Responsible for data extraction, cleaning, structuring, and aggregation.
Delivered the final user-level dataset serving as input for Machine Learning models.

https://www.dropbox.com/t/hobDzZlRdvYX5yju (CSV & JSON are here)

