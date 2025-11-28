# Google Analytics 4 - Facts and Dimensions Mapping

## Overview

This document provides a comprehensive mapping of Google Analytics 4 (GA4) data into a star schema dimensional model. The mapping is designed to support analytics, reporting, and data warehousing use cases.

## Schema Diagram

```
                                    ┌──────────────────┐
                                    │    dim_date      │
                                    ├──────────────────┤
                                    │ date_key (PK)    │
                                    │ full_date        │
                                    │ day_of_week      │
                                    │ month            │
                                    │ quarter          │
                                    │ year             │
                                    └────────┬─────────┘
                                             │
┌──────────────────┐                         │                    ┌──────────────────┐
│    dim_user      │                         │                    │   dim_geography  │
├──────────────────┤                         │                    ├──────────────────┤
│ user_key (PK)    │                         │                    │ geo_key (PK)     │
│ ga_user_id       │                         │                    │ continent        │
│ user_id          │     ┌───────────────────┼───────────────┐    │ country          │
│ user_type        │     │                   │               │    │ region           │
│ first_visit_date │     │                   ▼               │    │ city             │
└────────┬─────────┘     │    ┌──────────────────────────┐   │    └────────┬─────────┘
         │               │    │      fact_sessions       │   │             │
         │               │    ├──────────────────────────┤   │             │
         └───────────────┼───►│ session_key (PK)         │◄──┼─────────────┘
                         │    │ date_key (FK)            │   │
                         │    │ user_key (FK)            │   │
┌──────────────────┐     │    │ geo_key (FK)             │   │    ┌──────────────────┐
│    dim_device    │     │    │ device_key (FK)          │◄──┼────┤ dim_traffic_     │
├──────────────────┤     │    │ traffic_source_key (FK)  │   │    │ source           │
│ device_key (PK)  │     │    │ ─────────────────────────│   │    ├──────────────────┤
│ device_category  │     │    │ engagement_time_seconds  │   │    │ traffic_source_  │
│ browser          │     │    │ event_count              │   │    │ key (PK)         │
│ operating_system │     │    │ pageview_count           │   │    │ source           │
│ screen_resolution│     │    │ session_duration_seconds │   │    │ medium           │
└────────┬─────────┘     │    │ total_revenue            │   │    │ campaign         │
         │               │    └──────────────────────────┘   │    │ channel_group    │
         └───────────────┘                                   │    └──────────────────┘
                                                             │
                              ┌──────────────────────────┐   │
                              │      fact_pageviews      │   │
                              ├──────────────────────────┤   │
                              │ pageview_key (PK)        │◄──┤
                              │ date_key (FK)            │   │
                              │ user_key (FK)            │   │    ┌──────────────────┐
                              │ session_key (FK)         │   │    │    dim_page      │
                              │ page_key (FK)            │◄──┼────┤                  │
                              │ ─────────────────────────│   │    ├──────────────────┤
                              │ time_on_page_seconds     │   │    │ page_key (PK)    │
                              │ entrance_flag            │   │    │ hostname         │
                              │ exit_flag                │   │    │ page_path        │
                              │ scroll_depth             │   │    │ page_title       │
                              └──────────────────────────┘   │    └──────────────────┘
                                                             │
                              ┌──────────────────────────┐   │    ┌──────────────────┐
                              │      fact_events         │   │    │   dim_event      │
                              ├──────────────────────────┤   │    ├──────────────────┤
                              │ event_key (PK)           │◄──┘    │ event_key (PK)   │
                              │ date_key (FK)            │        │ event_name       │
                              │ user_key (FK)            │        │ event_category   │
                              │ session_key (FK)         │        │ is_conversion    │
                              │ event_type_key (FK)      │◄───────┤                  │
                              │ ─────────────────────────│        └──────────────────┘
                              │ event_timestamp          │
                              │ event_value              │
                              │ is_conversion            │
                              └──────────────────────────┘

                              ┌──────────────────────────┐        ┌──────────────────┐
                              │    fact_ecommerce        │        │   dim_product    │
                              ├──────────────────────────┤        ├──────────────────┤
                              │ transaction_key (PK)     │        │ product_key (PK) │
                              │ date_key (FK)            │        │ item_id          │
                              │ user_key (FK)            │        │ item_name        │
                              │ ─────────────────────────│        │ item_brand       │
                              │ transaction_revenue      │        │ item_category    │
                              │ transaction_tax          │        └────────┬─────────┘
                              │ transaction_shipping     │                 │
                              └──────────────────────────┘                 │
                                           │                               │
                                           ▼                               │
                              ┌──────────────────────────┐                 │
                              │  fact_ecommerce_items    │                 │
                              ├──────────────────────────┤                 │
                              │ item_line_key (PK)       │                 │
                              │ transaction_key (FK)     │                 │
                              │ product_key (FK)         │◄────────────────┘
                              │ ─────────────────────────│
                              │ item_price               │
                              │ item_quantity            │
                              │ item_revenue             │
                              └──────────────────────────┘
```

## Dimension Tables

### dim_date
**Purpose:** Calendar date dimension for time-based analysis  
**Grain:** One row per calendar day  
**Source:** Derived from GA4 `date` field

| Column | Description | Source |
|--------|-------------|--------|
| date_key | Surrogate key (YYYYMMDD format) | date |
| full_date | Calendar date | date |
| day_of_week | Day of week (0=Sunday) | dayOfWeek |
| day_of_week_name | Day name | Derived |
| week_of_year | ISO week number | isoWeek |
| month | Month number (1-12) | month |
| month_name | Month name | Derived |
| quarter | Quarter (1-4) | Derived |
| year | Calendar year | year |
| is_weekend | Weekend flag | Derived |

### dim_time
**Purpose:** Time-of-day dimension for hourly analysis  
**Grain:** One row per hour (24 rows)  
**Source:** Derived from GA4 `hour` field

### dim_user
**Purpose:** User/visitor dimension  
**Grain:** One row per unique user  
**Source:** GA4 user data

| Column | Description | Source |
|--------|-------------|--------|
| user_key | Surrogate key | Generated |
| ga_user_id | GA4 client ID (cookie-based) | user_pseudo_id |
| user_id | Custom user ID (if set) | user_id |
| first_visit_date | First visit timestamp | first_visit_date |
| user_type | New vs Returning | newVsReturning |
| first_traffic_source | First acquisition source | firstUserSource |
| first_traffic_medium | First acquisition medium | firstUserMedium |

### dim_geography
**Purpose:** Geographic location dimension  
**Grain:** One row per unique location combination  
**Source:** GA4 geo data

| Column | Description | Source |
|--------|-------------|--------|
| geo_key | Surrogate key | Generated |
| continent | Continent name | continent |
| sub_continent | Sub-continent region | subContinent |
| country | Country name | country |
| country_code | ISO country code | countryId |
| region | State/Province | region |
| city | City name | city |
| metro | Metro/DMA area | metro |

### dim_device
**Purpose:** Device and technology dimension  
**Grain:** One row per unique device configuration  
**Source:** GA4 device data

| Column | Description | Source |
|--------|-------------|--------|
| device_key | Surrogate key | Generated |
| device_category | Desktop/Mobile/Tablet | deviceCategory |
| mobile_device_brand | Device manufacturer | mobileDeviceBranding |
| mobile_device_model | Device model | mobileDeviceModel |
| operating_system | OS name | operatingSystem |
| os_version | OS version | operatingSystemVersion |
| browser | Browser name | browser |
| browser_version | Browser version | browserVersion |
| screen_resolution | Screen size | screenResolution |
| language | Browser language | language |

### dim_traffic_source
**Purpose:** Traffic acquisition source dimension  
**Grain:** One row per unique source/medium/campaign combination  
**Source:** GA4 traffic source data

| Column | Description | Source |
|--------|-------------|--------|
| traffic_source_key | Surrogate key | Generated |
| source | Traffic source | sessionSource |
| medium | Traffic medium | sessionMedium |
| campaign | Campaign name | sessionCampaign |
| content | Ad content | content |
| term | Search term | term |
| default_channel_group | Channel grouping | sessionDefaultChannelGroup |
| google_ads_campaign | Google Ads campaign | googleAdsCampaignName |

### dim_page
**Purpose:** Page/content dimension  
**Grain:** One row per unique page  
**Source:** GA4 page data

| Column | Description | Source |
|--------|-------------|--------|
| page_key | Surrogate key | Generated |
| hostname | Website hostname | hostName |
| page_path | URL path | pagePath |
| page_path_level_1-3 | Path hierarchy levels | Derived |
| page_title | Page title | pageTitle |
| content_group | Content grouping | contentGroup |

### dim_event
**Purpose:** Event type dimension  
**Grain:** One row per unique event type  
**Source:** GA4 event data

| Column | Description | Source |
|--------|-------------|--------|
| event_key | Surrogate key | Generated |
| event_name | Event name | eventName |
| event_category | Legacy category | event_params |
| event_action | Legacy action | event_params |
| event_label | Legacy label | event_params |
| is_conversion | Conversion flag | isConversionEvent |

### dim_product
**Purpose:** Product/item dimension for e-commerce  
**Grain:** One row per unique product  
**Source:** GA4 items array

| Column | Description | Source |
|--------|-------------|--------|
| product_key | Surrogate key | Generated |
| item_id | Product SKU | items.item_id |
| item_name | Product name | items.item_name |
| item_brand | Brand | items.item_brand |
| item_category 1-5 | Category hierarchy | items.item_category* |
| item_variant | Size/color variant | items.item_variant |

---

## Fact Tables

### fact_sessions
**Purpose:** Session-level metrics and foreign keys  
**Grain:** One row per session  
**Source:** GA4 session data

| Metric | Description | Calculation |
|--------|-------------|-------------|
| session_number | Session sequence for user | ga_session_number |
| session_engaged | Engaged session flag | session_engaged |
| engagement_time_seconds | Total engagement time | engagement_time_msec / 1000 |
| event_count | Events in session | COUNT(events) |
| pageview_count | Pageviews in session | COUNT(page_view) |
| session_duration_seconds | Session length | MAX - MIN timestamp |
| bounce_flag | Non-engaged indicator | NOT session_engaged |
| conversion_count | Conversions in session | COUNT(conversions) |
| total_revenue | Revenue in session | SUM(purchase_revenue) |

### fact_pageviews
**Purpose:** Page-level engagement metrics  
**Grain:** One row per pageview  
**Source:** GA4 page_view events

| Metric | Description | Calculation |
|--------|-------------|-------------|
| entrance_flag | First page of session | entrances |
| exit_flag | Last page of session | exits |
| time_on_page_seconds | Time on page | engagementTimeMsec / 1000 |
| scroll_depth | Scroll percentage | percent_scrolled |

### fact_events
**Purpose:** Event-level data for all GA4 events  
**Grain:** One row per event  
**Source:** GA4 events

| Metric | Description | Calculation |
|--------|-------------|-------------|
| event_timestamp | Event time (microseconds) | event_timestamp |
| event_value | Numeric value | event_params.value |
| is_conversion | Conversion indicator | isConversionEvent |

### fact_ecommerce
**Purpose:** Transaction-level e-commerce data  
**Grain:** One row per transaction  
**Source:** GA4 purchase events

| Metric | Description | Calculation |
|--------|-------------|-------------|
| transaction_revenue | Total revenue | ecommerce.purchase_revenue |
| transaction_tax | Tax amount | ecommerce.tax_value |
| transaction_shipping | Shipping cost | ecommerce.shipping_value |
| transaction_refund | Refund amount | ecommerce.refund_value |
| item_quantity | Total items | SUM(items.quantity) |
| unique_items | Distinct products | COUNT(DISTINCT item_id) |

### fact_ecommerce_items
**Purpose:** Line-item level e-commerce data  
**Grain:** One row per product per transaction  
**Source:** GA4 items array in purchase events

| Metric | Description | Calculation |
|--------|-------------|-------------|
| item_price | Unit price | items.price |
| item_quantity | Units purchased | items.quantity |
| item_revenue | Line total | price × quantity |
| item_discount | Discount applied | items.discount |

### fact_daily_aggregate
**Purpose:** Pre-aggregated daily summary metrics  
**Grain:** One row per day  
**Source:** Aggregated from other fact tables

| Metric | Description | Calculation |
|--------|-------------|-------------|
| total_users | Unique users | COUNT(DISTINCT user) |
| new_users | First-time users | COUNT(new users) |
| total_sessions | Session count | COUNT(sessions) |
| engaged_sessions | Engaged session count | COUNT(engaged) |
| engagement_rate | Engaged / Total | engaged_sessions / total_sessions |
| bounce_rate | Non-engaged rate | 1 - engagement_rate |
| total_pageviews | Pageview count | COUNT(pageviews) |
| pages_per_session | Avg pages | pageviews / sessions |
| total_conversions | Conversion count | COUNT(conversions) |
| total_revenue | Daily revenue | SUM(revenue) |

---

## GA4 Data Sources

### BigQuery Export Tables
If using BigQuery export, primary source tables are:
- `analytics_PROPERTY_ID.events_*` - Daily event tables
- `analytics_PROPERTY_ID.events_intraday_*` - Intraday streaming tables

### Data API
If using the GA4 Data API, dimensions and metrics are requested via:
- `runReport` method for standard reports
- `runRealtimeReport` for real-time data

---

## Implementation Notes

### Surrogate Keys
All dimension tables use integer surrogate keys for:
- Query performance
- Slowly changing dimension support
- Natural key independence

### Slowly Changing Dimensions
Consider SCD Type 2 for:
- `dim_user` (user attributes may change)
- `dim_product` (product details may change)

### Data Refresh
- **Daily batch:** Event data typically available T+1
- **Streaming:** Intraday tables for near-real-time
- **Aggregates:** Refresh daily summary tables after event data

### Key Metrics Definitions

| GA4 Term | Star Schema Equivalent |
|----------|----------------------|
| Users | COUNT(DISTINCT user_key) from fact_sessions |
| Sessions | COUNT(*) from fact_sessions |
| Engagement Rate | engaged_sessions / total_sessions |
| Bounce Rate | 1 - engagement_rate |
| Pages/Session | total_pageviews / total_sessions |
| Avg. Session Duration | AVG(session_duration_seconds) |
| Conversions | SUM(conversion_count) or COUNT(fact_events WHERE is_conversion) |

---

## Files

| File | Description |
|------|-------------|
| `google_analytics_facts_dimensions_mapping.csv` | Complete field-level mapping spreadsheet |
| `Google Analytics Star Schema Mapping.md` | This documentation file |

---

*Document Version: 1.0*  
*Last Updated: November 28, 2025*
