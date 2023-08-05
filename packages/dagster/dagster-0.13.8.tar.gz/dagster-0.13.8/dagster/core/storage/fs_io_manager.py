import os
import pickle

from dagster import check
from dagster.config import Field
from dagster.config.source import StringSource
from dagster.core.definitions.event_metadata import EventMetadataEntry
from dagster.core.definitions.events import AssetKey, AssetMaterialization
from dagster.core.execution.context.input import InputContext
from dagster.core.execution.context.output import OutputContext
from dagster.core.storage.io_manager import IOManager, io_manager
from dagster.core.storage.memoizable_io_manager import MemoizableIOManager
from dagster.utils import PICKLE_PROTOCOL, mkdir_p
from dagster.utils.backcompat import experimental


@io_manager(config_schema={"base_dir": Field(StringSource, is_required=False)})
def fs_io_manager(init_context):
    """Built-in filesystem IO manager that stores and retrieves values using pickling.

    Allows users to specify a base directory where all the step outputs will be stored. By
    default, step outputs will be stored in the directory specified by local_artifact_storage in
    your dagster.yaml file (which will be a temporary directory if not explicitly set).

    Serializes and deserializes output values using pickling and automatically constructs
    the filepaths for the assets.

    Example usage:

    1. Specify a job-level IO manager using the reserved resource key ``"io_manager"``,
    which will set the given IO manager on all ops in a job.

    .. code-block:: python

        from dagster import fs_io_manager, job, op

        @op
        def op_a():
            # create df ...
            return df

        @op
        def op_b(df):
            return df[:5]

        @job(
            resource_defs={
                "io_manager": fs_io_manager.configured({"base_path": "/my/base/path"})
            }
        )
        def job():
            op_b(op_a())


    2. Specify IO manager on :py:class:`Out`, which allows the user to set different IO managers on
    different step outputs.

    .. code-block:: python

        from dagster import fs_io_manager, job, op, Out

        @op(out=Out(io_manager_key="my_io_manager"))
        def op_a():
            # create df ...
            return df

        @op
        def op_b(df):
            return df[:5]

        @job(resource_defs={"my_io_manager": fs_io_manager})
        def job():
            op_b(op_a())

    """
    base_dir = init_context.resource_config.get(
        "base_dir", init_context.instance.storage_directory()
    )

    return PickledObjectFilesystemIOManager(base_dir=base_dir)


class PickledObjectFilesystemIOManager(MemoizableIOManager):
    """Built-in filesystem IO manager that stores and retrieves values using pickling.

    Args:
        base_dir (Optional[str]): base directory where all the step outputs which use this object
            manager will be stored in.
    """

    def __init__(self, base_dir=None):
        self.base_dir = check.opt_str_param(base_dir, "base_dir")
        self.write_mode = "wb"
        self.read_mode = "rb"

    def _get_path(self, context):
        """Automatically construct filepath."""
        keys = context.get_output_identifier()

        return os.path.join(self.base_dir, *keys)

    def has_output(self, context):
        filepath = self._get_path(context)

        return os.path.exists(filepath)

    def handle_output(self, context, obj):
        """Pickle the data and store the object to a file.

        This method omits the AssetMaterialization event so assets generated by it won't be tracked
        by the Asset Catalog.
        """
        check.inst_param(context, "context", OutputContext)

        filepath = self._get_path(context)
        context.log.debug(f"Writing file at: {filepath}")

        # Ensure path exists
        mkdir_p(os.path.dirname(filepath))

        with open(filepath, self.write_mode) as write_obj:
            pickle.dump(obj, write_obj, PICKLE_PROTOCOL)

    def load_input(self, context):
        """Unpickle the file and Load it to a data object."""
        check.inst_param(context, "context", InputContext)

        filepath = self._get_path(context.upstream_output)
        context.log.debug(f"Loading file from: {filepath}")

        with open(filepath, self.read_mode) as read_obj:
            return pickle.load(read_obj)


class CustomPathPickledObjectFilesystemIOManager(IOManager):
    """Built-in filesystem IO managerthat stores and retrieves values using pickling and
    allow users to specify file path for outputs.

    Args:
        base_dir (Optional[str]): base directory where all the step outputs which use this object
            manager will be stored in.
    """

    def __init__(self, base_dir=None):
        self.base_dir = check.opt_str_param(base_dir, "base_dir")
        self.write_mode = "wb"
        self.read_mode = "rb"

    def _get_path(self, path):
        return os.path.join(self.base_dir, path)

    def handle_output(self, context, obj):
        """Pickle the data and store the object to a custom file path.

        This method emits an AssetMaterialization event so the assets will be tracked by the
        Asset Catalog.
        """
        check.inst_param(context, "context", OutputContext)
        metadata = context.metadata
        path = check.str_param(metadata.get("path"), "metadata.path")

        filepath = self._get_path(path)

        # Ensure path exists
        mkdir_p(os.path.dirname(filepath))
        context.log.debug(f"Writing file at: {filepath}")

        with open(filepath, self.write_mode) as write_obj:
            pickle.dump(obj, write_obj, PICKLE_PROTOCOL)

        return AssetMaterialization(
            asset_key=AssetKey([context.pipeline_name, context.step_key, context.name]),
            metadata_entries=[EventMetadataEntry.fspath(os.path.abspath(filepath))],
        )

    def load_input(self, context):
        """Unpickle the file from a given file path and Load it to a data object."""
        check.inst_param(context, "context", InputContext)
        metadata = context.upstream_output.metadata
        path = check.str_param(metadata.get("path"), "metadata.path")
        filepath = self._get_path(path)
        context.log.debug(f"Loading file from: {filepath}")

        with open(filepath, self.read_mode) as read_obj:
            return pickle.load(read_obj)


@io_manager(config_schema={"base_dir": Field(StringSource, is_required=True)})
@experimental
def custom_path_fs_io_manager(init_context):
    """Built-in IO manager that allows users to custom output file path per output definition.

    It requires users to specify a base directory where all the step output will be stored in. It
    serializes and deserializes output values (assets) using pickling and stores the pickled object
    in the user-provided file paths.

    Example usage:

    .. code-block:: python

        from dagster import custom_path_fs_io_manager, job, op

        @op(out=Out(metadata={"path": "path/to/sample_output"}))
        def sample_data(df):
            return df[:5]

        my_custom_path_fs_io_manager = custom_path_fs_io_manager.configured(
            {"base_dir": "path/to/basedir"}
        )

        @job(resource_defs={"io_manager": my_custom_path_fs_io_manager})
        def my_job():
            sample_data()

    """

    return CustomPathPickledObjectFilesystemIOManager(
        base_dir=init_context.resource_config.get("base_dir")
    )
