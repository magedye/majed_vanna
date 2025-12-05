import argparse
from dbt_integration.doc_generator import SemanticDocGenerator


def main():
    parser = argparse.ArgumentParser(description="Semantic documentation utility")
    parser.add_argument("command", choices=["build", "preview", "search"])
    parser.add_argument("query", nargs="?", default=None, help="Query for search")
    args = parser.parse_args()

    generator = SemanticDocGenerator()

    if args.command == "build":
        result = generator.build()
        print("Build complete. Outputs:", result.get("outputs"))
    elif args.command == "preview":
        print(generator.preview())
    elif args.command == "search":
        if not args.query:
            print("Provide a search query")
            return
        results = generator.search(args.query)
        for r in results:
            print(f"[{r['source']}] {r['match']}")


if __name__ == "__main__":
    main()
