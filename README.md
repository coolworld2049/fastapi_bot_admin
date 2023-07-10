# Telegram bot admin panel

<div>
<img src="assets/react-logo.png" alt="react-logo" height="60" />
<img src="assets/fastapi-logo.png" alt="fastapi-logo" height="60"/>
<img src="assets/ngrok-logo.png" alt="sql-alchemy" height="60" />
</div>

---

![img.png](assets/ngrok-dash.png)

![cli-run.png](assets/cli-run.png)

![react-login.png](assets/react-login.png)

![react-botusers.png](assets/react-botusers.png)

![react-posts-create-1.png](assets/react-posts-create-1.png)

![react-posts-create-2.png](assets/react-posts-create-2.png)

![react-posts-create-3.png](assets/react-posts-create-3.png)

![react-posts-create-4.png](assets/react-posts-create-4.png)

![react-dash.png](assets/react-dash.png)

---

## Deployment

```text
git clone https://github.com/coolworld2049/<project_name>.git
```

```text
cd src/<project_name>;
cp .env.example .env;
nano .env
```

```text
cd deployment
bash cli.sh install
```

deployment/cli.sh

  ```text
  Usage: cli.sh [OPTION]
  Options:
    install           Bring up containers using Docker Compose
    delete            Remove containers, images
    --help            Display this help message
  
  ```