docker build -t guess-melody-fastapi .


version: '2'
services:
  python-container:
    image: python-image:latest
    environment:
      - USERNAME=test
      - PASSWORD=12345