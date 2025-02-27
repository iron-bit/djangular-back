#!/bin/bash

(cd ../deploy && docker-compose -f dc-mongodb.yml up -d)
