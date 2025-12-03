from vanna.core.lifecycle import LifecycleHook
class LoggingHook(LifecycleHook):
    async def before_message(self,u,m): print("[HOOK]",u.id,m)
    async def after_tool(self,r): print("[TOOL]",r.success)
lifecycle_hooks=[LoggingHook()]
