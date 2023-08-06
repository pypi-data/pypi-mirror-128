from .transformer import Transformer
from abc import ABC, ABCMeta, abstractmethod
import xarray as xr
import astropy.units as un
import dask.array as da


class HermitianSymmetry(Transformer, metaclass=ABCMeta):
    def __init__(self, **kwargs):
        """

        Parameters
        ----------
        kwargs
               Transformer object arguments
        """
        super().__init__(**kwargs)

    def transform(self):
        """
        Applies hermitian symmetry to the dataset
        """
        for ms in self.input_data.ms_list:
            uvw_aux = xr.apply_ufunc(lambda x: x.value, ms.visibilities.uvw, dask="parallelized",
                                     output_dtypes=[ms.visibilities.uvw.dtype])
            # This is faster than using the indexes as dask arrays
            idx = da.argwhere(uvw_aux[:, 0] < 0).squeeze().compute()
            if len(idx) > 0:
                uvw_aux[idx] *= -1
                ms.visibilities.uvw = uvw_aux * un.m
                ms.visibilities.data[idx] = da.conj(ms.visibilities.data[idx])
                ms.visibilities.model[idx] = da.conj(ms.visibilities.data[idx])
