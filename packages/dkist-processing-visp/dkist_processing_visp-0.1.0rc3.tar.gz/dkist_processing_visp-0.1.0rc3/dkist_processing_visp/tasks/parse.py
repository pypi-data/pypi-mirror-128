from typing import List
from typing import TypeVar

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.dsps_repeat import DspsRepeatNumberFlower
from dkist_processing_common.parsers.dsps_repeat import TotalDspsRepeatsBud
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.parsers.unique_bud import UniqueBud
from dkist_processing_common.tasks import ParseL0InputData

from dkist_processing_visp.models.tags import VispStemName
from dkist_processing_visp.parsers.polarimeter_mode import PolarimeterModeBud
from dkist_processing_visp.parsers.raster_step import RasterScanStepFlower
from dkist_processing_visp.parsers.raster_step import TotalRasterStepsBud
from dkist_processing_visp.parsers.spectral_line import SpectralLineBud
from dkist_processing_visp.parsers.task import VispTaskTypeFlower
from dkist_processing_visp.visp_l0_fits_access import VispL0FitsAccess

S = TypeVar("S", bound=Stem)


class ParseL0VispInputData(ParseL0InputData):
    @property
    def fits_parsing_class(self):
        return VispL0FitsAccess

    @property
    def constant_flowers(self) -> List[S]:
        return super().constant_flowers + [
            TotalDspsRepeatsBud(),
            TotalRasterStepsBud(),
            SpectralLineBud(),
            UniqueBud(
                constant_name=BudName.num_modstates.value, metadata_key="number_of_modulator_states"
            ),
            PolarimeterModeBud(),
        ]

    @property
    def tag_flowers(self) -> List[S]:
        return super().tag_flowers + [
            VispTaskTypeFlower(),
            DspsRepeatNumberFlower(),
            RasterScanStepFlower(),
            SingleValueSingleKeyFlower(
                tag_stem_name=VispStemName.modstate.value, metadata_key="modulator_state"
            ),
        ]
