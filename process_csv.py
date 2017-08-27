import csv
import pandas
import sqlite3

csv_file = "../datasets/instagram-posts.csv"
pictures = "../datasets/instagram-pictures/"

df = pandas.read_csv(csv_file)
conn = sqlite3.connect('../datasets/instagram.sqlite3')
df.to_sql("instagram", conn, if_exists='replace', index=False)