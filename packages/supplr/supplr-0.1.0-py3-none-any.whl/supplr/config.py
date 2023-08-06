import os

CAL_FILENAME_PREF = "calib_"
HOME_DIR = os.path.expanduser("~")

CAL_DIR = os.getenv("SUPPLR_CALDIR")

# Folder for are saving calibration files (calib mode)
CAL_DIR_TMP = HOME_DIR + "/marathon_board/calibration_research/calibration"
CAL_DIR_RAW = CAL_DIR_TMP+"/raw"
CAL_DIR_REC = CAL_DIR+"/rec"
