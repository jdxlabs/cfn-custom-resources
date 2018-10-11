#!/usr/bin/env bash

set -e

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <my_bucket> (e.g. \`$0 my-unique-bucket\`)" > /dev/stderr
    exit 127
fi

myBucket=$1
lambdasDir=build/lambdas

mkdir -p build && rm -rf build/*
mkdir ${lambdasDir}
for lambda in $(ls lambdas); do
    zip ${lambdasDir}/${lambda}.zip -r lambdas/${lambda}/* -j
    chmod 744 ${lambdasDir}/${lambda}.zip
    aws s3 cp ${lambdasDir}/${lambda}.zip s3://${myBucket}/lambdas/
done
