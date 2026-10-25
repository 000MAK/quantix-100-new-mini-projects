"""Reproducible K-Means demo using generated data, without external downloads."""
from __future__ import annotations

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler


def main() -> None:
    features, known_labels = make_blobs(
        n_samples=600,
        centers=4,
        n_features=2,
        cluster_std=1.15,
        random_state=42,
    )
    features = StandardScaler().fit_transform(features)

    model = KMeans(n_clusters=4, n_init=20, random_state=42)
    cluster_ids = model.fit_predict(features)

    print("K-Means clustering demo on synthetic data")
    print(f"Samples:              {len(features)}")
    print(f"Clusters requested:   {model.n_clusters}")
    print(f"Silhouette score:     {silhouette_score(features, cluster_ids):.3f}")
    print(
        "Adjusted Rand index: "
        f"{adjusted_rand_score(known_labels, cluster_ids):.3f}"
    )
    print("Cluster sizes:")
    for cluster_id, size in sorted(
        ((int(label), int((cluster_ids == label).sum())) for label in set(cluster_ids))
    ):
        print(f"  Cluster {cluster_id}: {size}")


if __name__ == "__main__":
    main()
