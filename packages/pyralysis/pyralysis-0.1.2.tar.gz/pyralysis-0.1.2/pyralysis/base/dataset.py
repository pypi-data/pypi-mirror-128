import numpy as np
import astropy.units as u
import dask.array as da
import xarray as xr
from astropy.constants import c
from .antenna import Antenna
from .baseline import Baseline
from .ms import MS
from ..reconstruction import PSF
from ..units.lambda_units import lambdas_equivalencies
from astropy.units import Quantity
from typing import List
import logging


def calc_beam_size(s_uu, s_vv, s_uv) -> tuple:
    """

    Parameters
    ----------
    s_uu : float
          Weighted sum of u^2.
    s_vv : float
          Weighted sum of v^2.
    s_uv : float
          Weighted sum of u*v.

    Returns
    -------
    tuple
        Beam major, minor and position angle in radians.
    """
    uv_squared = s_uv ** 2
    u_minus_v = s_uu - s_vv
    u_plus_v = s_uu + s_vv
    sqrt_par = np.sqrt(u_minus_v ** 2 + 4.0 * uv_squared)
    bmaj = 2.0 * np.sqrt(np.log(2.0)) / np.pi / np.sqrt(u_plus_v - sqrt_par)  # Major axis in radians
    bmin = 2.0 * np.sqrt(np.log(2.0)) / np.pi / np.sqrt(u_plus_v + sqrt_par)  # Minor axis in radians
    bpa = -0.5 * np.arctan2(2.0 * s_uv, u_minus_v)  # Angle in radians
    return bmaj * u.rad, bmin * u.rad, bpa * u.rad


class Dataset:
    def __init__(self, antenna: Antenna = None, baseline: Baseline = None,
                 spectral_window_dataset: List[xr.Dataset] = None, ms_list: List[MS] = None, psf_parhands: PSF = None,
                 psf_crossedhands: PSF = None, feed_kind: str = None):
        """

        Parameters
        ----------
        antenna : Full Antenna object
        baseline : Full Baseline object
        spectral_window_dataset : Full Spectral Window dataset
        ms_list : List of separated MS
        psf_parhands : PSF object for parallel hands
        psf_crossedhands : PSF object for crossed hands
        feed_kind : Kind of feed of the dataset. E.g "linear", "circular".
        """

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.antenna = antenna
        self.baseline = baseline
        self.spectral_window_dataset = spectral_window_dataset
        self.ms_list = ms_list
        self.psf_parhands = psf_parhands
        self.psf_crossedhands = psf_crossedhands
        self.feed_kind = feed_kind

        self.max_nu = 0.0 * u.Hz  # Maximum frequency in Hz
        self.min_nu = 0.0 * u.Hz  # Minimum frequency in Hz
        self.ref_nu = 0.0 * u.Hz  # Reference frequency in Hz

        self.lambda_min = 0.0 * u.m  # Minimum wavelength in meters
        self.lambda_max = 0.0 * u.m  # Maximum wavelength in meters
        self.lambda_ref = 0.0 * u.m  # Reference wavelength in meters

        self.max_baseline = 0.0 * u.m  # Maximum baseline in meters
        self.min_baseline = 0.0 * u.m  # Minimum baseline in meters

        self.max_antenna_diameter = 0.0 * u.m  # Maximum antenna diameter in meters
        self.min_antenna_diameter = 0.0 * u.m  # Minimum antenna diameter in meters

        self.theo_resolution = 0.0 * u.rad  # Theoretical resolution in radians
        self.fov = 0.0 * u.rad  # Field-of-view in radians

        self.ndatasets = 0

        self.corr_weight_sum = None
        self.parhands_weight_sum = 0.0
        self.crossedhands_weight_sum = 0.0
        self.weights_sum = 0.0

        if spectral_window_dataset is not None:
            max_freqs = []
            min_freqs = []
            ref_freqs = []
            for spw in spectral_window_dataset:
                max_freqs.append(spw.CHAN_FREQ.max().data)
                min_freqs.append(spw.CHAN_FREQ.min().data)
                ref_freqs.append(spw.REF_FREQUENCY.data)

            max_freqs = list(da.compute(*max_freqs))
            min_freqs = list(da.compute(*min_freqs))

            self.max_nu = max(max_freqs) * u.Hz
            self.min_nu = min(min_freqs) * u.Hz
            self.ref_nu = np.median(np.array(ref_freqs)) * u.Hz

            self.lambda_min = c / self.max_nu
            self.lambda_min = self.lambda_min.to(u.m)
            self.lambda_max = c / self.min_nu
            self.lambda_max = self.lambda_max.to(u.m)
            self.lambda_ref = c / self.ref_nu
            self.lambda_ref = self.lambda_ref.to(u.m)

        if antenna is not None:
            self.max_antenna_diameter = antenna.max_diameter
            self.min_antenna_diameter = antenna.min_diameter

        if baseline is not None:
            self.max_baseline = baseline.max_baseline
            self.min_baseline = baseline.min_baseline

        if antenna is not None and baseline is not None and spectral_window_dataset is not None:
            self.theo_resolution = (self.lambda_min / self.max_baseline) * u.rad
            self.fov = (self.lambda_max / self.max_antenna_diameter) * u.rad

        if ms_list is not None:
            self.ndatasets = len(self.ms_list)
            self.check_feed()

            if self.psf_parhands is None and self.psf_crossedhands is None:
                self.calculate_PSF()

    def check_feed(self) -> None:
        """
        Function to check if a feed of the dataset is
        linear, circular or mixed
        """
        feed_list = []
        for ms in self.ms_list:
            feed_list.append(ms.polarization.feed_kind)
        if all(x == "linear" for x in feed_list):
            self.feed_kind = "linear"
        elif all(x == "circular" for x in feed_list):
            self.feed_kind = "circular"
        else:
            self.feed_kind = "mixed"

    def max_ncorrs(self) -> int:
        ncorrs = []
        for ms in self.ms_list:
            ncorrs.append(ms.polarization.ncorrs)
        return max(ncorrs)

    def calculate_weights_sum(self) -> None:

        if self.feed_kind == "linear":
            hands_dict = {'XX': [], 'YX': [], 'XY': [], 'YY': []}
        elif self.feed_kind == "circular":
            hands_dict = {'LL': [], 'RL': [], 'LR': [], 'RR': []}
        else:
            hands_dict = {'XX': [], 'YX': [], 'XY': [], 'YY': [], 'LL': [], 'RL': [], 'LR': [], 'RR': []}

        for ms in self.ms_list:
            weight = ms.visibilities.weight
            ncorrs = ms.polarization.ncorrs
            corr_names = ms.polarization.corrs_names

            for idx_corr in range(0, ncorrs):
                hands_dict[corr_names[idx_corr]].append(da.sum(weight[:, idx_corr]))

        hands_dict = da.compute(hands_dict)[0]
        for i in hands_dict:
            hands_dict[i] = sum(hands_dict[i])

        if self.feed_kind == "linear":
            self.parhands_weight_sum = hands_dict["XX"] + hands_dict["YY"]
            self.crossedhands_weight_sum = hands_dict["YX"] + hands_dict["XY"]
        elif self.feed_kind == "circular":
            self.parhands_weight_sum = hands_dict["LL"] + hands_dict["RR"]
            self.crossedhands_weight_sum = hands_dict["LR"] + hands_dict["RL"]
        else:
            self.parhands_weight_sum = hands_dict["XX"] + hands_dict["YY"] + hands_dict["LL"] + hands_dict["RR"]
            self.crossedhands_weight_sum = hands_dict["YX"] + hands_dict["XY"] + hands_dict["LR"] + hands_dict["RL"]

        self.weights_sum = self.parhands_weight_sum + self.crossedhands_weight_sum
        self.corr_weight_sum = hands_dict

    def calculate_PSF(self) -> None: # TODO: Calculate PSF for all stokes if parameter is None, or for a stokes
        # parameter input
        """
        Function that calculates the PSF properties (bmaj, bmin and bpa) analytically using
        (u,v) positions and the weights
        """
        self.calculate_weights_sum()
        s_uu = [[], []]
        s_vv = [[], []]
        s_uv = [[], []]
        for ms in self.ms_list:
            chans = ms.spectral_window.chans.compute()
            nchans = ms.spectral_window.nchans
            uvw = ms.visibilities.uvw
            weight = ms.visibilities.weight
            flag = ms.visibilities.flag
            ncorrs = ms.polarization.ncorrs
            corr_names = ms.polarization.corrs_names

            uvw_broadcast = da.tile(uvw, nchans * ncorrs).reshape((len(uvw), nchans, ncorrs, 3))
            chans_broadcast = chans[np.newaxis, :, np.newaxis, np.newaxis]

            uvw_lambdas = da.map_blocks(
                lambda x: x.to(u.lambdas, equivalencies=lambdas_equivalencies(restfreq=chans_broadcast)).value,
                uvw_broadcast,
                dtype=np.float64)

            weight_broadcast = da.tile(weight, nchans).reshape((len(weight), nchans, ncorrs))
            weight_broadcast[flag.data] = 0.0

            idx_corr_linear = [key for key, value in corr_names.items()
                               if value == "XX" or value == "YY" or value == "LL" or value == "RR"]
            idx_corr_crossed = [key for key, value in corr_names.items()
                                if value == "XY" or value == "YX" or value == "LR" or value == "RL"]

            if idx_corr_linear:
                u_lambdas = uvw_lambdas[:, :, idx_corr_linear, 0]
                v_lambdas = uvw_lambdas[:, :, idx_corr_linear, 1]
                s_uu[0].append(da.sum((u_lambdas ** 2) * weight_broadcast[:, :, idx_corr_linear]))
                s_vv[0].append(da.sum((v_lambdas ** 2) * weight_broadcast[:, :, idx_corr_linear]))
                s_uv[0].append(da.sum((u_lambdas * v_lambdas) * weight_broadcast[:, :, idx_corr_linear]))

            if idx_corr_crossed:
                u_lambdas = uvw_lambdas[:, :, idx_corr_crossed, 0]
                v_lambdas = uvw_lambdas[:, :, idx_corr_crossed, 1]
                s_uu[1].append(da.sum((u_lambdas ** 2) * weight_broadcast[:, :, idx_corr_crossed]))
                s_vv[1].append(da.sum((v_lambdas ** 2) * weight_broadcast[:, :, idx_corr_crossed]))
                s_uv[1].append(da.sum((u_lambdas * v_lambdas) * weight_broadcast[:, :, idx_corr_crossed]))

        s_uu_parhands = np.asarray(da.compute(*s_uu[0])).sum()
        s_vv_parhands = np.asarray(da.compute(*s_vv[0])).sum()
        s_uv_parhands = np.asarray(da.compute(*s_uv[0])).sum()

        s_uu_crossedhands = np.asarray(da.compute(*s_uu[1])).sum()
        s_vv_crossedhands = np.asarray(da.compute(*s_vv[1])).sum()
        s_uv_crossedhands = np.asarray(da.compute(*s_uv[1])).sum()

        if self.parhands_weight_sum > 0.0:
            s_uu_parhands /= self.parhands_weight_sum
            s_vv_parhands /= self.parhands_weight_sum
            s_uv_parhands /= self.parhands_weight_sum
            bmaj_par, bmin_par, bpa_par = calc_beam_size(s_uu_parhands, s_vv_parhands, s_uv_parhands)
            self.psf_parhands = PSF(sigma=Quantity([bmaj_par, bmin_par]), theta=bpa_par)

        if self.crossedhands_weight_sum > 0.0:
            s_uu_crossedhands /= self.crossedhands_weight_sum
            s_vv_crossedhands /= self.crossedhands_weight_sum
            s_uv_crossedhands /= self.crossedhands_weight_sum
            bmaj_crossed, bmin_crossed, bpa_crossed = calc_beam_size(s_uu_crossedhands, s_vv_crossedhands,
                                                                     s_uv_crossedhands)
            self.psf_crossedhands = PSF(sigma=Quantity([bmaj_crossed, bmin_crossed]), theta=bpa_crossed)
