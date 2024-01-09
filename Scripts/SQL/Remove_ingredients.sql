
DELETE FROM public."Ingredients"
WHERE LENGTH("Ingredient") < 3
OR "Ingredient" !~ '[A-Za-z]'
OR "Ingredient" LIKE '%contains%'
OR "Ingredient" LIKE 'and %'
OR (
    LENGTH(REGEXP_REPLACE("Ingredient", '[^a-zA-Z]', '', 'g')) > 0 
    AND (
        REGEXP_REPLACE("Ingredient", '[^mgMG]', '', 'g') = REGEXP_REPLACE("Ingredient", '[^a-zA-Z]', '', 'g')
        OR REGEXP_REPLACE("Ingredient", '[^mlML]', '', 'g') = REGEXP_REPLACE("Ingredient", '[^a-zA-Z]', '', 'g')
    )
);