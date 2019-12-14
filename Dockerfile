FROM thoward27/grade:release-v2.0.1

RUN apt-get -y update --fix-missing && apt-get -y upgrade

RUN mkdir /gradelang/
COPY . /gradelang/
RUN python -m pip install /gradelang/
RUN python -m gradelang /gradelang/example.grade

RUN python -m pip install -r /gradelang/requirements.txt

WORKDIR /gradelang/
CMD ["python", "-m", "unittest", "discover"]
