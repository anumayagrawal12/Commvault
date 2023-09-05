import boto3

def s3_upload_files(s3_client,file ,file_name, s3_bucket_name, content_type):
    client = s3_client
    upload_file_response = client.put_object(Body = file.read(),
                                             Bucket=s3_bucket_name,
                                             Key=file_name,
                                             ContentType=file.content_type)
    return (upload_file_response["ResponseMetadata"]["HTTPStatusCode"])


def search_files(s3_client,file_name,s3_bucket_name):
    try:
        response = s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Prefix=file_name
    )
    
    # Iterate through the list of objects
        search_results = []
        if 'Contents' in response:
            for obj in response['Contents']:
                file_name = obj['Key']

                # Generate a pre-signed URL for each file
                download_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': s3_bucket_name,
                        'Key': file_name
                    },
                    ExpiresIn=3600  # URL will expire in 1 hour (adjust as needed)
                )
                search_results.append({'file_name': file_name, 'download_url': download_url})
        return search_results
    
    except Exception as e:
        return []