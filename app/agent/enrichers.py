from vanna.core.enricher import ToolContextEnricher


class TimezoneEnricher(ToolContextEnricher):
    async def enrich_context(self, ctx):
        ctx.metadata["timezone"] = "UTC"
        return ctx


context_enrichers = [TimezoneEnricher()]
