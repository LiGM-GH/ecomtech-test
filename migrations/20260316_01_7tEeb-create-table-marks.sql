-- Create table marks
-- depends:

CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    name TEXT,
    value INTEGER,
    creation_date DATE
);
