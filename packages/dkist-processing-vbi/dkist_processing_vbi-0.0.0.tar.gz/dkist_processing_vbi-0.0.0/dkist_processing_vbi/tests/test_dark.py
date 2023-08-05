import numpy as np
import pytest
from dkist_processing_common._util.scratch import WorkflowFileSystem

from dkist_processing_vbi.models.constants import VbiBudName
from dkist_processing_vbi.models.tags import VbiTag
from dkist_processing_vbi.tasks.dark import DarkCalibration
from dkist_processing_vbi.tests.conftest import ensure_all_inputs_used
from dkist_processing_vbi.tests.conftest import FakeGQLClient
from dkist_processing_vbi.tests.conftest import generate_214_l0_fits_frame
from dkist_processing_vbi.tests.conftest import Vbi122DarkFrames


@pytest.fixture(scope="function")
def dark_calibration_task(tmp_path, recipe_run_id):
    with DarkCalibration(
        recipe_run_id=recipe_run_id,
        workflow_name="vbi_dark_calibration",
        workflow_version="VX.Y",
    ) as task:
        task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        task.num_steps = 4
        task.num_exp_per_step = 3
        task.constants[VbiBudName.num_spatial_steps.value] = task.num_steps
        ds = Vbi122DarkFrames(
            array_shape=(1, 10, 10),
            num_steps=task.num_steps,
            num_exp_per_step=task.num_exp_per_step,
        )
        header_generator = (d.header() for d in ds)
        for p in range(1, task.num_steps + 1):
            for e in range(task.num_exp_per_step):
                header = next(header_generator)
                data = (np.ones((1, 10, 10)) * (e + 1)) * 10.0 ** p
                hdul = generate_214_l0_fits_frame(s122_header=header, data=data)
                task.fits_data_write(
                    hdu_list=hdul,
                    tags=[
                        VbiTag.input(),
                        VbiTag.task("DARK"),
                        VbiTag.spatial_step(p),
                        VbiTag.frame(),
                    ],
                )
        ensure_all_inputs_used(header_generator)
        yield task
        task.scratch.purge()
        task.constants.purge()


def test_dark_calibration_task(dark_calibration_task, mocker):
    """
    Given: a set of parsed input dark frames and a DarkCalibration task
    When: running the task
    Then: a single output array is produced for each spatial step and the array values are correct
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    dark_calibration_task()

    for p in range(1, dark_calibration_task.num_steps + 1):
        hdu_list = list(
            dark_calibration_task.fits_data_read_hdu(
                tags=[
                    VbiTag.intermediate(),
                    VbiTag.frame(),
                    VbiTag.task("DARK"),
                    VbiTag.spatial_step(p),
                ]
            )
        )
        assert len(hdu_list) == 1
        expected_array = np.ones((10, 10)) * 2 * 10.0 ** p
        np.testing.assert_equal(expected_array, hdu_list[0][1].data)
