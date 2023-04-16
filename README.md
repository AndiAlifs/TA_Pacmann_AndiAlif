# TA_Pacmann_AndiAlif

## Description
TA_Pacmann_AndiAlif is a web-based to-do list application built on Flask Python. It uses Postgres as the database and Bootstrap as the frontend framework. The application also uses Flask-JWT-Extended for authentication. With this application, you can easily keep track of your tasks and stay organized.

## Directory Structure

```bash
TA_Pacmann_AndiAlif/ 
├── Model/ 
│ └── Task.py
│ └── User.py
├── Templates/ 
│ └── add_task.html
│ └── edit_task.html
│ └── index.html
│ └── login.html
│ └── register.html
├── app.py 
├── env_copy.py 
└── requirement.txt
```

- `Model/`: This is a directory contain  `Model` object that interacted with database. There are two model, there are `Task.py` and `User.py`.
- `Templates/`: This is a directory contain all the html file that used in this application. There are five html file, there are `add_task.html`, `edit_task.html`, `index.html`, `login.html`, and `register.html`.
- `app.py`: This is the main file of this application. This file contain all the route and logic of this application.
- `env_copy.py`: This is a file that contain all the environment variable that used in this application.
- `requirement.txt`:  This is a file that contain all the package that used in this application.

## Installation
1. Copy the `env_copy.py` file and rename it to `env.py`.
2. Open the `env.py` file and configure the `DATABASE_URL` and `JWT_SECRET` keys according to your own settings.
3. Install the required packages by running the command `pip install -r requirements.txt`.

## Usage
Run the application by using the command `flask run`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)