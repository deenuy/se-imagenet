# Find count in table
SELECT count(*) FROM `SEWordSim-r1`.Word_Similarity;
SELECT * FROM `SEWordSim-r1`.Word_Similarity;

# Find count of distinct term1
SELECT count(distinct(term1)) from `SEWordSim-r1`.Word_Similarity;

# Find synset with term1
SELECT term1, count(term2) 
FROM `SEWordSim-r1`.Word_Similarity 
GROUP BY term1 
ORDER BY term1 DESC;

# Find synset with term1 having length > 5
SELECT term1, count(term2) 
FROM `SEWordSim-r1`.Word_Similarity 
GROUP BY term1 
HAVING length(term1) >= 5
ORDER BY term1 DESC;

# Find synset by term1 keyword
SELECT term1, term2 FROM `SEWordSim-r1`.Word_Similarity WHERE term1 like 'wheel';