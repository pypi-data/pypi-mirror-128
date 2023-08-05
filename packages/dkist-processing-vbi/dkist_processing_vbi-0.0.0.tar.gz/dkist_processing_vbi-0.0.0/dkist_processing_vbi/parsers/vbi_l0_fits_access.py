from typing import Optional
from typing import Union

from astropy.io import fits
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess


class VbiL0FitsAccess(L0FitsAccess):
    def __init__(
        self,
        hdu: Union[fits.ImageHDU, fits.PrimaryHDU, fits.CompImageHDU],
        name: Optional[str] = None,
    ):
        super().__init__(hdu=hdu, name=name)

        self.number_of_spatial_steps: int = self.header.get("VBINSTP")
        self.current_spatial_step: int = self.header.get("VBISTP")
