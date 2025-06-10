-- Create Banks table
CREATE TABLE Banks (
    bank_id VARCHAR(50) PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL
);

-- Create Reviews table
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id VARCHAR(50),
    review_text VARCHAR(1000),
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    date_posted DATE,
    source VARCHAR(50),
    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC(5,4),
    themes VARCHAR(100),
    FOREIGN KEY (bank_id) REFERENCES Banks(bank_id)
);

-- Insert sample bank data
INSERT INTO Banks (bank_id, bank_name) VALUES ('CBE', 'Commercial Bank of Ethiopia');
INSERT INTO Banks (bank_id, bank_name) VALUES ('BOA', 'Bank of Abyssinia');
INSERT INTO Banks (bank_id, bank_name) VALUES ('Dashen', 'Dashen Bank');