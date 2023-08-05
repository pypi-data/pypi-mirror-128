import logging
import random

import faiss

from autofaiss.external.quantize import Quantizer
from tests.unit.test_embeddings_iterators import build_test_collection_numpy, build_test_collection_parquet

logging.basicConfig(level=logging.DEBUG)


def test_quantize(tmpdir):
    min_size = random.randint(1, 100)
    max_size = random.randint(min_size, 10240)
    dim = random.randint(1, 100)
    nb_files = random.randint(1, 5)

    tmp_dir, sizes, dim, expected_array = build_test_collection_numpy(
        tmpdir, min_size=min_size, max_size=max_size, dim=dim, nb_files=nb_files
    )

    output_numpy_index = tmpdir.mkdir("autofaiss_quantize_numpy")

    quantizer = Quantizer()
    output_numpy_index_file = quantizer.quantize(
        embeddings_path=tmp_dir,
        file_format="npy",
        output_path=str(output_numpy_index),
        max_index_query_time_ms=10.0,
        max_index_memory_usage="1G",
        current_memory_available="2G",
    )
    output_numpy_index_faiss = faiss.read_index(output_numpy_index_file)
    assert output_numpy_index_faiss.ntotal == len(expected_array)

    tmp_dir, sizes, dim, expected_df = build_test_collection_parquet(
        tmpdir, min_size=min_size, max_size=max_size, dim=dim, nb_files=nb_files
    )

    output_parquet_index = tmpdir.mkdir("autofaiss_quantize_parquet")

    quantizer = Quantizer()
    output_parquet_index_file = quantizer.quantize(
        embeddings_path=tmp_dir,
        file_format="parquet",
        embedding_column_name="embedding",
        output_path=str(output_parquet_index),
        max_index_query_time_ms=10.0,
        max_index_memory_usage="1G",
        current_memory_available="2G",
    )
    output_parquet_index_faiss = faiss.read_index(output_parquet_index_file)
    assert output_parquet_index_faiss.ntotal == len(expected_df)
