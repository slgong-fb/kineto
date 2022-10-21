# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import enum
from typing import Optional

import numpy
import pandas as pd
import plotly.graph_objects as go
from plotly.io import to_html

# TODO: import when rebased onto diff stack
# currently commented import line out and pasted Category enum class to make visualize library independent
# from torch.profiler._memory_profiler import Category
class Category(enum.Enum):
    INPUT = enum.auto()
    TEMPORARY = enum.auto()
    ACTIVATION = enum.auto()
    GRADIENT = enum.auto()
    PARAMETER = enum.auto()
    OPTIMIZER_STATE = enum.auto()

class MemoryUsageVisualize:
    def __init__(self, memory_events: numpy.array) -> None:
        self.df = pd.DataFrame(
            memory_events,
            columns=[
                "time",
                "input",
                "temp",
                "actv",
                "grad",
                "param",
                "state",
            ],
        )

    def draw_breakdown(self, return_html_str: bool = False) -> Optional[str]:
        fig = go.Figure()
        # iterate over members of class Category (defined in _memory_profiler.py)
        for index in range(1, 7):
            fig.add_trace(
                go.Scatter(
                    name=Category(index).name,
                    x=self.df["time"],
                    y=self.df[self.df.columns[index]],
                    line_shape="hv",
                    mode="lines+markers",
                    stackgroup="one",
                )
            )

        fig.update_layout(xaxis_title=("Time (ms)"), yaxis_title="Memory Usage (B)")

        if return_html_str:
            return to_html(fig, include_plotlyjs="cdn")
        fig.show()
