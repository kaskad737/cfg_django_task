Status of Last Deployment:<br>
<img src="https://github.com/kaskad737/cfg_django_task/actions/workflows/django.yml/badge.svg?branch=master">
<br>

# cfg_django_task

## How to run project

1. "git clone" this project
2. Create ".local" or ".prod" file in the root folder of the project. You can find examples of what variables you need to have in one or another type of deployment in the files (".local.template" or ".prod.template") or you just can rename it.

3. In the root folder of the project, run "bash run_local.sh" for local deployment (docker compose up, so you will see log in console) or "bash run_prod.sh" for prod deployment (docker compose up -d)

## Views description

1. Each registered user has access only to his own list of portfolios and only to his list of created bonds.
2. A registered user can only create/update bonds in portfolios of which he is the owner/creator.
3. Each user has access only to his/her own portfolio details, if any, created by the user.
4. Each user only has access to their own bond details.
5. A user with admin rights has the right to view everything and change everything
6. Anonymous user has access only to registration and token_obtain_pair

## Documentation for api endpoints

When the project is launched

<http://localhost:8000/docs/>

## Tests

If you want to run tests, you need to create ".local" file with env veriables as described above and then run "bash run_test.sh"

Tests are implemented via pytest

Tests are run every time a commit is pushed to the repository. On the main page of this repo you can also see the result of testing workflow. Testing was realized through "Git Actions".

P.S.
You can find the bond emission isins here:
<https://www.kurzy.cz/akcie-cz/emise/>
