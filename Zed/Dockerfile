# Specify the parent image from which we build
FROM stereolabs/zed:3.8-runtime-cuda11.7-ubuntu22.04

# Set the working directory
WORKDIR /app

RUN apt-get update && \
apt-get install -y git && \
git clone https://github.com/stereolabs/zed-examples.git

# # Run the application
# CMD [bash]