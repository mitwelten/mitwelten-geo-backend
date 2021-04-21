conda activate tf-gpu-cuda8

# To ignore spatial or temporal parameters, set lat/lon or week to -1.
env RECORDING_LATITUDE = 47.0
env RECORDING_LONGITUDE = 8.0
#env RECORDING_LATITUDE = -1
#env RECORDING_LONGITUDE = -1
env RECORDING_WEEK = -1
env OVERLAP = 1
env MIN_CONFIDENCE = 0.2
env SENSITIVITY = 0.25

python3 analyze.py --i "mitwelten/data/audiomoth" \
                   --lat $RECORDING_LATITUDE \
                   --lon $RECORDING_LONGITUDE   \
                   --min_conf $MIN_CONFIDENCE \
                   --week $RECORDING_WEEK \
                   --overlap $OVERLAP \
                   --sensitivity $SENSITIVITY

