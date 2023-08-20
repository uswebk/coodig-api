<div align="center"> 
<img alt="coodig-icon" src="https://github.com/uswebk/coodig-api/assets/50518919/098489db-fce3-4bbb-a020-fe969fdf20f2">
<h1>coodig</h1>

<h4>Backend（API） of quiz application for engineers🧑‍💻</h4>
</div>

---

📱 Mobile: https://github.com/uswebk/coodig-mobile

## Run App 🚗
```
python3 manage.py runserver 0.0.0.0:9999
```

## Endpoints

* **Register account**

```
POST: /api/v1/accounts/register/
```

* **Login**

```
POST: /api/v1/accounts/login/
```

* **Refresh JWT**

```
POST: /api/token/refresh/
```

* **Verify JWT**

```
POST: /api/token/verify/
```

* **Fetch Me**

```
GET: /api/v1/accounts/me/
```

* **Send OTP**

```
POST: /api/v1/accounts/otp/send/
```

* **Verify OTP**

```
POST: /api/v1/accounts/otp/verify/
```

* **Fetch OTP**

```
GET: /api/v1/accounts/otp/
```

* **Send Reset Password Email**

```
POST: /api/v1/accounts/reset-password/send/
```

* **Reset Password**

```
POST: /api/v1/accounts/reset-password/
```
