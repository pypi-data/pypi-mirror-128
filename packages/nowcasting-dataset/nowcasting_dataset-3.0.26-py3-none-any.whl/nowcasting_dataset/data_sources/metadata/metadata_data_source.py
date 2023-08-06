""" Datetime DataSource - add hour and year features """
from dataclasses import dataclass
from numbers import Number

import numpy as np
import pandas as pd
import xarray as xr

from nowcasting_dataset.data_sources.data_source import DataSource
from nowcasting_dataset.data_sources.metadata.metadata_model import Metadata
from nowcasting_dataset.utils import to_numpy


@dataclass
class MetadataDataSource(DataSource):
    """Add metadata to the batch"""

    object_at_center: str = "GSP"

    def get_data_model_for_batch(self):
        """Get the model that is used in the batch"""
        return Metadata

    def get_example(
        self, t0_dt: pd.Timestamp, x_meters_center: Number, y_meters_center: Number
    ) -> xr.Dataset:
        """
        Get example data

        Args:
            t0_dt: list of timestamps
            x_meters_center: x center of patches - not needed
            y_meters_center: y center of patches - not needed

        Returns: batch data of datetime features

        """
        if self.object_at_center == "GSP":
            object_at_center_label = 1
        elif self.object_at_center == "PV":
            object_at_center_label = 2
        else:
            object_at_center_label = 0

        # TODO: data_dict is unused in this function.  Is that a bug?
        # https://github.com/openclimatefix/nowcasting_dataset/issues/279
        data_dict = dict(  # noqa: F841
            t0_dt=to_numpy(t0_dt),  #: Shape: [batch_size,]
            x_meters_center=np.array(x_meters_center),
            y_meters_center=np.array(y_meters_center),
            object_at_center_label=object_at_center_label,
        )

        d_all = {
            "t0_dt": {"dims": ("t0_dt"), "data": [t0_dt]},
            "x_meters_center": {"dims": ("t0_dt_index"), "data": [x_meters_center]},
            "y_meters_center": {"dims": ("t0_dt_index"), "data": [y_meters_center]},
            "object_at_center_label": {"dims": ("t0_dt_index"), "data": [object_at_center_label]},
        }

        data = (xr.DataArray.from_dict(d_all["t0_dt"])).to_dataset()

        for v in ["x_meters_center", "y_meters_center", "object_at_center_label"]:
            d: dict = d_all[v]
            d: xr.Dataset = (xr.DataArray.from_dict(d)).to_dataset().rename({"data": v})
            data[v] = getattr(d, v)

        return data
