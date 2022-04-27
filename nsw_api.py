from google.transit import gtfs_realtime_pb2
import requests

api_key = "apikey 8IOZ4anw9lGOlydaULFd2m6KUBwSIfB8DftQ"

headers = {"Authorization": api_key}

train_positions = requests.get(
    "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/sydneytrains", headers=headers)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(train_positions.content)


for entity in feed.entity[:5]:
    print(entity.vehicle.position.latitude,
          entity.vehicle.position.longitude,
          entity.vehicle.position.bearing,
          entity.vehicle.position.speed
          )
