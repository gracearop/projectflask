import csv

# File names
input_file = 'intentdata.csv'  # Your input CSV file
output_file = 'formatted_data.txt'  # Output file for the formatted data

# Open the input CSV file
with open(input_file, 'r') as infile:
    reader = csv.reader(infile)
    
    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        for row in reader:
            if len(row) == 2:
                # Extract text and intent from each row
                text, intent = row
                
                # Format the line as __label__intent text
                formatted_line = f"__label__{intent} {text}\n"
                
                # Write the formatted line to the output file
                outfile.write(formatted_line)

print(f"Formatted data saved to {output_file}")