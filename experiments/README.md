Requires gwpy, which is quirky enough not to work with pip. Requires conda.

`docker pull continuumio/miniconda3`

`docker run -i -v $(pwd):/home -w /home -e DISPLAY=$DISPLAY -t continuumio/miniconda3 /bin/bash`

`conda config --add channels conda-forge`

`conda install -c conda-forge gwpy python-nds2-client -y`

On the host machine

`xhost +local:docker`

To save current image

`docker commit -m="Base stuff" build ligo`