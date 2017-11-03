#!/bin/bash

# Parse cmd line args.
while getopts ":p:s:n:" opt; do
  case $opt in
    p)
      p=$OPTARG
      ;;
    s)
      s=$OPTARG
      ;;
    n)
      n=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z $p ]
  then
    echo 'public key file not specified'
    exit 1
fi
if [ -z $s ]
  then
    echo 'secret key file not specified'
    exit 1
fi
if [ -z $n ]
  then
    echo 'number of bits not specified'
    exit 1
fi

python3.6 src/rsa.py k $p $s $n