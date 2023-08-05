from dkist_processing_common.tasks import AddDatasetReceiptAccount
from dkist_processing_common.tasks import PublishCatalogAndQualityMessages
from dkist_processing_common.tasks import Teardown
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TransferL1Data
from dkist_processing_core import Workflow

from dkist_processing_vbi.tasks.dark import DarkCalibration
from dkist_processing_vbi.tasks.gain import GainCalibration
from dkist_processing_vbi.tasks.parse import ParseL0VbiInputData
from dkist_processing_vbi.tasks.science import ScienceCalibration

l0_pipeline = Workflow(
    process_category="vbi",
    process_name="l0_pipeline",
    workflow_package=__package__,
)

l0_pipeline.add_node(task=TransferL0Data, upstreams=None)
l0_pipeline.add_node(task=ParseL0VbiInputData, upstreams=TransferL0Data)
l0_pipeline.add_node(task=DarkCalibration, upstreams=ParseL0VbiInputData)
l0_pipeline.add_node(task=GainCalibration, upstreams=DarkCalibration)
l0_pipeline.add_node(task=ScienceCalibration, upstreams=GainCalibration)
l0_pipeline.add_node(task=AddDatasetReceiptAccount, upstreams=ScienceCalibration)
l0_pipeline.add_node(task=TransferL1Data, upstreams=ScienceCalibration)
l0_pipeline.add_node(
    task=PublishCatalogAndQualityMessages, upstreams=[TransferL1Data, AddDatasetReceiptAccount]
)
l0_pipeline.add_node(task=Teardown, upstreams=PublishCatalogAndQualityMessages)
