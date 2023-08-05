from random import randint

import numpy as np
import pytest
from astropy.io import fits
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.tasks import ScienceTaskL0ToL1Base

from dkist_processing_vbi.models.tags import VbiTag
from dkist_processing_vbi.tasks.mixin.intermediate_loaders import IntermediateLoaderMixin


@pytest.fixture(scope="module")
def science_task_with_intermediates(tmp_path_factory):
    class DummyTask(ScienceTaskL0ToL1Base, IntermediateLoaderMixin):
        def run(self):
            pass

    with DummyTask(
        recipe_run_id=randint(0, 99999),
        workflow_name="vbi_dummy_task",
        workflow_version="VX.Y",
    ) as task:

        task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path_factory.mktemp("scratch"))
        task.num_steps = 4
        for s in range(1, task.num_steps + 1):
            dark_cal = np.zeros((10, 10)) + (s * 10)
            dark_hdul = fits.HDUList([fits.PrimaryHDU(data=dark_cal)])
            task.fits_data_write(
                hdu_list=dark_hdul,
                tags=[
                    VbiTag.intermediate(),
                    VbiTag.frame(),
                    VbiTag.task("DARK"),
                    VbiTag.spatial_step(s),
                ],
            )

            gain_cal = np.zeros((10, 10)) + (s + 1)
            gain_hdul = fits.HDUList([fits.PrimaryHDU(data=gain_cal)])
            task.fits_data_write(
                hdu_list=gain_hdul,
                tags=[
                    VbiTag.intermediate(),
                    VbiTag.frame(),
                    VbiTag.task("GAIN"),
                    VbiTag.spatial_step(s),
                ],
            )

        yield task
        task.scratch.purge()
        task.constants.purge()


@pytest.mark.parametrize(
    "step",
    [
        pytest.param(1, id="step 1"),
        pytest.param(2, id="step 2"),
        pytest.param(3, id="step 3"),
        pytest.param(4, id="step 4"),
    ],
)
def test_intermediate_dark(science_task_with_intermediates, step):
    """
    Given: A task with some intermediate frames and an IntermediateLoaderMixin
    When: Asking for the intermediate dark calibration for a single step
    Then: The correct array is returned
    """
    truth = np.zeros((10, 10)) + (step * 10)
    np.testing.assert_equal(truth, science_task_with_intermediates.intermediate_dark_array(step))


@pytest.mark.parametrize(
    "step",
    [
        pytest.param(1, id="step 1"),
        pytest.param(2, id="step 2"),
        pytest.param(3, id="step 3"),
        pytest.param(4, id="step 4"),
    ],
)
def test_intermediate_gain(science_task_with_intermediates, step):
    """
    Given: A task with some intermediate frames and an IntermediateLoaderMixin
    When: Asking for the intermediate gain calibration for a single step
    Then: The correct array is returned
    """
    truth = np.zeros((10, 10)) + (step + 1)
    np.testing.assert_equal(truth, science_task_with_intermediates.intermediate_gain_array(step))
