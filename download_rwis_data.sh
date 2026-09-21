#!/usr/bin/env bash
#
# Downloads full-year IA_RWIS data from the Iowa Environmental Mesonet
# for each year from 2025 down to 2015, waiting 5 minutes between
# requests so we don't hammer the server.
#
# Output files: rwis_data_2025.txt, rwis_data_2024.txt, ... rwis_data_2015.txt
#
# Usage:
#   ./download_rwis_data.sh [output_dir]
#
# Run it in the background / in a screen or tmux session, since the
# full run takes ~50 minutes (10 years * 5 min spacing, minus the
# last wait).

set -euo pipefail

OUTDIR="${1:-.}"
mkdir -p "$OUTDIR"

BASE_URL="https://mesonet.agron.iastate.edu/cgi-bin/request/rwis.py"
START_YEAR=2017
END_YEAR=2015
SLEEP_SECONDS=300   # 5 minutes

for (( year=START_YEAR; year>=END_YEAR; year-- )); do
    outfile="${OUTDIR}/rwis_data_${year}.txt"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Downloading ${year} -> ${outfile}"

    curl -sS "${BASE_URL}" \
        --data-urlencode "network=IA_RWIS" \
        --data-urlencode "stations=_ALL" \
        --data-urlencode "year1=${year}" \
        --data-urlencode "month1=1" \
        --data-urlencode "day1=1" \
        --data-urlencode "hour1=0" \
        --data-urlencode "minute1=0" \
        --data-urlencode "year2=${year}" \
        --data-urlencode "month2=12" \
        --data-urlencode "day2=31" \
        --data-urlencode "hour2=23" \
        --data-urlencode "minute2=0" \
        --data-urlencode "tz=Etc/UTC" \
        --data-urlencode "what=txt" \
        --data-urlencode "delim=comma" \
        --data-urlencode "gis=yes" \
        -G -o "${outfile}"

    if [[ -s "${outfile}" ]]; then
        echo "  -> OK ($(wc -l < "${outfile}") lines)"
    else
        echo "  -> WARNING: ${outfile} is empty!"
    fi

    # Don't sleep after the final download
    if (( year > END_YEAR )); then
        echo "  Sleeping ${SLEEP_SECONDS}s before next request..."
        sleep "${SLEEP_SECONDS}"
    fi
done

echo "Done. Files written to ${OUTDIR}"
