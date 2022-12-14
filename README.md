
# A deep dive into Service Account Impersonation

A project that exposes two endpoints to demonstrate cross organizational service account impersonation while showing the Confused Deputy Problem on Google Cloud.

![Logo](https://github.com/g-emarco/ConfusedDeputyPOC/blob/main/static/banner.png)


## Demo

![Alt Text](https://github.com/g-emarco/ConfusedDeputyPOC/blob/main/static/demo.gif)



## Usage/Examples: Onbaording a customer

1. Config Google Cloud project

    `gcloud config set project customer1`

2. create scanner service account with  to be impersonated

    `gcloud iam service-accounts create cool-security-scanner-sa
`

3. Attach relevant permissions to the scanner service account
    ```bash
    gcloud projects add-iam-policy-binding customer1 --member
    "serviceAccount:cool-security-scanner-sa@customer1.iam.gserviceaccount.com" --role
    "role/storastoragege.objectViewer"
    
    gcloud projects add-iam-policy-binding customer1 --member
    "serviceAccount:cool-security-production-sa@cool-security-account.iam.gserviceaccount.com" --role
    "role/iam.serviceAccountTokenCreator" --service-account "cool-security-scanner-sa@customer1.iam.gserviceaccount.com"
    ```

where:

 `customer1` is your target project name


`cool-security-scanner-sa` is the service account created in the customer1 project to be the deputy of cool-security

`cool-security-production-sa@cool-security-account.iam.gserviceaccount.com` is the production service account of cool-security that has only TokenCreator Permission
## API Reference

#### Onboarding a customer

```http
  POST /api/organizations
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `organization_name` | `string` | **Required**. The organization name |
| `organizservice_account_emailation_name` | `string` | **Required**. The email of the service account created on the tenant's project that would be impersonated in the future |


#### Start security scanning (impersonating the taret service account)

```http
  GET /api/recommendations/${target_service_account_email}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `target_service_account_email`      | `string` | **Required**. Target service account the would be inpersonated |


## Run Server

Clone the project

```bash
  git clone https://github.com/g-emarco/ConfusedDeputyPOC/main
```

Go to the project directory

```bash
  cd ConfusedDeputyPOC
```

Install dependencies

```bash
  pipenv install
```

Start the Flask server

```bash
  pipenv run app.py
```

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://www.udemy.com/user/eden-marco/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eden-marco/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/EdenEmarco177)
