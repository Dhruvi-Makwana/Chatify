#!/bin/bash
if remove-print-statements chat/*.py; then
    exit 0
else
    exit 1
fi