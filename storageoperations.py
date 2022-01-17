from azure.storage.blob import *
from datetime import *

connect_str='DefaultEndpointsProtocol=https;AccountName=medrecordfiles;AccountKey=EbVY4ZM3XNywbJbeR6yDFCjJILD5Nqla3EPI7CU+B1QAXjk1wwstYTVPsxA1wyPuSBTGiO8d+uDBhg4Wa26yxw==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

cryptocontainer=blob_service_client.get_container_client('cryptofiles')
usercontainer=blob_service_client.get_container_client('userfiles')

def uploadUserFileToBlob(data, fln):
  blob_client = blob_service_client.get_blob_client(container='userfiles', blob=fln)
  blob_client.upload_blob(data)
  
def getDownloadLink(fln):
  block_blob_service = BlockBlobService(account_name='medrecordfiles', account_key='EbVY4ZM3XNywbJbeR6yDFCjJILD5Nqla3EPI7CU+B1QAXjk1wwstYTVPsxA1wyPuSBTGiO8d+uDBhg4Wa26yxw==')
  sas_url = block_blob_service.generate_blob_shared_access_signature('userfiles',fln,permission=BlobPermissions.READ,expiry= datetime.utcnow() + timedelta(hours=1))
  print('https://medrecordfiles.blob.core.windows.net/userfiles/'+fln+'?'+sas_url)
  return 'https://medrecordfiles.blob.core.windows.net/userfiles/'+fln+'?'+sas_url

def uploadCryptoFile(data,fln):
  blob_client = blob_service_client.get_blob_client(container='cryptofiles', blob=fln)
  blob_client.upload_blob(data, overwrite=True)
  
def downloadCryptoFile(fln):
  blob_client = blob_service_client.get_blob_client(container='cryptofiles', blob=fln)
  return blob_client.download_blob().readall()
