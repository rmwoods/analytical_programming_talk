"""This file contains tools for reading data produced by our arduinos that are
run with github.com/username/my_cool_project. The intention is to identify extreme
acceleration events, which correspond to throwing the arduino across the lab.


Usage: python good_code.py --help

To Do:
    # * Objectify
    # * Add requirements file, makefile, and/or scipts
    # * Add tests
    ### Bonus
    # * Separate data analysis from plotting
    # * Checkpoint long analyses
"""
import argparse
import logging
import sys

import pandas as pd


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

GRAVITY = 9.81  # m/s^2
# Default file to write results to
DEFAULT_OUTPUT_FILE = "exteme_accelerations.csv"
# Default number of points to smooth acceleration over
DEFAULT_SMOOTHING = 0


def load_accel_data(filename):
    """Load the acceleration file and perform basic data cleanup.

    Note that the data in the acceleration file is expected to be in the format
    as produced by my_cool_program (github.com/username/my_cool_project).

    Inputs:
        fname: str
            Path to the file containing the data.

    Returns:
        pd.DataFrame
    """
    try:
        accel_df = pd.read_csv(filename, index_col=0)
    except FileNotFoundError:
        logging.error("File %s does not exist.", filename)

    # By default, our timer is the index. We want it a column
    accel_df = accel_df.reset_index()
    # The timer is in milliseconds. It's more convenient to have seconds here
    accel_df["index"] = accel_df["index"] / 1e3
    # Rename for readbility
    accel_df.rename(
        {"Velocity (m/s)": "velocity", "index": "seconds_since_startup"},
        axis=1,
        inplace=True,
    )
    return accel_df


def calc_accel(velocity, time, smooth=0):
    """Calculate acceleration from velocity and time.

    Inputs:
        velocity: pd.Series
            A series containing velocity measurements
        time: pd.series
            A series containing time differences (interpreted as the time since
            the previous measurement).
        smooth: Optional, default 0
            The number of points to smooth the acceleration calculation over. A
            value of 0 indicates no smoothing.
    Returns:
        pd.series - acceleration
    """

    accel = velocity.diff() / time.diff()

    if smooth > 0:
        accel = accel.rolling(window=smooth).mean()

    return accel


def find_extreme_accelerations(
    input_file, output_file=DEFAULT_OUTPUT_FILE, smooth=DEFAULT_SMOOTHING
):
    logging.debug("Loading data from %s.", input_file)
    recorded_data = load_accel_data(input_file)

    logging.debug("Calculating acceleration with smooth = %d.", smooth)
    recorded_data["accel"] = calc_accel(
        recorded_data["velocity"], recorded_data["seconds_since_startup"], smooth
    )

    logging.debug("Mean acceleration: %s.", recorded_data["accel"].mean())
    high_accels = recorded_data.loc[recorded_data["accel"].abs() > GRAVITY]

    high_accels.to_csv(output_file)
    logging.info(
        "Successfully saved %d high acceleration events to %s.",
        len(high_accels),
        output_file,
    )


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-i",
        "--input-file",
        required=True,
        help="The file containing data that will be read in and analyzed.",
    )
    argparser.add_argument(
        "-o",
        "--output-file",
        default=DEFAULT_SMOOTHING,
        help="The file to write results to.",
    )
    argparser.add_argument(
        "-s",
        "--smooth",
        default=DEFAULT_SMOOTHING,
        type=int,
        help="The number of data points to smooth the acceleration over before "
        "detecting extreme accelerations. A value of 0 indicates no "
        "smoothing.",
    )
    args = argparser.parse_args()
    find_extreme_accelerations(args.input_file, args.output_file, args.smooth)
