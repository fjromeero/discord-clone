# discord-clone

This project contains the base for the discord clone fullstack (backend and frontend)

## 1. Clone the project

```bash
git clone git@github.com:fjromeero/discord-clone.git
```

## 2. Install
The local installation has been successfully tested in Ubuntu 22.04.

### 2.1. Backend
First, we need to install some requirements, The `install_local.sh` script deals
with this, so just execute from the backend directory:
```bash
./scripts/install_local.sh
```

## 3. Post-configuration of the app
### 3.1 Backend
We need to create the tables on the database:
```bash
./scripts/prestart.sh
```
#### 3.1.1. Imports troubleshouting
In case of imports troubles, it can be because in the environment variable is not the base path of the project:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
```
We have to execute in the base path of the backend of the project at console

## 4. Accessing the app

### 4.1. Backend
To run the server (considering that you have the virtualenv already active) using from the base path of the backend:
```bash
fastapi dev app/main.py
```
Navigate to the API documentation under [http://localhost:8000/docs](http://localhost:8000/docs).
