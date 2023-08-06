#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
import csv
from typing import Generator, Dict, Any, List

from loguru import logger
from elasticsearch import Elasticsearch, helpers


class ElasticSearchCollections:

    def __init__(self, hosts: Any = ..., **kwargs: Any) -> None:
        self.scroll_id = None
        self.client = Elasticsearch(hosts, **kwargs)

    def scroll_source_generator(self, search_info: Dict[str, any]) -> Generator[List[Dict[Any, Any]], None, None]:
        """Generator fn to get the scroll _source"""
        total_size = 0
        data = self.client.search(**search_info)
        scroll_size = len(data['hits']['hits'])
        self.scroll_id = data['_scroll_id']
        logger.info(f"Scrolling {str(self.client)} by index: {search_info['index']}\n scroll_id: {self.scroll_id}")
        if scroll_size == 0:
            self.client.clear_scroll(scroll_id=self.scroll_id)
        while scroll_size > 0:
            request_list = data['hits']['hits']
            total_size += scroll_size
            logger.info(f"scroll size: {total_size}")
            data = self.client.scroll(scroll_id=self.scroll_id, scroll=search_info["scroll"])
            scroll_size = len(data['hits']['hits'])
            yield request_list

    def bulk(self, actions: List[Dict[Any, Any]]):
        helpers.bulk(client=self.client, actions=actions)

    def delete_scroll_id(self):
        if self.scroll_id:
            self.client.clear_scroll(scroll_id=self.scroll_id)

    def upload_source_from_csv(self, csvfile):
        """
        update $.'_source' from csvfile.
        fn need to be re-written once the date parse logic changed.
        """
        with open(csvfile, "r") as f:
            csv_reader = csv.DictReader(f)
            actions = []
            for row in csv_reader:
                actions.append(row)
        if actions:
            self.bulk(actions)

    def download_source_to_csv(self, csvfile: str, field_names: List[str], search_info: Dict[str, any]):
        """
        Parse the search result ($.'_source': dict) to csv.
        Example: download_source_to_csv("test1.csv", ['_source']['xxxData'], es_search_info)
        fn need to be re-written once the date parse logic changed.
        """
        with open(csvfile, "w") as f:
            csv_writer = csv.DictWriter(f, fieldnames=field_names)
            csv_writer.writeheader()
            _res_list = self.scroll_source_generator(search_info)

            for _data_list in _res_list:
                for i in _data_list:
                    csv_writer.writerow(i['_source'])

            self.delete_scroll_id()
