echo "BUILD START"

python3.9 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

echo "BUILD END"

echo "Collecting static files..."
python3.9 manage.py collectstatic