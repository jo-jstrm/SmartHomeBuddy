import pandas as pd


def shaping_v0(df: pd.DataFrame) -> pd.DataFrame:
    """
    Countermeasure: Traffic Shaping
    Version: v0

    Pads all packets to the maximum packet size found in the capture.
    This reduces prediction accuracy for models relying on the packet size.
    """
    # Find the biggest packet
    max_size = df['data_len'].max()

    # Pad all elements to the size of the biggest packet
    df['data_len'].values[:] = max_size

    return df


COUNTERMEASURES = {"shaping_v0": shaping_v0}
