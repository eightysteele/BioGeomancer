#!/bin/bash

# Run a prediction against a model.
# Usage: oauth-predict.sh MODEL_NAME DATA

DATA=$1
INPUT="$2"
KEY=`cat googlekey`
MODEL=`echo $DATA | perl -pe 's:/:%2F:g'`
data="{\"input\" : { \"csvInstance\" : [ $INPUT ]}}"

java -cp ./oacurl-1.2.0.jar com.google.oacurl.Fetch -X POST \
-t JSON \
"https://www.googleapis.com/prediction/v1.2/training/$MODEL/predict?key=$KEY" <<< $data
echo
