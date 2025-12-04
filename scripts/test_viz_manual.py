import asyncio
from types import SimpleNamespace

from app.agent.tools import visualizer


async def run():
    # file_system expects a context.user.id for user-scoped paths
    context = SimpleNamespace(user=SimpleNamespace(id="manual-test"))
    await visualizer.write_file(
        "test_chart.html",
        "<html><body>TEST CHART</body></html>",
        context,
    )


if __name__ == "__main__":
    asyncio.run(run())
