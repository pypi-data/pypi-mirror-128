import boto3
from botocore.exceptions import ClientError
import os

client = boto3.client('s3')

def run():
    try:
        bucket_name=input("Please enter name of your bucket: ")
        key = input("Please enter key of your file.")
        filename=input("Please sign  name to file that you want to download")

        cwd = os.getcwd()
        folder_name = input('Please input the name for directory that we will be using for placment of downloaded files: ')
        os.mkdir(folder_name)
        cwd = cwd + '/' + folder_name + '/'
        os.chdir(cwd)

        client.download_file(Bucket=bucket_name , Key=key , Filename= filename )
        print(f"{key} is downloaded")
        print(f"{filename} is placed into your dir.")
    except ClientError as e:
        print(e)