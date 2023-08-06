import argparse
import logging
import os
import sys
from pathlib import Path

from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_header_validator import spec214_validator

from dkist_processing_visp.tasks.quality import WriteQualityReport

INV = False
try:
    from dkist_inventory.asdf_generator import dataset_from_fits

    INV = True
except ModuleNotFoundError:
    # Bitbucket pipelines won't have dkist-inventory installed
    pass
from dkist_processing_common.manual import ManualProcessing
from dkist_processing_common.tasks import WorkflowDataTaskBase

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.assemble_movie import AssembleVispMovie
from dkist_processing_visp.tasks.dark import DarkCalibration
from dkist_processing_visp.tasks.geometric import GeometricCalibration
from dkist_processing_visp.tasks.instrument_polarization import InstrumentPolarizationCalibration
from dkist_processing_visp.tasks.lamp import LampCalibration
from dkist_processing_visp.tasks.make_movie_frames import MakeVispMovieFrames
from dkist_processing_visp.tasks.parse import ParseL0VispInputData
from dkist_processing_visp.tasks.science import ScienceCalibration
from dkist_processing_visp.tasks.solar import SolarCalibration
from dkist_processing_visp.tasks.split import SplitBeams
from dkist_processing_visp.tasks.write_l1 import VispWriteL1Frame
from dkist_processing_visp.tests.e2e_helpers import LoadDarkCal
from dkist_processing_visp.tests.e2e_helpers import LoadGeometricCal
from dkist_processing_visp.tests.e2e_helpers import LoadInstPolCal
from dkist_processing_visp.tests.e2e_helpers import LoadLampCal
from dkist_processing_visp.tests.e2e_helpers import LoadSolarCal
from dkist_processing_visp.tests.e2e_helpers import SaveDarkCal
from dkist_processing_visp.tests.e2e_helpers import SaveGeometricCal
from dkist_processing_visp.tests.e2e_helpers import SaveInstPolCal
from dkist_processing_visp.tests.e2e_helpers import SaveLampCal
from dkist_processing_visp.tests.e2e_helpers import SaveSolarCal
from dkist_processing_visp.visp_base import VispScienceTask


class Translate122To214L0(WorkflowDataTaskBase):
    def run(self) -> None:
        raw_dir = Path(self.scratch.scratch_base_path) / f"VISP{self.recipe_run_id:03n}"
        if not os.path.exists(self.scratch.workflow_base_path):
            os.makedirs(self.scratch.workflow_base_path)

        if not raw_dir.exists():
            raise FileNotFoundError(
                f"Expected to find a raw VISP{{run_id:03n}} folder in {self.scratch.scratch_base_path}"
            )

        for file in raw_dir.glob("*.FITS"):
            translated_file_name = Path(self.scratch.workflow_base_path) / os.path.basename(file)
            logging.info(f"Translating {file} -> {translated_file_name}")
            hdl = fits.open(file)

            header = spec122_validator.validate_and_translate_to_214_l0(
                hdl[0].header, return_type=fits.HDUList
            )[0].header
            hdl[0].header = header

            hdl.writeto(translated_file_name, overwrite=True)
            hdl.close()
            del hdl


class TagInputs(WorkflowDataTaskBase):
    def run(self) -> None:
        logging.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
        for file in self.scratch.workflow_base_path.glob("*.FITS"):
            logging.info(f"Found {file}")
            self.tag(path=file, tags=[VispTag.input(), VispTag.frame()])


class ShowPolMode(VispScienceTask):
    def run(self) -> None:
        logging.info(f"{self.correct_for_polarization=}")


class ValidateL1Output(VispScienceTask):
    def run(self) -> None:
        files = self.read(tags=[VispTag.output(), VispTag.frame()])
        for f in files:
            logging.info(f"Validating {f}")
            spec214_validator.validate(f, extra=False)


def main(
    scratch_path: str,
    recipe_run_id: int = 2,
    skip_translation: bool = False,
    only_translate: bool = False,
    load_dark: bool = False,
    load_lamp: bool = False,
    load_geometric: bool = False,
    load_solar: bool = False,
    load_inst_pol: bool = False,
):
    with ManualProcessing(
        workflow_path=scratch_path, recipe_run_id=recipe_run_id, testing=True
    ) as manual_processing_run:
        if not skip_translation:
            manual_processing_run.run_task(task=Translate122To214L0)
        if only_translate:
            return
        manual_processing_run.run_task(task=TagInputs)
        manual_processing_run.run_task(task=ParseL0VispInputData)
        manual_processing_run.run_task(task=ShowPolMode)
        manual_processing_run.run_task(task=SplitBeams)
        if load_dark:
            manual_processing_run.run_task(task=LoadDarkCal)
        else:
            manual_processing_run.run_task(task=DarkCalibration)
            manual_processing_run.run_task(task=SaveDarkCal)

        if load_lamp:
            manual_processing_run.run_task(task=LoadLampCal)
        else:
            manual_processing_run.run_task(task=LampCalibration)
            manual_processing_run.run_task(task=SaveLampCal)

        if load_geometric:
            manual_processing_run.run_task(task=LoadGeometricCal)
        else:
            manual_processing_run.run_task(task=GeometricCalibration)
            manual_processing_run.run_task(task=SaveGeometricCal)

        if load_solar:
            manual_processing_run.run_task(task=LoadSolarCal)
        else:
            manual_processing_run.run_task(task=SolarCalibration)
            manual_processing_run.run_task(task=SaveSolarCal)

        if load_inst_pol:
            manual_processing_run.run_task(task=LoadInstPolCal)
        else:
            manual_processing_run.run_task(task=InstrumentPolarizationCalibration)
            manual_processing_run.run_task(task=SaveInstPolCal)

        manual_processing_run.run_task(task=ScienceCalibration)
        manual_processing_run.run_task(task=VispWriteL1Frame)
        manual_processing_run.run_task(task=WriteQualityReport)
        manual_processing_run.run_task(task=ValidateL1Output)
        manual_processing_run.run_task(task=MakeVispMovieFrames)
        manual_processing_run.run_task(task=AssembleVispMovie)

    if INV:
        output_dir = os.path.join(scratch_path, str(recipe_run_id))
        asdf_name = f"dataset_{recipe_run_id:03n}.asdf"
        logging.info(f"Creating ASDF file from {output_dir} and saving to {asdf_name}")
        dataset_from_fits(output_dir, asdf_name, hdu=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run an end-to-end test of the ViSP DC Science pipeline"
    )
    parser.add_argument("scratch_path", help="Location to use as the DC 'scratch' disk")
    parser.add_argument(
        "-i",
        "--run-id",
        help="Which subdir to use. This will become the recipe run id",
        type=int,
        default=4,
    )
    parser.add_argument(
        "-T",
        "--skip-translation",
        help="Skip the translation of raw 122 l0 frames to 214 l0",
        action="store_true",
    )
    parser.add_argument(
        "-t", "--only-translate", help="Do ONLY the translation step", action="store_true"
    )
    parser.add_argument(
        "-D",
        "--load-dark",
        help="Load dark calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-L",
        "--load-lamp",
        help="Load lamp calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-G",
        "--load-geometric",
        help="Load geometric calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-S",
        "--load-solar",
        help="Load solar calibration from previously saved run",
        action="store_true",
    )
    parser.add_argument(
        "-P",
        "--load-inst-pol",
        help="Load instrument polarization calibration from previously saved run",
        action="store_true",
    )
    args = parser.parse_args()
    sys.exit(
        main(
            scratch_path=args.scratch_path,
            recipe_run_id=args.run_id,
            skip_translation=args.skip_translation,
            only_translate=args.only_translate,
            load_dark=args.load_dark,
            load_lamp=args.load_lamp,
            load_geometric=args.load_geometric,
            load_solar=args.load_solar,
            load_inst_pol=args.load_inst_pol,
        )
    )
