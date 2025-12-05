_metrics = {
    "requests_total": 0,
    "errors_total": 0,
}


def increment_counter(name: str, amount: int = 1):
    _metrics[name] = _metrics.get(name, 0) + amount


def get_metrics_snapshot():
    return dict(_metrics)
