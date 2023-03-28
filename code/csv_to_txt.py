import csv

# Open the CSV file for reading
with open('data/luna16/csv/evaluationScript/annotations/annotations.csv', 'r') as csv_file:

    # Open the TXT file for writing
    with open('data/luna16/txt/evaluationScript/annotations.txt', 'w') as txt_file:
        
        # Create a CSV reader object
        csv_reader = csv.reader(csv_file)
        
        # Loop through each row in the CSV file
        for row in csv_reader:
            
            # Join each item in the row with a tab separator
            # and write the resulting string to the TXT file
            txt_file.write('\t'.join(row) + '\n')
