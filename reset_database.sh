apps="$(ls -d */ | grep itracdjangoapi -v)"

for app in ${apps[@]}
do
    rm -rf $app/migrations/0*
    sudo rm -rf $app/migrations/__pycache__
done

sudo docker-compose run web ./manage.py makemigrations
sudo docker-compose run web ./manage.py migrate
