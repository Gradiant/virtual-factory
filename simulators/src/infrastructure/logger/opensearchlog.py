import traceback
import simplejson
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from src.domain.ilogger import ILogger


class OpensearchLog(ILogger):

    def __init__(self, params: dict):
        self._config = params
        self._cache = []
        self._max_size_cache = self._config.get("max_size_cache", 1)
        self._index = self._config["index"]
        self._client = None

    def __connect(self):
        self._client = OpenSearch(
            hosts=[{'host': self._config["host"], 'port': self._config["port"]}],
            http_compress=True,
            http_auth=(self._config["user"], self._config["password"]),
            use_ssl=self._config["use_ssl"],
            verify_certs=self._config["verify_certs"],
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    def to_log(self, msg: dict):
        if not self._client:
            self.__connect()

        self._cache.append(msg)
        if len(self._cache) >= self._max_size_cache:

            try:
                bulk_generator = (
                    {
                        '_index': self._index+"-"+e["timestamp"][:10],
                        '_type: ': 'doc',
                        '_source': simplejson.dumps(e, ignore_nan=True),
                    }
                    for e in self._cache
                )

                bulk(self._client, bulk_generator)

            except Exception as e:
                print(f'Unable to emit event: {e}')
                if __debug__:
                    traceback.print_exc()
            self._cache.clear()

