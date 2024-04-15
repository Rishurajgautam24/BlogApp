echo "BUILD STARTED"
sudo apt update
sudo apt install python3 python3-pip
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
echo "BUILD ENDED"



