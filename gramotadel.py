import datetime
import csv
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont

def generate_certificate(row):
    name = row["name"]
    certificate_output_path = f"ALL_Certificates/{name}.png"

    image = Image.open("certificate_example.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("calibri.ttf", size=125)

    draw.text((209, 1851), name, font=font, fill="black")
    draw.text((700, 2520), f"{datetime.date.today()}", font=font, fill="black")
    font = ImageFont.truetype("calibri.ttf", size=110)
    draw.text((600, 2670), "ФИО Преподавателя", font=font, fill="black")

    im2 = Image.open('watermark.png')
    mask_im = Image.new("L", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 2, 680, 685), fill=255)
    image.paste(im2, (1870, 2820), mask_im)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("calibri.ttf", size=125)
    draw.text((600, 2820), "ФИО ОСНОВАТЕЛЯ КОМПАНИИ", font=font, fill="black")

    image.save(certificate_output_path, quality=95)
    im2.close()
    return 1

def truetype(input_image_path, output_path, csv_file_path):
    with open(csv_file_path, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        with ProcessPoolExecutor() as executor:
            results = executor.map(generate_certificate, reader)
            counter_clients = sum(results)
    return counter_clients

if __name__ == "__main__":
    start_time = datetime.datetime.now().replace(microsecond=0)
    print("Начал выполнение в", start_time)
    counter_clients = truetype("certificate_example.png", "gramota.png", "2k.csv")
    print("---" * 20)
    print("Затраченное время на выполнение:", datetime.datetime.now().replace(microsecond=0) - start_time)
    print("Обработано учеников:", counter_clients)
