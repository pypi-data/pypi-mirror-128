"""
Tests for the tasks defined in this repo
"""
import logging
from random import randint

import numpy as np
import pytest
from astropy.io import fits
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.graphql import InputDatasetResponse
from dkist_processing_common.models.graphql import RecipeInstanceResponse
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.models.graphql import RecipeRunStatusResponse
from dkist_processing_common.models.tags import Tag

from dkist_processing_test.tasks.fail import FailTask
from dkist_processing_test.tasks.fake_science import GenerateCalibratedData
from dkist_processing_test.tasks.movie import AssembleTestMovie
from dkist_processing_test.tasks.movie import MakeTestMovieFrames
from dkist_processing_test.tasks.noop import NoOpTask
from dkist_processing_test.tasks.write_l1 import WriteL1Data
from dkist_processing_test.tests.conftest import generate_214_l0_fits_frame
from dkist_processing_test.tests.conftest import S122Headers


class FakeGQLClient:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def execute_gql_query(**kwargs):
        query_base = kwargs["query_base"]

        if query_base == "recipeRunStatuses":
            return [RecipeRunStatusResponse(recipeRunStatusId=1)]
        if query_base == "recipeRuns":
            return [
                RecipeRunResponse(
                    recipeInstanceId=1,
                    recipeInstance=RecipeInstanceResponse(
                        recipeId=1,
                        inputDataset=InputDatasetResponse(
                            inputDatasetId=1,
                            isActive=True,
                            inputDatasetDocument='{"bucket": "bucket-name", "parameters": [{"parameterName": "", "parameterValues": [{"parameterValueId": 1, "parameterValue": "[[1,2,3],[4,5,6],[7,8,9]]", "parameterValueStartDate": "1/1/2000"}]}], "frames": ["objectKey1", "objectKey2", "objectKeyN"]}',
                        ),
                    ),
                )
            ]

    @staticmethod
    def execute_gql_mutation(**kwargs):
        pass


@pytest.fixture()
def noop_task():
    return NoOpTask(recipe_run_id=1, workflow_name="noop", workflow_version="VX.Y")


def test_noop_task(noop_task):
    """
    Given: A NoOpTask
    When: Calling the task instance
    Then: No errors raised
    """
    noop_task()


@pytest.fixture()
def fail_task():
    return FailTask(recipe_run_id=1, workflow_name="fail", workflow_version="VX.Y")


def test_fail_task(fail_task):
    """
    Given: A FailTask
    When: Calling the task instance
    Then: Runtime Error raised
    """
    with pytest.raises(RuntimeError):
        fail_task()


@pytest.fixture()
def generate_calibrated_data_task(tmp_path, recipe_run_id):
    number_of_frames = 10
    with GenerateCalibratedData(
        recipe_run_id=recipe_run_id, workflow_name="GenerateCalibratedData", workflow_version="VX.Y"
    ) as task:
        # configure input data
        task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        input_frame_set = Spec122Dataset(
            instrument="vbi",
            dataset_shape=(number_of_frames, 512, 512),
            array_shape=(1, 512, 512),
            time_delta=10,
        )
        # load input data
        for idx, input_frame in enumerate(input_frame_set):
            hdu = input_frame.hdu()
            hdu.header["DSPSNUM"] = 1
            hdul = fits.HDUList([hdu])
            file_name = f"input_{idx}.fits"
            task.fits_data_write(hdu_list=hdul, tags=Tag.input(), relative_path=file_name)
        # result
        yield task, number_of_frames
        # teardown
        task.scratch.purge()
        task.constants.purge()
    # disconnect


def test_generate_calibrated_data(generate_calibrated_data_task, mocker):
    """
    Given: A GenerateCalibratedData task
    When: Calling the task instance
    Then: Output files are generated for each input file with appropriate tags
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, number_of_frames = generate_calibrated_data_task
    task()
    # Then
    calibrated_frame_paths = list(task.read(tags=[Tag.calibrated(), Tag.frame()]))

    # Verify frames
    assert len(calibrated_frame_paths) == number_of_frames
    for filepath in calibrated_frame_paths:
        assert filepath.exists()


@pytest.fixture()
def calibrated_header():
    hdu = fits.PrimaryHDU(data=np.ones((1, 128, 128)))
    hdu.header["TELEVATN"] = 6.28
    hdu.header["TAZIMUTH"] = 3.14
    hdu.header["TTBLANGL"] = 1.23
    hdu.header["DATE-OBS"] = "2020-05-25T00:00:00.000"
    hdu.header["DKIST004"] = "observe"
    hdu.header["ID___004"] = "ip id"
    hdu.header["PAC__004"] = "Sapphire Polarizer"
    hdu.header["PAC__005"] = "0"
    hdu.header["PAC__006"] = "clear"
    hdu.header["PAC__007"] = "0"
    hdu.header["PAC__008"] = "FieldStop (2.8arcmin)"
    hdu.header["INSTRUME"] = "VBI"
    hdu.header["LINEWAV"] = 1080.0
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
    hdu.header["CUNIT1"] = ""
    hdu.header["CUNIT2"] = ""
    hdu.header["CUNIT3"] = ""
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
    hdu.header["WAVELNTH"] = 123.45
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


@pytest.fixture(scope="function", params=[1, 4])
def write_l1_task(calibrated_header, request):
    with WriteL1Data(
        recipe_run_id=randint(0, 99999),
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        num_of_stokes_params = request.param
        stokes_params = ["I", "Q", "U", "V"]
        hdu = fits.PrimaryHDU(data=np.ones(shape=(128, 128)), header=calibrated_header)
        logging.info(f"{num_of_stokes_params=}")
        hdul = fits.HDUList([hdu])
        for i in range(num_of_stokes_params):
            task.fits_data_write(
                hdu_list=hdul,
                tags=[Tag.calibrated(), Tag.frame(), Tag.stokes(stokes_params[i])],
            )
        task.constants[BudName.average_cadence.value] = 10
        task.constants[BudName.minimum_cadence.value] = 10
        task.constants[BudName.maximum_cadence.value] = 10
        task.constants[BudName.variance_cadence.value] = 0
        yield task, num_of_stokes_params
        task.constants.purge()
        task.scratch.purge()


def test_write_l1_task(write_l1_task, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_of_stokes_params = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    logging.info(f"{files=}")
    assert len(files) == num_of_stokes_params
    for file in files:
        logging.info(f"Checking file {file}")
        assert file.exists


@pytest.fixture()
def make_movie_frames_task(tmp_path, recipe_run_id):
    with MakeTestMovieFrames(
        recipe_run_id=recipe_run_id, workflow_name="MakeMovieFrames", workflow_version="VX.Y"
    ) as task:
        task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        task.testing_num_dsps_repeats = 10
        task.num_steps = 1
        task.num_exp_per_step = 1
        task.constants[BudName.num_dsps_repeats.value] = task.testing_num_dsps_repeats
        ds = S122Headers(
            array_shape=(1, 10, 10),
            num_steps=task.num_steps,
            num_exp_per_step=task.num_exp_per_step,
            num_dsps_repeats=task.testing_num_dsps_repeats,
        )
        header_generator = (d.header() for d in ds)
        for d, header in enumerate(header_generator):
            data = np.ones((10, 10))
            data[: d * 10, :] = 0.0
            hdl = generate_214_l0_fits_frame(data=data, s122_header=header)
            task.fits_data_write(
                hdu_list=hdl,
                tags=[
                    Tag.output(),
                    Tag.dsps_repeat(d + 1),
                ],
            )
        yield task
        task.scratch.purge()
        task.constants.purge()


def test_make_movie_frames_task(make_movie_frames_task, mocker):
    """
    :Given: an make_movie_frames_task task
    :When: running the task
    :Then: no errors are raised and a movie file is created
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = make_movie_frames_task
    task()
    movie_frames = list(task.read(tags=[Tag.movie_frame()]))
    logging.info(f"{movie_frames=}")
    assert len(movie_frames) == task.testing_num_dsps_repeats
    for frame in movie_frames:
        assert frame.exists()


@pytest.fixture()
def assemble_test_movie_task(tmp_path, recipe_run_id):
    with AssembleTestMovie(
        recipe_run_id=recipe_run_id, workflow_name="AssembleTestMovie", workflow_version="VX.Y"
    ) as task:
        task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        task.testing_num_dsps_repeats = 10
        task.num_steps = 1
        task.num_exp_per_step = 1
        task.constants[BudName.num_dsps_repeats.value] = task.testing_num_dsps_repeats
        ds = S122Headers(
            array_shape=(1, 10, 10),
            num_steps=task.num_steps,
            num_exp_per_step=task.num_exp_per_step,
            num_dsps_repeats=task.testing_num_dsps_repeats,
        )
        header_generator = (d.header() for d in ds)
        for d, header in enumerate(header_generator):
            data = np.ones((10, 10))
            data[: d * 10, :] = 0.0
            hdl = generate_214_l0_fits_frame(data=data, s122_header=header)
            task.fits_data_write(
                hdu_list=hdl,
                tags=[
                    Tag.movie_frame(),
                    Tag.dsps_repeat(d + 1),
                ],
            )
        yield task
        task.scratch.purge()
        task.constants.purge()


def test_assemble_test_movie_task(assemble_test_movie_task, mocker):
    """
    :Given: an assemble_test_movie task
    :When: running the task
    :Then: no errors are raised and a movie file is created
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task = assemble_test_movie_task
    task()
    movie_file = list(task.read(tags=[Tag.movie()]))
    logging.info(f"{movie_file=}")
    assert len(movie_file) == 1
    assert movie_file[0].exists()
