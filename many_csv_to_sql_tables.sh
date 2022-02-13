# !/bin/bash

for f in /var/lib/mysql-files/wiki_text_csvs/*.csv
do
    sudo mysql --local-infile wiki -e "CREATE TABLE IF NOT EXISTS "${f:36:-4}" (
        title_id INT PRIMARY KEY, 
        title VARCHAR(500) NOT NULL,
        text MEDIUMTEXT NOT NULL); 
    LOAD DATA INFILE '"$f"' 
        INTO TABLE "${f:36:-4}"
        FIELDS TERMINATED BY '|' 
        LINES TERMINATED BY '\n' 
        IGNORE 1 LINES"  
echo "Done: '"${f:36:-4}"' at $(date)"
done
