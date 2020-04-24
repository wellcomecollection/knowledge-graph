import logging
import os

from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm

logger = logging.getLogger(__name__)

def get_elasticsearch_client(config=None):
    if not config:
        config = os.environ

    logger.info('creating elasticsearch client')
    try:
        es_client = Elasticsearch(
            config['ES_HOST'],
            http_auth=(config['ES_USER'], config['ES_PASSWORD']),
        )
    except KeyError as error:
        logger.error('config must contain "ES_HOST", "ES_USER", "ES_PASSWORD"')
        raise error

    return es_client


def get_concepts_data(
    es_client,
    index='concepts_v1',
    query={'query': {'match_all': {}}}
):
    logger.info(f'fetching data from {index} with query: {str(query)}')
    results_generator = helpers.scan(
        client=es_client, index=index, query=query
    )
    loop = tqdm(results_generator, desc=f'fetching concepts from {index}')
    results = [result for result in loop]
    return results
