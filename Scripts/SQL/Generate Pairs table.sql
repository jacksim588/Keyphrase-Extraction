-- Drop the table if it exists
DROP TABLE IF EXISTS xml_pairs;

-- Create the xml_pairs table with the new 'date' column
CREATE TABLE xml_pairs (
  xml_pairs_id SERIAL PRIMARY KEY,
  xml_new VARCHAR(255) NOT NULL,
  xml_old VARCHAR(255) NOT NULL,
  date DATE NOT NULL
);

-- Common Table Expression (CTE) to compute xml_new, xml_old, and date
WITH CTE AS (
    SELECT
      curr.xml_id AS xml_new,
      LEAD(curr.xml_id) OVER (PARTITION BY curr.gtin ORDER BY curr.xml_id DESC) AS xml_old,
      curr.date::date AS date  -- Cast 'date' to the 'date' type
    FROM brandbankxml curr
    WHERE curr."isDelete" = 0
)

-- Insert into xml_pairs table
INSERT INTO xml_pairs (xml_new, xml_old, date)
SELECT xml_new, xml_old, date
FROM CTE
WHERE xml_old IS NOT NULL
ORDER BY xml_new DESC;

-- Add the 'change_in_text' column to the 'xml_pairs' table if it doesn't exist
ALTER TABLE xml_pairs
ADD COLUMN change_in_text BOOLEAN;

-- Update the 'change_in_text' column
UPDATE xml_pairs
SET change_in_text = (CASE
  WHEN bb_old.text <> bb_new.text THEN TRUE
  ELSE FALSE
END)
FROM brandbankxml AS bb_old, brandbankxml AS bb_new
WHERE xml_pairs.xml_old = bb_old.xml_id AND xml_pairs.xml_new = bb_new.xml_id;

-- Add the 'change_in_text' column to the 'xml_pairs' table if it doesn't exist
ALTER TABLE xml_pairs
ADD COLUMN change_in_ingredients BOOLEAN;

-- Update the 'change_in_text' column
UPDATE xml_pairs
SET change_in_ingredients = (CASE
  WHEN bb_old.ingredients <> bb_new.ingredients THEN TRUE
  ELSE FALSE
END)
FROM brandbankxml AS bb_old, brandbankxml AS bb_new
WHERE xml_pairs.xml_old = bb_old.xml_id AND xml_pairs.xml_new = bb_new.xml_id;


-- create the changes in phrases table

-- Create the 'Change_in_Phrases' table if it doesn't exist
CREATE TABLE IF NOT EXISTS Change_in_Phrases (
  NP_id SERIAL PRIMARY KEY,
  xml_pairs_id INT,
  phrase VARCHAR(255),
  added_removed VARCHAR(10)
);


INSERT INTO change_in_phrases (xml_pairs_id, phrase, added_removed)
SELECT 
    xp.xml_pairs_id,
    p."Phrase",
    'added' AS added_removed
FROM 
    xml_pairs xp
JOIN 
    brandbankxml bbx_new ON xp.xml_new = bbx_new.xml_id
JOIN 
    brandbankxml bbx_old ON xp.xml_old = bbx_old.xml_id
JOIN 
    phrases p ON bbx_new.text LIKE CONCAT('%', p."Phrase", '%')
WHERE 
    bbx_old.text NOT LIKE CONCAT('%', p."Phrase", '%');


INSERT INTO change_in_phrases (xml_pairs_id, phrase, added_removed)
SELECT 
    xp.xml_pairs_id,
    p."Phrase",
    'removed' AS added_removed
FROM 
    xml_pairs xp
JOIN 
    brandbankxml bbx_old ON xp.xml_old = bbx_old.xml_id
JOIN 
    brandbankxml bbx_new ON xp.xml_new = bbx_new.xml_id
JOIN 
    phrases p ON bbx_old.text LIKE CONCAT('%', p."Phrase", '%')
WHERE 
    bbx_new.text NOT LIKE CONCAT('%', p."Phrase", '%');
