# Welcome to MapServer

##Overview

If you're reading this documentation, you're likely working on the webserver portion of the pothole detection app.

The MapServer is a Django webserver that synchronizes with the Firebase DB that stores your recorded events and overlays the information on a google maps frontend.

In this documentation, we'll discuss setting up your development environment, the project layout, and how to make some simple changes to the project.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
