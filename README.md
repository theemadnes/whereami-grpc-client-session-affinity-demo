# whereami-grpc-client-session-affinity-demo
simple gRPC client that calls backend whereami and logs a bunch of 

this assumes you've already implemented the instructions from https://github.com/theemadnes/l7-rilb-gRPC-header-field-demo

### usage

first, make sure you activate the Python virtual environment and install the requirements - then issue the following commands from the repo directory
```
# export values
export PROJECT_ID=e2m-private-test-01 # replace with your project ID
export REGION=us-central1 # replace with your region
export FORWARDING_RULE=grpc-ilb-gke-forwarding-rule

# get LB VIP
LB_VIP=$(gcloud compute forwarding-rules describe $FORWARDING_RULE \
    --project=$PROJECT_ID \
    --region=$REGION \
    --format="value(IPAddress)")

# run client
python whereami_client_header.py ${LB_VIP}:80 --count 50 | grep pod_name_emoji
```