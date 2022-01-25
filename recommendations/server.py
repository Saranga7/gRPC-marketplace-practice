from concurrent import futures
import random
import time
import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse
)

import recommendations_pb2_grpc

_ONE_DAY_IN_SECONDS=86400

books_by_category={
    BookCategory.MYSTERY:[
        BookRecommendation(id=1,title="And Then There Were None"),
        BookRecommendation(id=2,title="The Adventures of Sherlock Holmes"),
        BookRecommendation(id=3,title="Sharp Objects"),
    ],
    BookCategory.SCIENCE_FICTION:[
        BookRecommendation(id=4,title="Dark Matter"),
        BookRecommendation(id=5,title="The Time Machine"),
        BookRecommendation(id=6,title="Time Raiders")
    ],
    BookCategory.SELF_HELP:[
        BookRecommendation(id=7,title="Rich Dad Poor Dad"),
        BookRecommendation(id=8,title="The 7 Habits of Highly Effective People"),
        BookRecommendation(id=9,title="The Secret"),
    ]

}

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):

    def Recommend(self,request,context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
        
        books_for_category=books_by_category[request.category]
        num_results=min(request.max_results,len(books_for_category))
        books_to_recommend=random.sample(books_for_category,num_results)

        return RecommendationResponse(recommendations=books_to_recommend)


def serve():
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(),server)
    server.add_insecure_port("[::]:50051")
    print("Server started at port 50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__=='__main__':
    serve()