FROM python:3.9-slim

# Mount: install directory
COPY . /adlinear
WORKDIR /adlinear/
# Install requirements first, that can avoid some conflicts sometimes (don't ask me why)
RUN pip install -r requirements.txt && pip install .
WORKDIR /
RUN rm -rf adlinear

