#! /bin/bash
REQUIREMENTS='./requirements.txt'
venv_tag='abd'
venv_name="${venv_tag}_venv"
venv_bin="./$venv_name/bin"
echo "Setting up virtual environment ($venv_name)" 1>&2
python -m venv "$venv_name"
echo "Activating ($venv_name)" 1>&2
source $venv_bin/activate
if [[ -e "$REQUIREMENTS" ]]; then
    echo "Installing modules in $REQUIREMENTS" 1>&2
    $venv_bin/pip install -r $REQUIREMENTS
fi
echo "Deactivating ($venv_name)" 1>&2
deactivate
echo "$venv_name" > .autovenv
echo 'Use 'source $PWD/"$venv_name"/bin/activate' to reactivate (venv), or use autovenv.' 1>&2

