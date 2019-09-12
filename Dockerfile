# run with:
# docker build -f Dockerfile -t brownie .
# docker run -v $PWD:/usr/src brownie pytest tests

FROM ubuntu:bionic
WORKDIR /usr/src

RUN  apt-get update

# Timezone required for tkinter
ENV TZ=America/Vancouver
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y python3.6 python3-pip python3-venv python3-tk wget curl git npm nodejs
RUN pip3 install wheel pip setuptools virtualenv py-solc-x eth-brownie

RUN npm install -g ganache-cli@6.5.1

# Brownie installs compilers at runtime so ensure the updates are
# in the compiled image so it doesn't do this every time
RUN brownie compile; true
RUN python -m pytest tests

# Fix UnicodeEncodeError error when running tests
ENV PYTHONIOENCODING=utf-8
