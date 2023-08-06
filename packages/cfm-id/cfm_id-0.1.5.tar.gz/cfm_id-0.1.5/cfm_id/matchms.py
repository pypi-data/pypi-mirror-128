import re
from io import StringIO
from typing import Tuple, List, Any, Dict, Iterable
from functools import reduce
import numpy as np
import pandas as pd
from matchms import Spectrum

SOURCE_METADATA_KEY = "source"
SOURCE_METADATA_VALUE = "cfm-id"
ENERGY_METADATA_KEY = "energy"
ENERGY_METADATA_MERGED_VALUE = "merged"


def load_from_cfm_id(raw_text: str, metadata: Dict[str, str]) -> List[Spectrum]:
    data_by_energy = re.split(r"(energy\d)\n", raw_text)[1:]
    spectra = []
    for energy, spectrum_str in pairwise(data_by_energy):
        spectrum_data = np.loadtxt(StringIO(spectrum_str))  # type: ignore
        spectrum = Spectrum(
            mz=spectrum_data[:, 0],
            intensities=spectrum_data[:, 1],
            metadata={
                SOURCE_METADATA_KEY: SOURCE_METADATA_VALUE,
                **metadata,
                ENERGY_METADATA_KEY: energy[-1],
            },
        )
        spectra.append(spectrum)
    spectra.append(merge_spectrums(spectra, metadata))
    return spectra


def pairwise(iterable: List[Any]) -> Iterable[Tuple[Any, Any]]:
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def merge_spectrums(spectra: List[Spectrum], metadata: Dict[str, str]) -> Spectrum:
    dfs = [
        pd.DataFrame({"intensities": sp.peaks.intensities}, index=sp.peaks.mz)
        for sp in spectra
    ]
    df = reduce(
        lambda left, right: pd.merge(
            left, right, how="outer", left_index=True, right_index=True
        ),
        dfs,
    )
    cum = df.fillna(0).mean(axis=1).to_frame().reset_index()
    cum.columns = ["mz", "intensities"]
    cum_spectrum = Spectrum(
        mz=cum.mz.values,
        intensities=cum.intensities.values,
        metadata={
            SOURCE_METADATA_KEY: SOURCE_METADATA_VALUE,
            **metadata,
            ENERGY_METADATA_KEY: ENERGY_METADATA_MERGED_VALUE,
        },
    )
    return cum_spectrum
