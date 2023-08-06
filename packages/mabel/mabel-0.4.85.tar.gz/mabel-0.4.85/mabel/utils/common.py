import glob
import datetime
from typing import Optional
from ..data.formats.json import parse
from ..logging import get_logger


def date_range(start_date: Optional[datetime.date], end_date: Optional[datetime.date]):
    """
    An interator over a range of dates
    """
    # if dates aren't provided, use today
    if not end_date:
        end_date = datetime.date.today()
    if not start_date:
        start_date = datetime.date.today()

    if end_date < start_date:
        raise ValueError(
            "date_range: end_date must be the same or later than the start_date "
        )

    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(n)


def build_context(**kwargs: dict):
    """
    Build Context takes an arbitrary dictionary and merges with a dictionary
    which reflects configuration read from a json file.
    """

    def read_config(config_file):
        # read the job configuration
        try:
            file_location = glob.glob("**/" + config_file, recursive=True).pop()
            get_logger().debug(f"Reading configuration from `{file_location}`.")
            with open(file_location, "r") as f:
                config = parse(f.read())
            return config
        except IndexError as e:
            raise IndexError(
                f"Error: {e}, Likely Cause: Config file `{config_file}` not found"
            )
        except ValueError as e:
            raise ValueError(
                f"Error: {e}, Likely Cause: Config file `{config_file}` incorrectly formatted"
            )
        except Exception as e:
            if type(e).__name__ == "JSONDecodeError":
                raise ValueError(f"Config file `{config_file}` not valid JSON")
            else:
                raise

    # read the configuration file
    config_file = kwargs.get("config_file", "config.json")
    config = read_config(config_file=config_file)
    if not config.get("config"):
        config["config"] = {}

    # merge the sources
    context = {**config, **kwargs}

    return context
