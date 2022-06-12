#!/usr/bin/env sh

download_tripos () {
    for paper in "$@"; do
        mkdir $paper && cd $paper
        curl -O -f "https://cribs-static.netlify.app/$year/tripos/$paper/QP_[1996-2019].pdf"
        curl -O -f "https://cribs-static.netlify.app/$year/tripos/$paper/CRIB_[1996-2019].pdf"
        cd ..
    done
}

year="IA"
mkdir -p $year/tripos && cd $year/tripos
download_tripos 1P1 1P2 1P3 1P4
cd ../..
