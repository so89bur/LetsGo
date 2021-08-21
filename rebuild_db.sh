sudo runuser -l postgres -c 'psql -c "drop database posteach"'
sudo runuser -l postgres -c 'psql -c "create database posteach"'

rm migrations/ -rf

flask db init
flask db migrate
flask db upgrade
python first_start.py
