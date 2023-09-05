# Import necessary libraries
import boto3
from flask import Flask, request, render_template, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
import os
from uploadFileToS3 import s3_upload_files,search_files

# Initialize Flask app
app = Flask(__name__)

# Configure AWS S3 client
def s3_client():
    """
        Function: get s3 client
         Purpose: get s3 client
        :returns: s3
    """
    session = boto3.session.Session(
          aws_access_key_id=os.getenv("ID"),
    aws_secret_access_key=os.getenv("KEY"),
    aws_session_token=os.getenv("TOKEN"),
    region_name="ap-south-1"
    )
    client = session.client('s3')
    """ :type : pyboto3.s3 """
    return client

# Define the S3 bucket name
bucket_name = 'commvaulttask'

# Define the folder where files will be stored in S3
s3_folder = 'uploads/'

# Route for uploading files
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        email = request.form['email']
        filename = request.form['filename']
        file = request.files['file']
        if email and filename and file:
            my_s3_client = s3_client()
            # Ensure a unique filename in S3
            filename = f"{email}_{secure_filename(filename)}"
            status = s3_upload_files(my_s3_client,file,filename,bucket_name,"")
            json_response = jsonify({'status_code': status})
            json_response.headers.add('Access-Control-Allow-Origin', '*')
            return json_response

    json_response = jsonify({'status_code': 500})
    json_response.headers.add('Access-Control-Allow-Origin', '*')
    return json_response

# Route for searching and displaying files
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        email = request.form['email']
        query = request.form['query']

        if email and query:
            # Perform S3 file search here
            # List objects in the S3 bucket matching the criteria
            my_s3_client = s3_client()
            results = search_files(my_s3_client, email+"_"+query,bucket_name)
            print(results)
            return render_template('search.html', results=results)

    return render_template('search.html',results=[])

# Main route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
