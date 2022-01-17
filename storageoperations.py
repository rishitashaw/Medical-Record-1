from azure.storage.blob import *
connect_str='DefaultEndpointsProtocol=https;AccountName=medrecordfiles;AccountKey=EbVY4ZM3XNywbJbeR6yDFCjJILD5Nqla3EPI7CU+B1QAXjk1wwstYTVPsxA1wyPuSBTGiO8d+uDBhg4Wa26yxw==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

cryptocontainer=blob_service_client.get_container_client('cryptofiles')
usercontainer=blob_servoce_client.get_container_client('userfiles')

def uploadUserFileToBlob(data, fln):
  blob_client = blob_service_client.get_blob_client(container='userfiles', blob=fln)
  blob_client.upload_data(data)
  
def getDownloadLink(fln):
  blob_sas_token= generate_blob_sas(
    account_name='medrecordfiles',
    container_name='userfiles',
    blob_name=fln,
    account_key='EbVY4ZM3XNywbJbeR6yDFCjJILD5Nqla3EPI7CU+B1QAXjk1wwstYTVPsxA1wyPuSBTGiO8d+uDBhg4Wa26yxw==',
    permission=ContainerSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
  )
  blob_url_with_sas="https://medrecordfiles.blob.core.windows.net/userfiles/"+fln+"?"+blob_sas_token
  return blob_url_with_sas

def uploadCryptoFile(data,fln):
  blob_client = blob_service_client.get_blob_client(container='cryptofiles', blob=fln)
  blob_client.upload_data(data, overwrite=True)
  
def downloadCryptoFile(fln):
  blob_client = blob_service_client.get_blob_client(container='cryptofiles', blob=fln)
  return blob_client.download_blob().readall()
