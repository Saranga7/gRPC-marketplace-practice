import os
from flask import Flask, render_template
import grpc

import recommendations_pb2, recommendations_pb2_grpc


app=Flask(__name__)

recommendations_host=os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel=grpc.insecure_channel(
    f"{recommendations_host}:50051"
)

recommendations_client=recommendations_pb2_grpc.RecommendationsStub(recommendations_channel)

@app.route('/')
def index():
    recommendations_request=recommendations_pb2.RecommendationRequest(
        user_id=7, category=recommendations_pb2.BookCategory.MYSTERY,max_results=2
    )
    recommendations_response=recommendations_client.Recommend(recommendations_request)

    return render_template("index.html", recommendations=recommendations_response.recommendations)


if __name__ == "__main__":
    app.run(debug=True)