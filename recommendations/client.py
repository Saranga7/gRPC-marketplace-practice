import grpc
from recommendations_pb2_grpc import RecommendationsStub
from recommendations_pb2 import RecommendationRequest, BookCategory

channel=grpc.insecure_channel('localhost:50051')
client=RecommendationsStub(channel)
request=RecommendationRequest(
    user_id=1,category=BookCategory.MYSTERY,max_results=2
)
response=client.Recommend(request)

print(response)



