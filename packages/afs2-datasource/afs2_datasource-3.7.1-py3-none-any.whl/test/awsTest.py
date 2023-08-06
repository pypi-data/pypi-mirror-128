import os
from afs2datasource import DBManager, constant

# # --------- config --------- #
# db_type = constant.DB_TYPE['AWS']
# access_key = ''
# secret_key = ''

# bucket_name = '' # bucket name
# source = '' # 要上傳的檔案(local)
# folder_name = ''  # 上傳上去的folder name

# # 會上傳 source 到azure blob container裡面
# # 一個在 /
# # 一個在 /folder_name 下面
# # 接著會下載這兩個檔案到local
# # -------------------------- #

# destination = os.path.join(folder_name, source)
# download_file = source
# query = {
#   'bucket': bucket_name,
#   'blobs': {
#     'folders': folder_name
#   }
# }

# manager = DBManager(db_type=db_type,
#   access_key=access_key,
#   secret_key=secret_key,
#   buckets=[query]
# )

# try:
#   # connect to azure blob
#   is_success = manager.connect()
#   print('Connection: {}'.format(is_success))

#   # check if container is exist
#   is_table_exist = manager.is_table_exist(bucket_name)

#   # create container
#   if not is_table_exist:
#     print('Create Bucket {0} successfully: {1}'.format(bucket_name, manager.create_table(bucket_name, region='us-west-1')))
#   print('Bucket {0} exist: {1}'.format(bucket_name, manager.is_table_exist(bucket_name)))

#   # insert file
#   is_file_exist = manager.is_file_exist(bucket_name, destination)
#   if not is_file_exist:
#     manager.insert(table_name=bucket_name, source=source, destination=destination)
#     print('Insert file {0} successfully: {1}'.format(source, manager.is_file_exist(bucket_name, destination)))
#   print('File {0} is exist: {1}'.format(source, is_file_exist))

#   # download files
#   is_file_exist = manager.is_file_exist(bucket_name, destination)
#   if is_file_exist:
#     response = manager.execute_query()
#     print('Execute query successfully: {}'.format(response))

# except Exception as e:
#   print(e)



os.environ['PAI_DATA_DIR'] = 'eyJ0eXBlIjogImF6dXJlLWZpcmVob3NlIiwgImRhdGEiOiB7ImFjY291bnROYW1lIjogIndpc2VwYWFzcHJvZHVjdGlvbiIsICJhY2NvdW50S2V5IjogIjE5MytYUE9MUnFUQm9XWWlnUnNZWnlDa3lkY2lSM1dLSkx1UXNadkdYdldrODVBNC9PV1lGU0FsRTV4R0paUjRHdVFndHQveUdCVXpTZTVJSG8rcGNBPT0iLCAiY29udGFpbmVycyI6IFt7ImJsb2JzIjogeyJmb2xkZXJzIjogWyJhdXRvbWwvT2JqZWN0RGV0ZWN0aW9uL0pQRUdJbWFnZXMvIl19LCAiY29udGFpbmVyIjogInpoeXRlc3QifV0sICJjcmVkZW50aWFsIjogeyJhY2NvdW50TmFtZSI6ICJ3aXNlcGFhc3Byb2R1Y3Rpb24iLCAiYWNjb3VudEtleSI6ICIxOTMrWFBPTFJxVEJvV1lpZ1JzWVp5Q2t5ZGNpUjNXS0pMdVFzWnZHWHZXazg1QTQvT1dZRlNBbEU1eEdKWlI0R3VRZ3R0L3lHQlV6U2U1SUhvK3BjQT09In19LCAibW9uZ29fdXNlcm5hbWUiOiAiYjhjYzFjZWYtYWU1OS00NWE2LWE5YWMtZDk3YjRhN2Y3NTE3IiwgIm1vbmdvX3Bhc3N3b3JkIjogIkJkRExSM1dmVHBNMGQxRG1ENHVxQVZ6TCIsICJtb25nb191cmkiOiAiMTcyLjE3LjIxLjExMToyNzAxNyIsICJtb25nb19kYXRhYmFzZSI6ICJhaWZzIn0='
manager = DBManager()

try:
  # connect to azure blob
  is_success = manager.connect()
  print('Connection: {}'.format(is_success))

  # download files
  response = manager.execute_query()
  print('Execute query successfully: {}'.format(response))

except Exception as e:
  print(e)