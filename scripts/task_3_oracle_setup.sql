-- Create database (manual step: ensure 'bank_reviews' is created in Oracle XE)
-- CREATE DATABASE bank_reviews;  (Run separately if needed)

-- Create Banks table
CREATE TABLE Banks (
    bank_id NUMBER PRIMARY KEY,
    bank_name VARCHAR2(100),
    app_id VARCHAR2(100)
);

-- Create Reviews table
CREATE TABLE Reviews (
    review_id NUMBER PRIMARY KEY,
    bank_id NUMBER,
    review_text VARCHAR2(4000),
    rating NUMBER,
    date DATE,
    source VARCHAR2(50),
    sentiment_label VARCHAR2(50),
    sentiment_score NUMBER,
    themes VARCHAR2(500),
    FOREIGN KEY (bank_id) REFERENCES Banks(bank_id)
);

-- Commit guidance (manual step): git add task_3_oracle_setup.sql; git commit -m "Add Oracle database schema"; git push