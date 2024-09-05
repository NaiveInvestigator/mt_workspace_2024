#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/mt-09/husky_ws/src/geonav_transform"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/mt-09/husky_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/mt-09/husky_ws/install/lib/python3/dist-packages:/home/mt-09/husky_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/mt-09/husky_ws/build" \
    "/usr/bin/python3" \
    "/home/mt-09/husky_ws/src/geonav_transform/setup.py" \
     \
    build --build-base "/home/mt-09/husky_ws/build/geonav_transform" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/mt-09/husky_ws/install" --install-scripts="/home/mt-09/husky_ws/install/bin"
