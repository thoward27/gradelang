FROM thoward27/grade:release-v1.1.2

RUN apt-get -y update --fix-missing && apt-get -y upgrade

RUN mkdir /gradelang/
COPY ./requirements.txt /gradelang/
RUN python -m pip install -r /gradelang/requirements.txt

COPY . /gradelang/
WORKDIR /gradelang/
CMD ["python", "-m", "unittest", "discover"]
