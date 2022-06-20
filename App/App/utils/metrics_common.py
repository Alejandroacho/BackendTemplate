from prometheus_client import Counter


# initialise a prometheus counter
class Metrics:
    upload_urls_created: Counter = Counter(
        "upload_urls", "total number of upload urls created"
    )
