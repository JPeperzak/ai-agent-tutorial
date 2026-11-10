from embedder import Embedder
from sklearn.metrics.pairwise import cosine_similarity

embedder = Embedder()

docker = embedder.embed("Docker")
containers = embedder.embed("containers")

similarity = cosine_similarity(
    [docker],
    [containers]
)

print(similarity)