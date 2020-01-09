FROM thoward27/grade:release-v2.0.1

RUN apt-get -y update --fix-missing && apt-get -y upgrade

RUN apt-get -y install \
    zsh

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN mkdir /gradelang/
COPY . /gradelang/
RUN python -m pip install /gradelang/

RUN python -m pip install -r /gradelang/requirements.txt

WORKDIR /gradelang/
