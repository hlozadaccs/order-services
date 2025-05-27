from prometheus_client import Counter, Histogram

orders_created_counter = Counter(
    "orders_created_total",
    "Total number of orders created successfully",
    ["order_type"],
)

order_creation_duration_seconds = Histogram(
    "order_creation_duration_seconds",
    "Duration (in seconds) to create an order",
    ["order_type"],
    buckets=[0.1, 0.5, 1, 2, 3, 5, 10],
)
