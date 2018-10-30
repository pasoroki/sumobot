#!/bin/bash -e

cd $(dirname "${BASH_SOURCE[0]}")

for arg in "$@"; do
    local_proxy="127.0.0.1:1086"
    case $arg in
    "-s"|"--nocapture" )
        echo "NO CAPTURE"
        capture="-s"
        ;;
    "-v"|"--verbose" )
        echo "VERBOSE"
        verbose="-vv"
        ;;
    * )
    	if [ -z "$testname" ]; then
			echo "RUN SPECIFIC TEST"
			testname="-k $arg"
    	else
			echo "Incorrect arguments"
        	exit 1
    	fi
        ;;
    esac
done

function activate
{
    BASE="./venv"
    source "${BASE}/bin/activate"
}



if ! activate; then
    echo "Failed to activate virtual environment."
    echo ""
    exit 1
fi



${BASE}/bin/pytest -v --import-mode=append $capture $verbose $testname
RESULT=$?

echo ""
echo "Result = ${RESULT}"
