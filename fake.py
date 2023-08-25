import sys
import csv
from faker import Faker

fake = Faker()
number_of_records = 2000000

with open('randomperson.csv', mode='w') as file:
  file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=1)

  file_writer.writerow(['first_name', 'last_name', 'age', 'price'])

  for _ in range(number_of_records):
    file_writer.writerow([fake.first_name(), fake.last_name(), fake.numerify("@#"), fake.pricetag()])