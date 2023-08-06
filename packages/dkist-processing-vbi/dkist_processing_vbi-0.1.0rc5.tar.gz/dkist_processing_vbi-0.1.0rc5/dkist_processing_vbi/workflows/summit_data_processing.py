"""
Workflow which exercises the common tasks in an end to end scenario
"""
from dkist_processing_common.tasks import AddDatasetReceiptAccount
from dkist_processing_common.tasks import PublishCatalogAndQualityMessages
from dkist_processing_common.tasks import Teardown
from dkist_processing_common.tasks import TransferL0Data
from dkist_processing_common.tasks import TransferL1Data
from dkist_processing_core import Workflow

from dkist_processing_vbi.tasks.parse import ParseL0VbiInputData
from dkist_processing_vbi.tasks.process_summit_processed import GenerateL1SummitData

summit_processed_data = Workflow(
    process_category="vbi",
    process_name="summit_processed_data",
    workflow_package=__package__,
)
summit_processed_data.add_node(task=TransferL0Data, upstreams=None)
summit_processed_data.add_node(task=ParseL0VbiInputData, upstreams=TransferL0Data)
summit_processed_data.add_node(task=GenerateL1SummitData, upstreams=ParseL0VbiInputData)
summit_processed_data.add_node(task=TransferL1Data, upstreams=GenerateL1SummitData)
summit_processed_data.add_node(task=AddDatasetReceiptAccount, upstreams=GenerateL1SummitData)
summit_processed_data.add_node(
    task=PublishCatalogAndQualityMessages, upstreams=[TransferL1Data, AddDatasetReceiptAccount]
)
summit_processed_data.add_node(task=Teardown, upstreams=PublishCatalogAndQualityMessages)
