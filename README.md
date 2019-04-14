# AeroVision
> Flight Trajectory Visualisation Toolkit

AeroVision is a Python tool specialised in transforming flight data into various KML visualisations that can be displayed in 3D using Google Earth.

![flights](https://user-images.githubusercontent.com/5946444/56076312-da160380-5dcf-11e9-8cfe-ccec4f1835ad.jpg)

## Installation

Dependencies can be installed by running `setup.sh`.

## Usage

The following command line arguments are supported:
```
$ aerovision.py -f <flightsFile> -o <outputfile> -v timespan|animation
```
This is also displayed by running `aerovision.py -h`.

All arguments are optional, with the following default settings if an argument is omitted:
```
flights file: data/flights.csv
out file: output/flights.kml
visualisation type: animation
```
