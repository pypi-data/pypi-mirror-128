#!/usr/bin/env python3

import requests as r
import aiohttp
import asyncio
import json
import elasticsearch
from datetime import datetime
def create_indice(host, name, settings=None):
    try:
        url = host + '/' +  name
        if settings:
            resp = requests.put(url, json=settings)
            return resp.text
        else:
            resp = requests.put(url)
            return resp.json()
    except ConnectionError as e:
        print(e)


async def insert_doc(host, index, doc, id=None):
    if id is None:
        path = host + f"/{index}/_doc/"
        r = requests.post(path, json=doc)
        return r
    else:
        path = host + f"/{index}/_doc/{id}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(path, json=doc) as r:
                    return  await r.text()
        except Exception as e:
            print(e)

async def search(host, query, size=0, index=None):
    if index:
        path = host + f"/{index}/_search?size={size}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(path, json=query) as r:
                    data = await r.json()
                    return data
        except ConnectionError as e:
            print(e)
    else:
        path = host + f"/_search?size={size}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(path, json=query) as r:
                    data = await r.json()
                    return data
        except ConnectionError as e:
            print(e)

def content_search(es_host, index, search_term, site, sort="asc", limit=25):
    es = elasticsearch.Elasticsearch([es_host])

    if site == "discord" or "telegram" or "twitter":
        q = {"sort": [{"date": {"order": sort}}],
             "query": {"simple_query_string": {"query": search_term, "fields": ["m", "sn", "cn", "username", "ut", "group"]}}}
    if site == "reddit":
        q = {
            "query": {
                "simple_query_string": {
                           "query": search_term,
                           "fields": ["body", "post-title"]
                }
            }
        }

    data = es.search(body=q, index=index, size=limit)
    return data

def search_by_user(es_host, index, username, site, limit=25):
    es = elasticsearch.Elasticsearch([CONFIG.es_host])
    if site == "discord" or "telegram":
        q = {"query": {"simple_query_string": {"query": username, "fields": ["ut"]}}}

    if site == "twitter":
        q = {"query": {"simple_query_string": {"query": username, "fields": ["username"]}}}
    if site == "reddit":
        q = {"query": {"simple_query_string": {"query": username, "fields": ["op", "author"]}}}

    data = es.search(body=q, index=index, size=limit)
    return data

def date_search(es_host, index, date_str, sort="desc", limit=25):
    """returns all messages from the specifed date to now"""
    now = datetime.now()
    q = {"sort": [{"date": {"order": sort}}], "query": {"range": {"date": {"gte": date_str, "lte": str(now.isoformat())}}}}
    data = asyncio.run(search(es_host, q, limit, index))
    return data

def get_count(es_host, index=None, **kwargs):
    user_count = False
    website = "none"
    for key, value in kwargs.items():
        if key == "user" and value == True:
            user_count = True
        if key == "website":
            website = value

    link = f"{es_host}/"
    count = 0
    if user_count:
        if website == "twitter":
            q = {
                "aggs": {
                    "type_count": {
                        "cardinality": {
                            "field": "username.keyword"
                        }
                    }
                }
            }

            resp = r.post(link + index + "/_search?size=0", json=q)
            data = resp.json()
            print(data)
            data = data["aggregations"]["type_count"]["value"]
            count = int(data)
            return count
        if website == "discord" or "telegram":
            q = {
                "aggs": {
                    "type_count": {
                        "cardinality": {
                            "field": "ut.keyword"
                        }
                    }
                }
            }
            resp = r.post(link + index + "/_search?size=0", json=q)
            data = resp.json()
            print(data)
            data = data["aggregations"]["type_count"]["value"]
            count = int(data)
            return count
        if website == "reddit":
            q1  =  {
                    "aggs": {
                        "type_count": {
                            "cardinality": {
                                "field": "op.keyword"
                            }
                        }
                    }
                }

            q2  =  {
                    "aggs": {
                        "type_count": {
                            "cardinality": {
                                "field": "op.keyword"
                            }
                        }
                    }
                }

            resp1 = r.get(link + index + "/_search?size=0", json=q1)
            resp2 = r.get(link + index + "/_search?size=0", json=q)

    else:
        resp = r.get(link + index + "/_count")
        data = resp.json()
        count = int(data["count"])
        return count
