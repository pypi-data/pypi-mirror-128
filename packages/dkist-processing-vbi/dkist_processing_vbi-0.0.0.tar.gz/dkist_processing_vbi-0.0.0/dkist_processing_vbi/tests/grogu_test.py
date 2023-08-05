import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

import numpy as np
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common.manual import ManualProcessing
from dkist_processing_common.tasks import WorkflowDataTaskBase

from dkist_processing_vbi.models.tags import VbiTag
from dkist_processing_vbi.parsers.vbi_l0_fits_access import VbiL0FitsAccess
from dkist_processing_vbi.tasks.assemble_movie import AssembleVbiMovie
from dkist_processing_vbi.tasks.dark import DarkCalibration
from dkist_processing_vbi.tasks.gain import GainCalibration
from dkist_processing_vbi.tasks.make_movie_frames import MakeVbiMovieFrames
from dkist_processing_vbi.tasks.parse import ParseL0VbiInputData
from dkist_processing_vbi.tasks.science import ScienceCalibration
from dkist_processing_vbi.tasks.write_l1 import VbiWriteL1Frame
from dkist_processing_vbi.vbi_base import VbiScienceTask


class TagInputs(WorkflowDataTaskBase):
    def run(self) -> None:
        logging.info(f"Looking in {os.path.abspath(self.scratch.workflow_base_path)}")
        for file in self.scratch.workflow_base_path.glob("*.FITS"):
            logging.info(f"Found {file}")
            self.tag(path=file, tags=[VbiTag.input(), VbiTag.frame()])


class Translate122To214L0(WorkflowDataTaskBase):
    def run(self) -> None:
        raw_dir = Path(self.scratch.scratch_base_path) / f"VBI{self.recipe_run_id:03n}"
        if not os.path.exists(self.scratch.workflow_base_path):
            os.makedirs(self.scratch.workflow_base_path)
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


class ExposeOutputData(VbiScienceTask):
    def run(self) -> None:
        for step in range(self.num_spatial_steps):
            output_access_list = list(
                self.fits_data_read_fits_access(
                    tags=[VbiTag.output(), VbiTag.frame(), VbiTag.spatial_step(step)],
                    cls=VbiL0FitsAccess,
                )
            )
            logging.info(f"found {len(output_access_list)} outputs for step {step}")
            fits.PrimaryHDU(output_access_list[0].data).writeto(f"comp_{step}.FITS", overwrite=True)


def compare_to_sv_data(sv_file_name: str) -> bool:

    sv_hdl = fits.open(sv_file_name)
    for i, sv_h in enumerate(sv_hdl[1:]):
        dc_data = fits.open(f"comp_{i}.FITS")[0].data
        if not np.allclose(sv_h.data[0], dc_data, atol=1e-5, rtol=1e-5):
            return False

    return True


def main(
    scratch_path="/media/FastPipelin/vbi/scratch",
    recipe_run_id=4,
    sv_file_to_test: Optional[str] = None,
):
    with ManualProcessing(
        workflow_path=scratch_path, recipe_run_id=recipe_run_id, testing=True
    ) as manual_processing_run:
        manual_processing_run.run_task(task=Translate122To214L0)
        manual_processing_run.run_task(task=TagInputs)
        manual_processing_run.run_task(task=ParseL0VbiInputData)
        manual_processing_run.run_task(task=DarkCalibration)
        manual_processing_run.run_task(task=GainCalibration)
        manual_processing_run.run_task(task=ScienceCalibration)
        manual_processing_run.run_task(task=VbiWriteL1Frame)
        manual_processing_run.run_task(task=MakeVbiMovieFrames)
        manual_processing_run.run_task(task=AssembleVbiMovie)
        if sv_file_to_test:
            manual_processing_run.run_task(task=ExposeOutputData)
            assert compare_to_sv_data(sv_file_to_test)
            logging.info("DC output matches SV output!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run an end-to-end test of the VBI DC Science pipeline"
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
        "-S",
        "--sv-file-to-test",
        help="If given, the result of the DC pipeline will be checked against this file on a pixel-by-pixel basis",
        type=str,
    )
    args = parser.parse_args()
    sys.exit(
        main(
            scratch_path=args.scratch_path,
            recipe_run_id=args.run_id,
            sv_file_to_test=args.sv_file_to_test,
        )
    )
