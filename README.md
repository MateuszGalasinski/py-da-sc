# Run jupyter in Docker
## Windows
docker run --rm -it -e NB_GID=100 -p 8889:8888 -v "$(pwd)/jupyter:/home/jovyan/host-note" jupyter/scipy-notebook:latest start-notebook.sh --NotebookApp.token=''

## MacOS
docker run --rm -it -e GRANT_SUDO=yes -p 8888:8888 -v $PWD/jupyter:/home/jovyan/host-note jupyter/scipy-notebook:latest