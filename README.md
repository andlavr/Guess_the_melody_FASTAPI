docker build -t guess-melody-api .


version: '2'
services:
  python-container:
    image: python-image:latest
    environment:
      - USERNAME=test
      - PASSWORD=12345