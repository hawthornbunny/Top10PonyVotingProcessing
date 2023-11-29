import csv
from modules import data_pulling
import re

input_file_duration = "modules/csv/data_link.csv"
input_file_additional_info = "outputs/processed_dates.csv"
output_file = "outputs/processed.csv"
date_time_pattern = r"\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{1,2}:\d{1,2}"


def is_date_time_match(cell):
    return bool(re.search(date_time_pattern, cell))


def check_duration(input):
    with open(input, "r", encoding="utf-8") as csv_data_link, open(
        input_file_additional_info, "r", encoding="utf-8"
    ) as csv_blacklist, open(output_file, "w", newline="", encoding="utf-8") as csv_out:
        reader_data_link = csv.reader(csv_data_link)
        reader_durations = csv.reader(csv_blacklist)
        writer = csv.writer(csv_out)

        for row_data_link, row_duration in zip(reader_data_link, reader_durations):
            new_row = row_data_link

            for index, cell in enumerate(row_data_link):
                if "youtube.com" in cell or "youtu.be" in cell:
                    video_id = data_pulling.extract_video_id(cell)

                    if video_id:
                        (
                            title,
                            uploader,
                            duration,
                            upload_date_str,
                        ) = data_pulling.yt_api(video_id)
                        seconds = int(duration)

                        if seconds <= 30:
                            row_duration[index] += " [Video too short]"
                        elif seconds <= 45:
                            row_duration[index] += " [Video maybe too short]"

                elif (
                    "pony.tube" in cell
                    or "vimeo.com" in cell
                    or "dailymotion.com" in cell
                ):
                    video_link = cell

                    if video_link:
                        print(video_link)
                        (
                            title,
                            uploader,
                            seconds,
                            upload_date_str,
                        ) = data_pulling.check_with_yt_dlp(video_link=video_link)
                        seconds = int(duration)

                        if seconds <= 30:
                            row_duration[index] += " [Video too short]"
                        elif seconds <= 45:
                            row_duration[index] += " [Video maybe too short]"
                elif cell.strip():
                    if index < len(row_duration):
                        row_duration[index] = cell + "[Unsupported Host]"
                    else:
                        row_duration.append(cell + "[Unsupported Host]")

            writer.writerow(row_duration)
