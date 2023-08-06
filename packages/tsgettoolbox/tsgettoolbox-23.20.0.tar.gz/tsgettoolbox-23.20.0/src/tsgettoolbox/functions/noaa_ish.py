# -*- coding: utf-8 -*-
import datetime
import io
import os
from collections import OrderedDict
from urllib.error import HTTPError

import mando
import numpy as np
import pandas as pd
import requests

try:
    from mando.rst_text_formatter import RSTHelpFormatter as HelpFormatter
except ImportError:
    from argparse import RawTextHelpFormatter as HelpFormatter

from requests import Request
from requests.utils import unquote
from tstoolbox import tsutils

from tsgettoolbox import utils

noaa_ish_docstrings = {
    "info": r"""Detailed information is available from
    https://www.ncei.noaa.gov/data/global-hourly/doc/isd-format-document.pdf

    +------+----------------------------------------------------------+
    | Code | Description                                              |
    +======+==========================================================+
    | ACMC | Average cloudiness midnight to midnight from 30-second   |
    |      | ceilometer data (percent)                                |
    +------+----------------------------------------------------------+
    | ACMH | Average cloudiness midnight to midnight from manual      |
    |      | observations (percent)                                   |
    +------+----------------------------------------------------------+
    | ACSC | Average cloudiness sunrise to sunset from 30-second      |
    |      | ceilometer data (percent)                                |
    +------+----------------------------------------------------------+
    | ACSH | Average cloudiness sunrise to sunset from manual         |
    |      | observations (percent)                                   |
    +------+----------------------------------------------------------+
    | AWDR | Average daily wind direction (degrees)                   |
    +------+----------------------------------------------------------+
    | AWND | Average daily wind speed (meters per second)             |
    +------+----------------------------------------------------------+
    | DAEV | Number of days included in the multiday evaporation      |
    |      | total (MDEV)                                             |
    +------+----------------------------------------------------------+
    | DAPR | Number of days included in the multiday precipitation    |
    |      | total (MDPR)                                             |
    +------+----------------------------------------------------------+
    | DASF | Number of days included in the multiday snowfall total   |
    |      | (MDSF)                                                   |
    +------+----------------------------------------------------------+
    | DATN | Number of days included in the multiday minimum          |
    |      | temperature (MDTN)                                       |
    +------+----------------------------------------------------------+
    | DATX | Number of days included in the multiday maximum          |
    |      | temperature (MDTX)                                       |
    +------+----------------------------------------------------------+
    | DAWM | Number of days included in the multiday wind movement    |
    |      | (MDWM)                                                   |
    +------+----------------------------------------------------------+
    | DWPR | Number of days with non-zero precipitation included in   |
    |      | multiday precipitation total (MDPR)                      |
    +------+----------------------------------------------------------+
    | EVAP | Evaporation of water from evaporation pan (mm)           |
    +------+----------------------------------------------------------+
    | FMTM | Time of fastest mile or fastest 1-minute wind (hours and |
    |      | minutes, i.e., HHMM)                                     |
    +------+----------------------------------------------------------+
    | FRGB | Base of frozen ground layer (cm)                         |
    +------+----------------------------------------------------------+
    | FRGT | Top of frozen ground layer (cm)                          |
    +------+----------------------------------------------------------+
    | FRTH | Thickness of frozen ground layer (cm)                    |
    +------+----------------------------------------------------------+
    | GAHT | Difference between river and gauge height (cm)           |
    +------+----------------------------------------------------------+
    | MDEV | Multiday evaporation total (use with DAEV)               |
    +------+----------------------------------------------------------+
    | MDPR | Multiday precipitation total (mm; use with               |
    |      | DAPR and DWPR, if available)                             |
    +------+----------------------------------------------------------+
    | MDSF | Multiday snowfall total                                  |
    +------+----------------------------------------------------------+
    | MDTN | Multiday minimum temperature (degrees C; use             |
    |      | with DATN)                                               |
    +------+----------------------------------------------------------+
    | MDTX | Multiday maximum temperature (degrees C; use             |
    |      | with DATX)                                               |
    +------+----------------------------------------------------------+
    | MDWM | Multiday wind movement (km)                              |
    +------+----------------------------------------------------------+
    | MNPN | Daily minimum temperature of water in an evaporation pan |
    |      | (degrees C)                                              |
    +------+----------------------------------------------------------+
    | MXPN | Daily maximum temperature of water in an evaporation pan |
    |      | (degrees C)                                              |
    +------+----------------------------------------------------------+
    | PGTM | Peak gust time (hours and minutes, i.e., HHMM)           |
    +------+----------------------------------------------------------+
    | PSUN | Daily percent of possible sunshine (percent)             |
    +------+----------------------------------------------------------+
    | TAVG | Average temperature (degrees C) [Note that               |
    |      | TAVG from source 'S' corresponds to an average for the   |
    |      | period ending at 2400 UTC rather than local midnight]    |
    +------+----------------------------------------------------------+
    | THIC | Thickness of ice on water (mm)                           |
    +------+----------------------------------------------------------+
    | TOBS | Temperature at the time of observation                   |
    |      | (degrees C)                                              |
    +------+----------------------------------------------------------+
    | TSUN | Daily total sunshine (minutes)                           |
    +------+----------------------------------------------------------+
    | WDF1 | Direction of fastest 1-minute wind (degrees)             |
    +------+----------------------------------------------------------+
    | WDF2 | Direction of fastest 2-minute wind (degrees)             |
    +------+----------------------------------------------------------+
    | WDF5 | Direction of fastest 5-second wind (degrees)             |
    +------+----------------------------------------------------------+
    | WDFG | Direction of peak wind gust (degrees)                    |
    +------+----------------------------------------------------------+
    | WDFI | Direction of highest instantaneous wind (degrees)        |
    +------+----------------------------------------------------------+
    | WDFM | Fastest mile wind direction (degrees)                    |
    +------+----------------------------------------------------------+
    | WDMV | 24-hour wind movement (km)                               |
    +------+----------------------------------------------------------+
    | WESD | Water equivalent of snow on the ground (mm)              |
    +------+----------------------------------------------------------+
    | WESF | Water equivalent of snowfall (mm)                        |
    +------+----------------------------------------------------------+
    | WSF1 | Fastest 1-minute wind speed (meters per                  |
    |      | second)                                                  |
    +------+----------------------------------------------------------+
    | WSF2 | Fastest 2-minute wind speed (meters per                  |
    |      | second)                                                  |
    +------+----------------------------------------------------------+
    | WSF5 | Fastest 5-second wind speed (meters per                  |
    |      | second)                                                  |
    +------+----------------------------------------------------------+
    | WSFG | Peak gust wind speed (meters per second)                 |
    +------+----------------------------------------------------------+
    | WSFI | Highest instantaneous wind speed (meters per             |
    |      | second)                                                  |
    +------+----------------------------------------------------------+
    | WSFM | Fastest mile wind speed (meters per second)              |
    +------+----------------------------------------------------------+

    SNXY and SXXY Table

    +-------+------------------------------------------------------------+
    | SNXY  | Minimum soil temperature (degrees C) where 'X'             |
    |       | corresponds to a code for ground cover and 'Y' corresponds |
    |       | to a code for soil depth.                                  |
    +=======+============================================================+
    |       | Ground cover codes include the following:                  |
    +-------+------------------------------------------------------------+
    | X = 0 | unknown                                                    |
    +-------+------------------------------------------------------------+
    | X = 1 | grass                                                      |
    +-------+------------------------------------------------------------+
    | X = 2 | fallow                                                     |
    +-------+------------------------------------------------------------+
    | X = 3 | bare ground                                                |
    +-------+------------------------------------------------------------+
    | X = 4 | brome grass                                                |
    +-------+------------------------------------------------------------+
    | X = 5 | sod                                                        |
    +-------+------------------------------------------------------------+
    | X = 6 | straw mulch                                                |
    +-------+------------------------------------------------------------+
    | X = 7 | grass muck                                                 |
    +-------+------------------------------------------------------------+
    | X = 8 | bare muck                                                  |
    +-------+------------------------------------------------------------+
    |       | Depth codes include the following:                         |
    +-------+------------------------------------------------------------+
    | Y = 1 | 5 cm                                                       |
    +-------+------------------------------------------------------------+
    | Y = 2 | 10 cm                                                      |
    +-------+------------------------------------------------------------+
    | Y = 3 | 20 cm                                                      |
    +-------+------------------------------------------------------------+
    | Y = 4 | 50 cm                                                      |
    +-------+------------------------------------------------------------+
    | Y = 5 | 100 cm                                                     |
    +-------+------------------------------------------------------------+
    | Y = 6 | 150 cm                                                     |
    +-------+------------------------------------------------------------+
    | Y = 7 | 180 cm                                                     |
    +-------+------------------------------------------------------------+
    | SXXY  | Maximum soil temperature (degrees C) where the             |
    |       | second 'X' corresponds to a code for ground cover and 'Y'  |
    |       | corresponds to a code for soil depth. See SNXY for ground  |
    |       | cover and depth codes.                                     |
    +-------+------------------------------------------------------------+

    WTXX and WVXX Table

    +------+-------------------------------------------------------+
    | XX   | Description                                           |
    +======+=======================================================+
    | 01   | Fog, ice fog, or freezing fog (may include heavy      |
    |      | fog)                                                  |
    +------+-------------------------------------------------------+
    | 02   | Heavy fog or heaving freezing fog (not always         |
    |      | distinguished from fog)                               |
    +------+-------------------------------------------------------+
    | 03   | Thunder                                               |
    +------+-------------------------------------------------------+
    | 04   | Ice pellets, sleet, snow pellets, or small hail       |
    +------+-------------------------------------------------------+
    | 05   | Hail (may include small hail)                         |
    +------+-------------------------------------------------------+
    | 06   | Glaze or rime                                         |
    +------+-------------------------------------------------------+
    | 07   | Dust, volcanic ash, blowing dust, blowing sand, or    |
    |      | blowing obstruction                                   |
    +------+-------------------------------------------------------+
    | 08   | Smoke or haze                                         |
    +------+-------------------------------------------------------+
    | 09   | Blowing or drifting snow                              |
    +------+-------------------------------------------------------+
    | 11   | High or damaging winds                                |
    +------+-------------------------------------------------------+
    | 12   | Blowing spray                                         |
    +------+-------------------------------------------------------+
    | 13   | Mist                                                  |
    +------+-------------------------------------------------------+
    | 14   | Drizzle                                               |
    +------+-------------------------------------------------------+
    | 15   | Freezing drizzle                                      |
    +------+-------------------------------------------------------+
    | 16   | Rain (may include freezing rain, drizzle, and         |
    |      | freezing drizzle)                                     |
    +------+-------------------------------------------------------+
    | 17   | Freezing rain                                         |
    +------+-------------------------------------------------------+
    | 18   | Snow, snow pellets, snow grains, or ice crystals      |
    +------+-------------------------------------------------------+
    | 19   | Unknown source of precipitation                       |
    +------+-------------------------------------------------------+
    | 21   | Ground fog                                            |
    +------+-------------------------------------------------------+
    | 22   | Ice fog or freezing fog                               |
    +------+-------------------------------------------------------+
    | WVXX | Weather in the Vicinity where XX has one of the       |
    |      | following values described above: 01, 03, 07, 18, and |
    |      | 20                                                    |
    +------+-------------------------------------------------------+""",
    "stations": r"""stations
        List of station IDs.
""",
}


@mando.command("noaa_ish", formatter_class=HelpFormatter, doctype="numpy")
@tsutils.doc(tsutils.merge_dicts(tsutils.docstrings, noaa_ish_docstrings))
def noaa_ish_cli(stations, start_date=None, end_date=None):
    r"""Download from the Global Historical Climatology Network - Daily.

    {info}

    Parameters
    ----------
    {stations}
    {start_date}
    {end_date}
    """
    tsutils._printiso(noaa_ish(stations, start_date=start_date, end_date=end_date))


def noaa_ish(station, start_date=None, end_date=None):
    r"""Download from the Global Historical Climatology Network - Daily."""
    station = station.replace("-", "")
    final = utils.file_downloader(
        "https://www.ncei.noaa.gov/data/global-hourly/access/{year}/{station}.csv",
        station,
        start_date=start_date,
        end_date=end_date,
    )

    if "WND" in final.columns:
        addto = final["WND"].str.split(",", expand=True)
        addto.columns = [
            "WIND_DIR:deg",
            "WIND_DIR_QC",
            "WIND_OBS_TYPE",
            "WIND_SPEED:m/s",
            "WIND_SPEED_QC",
        ]
        addto["WIND_DIR:deg"] = addto["WIND_DIR:deg"].astype(int)
        addto["WIND_SPEED:m/s"] = addto["WIND_SPEED:m/s"].replace("9999", np.nan)
        addto["WIND_SPEED:m/s"] = addto["WIND_SPEED:m/s"].astype(float) / 10.0
        final = final.drop("WND", axis="columns")
        final = pd.concat([final, addto], axis="columns")
    if "CIG" in final.columns:
        addto = final["CIG"].str.split(",", expand=True)
        addto.columns = ["CEILING:m", "CEILING_QC", "CEILING_DC", "CAVOK"]
        addto["CEILING:m"] = addto["CEILING:m"].replace("99999", np.nan).astype(float)
        addto["CEILING_DC"] = addto["CEILING_DC"].replace("9", np.nan)
        addto["CAVOK"] = addto["CAVOK"].replace("9", np.nan)
        final = final.drop("CIG", axis="columns")
        final = pd.concat([final, addto], axis="columns")
    if "VIS" in final.columns:
        addto = final["VIS"].str.split(",", expand=True)
        addto.columns = [
            "VISIBILITY:m",
            "VISIBILITY_QC",
            "VISIBILITY_VAR",
            "VISIBILITY_VAR_QC",
        ]
        addto["VISIBILITY:m"] = addto["VISIBILITY:m"].replace("999999", np.nan)
        addto["VISIBILITY:m"] = addto["VISIBILITY:m"].astype(float)
        addto["VISIBILITY_VAR"] = addto["VISIBILITY_VAR"].replace("0", np.nan)
        final = final.drop("VIS", axis="columns")
        final = pd.concat([final, addto], axis="columns")
    if "TMP" in final.columns:
        addto = final["TMP"].str.split(",", expand=True)
        addto.columns = ["AIRTEMP:degC", "AIRTEMP_QC"]
        addto["AIRTEMP:degC"] = addto["AIRTEMP:degC"].replace("9999", np.nan)
        addto["AIRTEMP:degC"] = addto["AIRTEMP:degC"].astype(float) / 10.0
        final = final.drop("TMP", axis="columns")
        final = pd.concat([final, addto], axis="columns")
    return final


def get_por(query_params, headers):
    # Get startdate and/or enddate information
    s = utils.requests_retry_session()
    ireq = Request(
        "GET",
        r"http://www.ncdc.noaa.gov/cdo-web/api/v2/stations/{}".format(
            query_params["stationid"]
        ),
        headers=headers,
    )
    prepped = ireq.prepare()
    dreq = s.send(prepped)
    dreq.raise_for_status()

    sdate = pd.to_datetime(dreq.json()["mindate"])
    edate = pd.to_datetime(dreq.json()["maxdate"])

    if "startdate" in query_params:
        tdate = tsutils.parsedate(query_params["startdate"])
        if tdate > sdate:
            sdate = tdate

    if "enddate" in query_params:
        tdate = tsutils.parsedate(query_params["enddate"])
        if tdate < edate:
            edate = tdate

    if sdate >= edate:
        raise ValueError(
            tsutils.error_wrapper(
                """
The startdate of {} is greater than, or equal to, the enddate of {}.
""".format(
                    sdate, edate
                )
            )
        )
    return sdate, edate


_units = OrderedDict(
    {
        "CLDD": "day",
        "DUTR": "day",
        "GRDD": "day",
        "HTDD": "day",
        "TMAX": "degC",
        "TMIN": "degC",
        "TAVG": "degC",
        "EMXT": "degC",
        "EMNT": "degC",
        "DX": "day",
        "DT": "day",
        "DP": "day",
        "DSNW": "day",
        "DSND": "day",
        "PRCP": "mm",
        "SNOW": "mm",
        "EMSN": "mm",
        "EMSD": "mm",
        "SNWD": "mm",
        "EVAP": "mm",
        "FRGB": "cm",
        "FRGT": "cm",
        "FRTH": "cm",
        "GAHT": "cm",
        "MDEV": "cm",
        "MDPR": "cm",
        "MDSF": "cm",
        "MDTN": "degC",
        "MDTX": "degC",
        "MDWM": "km",
        "MNPN": "degC",
        "MXPN": "degC",
        "PSUN": "percent",
        "MNPN": "degC",
        "MXPN": "degC",
        "TSUN": "minute",
        "PSUN": "percent",
        "ACMC": "percent",
        "ACMH": "percent",
        "ACSC": "percent",
        "ACSH": "percent",
        "AWDR": "degree",
        "WDFM": "degree",
        "WDF": "degree",
        "AWND": "m/s",
        "WSFM": "m/s",
        "WSF": "m/s",
        "DAEV": "day",
        "DAPR": "day",
        "DASF": "day",
        "DATN": "day",
        "DATX": "day",
        "DAWM": "day",
        "DWPR": "day",
        "HDSD": "day",
        "CDSD": "day",
        "MX": "degC",
        "MN": "degC",
        "HX": "degC",
        "HN": "degC",
        "LX": "degC",
        "LN": "degC",
        "THIC": "mm",
        "TOBS": "degC",
        "TSUN": "minute",
        "WDMV": "km",
        "WESD": "mm",
        "WESF": "mm",
        "SN": "degC",
        "SX": "degC",
        "DUTR-NORMAL": "degC",
        "DUTR-STDDEV": "degC",
        "AVGNDS": "day",
        "TPCP": "mm",
        "QGAG": "mm",
        "QPCP": "mm",
        "HPCP": "mm",
        "-CLDH-": "hour",
        "-CLOD-": "percent",
        "-DEWP-": "degC",
        "-HTDH-": "hour",
        "-TEMP-": "degC",
        "-WCHL-": "degC",
        "-AVGSPD": "m/s",
        "-1STDIR": "degree",
        "-2NDDIR": "degree",
        "-1STPCT": "percent",
        "-2NDPCT": "percent",
        "-PCTCLM": "percent",
        "-VCTDIR": "percent",
        "-VCTSPD": "m/s",
    }
)


def add_units(dfcols):
    ncols = {}
    for col in dfcols:
        for key, value in _units.items():
            if (key in col and "value_" in col) or key == col:
                ncols[col] = f"{col}:{value}"
    return ncols


noaa_ish.__doc__ = noaa_ish_cli.__doc__


if __name__ == "__main__":
    r = noaa_ish(
        station="ASN00075020",
        start_date="2000-01-01",
        end_date="2001-01-01",
    )

    print("ghcnd")
    print(r)

    r = noaa_ish(
        station="ASN00075020",
        start_date="10 years ago",
        end_date="9 years ago",
    )

    print("ghcnd")
    print(r)

    # http://www.ncdc.noaa.gov/cdo-web/api/v2/data?
    #  datasetid=PRECIP_15&
    #  stationid=COOP:010008&
    #  units=metric&startdate=2010-05-01&enddate=2010-05-31
    r = noaa_cdo_json_to_df(
        r"http://www.ncdc.noaa.gov/cdo-web/api/v2/data",
        startdate="2010-05-01",
        enddate="2010-05-31",
        stationid="COOP:010008",
        datasetid="PRECIP_15",
    )
    print(r)
    mardi = [
        ["GHCND", "GHCND:AE000041196"],
        ["GHCND", "GHCND:USR0000GCOO"],
        ["PRECIP_HLY", "COOP:087440"],
        ["PRECIP_15", "COOP:087440"],
        # ['ANNUAL', 'GHCND:US1MOLN0006'],
        ["GHCNDMS", "GHCND:US1FLAL0004"],
        ["GSOM", "GHCND:US1FLAL0004"],
        ["GSOY", "GHCND:USW00012816"],
        # ['NORMAL_ANN', 'GHCND:USC00083322'],
        ["NORMAL_HLY", "GHCND:USW00013889"],
        ["NORMAL_DLY", "GHCND:USC00084731"],
        ["NORMAL_MLY", "GHCND:USC00086618"],
        # ['NEXRAD3', 'NEXRAD:KJAX'],
        # ['NEXRAD2', 'NEXRAD:KJAX'],
    ]
    for did, sid in mardi:
        startdate = "2010-01-01"
        enddate = "2013-01-01"
        if "NEXRAD" in did:
            startdate = "2000-01-01"
        if "PRECIP_" in did:
            startdate = "2009-01-01"

        r = noaa_cdo_json_to_df(
            r"http://www.ncdc.noaa.gov/cdo-web/api/v2/data",
            startdate=startdate,
            stationid=sid,
            datasetid=did,
        )

        print(did)
        print(r)
