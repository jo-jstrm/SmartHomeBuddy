get_data_flux = """
        from(bucket: _bucket)
        |> range(start: _start, stop: _stop)
        |> filter(fn: (r) => r["_measurement"] == _measurement_name)
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    """
