from concurrent import futures

import grpc
import generated.service_pb2 as s
import generated.service_pb2_grpc as sg
import generated.system_pb2 as sys_service
import generated.system_pb2_grpc as sys_service_g

import environment.sun as sun

store = {}


class SystemServicer(sys_service_g.SystemServiceServicer):

  def GetVersion(self, request, context):
    print(request)

    result = sys_service.VersionResponse(
      version='0.0.0'
    )

    return result


class SiteModelServicer(sg.SiteModelServiceServicer):

  def BuildingModelById(self, request, context):
    print(request)

    model = str.encode('this is a model')

    result = s.BuildingModelBlenderResponse(
      model=model
    )

    return result


class SunServicer(sg.SunServiceServicer):

  def Position(self, request, context):
    location = [request.location.lat, request.location.lon]
    date = request.date_time

    az = sun.azimuth(location, date)
    alt = sun.altitude(location, date)
    rad = sun.radiation(location, date)

    result = s.SunPositionResponse(
      azimuth=az,
      altitude=alt,
      radiation=rad,
      color=s.ColorRGBA(red=1.0, green=1.0, blue=1.0, alpha=1.0)
    )

    return result


server = grpc.server(futures.ThreadPoolExecutor(1))
sg.add_SunServiceServicer_to_server(SunServicer(), server)
sg.add_SiteModelServiceServicer_to_server(SiteModelServicer(), server)
sys_service_g.add_SystemServiceServicer_to_server(SystemServicer(), server)

server.add_insecure_port("[::]:50051")
server.start()
print('started server')
server.wait_for_termination()
