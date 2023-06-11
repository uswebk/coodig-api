# coodig

Backend of quiz application for engineers🧑‍💻

Frontend(Mobile): https://github.com/uswebk/coodig-mobile

---

### Endpoints

* Register account

```
POST: /api/v1/accounts/register/
```

* Login

```
POST: /api/v1/accounts/login/
```

* Refresh JWT

```
POST: /api/token/refresh/
```

* Verify JWT

```
POST: /api/token/verify/
```

* Fetch User

```
GET: /api/v1/accounts/me/
```

* Send OTP

```
POST: /api/v1/accounts/otp/send/
```

* Verify OTP

```
POST: /api/v1/accounts/otp/verify/
```

* Fetch OTP

```
GET: /api/v1/accounts/otp/
```

* Send Reset Password Email

```
POST: /api/v1/accounts/reset-password/send/
```

* Reset Password

```
POST: /api/v1/accounts/reset-password/
```
