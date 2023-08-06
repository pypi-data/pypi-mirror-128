import os

os.environ['PAI_DATA_DIR'] = 'eyJ0eXBlIjogImFwbS1maXJlaG9zZSIsICJkYXRhIjogeyJ1c2VybmFtZSI6ICJ6aHVhbmcueXVhbkBhZHZhbnRlY2guY29tLmNuIiwgInBhc3N3b3JkIjogIk1USXpORFUyV21oNUx3PT0iLCAiYXBtVXJsIjogImh0dHBzOi8vcG9ydGFsLWFwbS11c2VyMzAtZWtzMDExLnNhLndpc2UtcGFhcy5jb20vYXBpLWFwbSIsICJkYlR5cGUiOiAiZXh0ZXJuYWwiLCAiY3JlZGVudGlhbCI6IHsidXJpIjogIm1vbmdvZGI6Ly9jMWE5NDhmNi0wZjBkLTQ1MTktOWU5NS0yZDVjNWVjMzBjMWY6OXR1SHpFdHl5SmVpc09Oa2FVTlBicWNBQDUyLjE4Ny4xMjUuMTYyOjI3MDE3LzgyMGFiOTliLTQzMGYtNGJlMS1hZThhLWUwYjk3MzAzMmM3NSIsICJ1c2VybmFtZSI6ICJjMWE5NDhmNi0wZjBkLTQ1MTktOWU5NS0yZDVjNWVjMzBjMWYiLCAicGFzc3dvcmQiOiAiOXR1SHpFdHl5SmVpc09Oa2FVTlBicWNBIiwgImhvc3QiOiAiNTIuMTg3LjEyNS4xNjIiLCAicG9ydCI6ICIyNzAxNyIsICJkYXRhYmFzZSI6ICI4MjBhYjk5Yi00MzBmLTRiZTEtYWU4YS1lMGI5NzMwMzJjNzUifSwgImFwbV9jb25maWciOiBbeyJuYW1lIjogImFwbS0xIiwgInByb2ZpbGUiOiB7Im5hbWUiOiAiIiwgImlkIjogIiJ9LCAibWFjaGluZXMiOiBbeyJuYW1lIjogImFpZnNfdGVzdCIsICJpZCI6IDE5M30sIHsibmFtZSI6ICJcdTUzODJcdTYyM2ZcdTZhMjFcdTY3N2YiLCAiaWQiOiAxNDF9XSwgInBhcmFtZXRlcnMiOiBbIkRITm9kZVN0YXR1cyJdLCAibm9kZV9wYXRoIjogW3siaWQiOiAyOSwgImxheWVyTmFtZSI6ICIiLCAibmFtZSI6ICJhaWZzX3Rlc3QifV19XSwgInRpbWVMYXN0IjogeyJsYXN0RGF5cyI6IDM2MCwgImxhc3RIb3VycyI6IDExLCAibGFzdE1pbnMiOiAxfX19'


# from afs2datasource import DBManager, constant

# manager = DBManager()
# manager.connect()
# data = manager.execute_query()
# print(data)

from afs2datasource import DBManager, constant
# manager = DBManager(db_type=constant.DB_TYPE['DATAHUB'],
#   username='ssopassroot@email.com',  # sso username
#   password='ToorSs@p0SS',  # sso password
#   datahub_url='https://portal-datahub-ensaas.aifs.wise-paas.com',
#   datahub_config=[{
#     "name": "test0510", # dataset name
#     "project_id": "afs-demo",#datahub的mongodb数据库中不会存这个参数
#     "node_id": "90b016ce-d171-423b-b16f-2d2eeb82f49e",
#     "device_id": "Device1",
#     "tags": [
#       "ATag0"
#     ]
#   }],
#   uri='influxdb://d44b1476-f532-4ce2-8244-fec7bffd858e:0ERVNiAbxCBWJZldFT6JMHdr4@172.17.21.111:8086/1f65d529-898c-46d8-8d71-30671a3f820b',
#   # timeRange or timeLast
#   #timeRange=[{'start': start_ts, 'end': end_ts}],
#   timeLast={'lastDays': 360, 'lastHours': 77, 'lastMins': 77}
# )
manager = DBManager()
manager.connect()
df = manager.execute_query()
print(df)