import csv

input_file_path = "outputs/temp_outputs/uploaders_output.csv"
# input_file_path = "outputs/temp_outputs/test_input_delete.csv"
output_file_path = "outputs/processed.csv"
# output_file_path = "outputs/processed_test_delete.csv"


def check_uploader_diversity():
    # Checks the names of all uploaders within every submission.
    # If a submission contains < 5 unique uploaders, each cell of
    # the submission in processed.csv is flagged with the "[DUPLICATE CREATOR]"
    # tag to signify that the entire submission is invalidated.
    with open(input_file_path, "r", newline="", encoding="utf-8") as input_file, open(
        output_file_path, "r+", newline="", encoding="utf-8"
    ) as output_file:
        uploader_reader = csv.reader(input_file)
        uploader_rows = list(uploader_reader)
        processed_reader = csv.reader(output_file)
        processed_rows = list(processed_reader)
        processed_writer = csv.writer(output_file)

        for line_number in range(1, len(uploader_rows)):
            # For each line in uploaders_output.csv
            uploaders = [
                uploader.strip() for uploader in uploader_rows[line_number][1:]
            ]
            uploaders = [item for item in uploaders if item]
            # Remove empty elements from list

            if len(set(uploaders)) < 5:
                # If this submission has < 5 unique uploaders
                for cell_number in range(2, len(processed_rows[line_number])):
                    # For each corresponding cell in processed.csv
                    cell = processed_rows[line_number][cell_number]
                    if cell != "" and not contains_note(cell):
                        # If cell is a video title
                        processed_rows[line_number][
                            cell_number + 1
                        ] += "[5 CHANNEL RULE]"
                        # Append note to notes column

        output_file.seek(0)
        processed_writer.writerows(processed_rows)


with open("modules/csv/possible_notes.csv", "r") as csvfile:
    notes = []
    reader = csv.reader(csvfile)
    for row in reader:
        notes.extend(row)
    # Initialize list of notes for contains_note() check.


def contains_note(cell):
    # Returns true if cell contains at least one note, e.g. [DUPLICATE CREATOR]
    return any(domain in cell for domain in notes)
