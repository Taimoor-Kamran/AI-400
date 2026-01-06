# FastAPI Authentication

## JWT Authentication

```python
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# Config
SECRET_KEY = "your-secret-key"  # Use env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Token creation
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Get current user dependency
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(user_id)  # Your DB lookup
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
```

## Login Endpoint

```python
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

## Role-Based Access

```python
def require_role(allowed_roles: list[str]):
    def dependency(user: CurrentUser):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return dependency

AdminUser = Annotated[User, Depends(require_role(["admin"]))]

@app.delete("/users/{id}")
def delete_user(id: int, admin: AdminUser):
    pass
```

## API Key Authentication

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: Annotated[str, Depends(api_key_header)]):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

## OAuth2 Scopes

```python
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"read": "Read access", "write": "Write access", "admin": "Admin access"}
)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    # Verify token and check scopes
    token_scopes = payload.get("scopes", [])
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

# Usage with scopes
from fastapi import Security

@app.get("/admin/users")
def admin_users(user: Annotated[User, Security(get_current_user, scopes=["admin"])]):
    pass
```

## Refresh Tokens

```python
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_tokens(user_id: int):
    access_token = create_access_token(
        {"sub": str(user_id), "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_access_token(
        {"sub": str(user_id), "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/refresh")
def refresh(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("type") != "refresh":
        raise HTTPException(400, "Invalid token type")
    return create_tokens(payload["sub"])
```
