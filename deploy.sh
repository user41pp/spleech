#!/bin/bash
fly deploy --build-arg CACHEBUSTER=$(date +%s)