from Database.config import supabase
import bcrypt


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def check_password(password, hashed_password):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


def validate_user(
    username,
    email,
    password
):

    if not username.strip():
        raise Exception(
            "Username is required"
        )

    if not email.strip():
        raise Exception(
            "Email is required"
        )

    if not password:
        raise Exception(
            "Password is required"
        )

    if len(username) < 3:
        raise Exception(
            "Username must be at least 3 characters"
        )

    if len(password) < 8:
        raise Exception(
            "Password must be at least 8 characters"
        )

    if "@" not in email:
        raise Exception(
            "Invalid email address"
        )

    return True


def register_user(
    username,
    email,
    password
):
    validate_user(
        username,
        email,
        password
    )
    existing_user = (
        supabase
        .table("users")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if len(existing_user.data) > 0:
        raise Exception(
            "Username already exists"
        )

    hashed_password = hash_password(
        password
    )

    result = (
        supabase
        .table("users")
        .insert({
            "username": username,
            "email": email,
            "password_hash": hashed_password
        })
        .execute()
    )

    return result


def login_user(
    username,
    password
):

    result = (
        supabase
        .table("users")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if len(result.data) == 0:

        return None

    user = result.data[0]

    if check_password(
        password,
        user["password_hash"]
    ):

        return user

    return None