from vanna.core.user import UserResolver, RequestContext, User

class SimpleUserResolver(UserResolver):
    async def resolve_user(self, req:RequestContext)->User:
        email=req.get_cookie("vanna_email") or "guest@example.com"
        group="admin" if email=="admin@example.com" else "user"
        return User(id=email, username=email.split("@")[0], email=email, group_memberships=[group], permissions=["basic"])
user_resolver=SimpleUserResolver()
