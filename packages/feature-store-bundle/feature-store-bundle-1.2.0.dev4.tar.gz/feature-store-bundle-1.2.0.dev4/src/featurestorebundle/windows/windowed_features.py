from pyspark.sql import Column, functions as f
from typing import Any, List, Callable

from pyspark.sql import DataFrame


HOUR = 60 * 60
DAY = 24 * HOUR
WEEK = 7 * DAY

PERIODS = {
    "h": HOUR,
    "d": DAY,
    "w": WEEK,
}

past_time_window_column_template = "is_time_window_{time_window}"
future_time_window_column_template = "is_future_time_window_{time_window}"


def _is_past_time_window(target_date: Column, window_argument_date: Column, time_window) -> Column:
    period = PERIODS[time_window[-1]] * int(time_window[:-1])
    delta = target_date - window_argument_date
    return (0 <= delta) & (delta <= period)


def _is_future_time_window(target_date: Column, window_argument_date: Column, time_window) -> Column:
    return _is_past_time_window(window_argument_date, target_date, time_window)


def __with_time_windows(
    df: DataFrame,
    window_col: str,
    target_date_column: Column,
    time_windows: List,
    is_time_window_function: Callable,
    time_window_column_template: str,
) -> DataFrame:
    target_date = target_date_column.cast("long")
    window_argument_date = f.col(window_col).cast("long")

    for time_window in time_windows:
        df = df.withColumn(
            time_window_column_template.format(time_window=time_window),
            is_time_window_function(target_date, window_argument_date, time_window),
        )
    return df


def __windowed(time_window_column_template: str, column: Column, time_window: str, default_value: Any = 0) -> Column:
    time_window_col_name = time_window_column_template.format(time_window=time_window)
    return f.when(f.col(time_window_col_name), column).otherwise(f.lit(default_value))


def windowed(column: Column, time_window: str, default_value: Any = 0) -> Column:
    return __windowed(past_time_window_column_template, column, time_window, default_value)


def future_windowed(column: Column, time_window: str, default_value: Any = 0) -> Column:
    return __windowed(future_time_window_column_template, column, time_window, default_value)


def with_time_windows(df: DataFrame, window_col: str, target_date_column: Column, time_windows: List) -> DataFrame:
    return __with_time_windows(df, window_col, target_date_column, time_windows, _is_past_time_window, past_time_window_column_template)


def with_future_time_windows(df: DataFrame, window_col: str, target_date_column: Column, time_windows: List) -> DataFrame:
    return __with_time_windows(df, window_col, target_date_column, time_windows, _is_future_time_window, future_time_window_column_template)
