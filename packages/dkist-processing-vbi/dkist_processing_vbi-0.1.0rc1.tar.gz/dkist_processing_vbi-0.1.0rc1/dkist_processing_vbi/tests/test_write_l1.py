import logging
from random import randint

import numpy as np
import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_header_validator import spec214_validator
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.tags import Tag

from dkist_processing_vbi.tasks.write_l1 import VbiWriteL1Frame
from dkist_processing_vbi.tests.conftest import FakeGQLClient


@pytest.fixture(scope="session")
def calibrated_header():
    hdu = fits.PrimaryHDU(data=np.ones((10, 10, 1)))
    hdu.header["TELEVATN"] = 6.28
    hdu.header["TAZIMUTH"] = 3.14
    hdu.header["TTBLANGL"] = 1.23
    hdu.header["DATE-OBS"] = "1988-05-25T01:23:45.678"
    hdu.header["DKIST004"] = "observe"
    hdu.header["ID___004"] = "ip id"
    hdu.header["PAC__004"] = "Sapphire Polarizer"
    hdu.header["PAC__005"] = "0"
    hdu.header["PAC__006"] = "clear"
    hdu.header["PAC__007"] = "0"
    hdu.header["PAC__008"] = "FieldStop (2.8arcmin)"
    hdu.header["INSTRUME"] = "VISP"
    hdu.header["LINEWAV"] = 656.282
    hdu.header["DATE-BGN"] = "2020-03-13T00:00:00.000"
    hdu.header["DATE-END"] = "2021-08-15T00:00:00.000"
    hdu.header["ID___013"] = "PROPOSAL_ID1"
    hdu.header["ID___005"] = "id string"
    hdu.header["PAC__002"] = "clear"
    hdu.header["PAC__003"] = "on"
    hdu.header["TELSCAN"] = "Raster"
    hdu.header["DKIST008"] = 1
    hdu.header["DKIST009"] = 1
    hdu.header["BTYPE"] = ""
    hdu.header["BUNIT"] = ""
    hdu.header["CAMERA"] = ""
    hdu.header["CDELT1"] = 1
    hdu.header["CDELT2"] = 1
    hdu.header["CDELT3"] = 1
    hdu.header["CRPIX1"] = 0
    hdu.header["CRPIX2"] = 0
    hdu.header["CRPIX3"] = 0
    hdu.header["CRVAL1"] = 0
    hdu.header["CRVAL2"] = 0
    hdu.header["CRVAL3"] = 0
    hdu.header["CTYPE1"] = ""
    hdu.header["CTYPE2"] = ""
    hdu.header["CTYPE3"] = ""
    # These units are garbage just for checking
    hdu.header["CUNIT1"] = "m"
    hdu.header["CUNIT2"] = "arcsec"
    hdu.header["CUNIT3"] = "s"
    hdu.header["DATE"] = "2021-08-20T00:00:00.000"
    hdu.header["DKIST003"] = "observe"
    hdu.header["DKISTVER"] = ""
    hdu.header["ID___012"] = ""
    hdu.header["CAM__002"] = ""
    hdu.header["CAM__004"] = 1
    hdu.header["CAM__005"] = 1
    hdu.header["CAM__014"] = 1
    hdu.header["FILE_ID"] = ""
    hdu.header["ID___001"] = ""
    hdu.header["ID___002"] = ""
    hdu.header["ID___008"] = ""
    hdu.header["NETWORK"] = "NSF-DKIST"
    hdu.header["OBJECT"] = "quietsun"
    hdu.header["OBSERVAT"] = "Haleakala High Altitude Observatory Site"
    hdu.header["OBSPR_ID"] = ""
    hdu.header["ORIGIN"] = "National Solar Observatory"
    hdu.header["TELESCOP"] = "Daniel K. Inouye Solar Telescope"
    hdu.header["WAVELNTH"] = 656.282
    hdu.header["WCSAXES"] = 3
    hdu.header["WCSNAME"] = "Helioprojective-cartesian"
    hdu.header["PC1_1"] = 0
    hdu.header["PC1_2"] = 0
    hdu.header["PC1_3"] = 0
    hdu.header["PC2_1"] = 0
    hdu.header["PC2_2"] = 0
    hdu.header["PC2_3"] = 0
    hdu.header["PC3_1"] = 0
    hdu.header["PC3_2"] = 0
    hdu.header["PC3_3"] = 0
    hdu.header["CHECKSUM"] = ""
    hdu.header["DATASUM"] = ""
    hdu.header["NBIN"] = 1
    hdu.header["NBIN1"] = 1
    hdu.header["NBIN2"] = 1
    hdu.header["NBIN3"] = 1
    hdu.header["CAM__001"] = "cam string"
    hdu.header["CAM__003"] = 1
    hdu.header["CAM__006"] = 1
    hdu.header["CAM__007"] = 1
    hdu.header["CAM__008"] = 1
    hdu.header["CAM__009"] = 1
    hdu.header["CAM__010"] = 1
    hdu.header["CAM__011"] = 1
    hdu.header["CAM__012"] = 1
    hdu.header["CAM__013"] = 1
    hdu.header["CAM__015"] = 1
    hdu.header["CAM__016"] = 1
    hdu.header["CAM__017"] = 1
    hdu.header["CAM__018"] = 1
    hdu.header["CAM__019"] = 1
    hdu.header["CAM__020"] = 1
    hdu.header["CAM__033"] = 1
    hdu.header["CAM__034"] = 1
    hdu.header["CAM__035"] = 1
    hdu.header["CAM__036"] = 1
    hdu.header["CAM__037"] = 1
    hdu.header["DKIST001"] = "Auto"
    hdu.header["DKIST002"] = "Full"
    hdu.header["DKIST005"] = "id string"
    hdu.header["DKIST006"] = "Good"
    hdu.header["DKIST007"] = True
    hdu.header["DKIST010"] = 1
    hdu.header["ID___003"] = "id string"
    hdu.header["ID___006"] = "id string"
    hdu.header["ID___007"] = "id string"
    hdu.header["ID___009"] = "id string"
    hdu.header["ID___010"] = "id string"
    hdu.header["ID___011"] = "id string"
    hdu.header["ID___014"] = "id string"
    hdu.header["PAC__001"] = "open"
    hdu.header["PAC__009"] = "None"
    hdu.header["PAC__010"] = "closed"
    hdu.header["PAC__011"] = 0
    hdu.header["WS___001"] = "ws string"
    hdu.header["WS___002"] = 0
    hdu.header["WS___003"] = 0
    hdu.header["WS___004"] = 0
    hdu.header["WS___005"] = 0
    hdu.header["WS___006"] = 0
    hdu.header["WS___007"] = 0
    hdu.header["WS___008"] = 0

    return spec122_validator.validate_and_translate_to_214_l0(hdu.header, return_type=fits.HDUList)[
        0
    ].header


@pytest.fixture(scope="session")
def write_l1_task(calibrated_header):
    with VbiWriteL1Frame(
        recipe_run_id=randint(0, 99999),
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        hdu = fits.PrimaryHDU(data=np.ones(shape=(10, 11)), header=calibrated_header)
        hdul = fits.HDUList([hdu])
        task.fits_data_write(
            hdu_list=hdul,
            tags=[Tag.calibrated(), Tag.frame(), Tag.stokes("I")],
        )
        # files = list(task.read(tags=[Tag.frame(), Tag.calibrated()]))
        task.constants[BudName.average_cadence.value] = 10
        task.constants[BudName.minimum_cadence.value] = 10
        task.constants[BudName.maximum_cadence.value] = 10
        task.constants[BudName.variance_cadence.value] = 0
        task.constants[BudName.num_dsps_repeats.value] = 1
        task.constants[BudName.spectral_line.value] = "VBI-Red H-alpha"

        yield task
        task.constants.purge()
        task.scratch.purge()


def test_write_l1_frame(write_l1_task, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output(), Tag.stokes("I")]))
    assert len(files) == 1
    for file in files:
        logging.info(f"Checking file {file}")
        assert file.exists
        hdl = fits.open(file)
        assert len(hdl) == 2
        header = hdl[1].header
        # TODO: Uncomment this validation once all the bugs in fits-spec/common have been ironed out
        # assert spec214_validator.validate(input_headers=header, extra=False)
        assert header["DNAXIS1"] == 11
        assert header["DNAXIS2"] == 10
        assert header["DNAXIS3"] == 1
        assert header["DINDEX3"] == 1
        assert header["DUNIT1"] == "m"
        assert header["DUNIT2"] == "arcsec"
        assert header["DUNIT3"] == "s"
        assert header["WAVEMIN"] == 656.258
        assert header["WAVEMAX"] == 656.306
        assert header["WAVEBAND"] == "VBI-Red H-alpha"
