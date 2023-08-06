# -*- coding: utf-8 -*-

def test_import():
    import pyftdc
    assert 0 == 0

diagnostics_file = './diagnostic.data_40/metrics.2021-07-22T17-16-31Z-00000'

def test_parse():
    import pyftdc

    # Create a parser object
    p = pyftdc.FTDCParser()
    status = p.parse_file(diagnostics_file)

    assert status == 0


def test_parse_get_metadata():
    import pyftdc

    # Create a parser object
    p = pyftdc.FTDCParser()
    status = p.parse_file(diagnostics_file)

    assert status == 0

    meta = p.metadata
    if len(meta) > 0:
        print(meta[0])
    print(f"metadata has {len(meta)} elements")

    assert len(meta) > 0


def test_parse_get_timestamps():
    import pyftdc

    # Create a parser object
    p = pyftdc.FTDCParser()
    status = p.parse_file(diagnostics_file)

    assert status == 0

    ts = p.timestamps

    print(f"There are {len(ts)} timestamps")
    assert len(ts) > 0


def test_parse_metrics():
    import pyftdc

    # Create a parser object
    p = pyftdc.FTDCParser()
    status = p.parse_file(diagnostics_file)

    assert status == 0
    metrics = p.metric_names

    for m in metrics:
        print(f"\tMetric: {m}")
    print(f"There are {len(metrics)} metrics")
    assert len(metrics) > 0


def test_metrics_samples():
    import pyftdc

    # Create a parser object
    p = pyftdc.FTDCParser()
    status = p.parse_file(diagnostics_file)
    assert status == 0

    metrics = p.metric_names
    m = p.get_metric(metrics[37])
    n = p.get_metric(metrics[73])

    assert len(n) == len(m)

    ts = p.timestamps
    middle_ts = ts[int(len(ts)/2)]

    h1 = p.get_metric(metrics[73], end=middle_ts)
    h2 = p.get_metric(metrics[73], start=middle_ts)

    assert len(ts) == len(h1) + len(h2)

    # Ten samples (same chunk, for this metrics file)
    ten_more = ts[int(len(ts)/2)+10]
    m_10 = p.get_metric(metrics[37], start=middle_ts, end=ten_more)

    assert 10 == len(m_10)

    # Four hundred so me use two chunks (again, for this particular metrics file)
    four_hundred_more = ts[int(len(ts)/2)+400]
    m_400 = p.get_metric(metrics[37], start=middle_ts, end=four_hundred_more)
    assert 400 == len(m_400)


#TODO: Test for lists of samples

def test_metrics_numpy():
    import pyftdc

    # Create a parser object
    p = pyftdc.FTDCParser()
    status = p.parse_file(diagnostics_file)
    assert status == 0

    metrics = p.metric_names
    m = p.get_metric(metrics[37])
    n = p.get_metric(metrics[73])

    assert len(n) == len(m)

    ts = p.timestamps
    middle_ts = ts[int(len(ts)/2)]

    h1 = p.get_metric_numpy(metrics[73], end=middle_ts)
    h2 = p.get_metric_numpy(metrics[73], start=middle_ts)

    assert len(ts) == len(h1) + len(h2)

    # Ten samples (same chunk, for this metrics file)
    ten_more = ts[int(len(ts)/2)+10]
    m_10 = p.get_metric_numpy(metrics[37], start=middle_ts, end=ten_more)

    assert 10 == len(m_10)

    # Four hundred so me use two chunks (again, for this particular metrics file)
    four_hundred_more = ts[int(len(ts)/2)+400]
    m_400 = p.get_metric_numpy(metrics[37], start=middle_ts, end=four_hundred_more)
    assert 400 == len(m_400)
    assert str(type(m_400)) == "<class 'numpy.ndarray'>"
    mm = p.get_metrics_list_numpy([metrics[73], metrics[37]])

    assert str(type(mm[0])) == "<class 'numpy.ndarray'>"
    assert len(mm) == 2
    assert len(mm[0]) == len(n)
    assert len(mm[1]) == len(m)


def test_metrics_rated_numpy():
    import pyftdc

    # Create a parser object
    p = pyftdc.FTDCParser()
    status = p.parse_file(diagnostics_file)
    assert status == 0

    metrics = p.metric_names
    m = p.get_metric(metrics[37])
    n = p.get_metric(metrics[73])

    assert len(n) == len(m)

    m_rated_with_name = p.get_metric('@'+metrics[37])
    m_rated = p.get_metric(metrics[37], rated_metric=True)

    assert len(m_rated_with_name) == len(m_rated)
